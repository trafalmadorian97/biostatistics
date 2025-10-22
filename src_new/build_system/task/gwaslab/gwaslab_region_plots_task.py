from typing import Sequence

import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = (
    "DejaVu Sans"  # Gwaslab defaults to plotting in Arial font, which is not availible by default on linux
)
plt.rcParams["font.family"] = "sans-serif"

import structlog

from src_new.build_system.asset.directory_asset import DirectoryAsset

logger = structlog.get_logger()

from pathlib import Path

import gwaslab as gl
from attrs import field, frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.gwaslab_meta.gwaslab_lead_variants_meta import (
    GWASLabLeadVariantsMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_region_plots_meta import (
    GWASLabRegionPlotsMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_sumstats_meta import (
    GWASLabSumStatsMeta,
)
from src_new.build_system.meta.read_spec.read_dataframe import scan_dataframe_asset
from src_new.build_system.meta.read_spec.read_sumstats import read_sumstats
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.task.gwaslab.gwaslab_constants import (
    GWASLabVCFRefFile,
)
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)
from src_new.build_system.task.gwaslab.gwaslab_lead_variants_task import (
    GwasLabLeadVariantsTask,
)
from src_new.build_system.task.gwaslab.gwaslab_util import (
    Variant,
    df_to_variants,
    gwaslab_download_ref_if_missing,
)
from src_new.build_system.wf.base_wf import WF


@frozen
class GwasLabRegionPlotsFromLeadVariantsTask(Task):
    """
    A task to generate region plots near the lead variants described by GWAS summary statistics
    Useful for visualizing the local significance structure around lead variants, and their nearby genes.
     see https://cloufield.github.io/gwaslab/tutorial_3.4/#quick-regional-plot-without-ld-information
    Gwaslab can also use a vcf reference file to plot the linkage disequilibrium structure around the lead variants
    (vcf_name_for_lead_variants).  Doing this at a reasonable speed requires the installation of the "tabix" binary.
    """

    _lead_variants_task: GwasLabLeadVariantsTask
    _sumstats_task: GWASLabCreateSumstatsTask
    vcf_name_for_ld: GWASLabVCFRefFile | None
    short_id: AssetId = field(converter=AssetId)

    def __attrs_post_init__(self):
        # might remove these checks if we end up wanting to explore lead variants from one project in the data of another
        assert self._lead_variants_task_meta.trait == self._sumstats_meta.trait
        assert self._lead_variants_task_meta.project == self._sumstats_meta.project

    @property
    def meta(self) -> GWASLabRegionPlotsMeta:
        return GWASLabRegionPlotsMeta(
            trait=self._lead_variants_task_meta.trait,
            project=self._lead_variants_task_meta.project,
            short_id=self.short_id,
        )

    @property
    def _lead_variants_task_meta(self) -> GWASLabLeadVariantsMeta:
        return self._lead_variants_task.meta

    @property
    def _lead_variants_id(self) -> AssetId:
        return self._lead_variants_task_meta.asset_id

    @property
    def _sumstats_meta(self) -> GWASLabSumStatsMeta:
        meta = self._sumstats_task.meta
        assert isinstance(meta, GWASLabSumStatsMeta)
        return meta

    @property
    def _sumstats_id(self) -> AssetId:
        return self._sumstats_meta.asset_id

    @property
    def deps(self) -> list["Task"]:
        return [self._lead_variants_task, self._sumstats_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> DirectoryAsset:
        target_path = scratch_dir / "plot_dir"
        target_path.mkdir(parents=True, exist_ok=True)
        sumstats = read_sumstats(fetch(self._sumstats_id))
        variant_df = (
            scan_dataframe_asset(
                asset=fetch(self._lead_variants_id), meta=self._lead_variants_task_meta
            )
            .collect()
            .to_pandas()
        )
        variants = df_to_variants(variant_df)
        plot_region_around_variants(
            sumstats=sumstats,
            variants=variants,
            output_dir=target_path,
            vcf_name_for_ld=self.vcf_name_for_ld,
        )
        return DirectoryAsset(
            path=target_path,
        )


def _plot_region_around_variant(
    sumstats: gl.Sumstats,
    chrom: int,
    pos: int,
    buffer: int,
    output_path: Path,
    vcf_name_for_ld: GWASLabVCFRefFile | None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if vcf_name_for_ld is not None:
        gwaslab_download_ref_if_missing(vcf_name_for_ld)
        vcf_path = gl.get_path(vcf_name_for_ld)
    else:
        vcf_path = None
    sumstats.plot_mqq(
        mode="r",
        skip=2,
        cut=20,
        scaled=True,
        region_grid=True,
        region=(chrom, max(pos - buffer, 0), pos + buffer),
        save=str(
            output_path,
        ),
        save_args={"dpi": 400, "facecolor": "white"},
        vcf_path=vcf_path,
    )


def plot_region_around_variants(
    sumstats: gl.Sumstats,
    variants: Sequence[Variant],
    output_dir: Path,
    vcf_name_for_ld: GWASLabVCFRefFile | None,
    buffer: int = 500_000,
) -> None:
    for variant in variants:
        logger.debug(f"Creating region plot around variant {variant.id}")
        _plot_region_around_variant(
            sumstats=sumstats,
            chrom=variant.chromosome,
            pos=variant.position,
            buffer=buffer,
            output_path=output_dir / str(variant.id_normalized + ".png"),
            vcf_name_for_ld=vcf_name_for_ld,
        )
