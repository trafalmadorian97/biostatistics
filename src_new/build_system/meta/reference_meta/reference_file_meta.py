from pathlib import PurePath

from attrs import field, frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta


@frozen
class ReferenceFileMeta(FileMeta):
    group: str
    sub_folder: PurePath
    _asset_id: AssetId = field(converter=AssetId)
    extension: str = ".zip"

    @property
    def asset_id(self) -> AssetId:
        return self._asset_id
