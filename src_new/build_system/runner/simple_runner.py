from pathlib import Path
from typing import Mapping, Sequence

import attrs
from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import (
    SimpleMetaToPath,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.base_tracer import (
    Tracer,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.simple_hasher import (
    SimpleHasher,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_info import (
    VerifyingTraceInfo,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_rebuilder_core import (
    VerifyingTraceRebuilder,
)
from src_new.build_system.scheduler.topological_scheduler import (
    dependees_of_targets_from_tasks,
    topological,
)
from src_new.build_system.task.base_task import Task
from src_new.build_system.tasks.simple_tasks import find_tasks
from src_new.build_system.wf.base_wf import SimpleWF


@frozen
class SimpleRunner:
    """
    Simple wrapper class that orchestrates
    an execution of the workflow build system with a topological scheduler and verifying trace rebuilder

    info_store: path at which to store persistent cash for build-system internal information
    asset_root: root under which to create the asset store
    tracer: algorithm uses to calculate verifying traces of assets.  An example would be a hashing algorithm.  changing this forces all assets to be rebuilt
    """

    info_store: Path
    asset_root: Path
    tracer: Tracer = SimpleHasher.md5_hasher()

    @property
    def meta_to_path(self) -> SimpleMetaToPath:
        return SimpleMetaToPath(root=self.asset_root)

    def run(
        self, targets: list[Task], must_rebuild_transitive: Sequence[Task] = tuple()
    ) -> Mapping[AssetId, Asset]:
        """
        Targets: the ultimate targets we aim to produce.  All transitive dependencies of these targets will either be rebuilt, or fetched (determined according to that status of their trace)
        must_rebuild_transitive: list of tasks that the rebuilder will be forced to rebuild, regardless of the status of their trace.
           - This is particularly useful when you have changed the code that generates and asset, and so want it and its depndees to be regenerated.
        returns:
        mapping from asset id to file system information for all assets that were built or retrieved as part of the execution of the scheduler
        """
        if self.info_store.is_file():
            info = VerifyingTraceInfo.deserialize(self.info_store)
        else:
            info = VerifyingTraceInfo.empty()
        rebuilder = VerifyingTraceRebuilder(self.tracer)
        wf = SimpleWF()
        meta_to_path = self.meta_to_path
        tasks = find_tasks(targets)
        must_rebuild_graph = dependees_of_targets_from_tasks(
            tasks=tasks,
            targets=[task.asset_id for task in must_rebuild_transitive],
        )
        info = attrs.evolve(info, must_rebuild=set(must_rebuild_graph.nodes))
        store, info = topological(
            rebuilder=rebuilder,
            tasks=tasks,
            info=info,
            wf=wf,
            meta_to_path=meta_to_path,
            targets=[target.asset_id for target in targets],
        )
        self.info_store.parent.mkdir(parents=True, exist_ok=True)
        info.serialize(self.info_store)
        return store
