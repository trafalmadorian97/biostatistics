from pathlib import PurePath
from typing import Literal

import gwaslab
import gwaslab as gl
import narwhals
from attrs import frozen
from gwaslab.util.util_in_filter_value import _exclude_sexchr

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_STATUS_COL,
    GwaslabKnownFormat,
    GWASLabVCFRef,
)

GenomeBuildMode = Literal["infer", "19", "38"]
GenomeBuild = Literal["19", "38"]


@frozen
class HarmonizationOptions:
    """
    Options for the call to GWASLab's harmonize function
    """

    ref_infer: GWASLabVCFRef
    ref_seq: str
    cores: int
    check_ref_files: bool
    drop_missing_from_ref: bool


def _do_harmonization(
    sumstats: gl.Sumstats, basic_check: bool, options: HarmonizationOptions
):
    if options.check_ref_files:
        gwaslab.download_ref(name=options.ref_infer.name, overwrite=False)
        gwaslab.download_ref(name=options.ref_seq, overwrite=False)
    sumstats.harmonize(
        basic_check=basic_check,
        n_cores=options.cores,
        ref_seq=gl.get_path(options.ref_seq),
        ref_infer=gl.get_path(options.ref_infer.name),
        ref_alt_freq=options.ref_infer.ref_alt_freq,
    )
    if options.drop_missing_from_ref:
        # see meaning of status codes here: https://cloufield.github.io/gwaslab/StatusCode/
        missing_from_ref = sumstats.data[GWASLAB_STATUS_COL].str[5:6] == "8"
        print(
            f"Dropping {missing_from_ref.sum()} variants that are missing from the reference"
        )
        sumstats.data = sumstats.data.loc[~missing_from_ref, :]


@frozen
class GWASLabColumnSpecifiers:
    rsid: str | None
    snpid: str | None
    chrom: str
    pos: str
    ea: str
    nea: str
    OR: str | None
    se: str | None
    p: str
    info: str
    eaf: str | None = None
    neaf: str | None = None
    beta: str | None = None
    ncase: str | None = None
    ncontrol: str | None = None
    neff: str | None = None
    n: str | None = None


def _get_sumstats(
    x: narwhals.LazyFrame, fmt: GwaslabKnownFormat | GWASLabColumnSpecifiers
) -> gl.Sumstats:
    if isinstance(fmt, GWASLabColumnSpecifiers):
        return gl.Sumstats(
            x.collect().to_pandas(),
            rsid=fmt.rsid,
            snpid=fmt.snpid,
            chrom=fmt.chrom,
            pos=fmt.pos,
            ea=fmt.ea,
            nea=fmt.nea,
            OR=fmt.OR,
            se=fmt.se,
            p=fmt.p,
            info=fmt.info,
            eaf=fmt.eaf,
            neaf=fmt.neaf,
            beta=fmt.beta,
            ncase=fmt.ncase,
            ncontrol=fmt.ncontrol,
            neff=fmt.neff,
            n=fmt.n,
        )

    return gl.Sumstats(
        x.collect().to_pandas(),
        fmt=fmt,
    )


@frozen
class GWASLabPipe(DataProcessingPipe):
    """
    basic_check: Whether to run the GWASLAB basic check
    filter_hapmap3: Set to True to keep only variants in hapmap3
    filter_indels:  Set to True to exclude variants that are insertions or deletions
    filter_palindromic: Set to True to exclude palindromic variants
    exclude_hla: Set to True to exclude variants on the HLA region
    exclude_sexchr: set to True to exclude the sex chromosomes
    """

    basic_check: bool
    genome_build: GenomeBuildMode
    filter_hapmap3: bool
    filter_indels: bool
    filter_palindromic: bool
    exclude_hla: bool
    exclude_sexchr: bool
    harmonize_options: HarmonizationOptions | None
    liftover_to: GenomeBuild | None
    fmt: GwaslabKnownFormat | GWASLabColumnSpecifiers

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        sumstats = _get_sumstats(x, self.fmt)
        if self.genome_build == "infer":
            sumstats.infer_build()
            build = sumstats.meta["gwaslab"]["genome_build"]
            forced_build = None
            print(f"Build is {build}")
        else:
            build = self.genome_build
            forced_build = build
        if self.basic_check:
            sumstats.basic_check()

        if self.liftover_to is not None and (build != self.liftover_to):
            sumstats.liftover(to_build=self.liftover_to, from_build=forced_build)
        if self.filter_hapmap3:
            sumstats.filter_hapmap3(inplace=True, build=forced_build)
        if self.filter_indels:
            sumstats.filter_indel(inplace=True, mode="out")
        if self.filter_palindromic:
            sumstats.filter_palindromic(inplace=True, mode="out")
        if self.exclude_hla:
            sumstats.exclude_hla(inplace=True)
        if self.exclude_sexchr:
            sumstats = _exclude_sexchr(sumstats)
        if self.harmonize_options is not None:
            _do_harmonization(
                sumstats,
                basic_check=(not self.basic_check),
                options=self.harmonize_options,
            )
        _sumstats_raise_on_error(sumstats)
        print(f"Finished gwaslab pipe.  Data has shape {sumstats.data.shape}")
        return narwhals.from_native(sumstats.data).lazy()


def _sumstats_raise_on_error(sumstats: gl.Sumstats):
    error_status = sumstats.data[GWASLAB_STATUS_COL] == "9999999"
    if error_status.any():
        raise ValueError("GWASLAB Error")
