from attrs import frozen

from src_new.build_system.meta.base_meta import DirMeta

# from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleDirectoryMeta(DirMeta):
    directory_short_id: str

    @property
    def short_name(self) -> str:
        return self.directory_short_id
