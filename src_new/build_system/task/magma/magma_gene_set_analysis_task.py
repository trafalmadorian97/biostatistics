from pathlib import Path, PurePath

import structlog
from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.directory_asset import DirectoryAsset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.procesed_gwas_data_directory_meta import (
    ProcessedGwasDataDirectoryMeta,
)
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.task.magma.magma_gene_analysis_task import (
    GENE_ANALYSIS_OUTPUT_STEM_NAME,
)
from src_new.build_system.wf.base_wf import WF
from src_new.util.subproc.run_command import execute_command

logger = structlog.get_logger()

GENE_SET_ANALYSIS_OUTPUT_STEM_NAME = "gene_set_analysis_output"


@frozen
class DirectoryGeneSetSpec:
    gene_set_task: Task
    path_in_dir: PurePath


@frozen
class MagmaGeneSetAnalysisTask(Task):
    """
    The final step in the canonical MAGMA pipeline.
    See page 18 of the manual here: https://vu.data.surfsara.nl/s/MUiv3y1SFRePnyG?dir=/&editing=false&openfile=true
    """

    _meta: Meta
    magma_binary_task: Task
    magma_gene_analysis_task: Task
    gene_set: Task | DirectoryGeneSetSpec

    @property
    def _magma_binary_id(self) -> AssetId:
        return self.magma_binary_task.asset_id

    def _magma_gene_analysis_id(self) -> AssetId:
        return self.magma_gene_analysis_task.asset_id

    @property
    def _gene_set_task_id(self) -> AssetId:
        if isinstance(self.gene_set, Task):
            return self.gene_set.asset_id
        return self.gene_set.gene_set_task.asset_id

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        deps = [self.magma_binary_task, self.magma_gene_analysis_task]
        if isinstance(self.gene_set, Task):
            deps.append(self.gene_set)
        else:
            deps.append(self.gene_set.gene_set_task)
        return deps

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        binary_asset = fetch(self._magma_binary_id)
        gene_analysis_asset = fetch(self._magma_gene_analysis_id())
        gene_set_asset = fetch(self._gene_set_task_id)
        assert isinstance(binary_asset, FileAsset)
        assert isinstance(gene_analysis_asset, DirectoryAsset)
        if isinstance(self.gene_set, Task):
            assert isinstance(gene_set_asset, FileAsset)
            gene_set_path = gene_set_asset.path
        else:
            assert isinstance(self.gene_set, DirectoryGeneSetSpec)
            assert isinstance(gene_set_asset, DirectoryAsset)
            gene_set_path = gene_set_asset.path / self.gene_set.path_in_dir

        binary_path = binary_asset.path
        gene_analysis_path_root_path = gene_analysis_asset.path
        gene_analysis_full_path = gene_analysis_path_root_path / (
            GENE_ANALYSIS_OUTPUT_STEM_NAME + ".genes.raw"
        )
        out_dir = scratch_dir / "gene_set_analysis_dir"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_base_path = out_dir / GENE_SET_ANALYSIS_OUTPUT_STEM_NAME
        cmd = [
            str(binary_path),
            "--gene-results",
            str(gene_analysis_full_path),
            "--set-annot",
            str(gene_set_path),
            "--out",
            str(out_base_path),
        ]
        logger.debug(f"Running command: {' '.join(cmd)}")
        execute_command(cmd)
        return DirectoryAsset(out_dir)

    @classmethod
    def create(
        cls,
        asset_id: str,
        magma_gene_analysis_task: Task,
        magma_binary_task: Task,
        gene_set_task: Task | DirectoryGeneSetSpec,
    ):
        gene_analysis_meta = magma_gene_analysis_task.meta
        assert isinstance(gene_analysis_meta, ProcessedGwasDataDirectoryMeta)
        meta = ProcessedGwasDataDirectoryMeta(
            short_id=AssetId(asset_id),
            trait=gene_analysis_meta.trait,
            project=gene_analysis_meta.project,
            sub_dir=PurePath("analysis_results") / "magma",
        )
        return cls(
            magma_binary_task=magma_binary_task,
            gene_set=gene_set_task,
            magma_gene_analysis_task=magma_gene_analysis_task,
            meta=meta,
        )
