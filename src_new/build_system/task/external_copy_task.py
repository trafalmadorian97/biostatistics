import shutil
from pathlib import Path

from pathlib_abc import WritablePath

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


class ExternalCopyTask(Task[FileAsset]):
    """
    Copies a file from an external source.
    Use for testing
    """

    _meta: SimpleFileMeta
    external_path: Path

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
