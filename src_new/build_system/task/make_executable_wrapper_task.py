import os
import stat
from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class MakeExecutableWrapperTask(Task):
    _inner: Task

    @property
    def meta(self) -> Meta:
        return self._inner.meta

    @property
    def deps(self) -> list["Task"]:
        return self._inner.deps

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        asset = self._inner.execute(scratch_dir=scratch_dir, fetch=fetch, wf=wf)
        assert isinstance(asset, FileAsset)
        current_permissions = asset.path.stat().st_mode
        new_permissions = (
            current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )
        os.chmod(asset.path, new_permissions)
        return asset
