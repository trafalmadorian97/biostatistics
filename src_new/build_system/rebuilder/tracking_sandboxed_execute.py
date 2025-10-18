from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.rebuilder.sandboxed_execute import sandboxed_execute
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


def tracking_sandboxed_execute[A: Asset](
    task: Task[A],
    meta_to_path: MetaToPath,
    wf: WF,
    fetch: Fetch,
) -> tuple[A, list[tuple[Meta, Asset]]]:
    deps: list[tuple[Meta, Asset]] = []

    class TrackingFetch(Fetch):
        def __call__[A2: Asset](self, m: Meta[A2]) -> A2:
            a = fetch(m)
            deps.append((m, a))
            return a

    result = sandboxed_execute(
        task=task, meta_to_path=meta_to_path, wf=wf, fetch=TrackingFetch()
    )
    return result, deps
