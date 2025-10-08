from pathlib import PurePath

import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import GWASLAB_INFO_SCORE_COL


@frozen
class InfoFilterPipe(DataProcessingPipe):
    info_low_bound: float
    info_col_name: str = GWASLAB_INFO_SCORE_COL

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        return x.filter(narwhals.col(self.info_col_name) >= self.info_low_bound)
