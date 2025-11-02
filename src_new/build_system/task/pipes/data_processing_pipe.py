from abc import ABC, abstractmethod

import narwhals


class DataProcessingPipe(ABC):
    @abstractmethod
    def process(self, x: narwhals.LazyFrame) -> narwhals.LazyFrame:
        pass
