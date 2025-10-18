from typing import Iterator, Mapping

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.task.base_task import Task
from src_new.build_system.tasks.base_tasks import Tasks


@frozen
class SimpleTasks(Tasks):
    _tasks: Mapping[Meta, Task]  # implicit invariant: maps Meta[A] to Task[A]

    def __attrs_post_init__(self):
        for meta, task in self._tasks.items():
            assert task.meta == meta

    def __getitem__[A: Asset](self, meta: Meta[A]) -> Task[A]:
        return self._tasks[meta]

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[Meta]:
        yield from self._tasks


# def
