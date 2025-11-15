from pathlib import PurePath

from attrs import frozen

from mecfs_bio.build_system.meta.asset_id import AssetId
from mecfs_bio.build_system.meta.base_meta import FileMeta


@frozen
class ResultTableMeta(FileMeta):
    _asset_id: str
    trait: str
    project: str
    extension: str
    sub_dir: PurePath = PurePath("analysis")

    @property
    def asset_id(self) -> AssetId:
        return AssetId(self._asset_id)
