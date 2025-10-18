import tempfile
from pathlib import Path

import attr

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


def sandboxed_execute[A: Asset](
    task: Task[A],
    meta_to_path: MetaToPath,
    wf: WF,
    fetch: Fetch,
) -> A:
    """
    Execute a task in a temporary directory, then move its result to the final location
    determined by the task's metadata.
    """
    meta = task.meta
    target_path = meta_to_path(meta)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "temp"
        temp_path.mkdir(parents=True, exist_ok=True)
        result = task.execute(scratch_dir=temp_path, fetch=fetch, wf=wf)
        target_path.parent.mkdir(exist_ok=True, parents=True)
        result = _move_asset(result, target_path)
    return result


def _move_asset[A: Asset](asset: A, dst: Path) -> A:
    if isinstance(asset, FileAsset):
        return attr.evolve(
            asset,
            path=asset.path.rename(dst),
        )
    raise ValueError("Unknown Asset Type")
