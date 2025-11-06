from typing import Sequence

import narwhals
from attrs import frozen

from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


@frozen
class ShiftedLogPipe(DataProcessingPipe):
    base: int
    cols_to_exclude: Sequence[str]

    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        schema = x.collect_schema()
        for col_name in schema.keys():
            if col_name not in self.cols_to_exclude:
                x = x.with_columns(
                    (narwhals.col(col_name) + 1).log(base=self.base).alias(col_name)
                )
        return x
