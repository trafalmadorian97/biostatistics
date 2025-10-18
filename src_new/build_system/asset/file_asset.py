from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset


@frozen
class FileAsset(Asset):
    path: Path

    def __attrs_post_init__(self):
        assert self.path.is_file()
