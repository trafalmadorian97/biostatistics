from pathlib import PurePath

import narwhals

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_SAMPLE_SIZE_COLUMN,
)


class EstimateNPipe(DataProcessingPipe):
    """
    Add cases and controls to get sample size.
    Due to effective sample size versus sample size contrast, this is approximate.
    """

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        return x.with_columns(
            (narwhals.col("NCAS") + narwhals.col("NCON")).alias(
                GWASLAB_SAMPLE_SIZE_COLUMN
            )
        )
