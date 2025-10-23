import zipfile
from pathlib import Path

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.task.extraction_from_zip_task import ExtractFromZipTask
from src_new.build_system.task.fake_task import FakeTask
from src_new.build_system.wf.base_wf import SimpleWF


def test_extraction_from_zip(tmp_path: Path):
    name_in_archive = "my_compressed_file"
    source_zip_path = tmp_path / "source_zip.zip"
    scratch_dir = tmp_path / "scratch"
    with zipfile.ZipFile(source_zip_path, "w") as source_zip:
        source_zip.writestr(name_in_archive, "12345678910")
    tsk = ExtractFromZipTask(
        meta=SimpleFileMeta(AssetId("my_file")),
        source_file_task=FakeTask(meta=SimpleFileMeta(AssetId("dummy_file"))),
        file_to_extract=name_in_archive,
    )

    def fetch(asset_id: AssetId) -> Asset:
        return FileAsset(source_zip_path)

    result = tsk.execute(scratch_dir=scratch_dir, fetch=fetch, wf=SimpleWF())
    assert isinstance(result, FileAsset)
    assert result.path == scratch_dir / name_in_archive
