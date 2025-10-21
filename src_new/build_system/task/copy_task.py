import shutil
from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import GeneratingTask, Task
from src_new.build_system.wf.base_wf import WF


@frozen
class CopyTask(GeneratingTask):
    """
    Copies a file from a dependency
    Used for testing
    """

    _meta: SimpleFileMeta
    dep_file_task: Task

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return [self.dep_file_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> FileAsset:
        dep_asset = fetch(self.dep_file_task.asset_id)
        temp_dst = scratch_dir / "temp_dst"
        assert isinstance(dep_asset, FileAsset)
        shutil.copyfile(dep_asset.path, temp_dst)
        return FileAsset(temp_dst)
