from abc import ABC, abstractmethod

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta


class Fetch(ABC):
    """
    An interface for materializing or retrieving assets, given their metadata.
    """

    @abstractmethod
    def __call__[A: Asset](self, m: Meta[A]) -> A:
        pass
