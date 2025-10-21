from pathlib import Path
from typing import Mapping

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import SimpleMetaToPath
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.base_tracer import Tracer
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_info import VerifyingTraceInfo
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_rebuilder_core import \
    VerifyingTraceRebuilder
from src_new.build_system.scheduler.topological_scheduler import topological
from src_new.build_system.task.base_task import Task
from src_new.build_system.tasks.simple_tasks import find_tasks
from src_new.build_system.wf.base_wf import DummyWF


@frozen
class SimpleRunner:
    info_store: Path
    tracer: Tracer
    asset_root: Path

    def run(self,targets: list[Task] ) -> Mapping[AssetId, Asset]:
        if self.info_store.is_file():
            info=  VerifyingTraceInfo.deserialize(self.info_store)
        else:
            info = VerifyingTraceInfo.empty()
        rebuilder = VerifyingTraceRebuilder(self.tracer)
        wf =DummyWF()
        meta_to_path = SimpleMetaToPath(root=self.asset_root)
        tasks = find_tasks(targets)
        store, info =topological(
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
