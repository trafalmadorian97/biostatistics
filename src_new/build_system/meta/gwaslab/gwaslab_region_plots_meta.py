from pathlib import PurePath

from attrs import field, frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import DirMeta


@frozen
class GWASLabRegionPlotsMeta(DirMeta):
    trait: str
    project: str
    short_id: AssetId = field(converter=AssetId)
    sub_dir: PurePath = PurePath("analysis/lead_variant_region_plots")

    @property
    def asset_id(self) -> AssetId:
        return self.short_id
