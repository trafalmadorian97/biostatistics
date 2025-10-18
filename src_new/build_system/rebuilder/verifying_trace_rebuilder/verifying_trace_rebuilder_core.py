from typing import Mapping, Callable

from attrs import frozen
from numpy.lib.tests.test_utils import old_func

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.rebuilder.base_fetch import Fetch
from src_new.build_system.rebuilder.base_rebuilder import Rebuilder
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath
from src_new.build_system.rebuilder.tracking_sandboxed_execute import (
    tracking_sandboxed_execute,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.hasher.base_hasher import (
    Hasher,
)
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class VerifyingTraceInfo:
    hash_store: Mapping[Meta, tuple[str, list[tuple[Meta, str]]]]
    must_rebuild: frozenset[Meta]


def update_verifying_trace_info(
    verifying_trace_info: VerifyingTraceInfo,
    meta: Meta,
    new_value_hash: str,
    deps_hashed: list[tuple[Meta, str]],
):
    new_rebuild_set = frozenset(set(verifying_trace_info.must_rebuild) - {meta})
    new_hash_store = dict(verifying_trace_info.hash_store)
    new_hash_store[meta] = new_value_hash, deps_hashed
    return VerifyingTraceInfo(
        must_rebuild=new_rebuild_set,
        hash_store=new_hash_store,
    )


@frozen
class VerifyingTraceRebuilder(Rebuilder[VerifyingTraceInfo]):
    """
    Based on:
    Mokhov, Andrey, Neil Mitchell, and Simon Peyton Jones.
    "Build systems à la carte: Theory and practice."
    Journal of Functional Programming 30 (2020): e11.
    and Google AI
    """

    hasher: Hasher
    meta_to_path: MetaToPath

    def rebuild[A: Asset](
        self,
        task: Task[A],
        value: A | None,
        fetch: Fetch,
        wf: WF,
        info: VerifyingTraceInfo,
    ) -> tuple[A, VerifyingTraceInfo]:
        must_rebuild = task.meta in info.must_rebuild

        def fetch_hash(meta: Meta) -> str:
            return self.hasher.compute_hash(fetch(meta))

        if not must_rebuild and value is not None:
            old_value_hash = self.hasher.compute_hash(value)
            if verify_hash(
                m=task.meta, value_hash=old_value_hash, fetch_hash=fetch_hash, info=info
            ):
                return value, info

        new_value, deps = tracking_sandboxed_execute(
            task=task,
            meta_to_path=self.meta_to_path,
            wf=wf,
            fetch=fetch,
        )
        deps_hashed = [(k, self.hasher.compute_hash(v)) for k, v in deps]
        info = update_verifying_trace_info(
            verifying_trace_info=info,
            meta=task.meta,
            new_value_hash=self.hasher.compute_hash(new_value),
            deps_hashed=deps_hashed,
        )
        return new_value, info


def verify_hash(
    m: Meta,
    value_hash: str,
    fetch_hash: Callable[[Meta], str],
    info: VerifyingTraceInfo,
) -> bool:
    """ """
    if m not in info.hash_store:
        return False
    recorded_hash, recorded_deps = info.hash_store[m]
    if recorded_hash != value_hash:
        return False
    for dep, dep_hash in recorded_deps:
        if fetch_hash(dep) != dep_hash:
            return False
    return True
