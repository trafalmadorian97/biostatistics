from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta
from src_new.build_system.meta.read_spec.read_spec import ReadSpec

# from src_new.build_system.meta.file_meta import FileMeta


@frozen
class SimpleFileMeta(FileMeta):
    short_id: AssetId
    _read_spec: ReadSpec | None = None

    @property
    def asset_id(self) -> AssetId:
        return self.short_id

    def read_spec(self) -> ReadSpec | None:
        return self._read_spec
