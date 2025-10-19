from attrs import frozen
from pathlib_abc import WritablePath

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.task.remote_file_task import RemoteFileTask
from src_new.build_system.wf.base_wf import WF


@frozen
class GWASSummaryStatsFileTask(RemoteFileTask):
    """
    A task that fetches GWAS summary statistics from a remote server.
    """

    url: str
    md5: str | None
    _meta: GWASSummaryDataFileMeta

    @property
    def meta(self) -> GWASSummaryDataFileMeta:
        return self._meta

    @property
    def deps(self) -> list[Task]:
        return []

    def execute(self, scratch_dir: WritablePath, fetch: Fetch, wf: WF) -> FileAsset:
        local_target = scratch_dir / "target"
        wf.download_from_url(
            url=self.url,
            md5_hash=self.md5,
            local_path=local_target,
        )
        return FileAsset(
            path=local_target,
        )
