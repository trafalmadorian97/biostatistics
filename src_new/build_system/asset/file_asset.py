from pathlib import Path

from attrs import frozen
from upath import UPath

from src_new.build_system.asset.base_asset import Asset


@frozen
class FileAsset(Asset):
    path: Path
