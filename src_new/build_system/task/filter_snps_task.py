from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import FileMeta
from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class FilterSNPsTask(Task):
    _raw_gwas_data_task: Task
    _filtration_data_task: Task
    _meta: FilteredGWASDataMeta
    _col_in_raw_data: str= "ID"
    _col_in_filter_data:str = "ID"
    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return [self._raw_gwas_data_task, self._filtration_data_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> FileAsset:
        asset_1 = fetch(self._raw_gwas_data_task.asset_id)
        asset_2 = fetch(self._filtration_data_task.asset_id)
        meta_1 = self._raw_gwas_data_task.meta
        meta_2 = self._filtration_data_task.meta
        assert isinstance(asset_1, FileAsset)
        assert isinstance(asset_2, FileAsset)
        assert isinstance(meta_1, FileMeta)
        assert isinstance(meta_2, FileMeta)
