import shutil
from pathlib import Path

from attrs import frozen
from pathlib_abc import WritablePath

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import GeneratingTask, Task
from src_new.build_system.wf.base_wf import WF


@frozen
class ExternalFileCopyTask(GeneratingTask):
    """
    Copies a file from an external source.
    Used for testing
    """

    _meta: SimpleFileMeta
    external_path: Path

    def __attrs_post_init__(self):
        assert self.external_path.is_file()

    @property
    def meta(self) -> SimpleFileMeta:
        return self._meta

    @property
    def deps(self) -> list[Task]:
        return []

    def execute(self, scratch_dir: WritablePath, fetch: Fetch, wf: WF) -> FileAsset:
        target_path = scratch_dir / "target"
        shutil.copy(str(self.external_path), str(target_path))
        return FileAsset(target_path)
