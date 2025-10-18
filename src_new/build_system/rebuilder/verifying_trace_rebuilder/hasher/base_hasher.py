from abc import ABC, abstractmethod

from src_new.build_system.asset.base_asset import Asset


class Hasher(ABC):
    @abstractmethod
    def compute_hash(self, a: Asset) -> str:
        pass
