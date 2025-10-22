from pathlib import Path

import gwaslab as gl
from attrs import field, frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.gwaslab_meta.gwaslab_lead_variants_meta import (
    GWASLabLeadVariantsMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_sumstats_meta import (
    GWASLabSumStatsMeta,
)
from src_new.build_system.meta.read_spec.read_sumstats import read_sumstats
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)
from src_new.build_system.wf.base_wf import WF


@frozen
class GwasLabLeadVariantsTask(Task):
    """
    A task to generate a list of lead variants from summary statistics.
    Uses Gwaslab.
    see: https://cloufield.github.io/gwaslab/utility_get_lead_novel/
    """

    _sumstats_task: GWASLabCreateSumstatsTask
    short_id: AssetId = field(converter=AssetId)
    sig_level: float = 5e-8

    @property
    def meta(self) -> GWASLabLeadVariantsMeta:
        return GWASLabLeadVariantsMeta(
            trait=self._input_meta.trait,
            project=self._input_meta.project,
            short_id=self.short_id,
        )

    @property
    def _input_meta(self) -> GWASLabSumStatsMeta:
        input_meta = self._sumstats_task.meta
        assert isinstance(input_meta, GWASLabSumStatsMeta)
        return input_meta

    @property
    def _input_asset_id(self) -> AssetId:
        return self._input_meta.asset_id

    @property
    def deps(self) -> list["Task"]:
        return [self._sumstats_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        sumstats_asset = fetch(self._input_asset_id)
        sumstats: gl.Sumstats = read_sumstats(sumstats_asset)
        variant_df = sumstats.get_lead(anno=True, sig_level=self.sig_level)
        out_path = scratch_dir / "lead_variants.csv"
        variant_df.to_csv(out_path, index=False)
        return FileAsset(out_path)
