from pathlib import Path

import pandas as pd
from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.gwaslab_meta.gwaslab_sumstats_meta import (
    GWASLabSumStatsMeta,
)
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameParquetFormat,
    DataFrameReadSpec,
)
from src_new.build_system.meta.read_spec.read_sumstats import read_sumstats
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class GwasLabSumstatsToTableTask(Task):
    """
    Task to write a sumstats object to a plain table for further processing.
    """
    _meta: Meta
    source_sumstats_task: Task

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def source_meta(self) -> Meta:
        return self.source_sumstats_task.meta

    @property
    def source_asset_id(self) -> AssetId:
        return self.source_meta.asset_id

    @property
    def deps(self) -> list["Task"]:
        return [self.source_sumstats_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        asset = fetch(self.source_asset_id)
        sumstats = read_sumstats(asset)
        df: pd.DataFrame = sumstats.data
        out_loc = scratch_dir / "data.parquet"
        df.to_parquet(out_loc)
        return FileAsset(path=out_loc)

    @classmethod
    def create_from_source_task(cls, source_tsk: Task, asset_id: str, sub_dir: str):
        source_meta = source_tsk.meta
        assert isinstance(source_meta, GWASLabSumStatsMeta)
        meta = FilteredGWASDataMeta(
            short_id=AssetId(asset_id),
            trait=source_meta.trait,
            project=source_meta.project,
            sub_dir=sub_dir,
            read_spec=DataFrameReadSpec(format=DataFrameParquetFormat()),
        )
        return cls(
            meta=meta,
            source_sumstats_task=source_tsk,
        )
