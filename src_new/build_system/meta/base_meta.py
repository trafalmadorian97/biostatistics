from abc import ABC, abstractmethod

from src_new.build_system.meta.asset_id import AssetId

# @frozen
# class Meta[S: Asset](ABC):


class FileMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        pass


class DirMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        pass
