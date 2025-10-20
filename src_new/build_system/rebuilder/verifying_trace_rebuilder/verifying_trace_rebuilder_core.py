from typing import Callable

from attrs import frozen
from loguru import logger

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.rebuilder.fetch.restricted_fetch import RestrictedFetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.rebuilder.tracking_sandboxed_execute import (
    tracking_sandboxed_execute,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.info import (
    VerifyingTraceInfo,
    update_verifying_trace_info_in_place,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.base_tracer import (
    Tracer,
)
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class VerifyingTraceRebuilder(Rebuilder[VerifyingTraceInfo]):
    """
    A rebuilder that calculates traces for the assets it manages, and uses these traces
    to decide when to rebuild.
    Based on:
    Mokhov, Andrey, Neil Mitchell, and Simon Peyton Jones.
    "Build systems à la carte: Theory and practice."
    Journal of Functional Programming 30 (2020): e11.
    """

    tracer: Tracer

    def rebuild(
        self,
        task: Task,
        asset: Asset | None,
        fetch: Fetch,
        wf: WF,
        info: VerifyingTraceInfo,
        meta_to_path: MetaToPath,
    ) -> tuple[Asset, VerifyingTraceInfo]:
        must_rebuild = task.meta in info.must_rebuild

        def fetch_trace(meta: Meta) -> str:
            return self.tracer(fetch(meta))

        if not must_rebuild and asset is not None:
            logger.debug(
                f"Attempting to verify the trace of asset {task.meta.short_name}..."
            )
            old_value_trace = self.tracer(asset)
            if verify_trace(
                m=task.meta,
                value_trace=old_value_trace,
                fetch_trace=fetch_trace,
                info=info,
            ):
                logger.debug(
                    f"Successfully verified the trace of asset {task.meta.short_name}."
                )
                return asset, info
            logger.debug(
                f"Failed to verify the trace  of asset {task.meta.short_name}."
            )

        logger.debug(f"Materializing asset {task.meta.short_name}....")
        new_value, deps = tracking_sandboxed_execute(
            task=task,
            meta_to_path=meta_to_path,
            wf=wf,
            fetch=RestrictedFetch.from_task(fetch=fetch, task=task),
        )
        deps_traced = [(k, self.tracer(v)) for k, v in deps]
        update_verifying_trace_info_in_place(
            verifying_trace_info=info,
            meta=task.meta,
            new_value_trace=self.tracer(new_value),
            deps_traced=deps_traced,
        )
        return new_value, info


def verify_trace(
    m: Meta,
    value_trace: str,
    fetch_trace: Callable[[Meta], str],
    info: VerifyingTraceInfo,
) -> bool:
    """ """
    if m not in info.trace_store:
        return False
    recorded_trace, recorded_deps = info.trace_store[m]
    if recorded_trace != value_trace:
        return False
    for dep, dep_hash in recorded_deps:
        if fetch_trace(dep) != dep_hash:
            return False
    return True
