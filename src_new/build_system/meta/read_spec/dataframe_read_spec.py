import polars as pl
import narwhals as nw
from pathlib import Path
from typing import Literal

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import FileMeta

Compression = Literal["gzip"]

@frozen
class DataFrameTextFormat:
    separator: str

@frozen
class DataFrameParquetFormat:
    pass

DataFrameFormat = DataFrameTextFormat | DataFrameParquetFormat

@frozen
class DataFrameReadSpec:
    format: DataFrameFormat


def scan_dataframe(path: Path, spec: DataFrameReadSpec) -> nw.LazyFrame:
    if isinstance(spec.format,DataFrameParquetFormat ):
        return nw.scan_parquet(path, backend="polars")
    if isinstance(spec.format,DataFrameTextFormat):
        return nw.from_native(pl.scan_csv(path,separator=spec.format.separator))
    raise ValueError("Unknown format")


def scan_dataframe_asset(asset: FileAsset, meta: FileMeta) -> nw.LazyFrame:
    assert meta.read_spec() is not None
    return scan_dataframe(asset.path, meta.read_spec())