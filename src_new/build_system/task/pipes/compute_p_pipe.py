import narwhals

from src_new.build_system.task.gwaslab.gwaslab_constants import (
    GWASLAB_MLOG10P_COL,
    GWASLAB_P_COL,
)
from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


class ComputePPipe(DataProcessingPipe):
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        schema = x.collect_schema()
        assert GWASLAB_P_COL not in schema
        assert GWASLAB_MLOG10P_COL in schema
        return x.with_columns(
            (10 ** (-1 * narwhals.col(GWASLAB_MLOG10P_COL))).alias(GWASLAB_P_COL)
        )
