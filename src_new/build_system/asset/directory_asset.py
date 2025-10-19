from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset


@frozen
class DirectoryAsset(Asset):
    path: Path

    def __attrs_post_init__(self):
        assert self.path.is_dir()
