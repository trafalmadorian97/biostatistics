import narwhals

from src_new.build_system.task.pipes.data_processing_pipe import DataProcessingPipe


class IdentityPipe(DataProcessingPipe):
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        return x