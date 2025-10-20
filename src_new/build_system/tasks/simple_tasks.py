from typing import Iterator, Mapping

from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.task.base_task import Task
from src_new.build_system.tasks.base_tasks import Tasks


@frozen
class SimpleTasks(Tasks):
    _tasks: Mapping[AssetId, Task]  # implicit invariant: maps Meta[A] to Task[A]

    def __attrs_post_init__(self):
        for asset_id, task in self._tasks.items():
            assert task.meta.asset_id == asset_id

    def __getitem__(self, meta: AssetId) -> Task:
        return self._tasks[meta]

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[AssetId]:
        yield from self._tasks


# def
