from pathlib import PurePath

import narwhals

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_BETA_COL,
    GWASLAB_ODDS_RATIO_COL,
)


class ComputeBetaPipe(DataProcessingPipe):
    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        return x.with_columns(
            narwhals.col(GWASLAB_ODDS_RATIO_COL).log().alias(GWASLAB_BETA_COL)
        )
