from abc import ABC, abstractmethod
from typing import Mapping

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.task.base_task import Task


class Tasks(ABC, Mapping[Meta, Task]):
    """
    Collection associating a piece of metadata with a task that can produce the corresponding asset.
    """

    @abstractmethod
    def __getitem__[A: Asset](self, meta: Meta[A]) -> Task[A]:
        pass
