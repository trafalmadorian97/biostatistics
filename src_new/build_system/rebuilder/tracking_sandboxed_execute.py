from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.rebuilder.sandboxed_execute import sandboxed_execute
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


def tracking_sandboxed_execute(
    task: Task,
    meta_to_path: MetaToPath,
    wf: WF,
    fetch: Fetch,
) -> tuple[Asset, list[tuple[AssetId, Asset]]]:
    deps: list[tuple[AssetId, Asset]] = []

    class TrackingFetch(Fetch):
        def __call__(self, asset_id: AssetId) -> Asset:
            a = fetch(asset_id)
            deps.append((asset_id, a))
            return a

    result = sandboxed_execute(
        task=task, meta_to_path=meta_to_path, wf=wf, fetch=TrackingFetch()
    )
    return result, deps
