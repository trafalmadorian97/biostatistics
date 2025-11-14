from typing import Iterator, Mapping

from attrs import frozen

from mecfs_bio.build_system.meta.asset_id import AssetId
from mecfs_bio.build_system.task.base_task import Task
from mecfs_bio.build_system.tasks.base_tasks import Tasks


@frozen
class SimpleTasks(Tasks):
    _tasks: Mapping[AssetId, Task]

    def __attrs_post_init__(self):
        for asset_id, task in self._tasks.items():
            assert task.asset_id == asset_id

    def __getitem__(self, asset_id: AssetId) -> Task:
        return self._tasks[asset_id]

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[AssetId]:
        yield from self._tasks


def find_tasks(tasks: list[Task]) -> SimpleTasks:
    """
    Build a SimpleTasks object by walking the task graph
    """
    _tasks = {}
    visited = set()

    def explore_task(t: Task):
        visited.add(t.asset_id)
        for dep in t.deps:
            if dep.asset_id not in visited:
                explore_task(dep)
        _tasks[t.asset_id] = t

    for task in tasks:
        explore_task(task)
    return SimpleTasks(_tasks)
