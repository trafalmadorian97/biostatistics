from pathlib import PurePath
from typing import Sequence

import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)


@frozen
class CompositePipe(DataProcessingPipe):
    pipes: Sequence[DataProcessingPipe]

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        for pipe in self.pipes:
            x = pipe.process(x, data_cache_root)
        return x
