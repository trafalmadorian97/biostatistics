from abc import ABC, abstractmethod

from src_new.build_system.asset.base_asset import Asset


class Tracer(ABC):
    @abstractmethod
    def __call__(self, a: Asset) -> str:
        pass
