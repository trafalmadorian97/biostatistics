from abc import ABC, abstractmethod
from pathlib import PurePath

import narwhals


class DataProcessingPipe(ABC):
    @abstractmethod
    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        pass
