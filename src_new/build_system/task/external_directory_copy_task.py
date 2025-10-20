import shutil

from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.meta.simple_directory_meta import SimpleDirectoryMeta

shutil
from pathlib import Path

from attrs import frozen
from pathlib_abc import WritablePath

from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import GeneratingTask, Task
from src_new.build_system.wf.base_wf import WF


@frozen
class ExternalDirectoryCopyTask(GeneratingTask):
    """
    Copies a directory from an external source.
    Used for testing.
    """

    _meta: SimpleDirectoryMeta
    external_path: Path

    def __attrs_post_init__(self):
        assert self.external_path.is_file()

    @property
    def meta(self) -> SimpleDirectoryMeta:
        return self._meta

    @property
    def deps(self) -> list[Task]:
        return []

    def execute(
        self, scratch_dir: WritablePath, fetch: Fetch, wf: WF
    ) -> DirectoryAsset:
        target_path = scratch_dir / "target"
        shutil.copy(str(self.external_path), str(target_path))
        return DirectoryAsset(target_path)
