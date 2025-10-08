from pathlib import PurePath
from typing import Literal

import gwaslab as gl
import narwhals
from attrs import frozen
from gwaslab.util.util_in_filter_value import _exclude_sexchr

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import GwaslabKnownFormat

GenomeBuildMode = Literal["infer", "19", "38"]


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
    fmt: GwaslabKnownFormat = "regenie"

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        sumstats = gl.Sumstats(
            x.collect().to_pandas(),
            fmt=self.fmt,
        )
        if self.basic_check:
            sumstats.basic_check()
        if self.genome_build == "infer":
            sumstats.infer_build()
            forced_build = None
            print(f"Build is {sumstats.meta['gwaslab']['genome_build']}")
        else:
            forced_build = self.genome_build
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
        return narwhals.from_native(sumstats.data).lazy()
