from attrs import define
from pathlib_abc import WritablePath

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@define
class CountingTask[A: Asset](Task[A]):
    """
    For testing.  Records the number of times a task has been executed
    """

    wrapped: Task[A]
    run_count: int = 0

    @property
    def deps(self) -> list["Task"]:
        return self.wrapped.deps

    def execute(self, scratch_dir: WritablePath, fetch: Fetch, wf: WF) -> A:
        self.run_count += 1
        return self.wrapped.execute(scratch_dir, fetch, wf)

    @property
    def meta(self) -> Meta[A]:
        return self.wrapped.meta
