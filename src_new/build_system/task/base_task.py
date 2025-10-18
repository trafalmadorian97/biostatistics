from abc import ABC, abstractmethod
from pathlib import Path

from pathlib_abc import WritablePath

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.wf.base_wf import WF


class Task[A: Asset](ABC):
    """
    Instructions for materializing an asset.
    """

    @abstractmethod
    @property
    def meta(self) -> Meta[A]:
        pass

    @abstractmethod
    @property
    def deps(self) -> list["Task"]:
        pass

    @abstractmethod
    def execute(
        self,
        scratch_dir: Path,
        fetch: Fetch,
        wf: WF,
    ) -> A:
        pass
