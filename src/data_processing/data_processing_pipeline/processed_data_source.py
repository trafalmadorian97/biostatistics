from abc import ABC, abstractmethod
from pathlib import Path, PurePath

import narwhals
import polars
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_pull_util.data_source import DataSource


class ProcessedDataSource(ABC):
    @abstractmethod
    def processed_data(self, data_cache_root: Path) -> narwhals.LazyFrame:
        pass


class DataOpener(ABC):
    @abstractmethod
    def open_data(self, data_path: Path) -> narwhals.LazyFrame:
        pass


class ParquetDataOpener(DataOpener):
    def open_data(self, data_path: Path) -> narwhals.LazyFrame:
        return narwhals.from_native(polars.scan_parquet(data_path))


class TSVDataOpener(DataOpener):
    def open_data(self, data_path: Path) -> narwhals.LazyFrame:
        return narwhals.from_native(polars.scan_csv(data_path, separator=" "))


@frozen
class ParquetCachingProcessedDataSource(ProcessedDataSource):
    data_source: DataSource
    input_opener: DataOpener
    processed_filename: str
    processed_path_extension_from_root: PurePath
    pipe: DataProcessingPipe

    def _cached_processed_data_path(self, data_cache_root: Path) -> Path:
        return (
            data_cache_root
            / self.processed_path_extension_from_root
            / self.processed_filename
        )

    def _cached_processed_data_exists(self, data_cache_root: Path) -> bool:
        return self._cached_processed_data_path(
            data_cache_root=data_cache_root
        ).exists()

    def _prepare_processed_data(self, data_cache_root: Path):
        extracted_path = self.data_source.extracted_path(data_cache_root)
        processed_path = self._cached_processed_data_path(data_cache_root)
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        data = self.input_opener.open_data(extracted_path)
        data = self.pipe.process(data, data_cache_root=data_cache_root)
        data.sink_parquet(processed_path)

    def processed_data(self, data_cache_root: Path) -> narwhals.LazyFrame:
        if not self._cached_processed_data_exists(data_cache_root):
            self._prepare_processed_data(data_cache_root)
        return narwhals.scan_parquet(
            self._cached_processed_data_path(data_cache_root), backend="polars"
        )
