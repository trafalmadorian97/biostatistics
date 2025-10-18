from abc import ABC

from src_new.build_system.asset.base_asset import Asset


class Meta[S: Asset](ABC):
    """
    Stores uniquely identifying metadata describing either an asset that currently exists,
    or an asset that can be created by a build system.
    """

    pass
