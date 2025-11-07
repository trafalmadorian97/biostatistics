import polars as pl
import narwhals
from attrs import frozen

from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


@frozen
class SplitColPipe(DataProcessingPipe):
    col_to_split: str
    split_by: str
    new_col_names: tuple[str, str]

    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        xp = (
            x.collect()
            .to_polars()
            .with_columns(
                pl.col(self.col_to_split)
                .str.split_exact(self.split_by, n=1)
                .struct.rename_fields(self.new_col_names)
                .alias("fields")
            )
            .unnest("fields")
        )
        return narwhals.from_native(xp).lazy()
