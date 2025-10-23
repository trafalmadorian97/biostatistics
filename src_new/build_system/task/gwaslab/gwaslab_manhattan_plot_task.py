from pathlib import Path

import attrs
import gwaslab as gl
import matplotlib.pyplot as plt

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.gwaslab_meta.gwaslab_manhattan_plot_meta import (
    GWASLabManhattanQQPlotMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_sumstats_meta import (
    GWASLabSumStatsMeta,
)
from src_new.build_system.meta.read_spec.read_sumstats import read_sumstats
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)
from src_new.build_system.wf.base_wf import WF
from src_new.util.plotting.save_fig import write_plots_to_dir


@attrs.frozen
class GWASLabManhattanPlotTask(Task):
    """
    A task to generate a manhattan plot
    Uses Gwaslab.
    see: https://cloufield.github.io/gwaslab/Visualization/
    """

    _sumstats_task: GWASLabCreateSumstatsTask
    _meta: GWASLabManhattanQQPlotMeta
    sig_level: float = 5e-8
    top_cut: int = 12  # upper bound of graph

    @property
    def meta(self) -> GWASLabManhattanQQPlotMeta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return [self._sumstats_task]

    @property
    def _input_meta(self) -> GWASLabSumStatsMeta:
        input_meta = self._sumstats_task.meta
        assert isinstance(input_meta, GWASLabSumStatsMeta)
        return input_meta

    @property
    def _input_asset_id(self) -> AssetId:
        return self._input_meta.asset_id

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        sumstats_asset = fetch(self._input_asset_id)
        sumstats: gl.Sumstats = read_sumstats(sumstats_asset)
        fig, (ax1, ax2) = plt.subplots(figsize=(24, 16), ncols=2, nrows=1)
        figs = {}
        plot_name = "mqq"
        sumstats.plot_mqq(
            figax=[fig, ax1, ax2],
            skip=2,
            cut=self.top_cut,
            mode="mqq",
            scaled=True,
            anno="GENENAME",
            sig_level_lead=self.sig_level,
        )
        figs[plot_name] = fig
        write_plots_to_dir(scratch_dir, figs)
        return FileAsset(scratch_dir / str(plot_name + ".png"))

    @classmethod
    def create(
        cls,
        sumstats_task: GWASLabCreateSumstatsTask,
        asset_id: str,
        sig_leve: float = 5e-8,
    ):
        input_meta = sumstats_task.meta
        assert isinstance(input_meta, GWASLabSumStatsMeta)
        meta = GWASLabManhattanQQPlotMeta(
            trait=input_meta.trait,
            project=input_meta.project,
            short_id=AssetId(asset_id),
        )
        return cls(
            sumstats_task=sumstats_task,
            meta=meta,
            sig_level=sig_leve,
        )
