from typing import Callable

from attrs import define, frozen
from loguru import logger

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.rebuilder.fetch.restricted_fetch import RestrictedFetch
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.rebuilder.tracking_sandboxed_execute import (
    tracking_sandboxed_execute,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.base_tracer import (
    Tracer,
)
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@define
class VerifyingTraceInfo:
    """
    Note that this is mutable
    """

    trace_store: dict[Meta, tuple[str, list[tuple[Meta, str]]]]
    must_rebuild: set[Meta]

    @classmethod
    def empty(cls) -> "VerifyingTraceInfo":
        return cls(
            trace_store={},
            must_rebuild=set(),
        )


def update_verifying_trace_info_in_place(
    verifying_trace_info: VerifyingTraceInfo,
    meta: Meta,
    new_value_hash: str,
    deps_hashed: list[tuple[Meta, str]],
) -> None:
    new_rebuild_set = set(verifying_trace_info.must_rebuild) - {meta}
    new_trace_store = dict(verifying_trace_info.trace_store)
    new_trace_store[meta] = new_value_hash, deps_hashed
    verifying_trace_info.must_rebuild = new_rebuild_set
    verifying_trace_info.trace_store = new_trace_store


@frozen
class VerifyingTraceRebuilder(Rebuilder[VerifyingTraceInfo]):
    """
    Based on:
    Mokhov, Andrey, Neil Mitchell, and Simon Peyton Jones.
    "Build systems à la carte: Theory and practice."
    Journal of Functional Programming 30 (2020): e11.
    and Google AI
    """

    tracer: Tracer

    def rebuild[A: Asset](
        self,
        task: Task[A],
        asset: A | None,
        fetch: Fetch,
        wf: WF,
        info: VerifyingTraceInfo,
        meta_to_path: MetaToPath,
    ) -> tuple[A, VerifyingTraceInfo]:
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
            new_value_hash=self.tracer(new_value),
            deps_hashed=deps_traced,
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
