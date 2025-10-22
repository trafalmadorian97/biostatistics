from pathlib import PurePath

from attrs import field, frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta
from src_new.build_system.meta.read_spec.dataframe_read_spec import DataFrameTextFormat
from src_new.build_system.meta.read_spec.read_spec import ReadSpec


@frozen
class GWASLabLeadVariantsMeta(FileMeta):
    @property
    def asset_id(self) -> AssetId:
        return self.short_id

    trait: str
    project: str
    short_id: AssetId = field(converter=AssetId)
    sub_dir: PurePath = PurePath("analysis/lead_variants")

    def read_spec(self) -> ReadSpec | None:
        return ReadSpec(format=DataFrameTextFormat(separator=","))
