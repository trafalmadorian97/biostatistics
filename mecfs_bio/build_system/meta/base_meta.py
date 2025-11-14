from abc import ABC, abstractmethod

from mecfs_bio.build_system.meta.asset_id import AssetId
from mecfs_bio.build_system.meta.read_spec.read_spec import ReadSpec

# @frozen
# class Meta[S: Asset](ABC):


class FileMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        """
        A uniquely identifying ID for the asset
        """
        pass

    def read_spec(self) -> ReadSpec | None:
        """
        A specifier describing how the data should be read
        """
        return None


class DirMeta(ABC):
    @property
    @abstractmethod
    def asset_id(self) -> AssetId:
        pass
