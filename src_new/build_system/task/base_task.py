from abc import ABC, abstractmethod
from pathlib import Path

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.wf.base_wf import WF


class GeneratingTask[A: Asset](ABC):
    """
    Instructions for materializing an asset.
    """

    @property
    @abstractmethod
    def meta(self) -> Meta[A]:
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
    ) -> A:
        pass


class SelectingTask[A: Asset](ABC):
    """
    Instructions for specifying an asset without generating new files.
    Example: the result might be a pointer into a pre-existing zip archive.
    """

    @property
    @abstractmethod
    def meta(self) -> Meta[A]:
        pass

    @property
    @abstractmethod
    def deps(self) -> list["Task"]:
        pass

    @abstractmethod
    def execute(
            self,
            fetch: Fetch,
            wf: WF,
    ) -> A:
        pass


Task = GeneratingTask | SelectingTask
