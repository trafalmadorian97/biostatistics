from abc import ABC, abstractmethod

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId


class Fetch(ABC):
    """
    An interface for materializing or retrieving assets, given their id.
    """

    @abstractmethod
    def __call__(self, asset_id: AssetId) -> Asset:
        pass
