from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class DownloadFileTask(Task):
    _meta: Meta
    _url: str
    _md5_hash: str | None

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return []

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> FileAsset:
        target = scratch_dir / self.meta.asset_id
        wf.download_from_url(url=self._url, md5_hash=self._md5_hash, local_path=target)
        return FileAsset(target)
