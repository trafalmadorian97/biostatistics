import pickle
from pathlib import Path

import gwaslab

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameReadSpec,
    DataFrameTextFormat,
)
from src_new.build_system.task.fake_task import FakeTask
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)
from src_new.build_system.wf.base_wf import SimpleWF


def test_gwaslab_sumstats(
    tmp_path: Path,
):
    task = GWASLabCreateSumstatsTask(
        asset_id=AssetId("sumstats_task"),
        basic_check=True,
        df_source_task=FakeTask(
            meta=FilteredGWASDataMeta(
                AssetId("input"),
                "dummy_trait",
                "dummy_project",
                "dummy_Dir",
                read_spec=DataFrameReadSpec(DataFrameTextFormat(separator=" ")),
            )
        ),
        genome_build="38",
    )

    def fetch(asset_id: AssetId) -> Asset:
        return FileAsset(Path("test_src_new/unit/build_system/task/dummy_data.regenie"))

    asset_result = task.execute(scratch_dir=tmp_path, fetch=fetch, wf=SimpleWF())
    with open(asset_result.path, "rb") as f:
        loaded = pickle.load(
            f,
        )
    assert isinstance(loaded, gwaslab.Sumstats)
