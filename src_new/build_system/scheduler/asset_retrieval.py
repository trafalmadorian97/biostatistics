from typing import cast

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath


def get_asset_if_exists[A: Asset](
    meta: Meta[A],
    meta_to_path: MetaToPath,
) -> A | None:
    asset_type = meta.asset_type
    if asset_type == FileAsset:
        path = meta_to_path(meta)
        if path.is_file():
            return cast(A, FileAsset(path))
        return None
    raise ValueError(f"Unknown asset type{asset_type}")
