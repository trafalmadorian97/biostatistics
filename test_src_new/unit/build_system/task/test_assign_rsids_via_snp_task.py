import tempfile
from pathlib import Path
from typing import Iterator

import polars as pl
import pytest

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameParquetFormat,
    DataFrameReadSpec,
)
from src_new.build_system.meta.read_spec.read_dataframe import scan_dataframe_asset
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.simple_meta_to_path import (
    SimpleMetaToPath,
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
from src_new.build_system.reference.schemas.chrom_rename_rules import CHROM_RENAME_RULES
from src_new.build_system.reference.schemas.hg19_sn151_schema import HG19_SNP151_SCHEMA
from src_new.build_system.reference.schemas.hg19_snp151_schema_valid_choms import (
    HG19_SNP151_VALID_CHROMS,
)
from src_new.build_system.scheduler.topological_scheduler import topological
from src_new.build_system.task.assign_rsids_via_snp151_task import (
    AssignRSIDSToSNPsViaSNP151Task,
)
from src_new.build_system.task.external_file_copy_task import ExternalFileCopyTask
from src_new.build_system.task.gwaslab.gwaslab_constants import GWASLAB_RSID_COL
from src_new.build_system.tasks.simple_tasks import find_tasks
from src_new.build_system.wf.base_wf import SimpleWF


@pytest.fixture
def parquet_snp151() -> Iterator[Path]:
    df = pl.scan_csv(
        "test_src_new/unit/build_system/task/dummy_snp151.txt",
        separator="\t",
        has_header=False,
        with_column_names=lambda x: HG19_SNP151_SCHEMA,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        out_path = tmpdir_path / "out.parquet"
        df.sink_parquet(out_path)
        yield out_path


@pytest.fixture
def dummy_processed_gwas_parquet() -> Iterator[Path]:
    df = pl.scan_csv(
        "test_src_new/unit/build_system/task/dummy_processed_gwas.csv",
        separator=",",
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        out_path = tmpdir_path / "out.parquet"
        df.sink_parquet(out_path)
        yield out_path


def test_assign_rsids_via_snp_task(
    tmp_path: Path, parquet_snp151: Path, dummy_processed_gwas_parquet: Path
):
    raw_snp_data_task = ExternalFileCopyTask(
        meta=SimpleFileMeta(
            AssetId("file_1"),
            read_spec=DataFrameReadSpec(format=DataFrameParquetFormat()),
        ),
        external_path=dummy_processed_gwas_parquet,
    )
    snp151_database_task = ExternalFileCopyTask(
        meta=SimpleFileMeta(
            AssetId("file_2"),
            read_spec=DataFrameReadSpec(format=DataFrameParquetFormat()),
        ),
        external_path=parquet_snp151,
    )

    task3 = AssignRSIDSToSNPsViaSNP151Task.create(
        raw_snp_data_task=raw_snp_data_task,
        snp151_database_file_task=snp151_database_task,
        asset_id="assign_rsids_via_snp_task",
        valid_chroms=HG19_SNP151_VALID_CHROMS,
        chrom_replace_rules=CHROM_RENAME_RULES,
    )

    tasks = find_tasks([task3])

    wf = SimpleWF()
    info: VerifyingTraceInfo = VerifyingTraceInfo.empty()

    asset_dir = tmp_path / "asset_dir"
    asset_dir.mkdir(exist_ok=True, parents=True)
    meta_to_path = SimpleMetaToPath(root=asset_dir)

    tracer = SimpleHasher.md5_hasher()
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
    asset = store[AssetId("assign_rsids_via_snp_task")]
    assert isinstance(asset, FileAsset)
    df = scan_dataframe_asset(asset, task3.meta).collect().to_pandas()
    assert "bad_chrom_dummy" not in df[GWASLAB_RSID_COL].tolist()
    assert len(df) == 1
    assert GWASLAB_RSID_COL in df.columns
    assert df[GWASLAB_RSID_COL].iloc[0] == "rstest_dummy"
