from abc import ABC, abstractmethod
from pathlib import Path

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.wf.base_wf import WF


class GeneratingTask(ABC):
    """
    Instructions for materializing an asset.
    """

    @property
    @abstractmethod
    def meta(self) -> Meta:
        pass

    @property
    @abstractmethod
    def deps(self) -> list["Task"]:
        pass

    @abstractmethod
    def execute(
        self,
        scratch_dir: Path,
        fetch: Fetch,
        wf: WF,
    ) -> Asset:
        pass


Task = GeneratingTask
