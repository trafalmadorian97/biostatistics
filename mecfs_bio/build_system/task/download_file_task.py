import hashlib
from pathlib import Path

import structlog
from attrs import frozen

from mecfs_bio.build_system.asset.file_asset import FileAsset
from mecfs_bio.build_system.meta.meta import Meta
from mecfs_bio.build_system.rebuilder.fetch.base_fetch import Fetch
from mecfs_bio.build_system.task.base_task import Task
from mecfs_bio.build_system.wf.base_wf import WF

logger = structlog.get_logger()


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
        wf.download_from_url(url=self._url, local_path=target)
        if self._md5_hash is not None:
            logger.debug("Verifying MD5 hash of downloaded file...")
            hash_of_downloaded_file = calc_md5_checksum(target)
            assert hash_of_downloaded_file == self._md5_hash, (
                f"Expected Hash {hash_of_downloaded_file} to be equal to {self._md5_hash}"
            )
            logger.debug("Hash verified.")
        return FileAsset(target)


def calc_md5_checksum(filepath: Path, chunk_size: int = 8192) -> str:
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break  # End of file
            hasher.update(chunk)
    return hasher.hexdigest()
