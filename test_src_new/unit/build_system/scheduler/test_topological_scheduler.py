from pathlib import Path

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import (
    SimpleMetaToPath,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.simple_hasher import (
    SimpleHasher,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_rebuilder_core import (
    VerifyingTraceInfo,
    VerifyingTraceRebuilder,
)
from src_new.build_system.scheduler.topological_scheduler import topological
from src_new.build_system.task.copy_task import CopyTask
from src_new.build_system.task.counting_task import CountingTask
from src_new.build_system.task.external_file_copy_task import ExternalFileCopyTask
from src_new.build_system.tasks.simple_tasks import SimpleTasks
from src_new.build_system.wf.base_wf import DummyWF


def test_file_copying_task(tmp_path: Path):
    """
    Test a number of basic properties of the topological scheduler
    """
    external_dir = tmp_path / "external"
    external_dir.mkdir(exist_ok=True, parents=True)
    external_file = external_dir / "external_file.txt"
    external_file.write_text("abc123")
    task1 = CountingTask(
        ExternalFileCopyTask(meta=SimpleFileMeta("file_1"), external_path=external_file)
    )

    task2 = CountingTask(
        CopyTask(
            meta=SimpleFileMeta("file_2"),
            dep_file_task=task1,
        )
    )

    task3 = CountingTask(
        CopyTask(
            meta=SimpleFileMeta("file_3"),
            dep_file_task=task2,
        )
    )

    tasks = SimpleTasks(
        {
            task1.meta: task1,
            task2.meta: task2,
            task3.meta: task3,
        }
    )

    wf = DummyWF()
    info = VerifyingTraceInfo.empty()

    asset_dir = tmp_path / "asset_dir"
    asset_dir.mkdir(exist_ok=True, parents=True)
    meta_to_path = SimpleMetaToPath(root=asset_dir)

    rebuilder = VerifyingTraceRebuilder(SimpleHasher.md5_hasher())

    targets = [task3.meta]

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
        task1.meta: FileAsset(file_1_path),
        task2.meta: FileAsset(file_2_path),
        task3.meta: FileAsset(file_3_path),
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
