from attrs import frozen

from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.meta.base_meta import Meta

# from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleDirectoryMeta(Meta[DirectoryAsset]):
    short_id: str

    @property
    def short_name(self) -> str:
        return self.short_id
