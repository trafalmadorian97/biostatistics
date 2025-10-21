from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta


@frozen
class FilteredGWASDataMeta(FileMeta):
    @property
    def asset_id(self) -> AssetId:
        return self.short_id

    short_id: AssetId
    trait: str
    project: str
    sub_dir: str
    extension:str =".parquet"
