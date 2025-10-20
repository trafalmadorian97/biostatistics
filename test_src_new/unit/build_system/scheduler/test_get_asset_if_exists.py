from pathlib import Path

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import (
    SimpleMetaToPath,
)
from src_new.build_system.scheduler.asset_retrieval import get_asset_if_exists


def test_get_asset_if_exists(tmp_path: Path):
    meta = SimpleFileMeta(AssetId("test_item"))
    meta_to_path = SimpleMetaToPath(tmp_path)
    expected_path = meta_to_path(meta)
    expected_path.parent.mkdir(parents=True, exist_ok=True)
    expected_path.write_text("test file")
    expected_asset = FileAsset(expected_path)
    actual_asset = get_asset_if_exists(
        meta=meta,
        meta_to_path=meta_to_path,
    )
    assert actual_asset == expected_asset
