from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import DirMeta

# from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleDirectoryMeta(DirMeta):
    directory_short_id: AssetId

    @property
    def asset_id(self) -> AssetId:
        return self.directory_short_id
