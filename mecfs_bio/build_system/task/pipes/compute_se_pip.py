import narwhals
import scipy.stats

from mecfs_bio.build_system.task.gwaslab.gwaslab_constants import (
    GWASLAB_BETA_COL,
    GWASLAB_P_COL,
    GWASLAB_SE_COLUMN,
)
from mecfs_bio.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


class ComputeSEPipe(DataProcessingPipe):
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        pd_x = x.collect().to_pandas()
        pd_x[GWASLAB_SE_COLUMN] = abs(pd_x[GWASLAB_BETA_COL]) / abs(
            scipy.stats.norm.ppf(pd_x[GWASLAB_P_COL] / 2)
        )
        return narwhals.from_native(pd_x).lazy()
