from abc import ABC, abstractmethod
from typing import Mapping

from src_new.build_system.meta.meta import Meta
from src_new.build_system.task.base_task import Task


class Tasks(ABC, Mapping[Meta, Task]):
    """
    Collection associating a piece of metadata with a task that can produce the corresponding asset.
    """

    @abstractmethod
    def __getitem__(self, meta: Meta) -> Task:
        pass
