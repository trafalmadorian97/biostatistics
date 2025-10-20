from abc import ABC, abstractmethod
from typing import Mapping

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.task.base_task import Task


class Tasks(ABC, Mapping[AssetId, Task]):
    """
    Collection associating a piece of metadata with a task that can produce the corresponding asset.
    """

    @abstractmethod
    def __getitem__(self, asset_id: AssetId) -> Task:
        pass
