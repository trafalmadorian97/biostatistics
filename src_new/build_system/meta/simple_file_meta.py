from attrs import frozen

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleFileMeta(FileMeta):
    short_id: str
