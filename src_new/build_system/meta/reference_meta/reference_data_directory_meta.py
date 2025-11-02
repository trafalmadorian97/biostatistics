from pathlib import PurePath

from attrs import field, frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import DirMeta


@frozen
class ReferenceDataDirectoryMeta(DirMeta):
    group: str
    sub_group: str
    sub_folder: PurePath
    _asset_id: AssetId = field(converter=AssetId)
    dirname: str | None = None

    @property
    def asset_id(self) -> AssetId:
        return self._asset_id
