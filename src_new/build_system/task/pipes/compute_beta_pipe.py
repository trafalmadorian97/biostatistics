import narwhals

from src_new.build_system.task.gwaslab.gwaslab_constants import (
    GWASLAB_BETA_COL,
    GWASLAB_ODDS_RATIO_COL,
)
from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


class ComputeBetaPipe(DataProcessingPipe):
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        schema = x.collect_schema()
        assert GWASLAB_BETA_COL not in schema.keys()
        x = x.with_columns(
            narwhals.col(GWASLAB_ODDS_RATIO_COL).log().alias(GWASLAB_BETA_COL)
        )
        return x
