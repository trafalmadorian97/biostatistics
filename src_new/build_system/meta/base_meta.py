from abc import ABC, abstractmethod
from types import get_original_bases
from typing import ClassVar, get_args

from src_new.build_system.asset.base_asset import Asset


class Meta[S: Asset](ABC):
    """
    Stores uniquely identifying metadata describing either an asset that currently exists,
    or an asset that can be created by a build system.
    """

    asset_type: ClassVar

    @classmethod
    def __attrs_init_subclass__(cls):
        """
        Allows concrete subclasses to find their associated asset type at runtime.
        """
        cls.asset_type = get_args(get_original_bases(cls)[0])[0]

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass
