from abc import ABC, abstractmethod

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.asset.file_asset import FileAsset


@frozen
class Meta[S: Asset](ABC):
    """
    Stores uniquely identifying metadata describing either an asset that currently exists,
    or an asset that can be created by a build system.
    """

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass


class FileMeta(Meta[FileAsset], ABC):
    pass


class DirMeta(Meta[DirectoryAsset], ABC):
    pass
