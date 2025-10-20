from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta

# from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleFileMeta(FileMeta):
    short_id: AssetId

    @property
    def asset_id(self) -> AssetId:
        return self.short_id
