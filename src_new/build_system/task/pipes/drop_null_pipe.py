import narwhals
from attrs import frozen

from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


@frozen
class DropNullsPipe(DataProcessingPipe):
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        y = x.drop_nulls()
        return y
