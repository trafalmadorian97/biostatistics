import shlex
import subprocess
from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import GeneratingTask, Task
from src_new.build_system.wf.base_wf import WF


@frozen
class OSFRetrievalTask(GeneratingTask[FileAsset]):
    _meta: GWASSummaryDataFileMeta
    osf_project_id: str

    @property
    def meta(self) -> GWASSummaryDataFileMeta:
        return self._meta

    @property
    def deps(self) -> list[Task]:
        return []

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> FileAsset:
        tmp_dst = scratch_dir / "tmp"
        result = subprocess.run(
            [
                "uv",
                "run",
                "osf",
                "-p",
                self.osf_project_id,
                "fetch",
                shlex.quote(str(self._meta.project_path)),
                str(tmp_dst),
            ],
            check=True,
        )
        return FileAsset(
            tmp_dst,
        )
