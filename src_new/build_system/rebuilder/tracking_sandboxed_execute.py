from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.meta import Meta
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
) -> tuple[Asset, list[tuple[Meta, Asset]]]:
    deps: list[tuple[Meta, Asset]] = []

    class TrackingFetch(Fetch):
        def __call__(self, m: Meta) -> Asset:
            a = fetch(m)
            deps.append((m, a))
            return a

    result = sandboxed_execute(
        task=task, meta_to_path=meta_to_path, wf=wf, fetch=TrackingFetch()
    )
    return result, deps
