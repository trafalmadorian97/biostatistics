from abc import ABC, abstractmethod
from typing import Sequence

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.read_spec.read_spec import ReadSpec


# @frozen
# class Meta[S: Asset](ABC):


class FileMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        pass

    def read_spec(self) ->ReadSpec | None:
        return None


class DirMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        pass

