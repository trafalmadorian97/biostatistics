from pathlib import PurePath

import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_SAMPLE_SIZE_COLUMN,
)


@frozen
class SetSampleSizePipe(DataProcessingPipe):
    sample_size: int

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        return x.with_columns(
            narwhals.lit(self.sample_size, dtype=narwhals.dtypes.Int64).alias(
                GWASLAB_SAMPLE_SIZE_COLUMN
            )
        )
