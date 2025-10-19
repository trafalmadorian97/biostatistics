from abc import ABC
from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import GeneratingTask, Task
from src_new.build_system.wf.base_wf import WF


@frozen
class OSFCloneTask[A](GeneratingTask[DirectoryAsset]):
    _meta: Meta[DirectoryAsst]

    @property
    def meta(self) -> Meta[DirectoryAsset]:
        return self._meta

    @property
    def deps(self) -> list[Task]:
        return []

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> DirectoryAsset:
        pass
