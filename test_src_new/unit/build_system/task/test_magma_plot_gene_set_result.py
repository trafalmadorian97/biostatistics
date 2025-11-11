from pathlib import Path

from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.simple_directory_meta import SimpleDirectoryMeta
from src_new.build_system.task.fake_task import FakeTask
from src_new.build_system.task.magma.magma_plot_gene_set_result import (
    MAGMAPlotGeneSetResult,
)
from src_new.build_system.wf.base_wf import SimpleWF


def test_plot_gene_set_result(tmp_path: Path):
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    plot_task = MAGMAPlotGeneSetResult(
        meta=SimpleDirectoryMeta(AssetId("my_plot")),
        gene_set_analysis_task=FakeTask(SimpleDirectoryMeta(AssetId("gene_set"))),
    )

    def fetch(asset_id: AssetId):
        return DirectoryAsset(Path("test_src_new/unit/dummy_data/fake_gene_set_result"))

    result = plot_task.execute(scratch_dir=scratch, fetch=fetch, wf=SimpleWF())
    assert isinstance(result, DirectoryAsset)
