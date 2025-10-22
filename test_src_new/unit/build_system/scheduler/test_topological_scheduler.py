from pathlib import Path

import pytest

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import (
    SimpleMetaToPath,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.base_tracer import (
    Tracer,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.imohash import (
    ImoHasher,
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
    dependency_graph,
    topological,
)
from src_new.build_system.task.copy_task import CopyTask
from src_new.build_system.task.counting_task import CountingTask
from src_new.build_system.task.external_file_copy_task import ExternalFileCopyTask
from src_new.build_system.tasks.simple_tasks import find_tasks
from src_new.build_system.wf.base_wf import DummyWF

#


@pytest.mark.parametrize(
    argnames="tracer",
    argvalues=[
        SimpleHasher.md5_hasher(),
        ImoHasher.with_xxhash_32(),
        ImoHasher.with_xxhash_128(),
    ],
)
def test_file_copying_task(tmp_path: Path, tracer: Tracer) -> None:
    """
    Test a number of basic properties of the topological scheduler
    """
    external_dir = tmp_path / "external"
    external_dir.mkdir(exist_ok=True, parents=True)
    external_file = external_dir / "external_file.txt"
    external_file.write_text("abc123")
    task1 = CountingTask(
        ExternalFileCopyTask(
            meta=SimpleFileMeta(AssetId("file_1")), external_path=external_file
        )
    )

    task2 = CountingTask(
        CopyTask(
            meta=SimpleFileMeta(
                AssetId("file_2"),
            ),
            dep_file_task=task1,
        )
    )

    task3 = CountingTask(
        CopyTask(
            meta=SimpleFileMeta(
                AssetId("file_3"),
            ),
            dep_file_task=task2,
        )
    )

    tasks = find_tasks([task3])

    wf = DummyWF()
    info: VerifyingTraceInfo = VerifyingTraceInfo.empty()

    asset_dir = tmp_path / "asset_dir"
    asset_dir.mkdir(exist_ok=True, parents=True)
    meta_to_path = SimpleMetaToPath(root=asset_dir)

    rebuilder = VerifyingTraceRebuilder(tracer)

    targets = [task3.meta.asset_id]

    # Verify that all files are created in the correct location
    store, info = topological(
        rebuilder=rebuilder,
        tasks=tasks,
        targets=targets,
        wf=wf,
        info=info,
        meta_to_path=meta_to_path,
    )

    file_1_path = meta_to_path(task1.meta)
    file_2_path = meta_to_path(task2.meta)
    file_3_path = meta_to_path(task3.meta)

    expected_store = {
        task1.meta.asset_id: FileAsset(file_1_path),
        task2.meta.asset_id: FileAsset(file_2_path),
        task3.meta.asset_id: FileAsset(file_3_path),
    }
    assert expected_store == store
    assert task1.run_count == 1
    assert task2.run_count == 1
    assert task3.run_count == 1

    # verify that only the 3rd task if rerun if the 3rd file is deleted

    file_3_path.unlink()
    topological(
        rebuilder=rebuilder,
        tasks=tasks,
        targets=targets,
        wf=wf,
        info=info,
        meta_to_path=meta_to_path,
    )

    assert task1.run_count == 1
    assert task2.run_count == 1
    assert task3.run_count == 2

    # verify early_cutoff: deleting the second file causes only the second task to be rerun

    file_2_path.unlink()
    topological(
        rebuilder=rebuilder,
        tasks=tasks,
        targets=targets,
        wf=wf,
        info=info,
        meta_to_path=meta_to_path,
    )

    assert task1.run_count == 1
    assert task2.run_count == 2
    assert task3.run_count == 2

    # check that verification failure works: if the input data changes, all downstream tasks are run

    file_1_path.unlink()
    external_file.write_text("Modified file")
    topological(
        rebuilder=rebuilder,
        tasks=tasks,
        targets=targets,
        wf=wf,
        info=info,
        meta_to_path=meta_to_path,
    )

    assert task1.run_count == 2
    assert task2.run_count == 3
    assert task3.run_count == 3

    # check that a deserialized info object can be used with the scheduler
    serialization_loc = tmp_path / "serialization_loc" / "info.yaml"
    info.serialize(serialization_loc)
    info_2 = VerifyingTraceInfo.deserialize(serialization_loc)
    topological(
        rebuilder=rebuilder,
        tasks=tasks,
        targets=targets,
        wf=wf,
        info=info_2,
        meta_to_path=meta_to_path,
    )

    assert task1.run_count == 2
    assert task2.run_count == 3
    assert task3.run_count == 3


def test_graph_generation(tmp_path: Path):
    external_dir = tmp_path / "external"
    external_dir.mkdir(exist_ok=True, parents=True)
    external_file = external_dir / "external_file.txt"
    external_file.write_text("abc123")
    task1 = ExternalFileCopyTask(
        meta=SimpleFileMeta(AssetId("file_1")), external_path=external_file
    )

    task2 = CopyTask(
        meta=SimpleFileMeta(
            AssetId("file_2"),
        ),
        dep_file_task=task1,
    )

    task3 = CopyTask(
        meta=SimpleFileMeta(
            AssetId("file_3"),
        ),
        dep_file_task=task2,
    )
    tasks = find_tasks([task3])
    graph_1 = dependency_graph(tasks, [task1.asset_id])
    graph_2 = dependency_graph(tasks, [task2.asset_id])
    graph_3 = dependency_graph(tasks, [task3.asset_id])
    assert len(graph_1) == 1
    assert len(graph_2) == 2
    assert len(graph_3) == 3
