from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class FakeTask(Task):
    _meta: Meta
    """
    For testing
    """

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return []

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        raise NotImplementedError()
