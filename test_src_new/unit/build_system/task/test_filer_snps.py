from pathlib import Path

import pandas as pd

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameParquetFormat,
    DataFrameReadSpec,
)
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.runner.simple_runner import SimpleRunner
from src_new.build_system.task.external_file_copy_task import ExternalFileCopyTask
from src_new.build_system.task.filter_snps_task import FilterSNPsTask


def test_filer_snps(tmp_path: Path):
    """
    Test that we can correctly filter a dataframe of SNPs
    """
    external_dir = tmp_path / "external"
    store_path = tmp_path / "store.yaml"
    asset_root = tmp_path / "assets"
    external_dir.mkdir(parents=True, exist_ok=True)
    asset_root.mkdir(parents=True, exist_ok=True)
    df_1 = pd.DataFrame({"ID": [1, 2, 3]})
    df_2 = pd.DataFrame({"ID": [1]})
    path_1 = external_dir / "df_1.parqet"
    path_2 = external_dir / "df_2.parqet"
    df_1.to_parquet(path_1)
    df_2.to_parquet(path_2)
    task_1 = ExternalFileCopyTask(
        meta=SimpleFileMeta(
            AssetId("file_1"), read_spec=DataFrameReadSpec(DataFrameParquetFormat())
        ),
        external_path=path_1,
    )

    task_2 = ExternalFileCopyTask(
        meta=SimpleFileMeta(
            AssetId("file_2"), read_spec=DataFrameReadSpec(DataFrameParquetFormat())
        ),
        external_path=path_2,
    )
    task3 = FilterSNPsTask(
        raw_gwas_task=task_1,
        snp_list_task=task_2,
        meta=FilteredGWASDataMeta(
            AssetId("file3"), "trait", "proj", "raw", extension=".parquet"
        ),
    )
    runner = SimpleRunner(info_store=store_path, asset_root=asset_root)
    runner.run(targets=[task3])
    result_df = pd.read_parquet(runner.meta_to_path(task3.meta))
    assert len(result_df) == 1
