import shutil
from pathlib import Path

import pytest
from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.task.reference.download_file_task import (
    DownloadFileTask,
    calc_md5_checksum,
)
from src_new.build_system.wf.base_wf import WF


@frozen
class FakeWF(WF):
    source_file: Path

    def download_from_url(self, url: str, local_path: Path) -> None:
        shutil.copyfile(self.source_file, local_path)


def test_md5_check_passes_fails_appropriately(tmp_path: Path):
    """
    Check that a mismatched md5 hash raises an error, while a matching hash does not
    """
    external_file_path = tmp_path / "external" / "myfile.txt"
    external_file_path.parent.mkdir(parents=True, exist_ok=True)
    external_file_path.write_text("yoyoyoy")
    hash_of_file = calc_md5_checksum(external_file_path)
    wf = FakeWF(source_file=external_file_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    tsk_1 = DownloadFileTask(
        meta=SimpleFileMeta.create("my_file"), url="fake_url", md5_hash=hash_of_file
    )

    tsk_2 = DownloadFileTask(
        meta=SimpleFileMeta.create("my_file"), url="fake_url", md5_hash="wrong_hash"
    )

    def fake_fetch(asset_id: AssetId) -> Asset:
        raise NotImplementedError("")

    tsk_1.execute(scratch_dir=scratch, fetch=fake_fetch, wf=wf)
    with pytest.raises(AssertionError):
        tsk_2.execute(scratch_dir=scratch, fetch=fake_fetch, wf=wf)
