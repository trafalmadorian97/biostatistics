from pathlib import Path

import narwhals as nw
import polars as pl

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import FileMeta
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameParquetFormat,
    DataFrameReadSpec,
    DataFrameTextFormat,
)


def scan_dataframe(path: Path, spec: DataFrameReadSpec) -> nw.LazyFrame:
    if isinstance(spec.format, DataFrameParquetFormat):
        return nw.scan_parquet(path, backend="polars")
    if isinstance(spec.format, DataFrameTextFormat):
        return nw.from_native(pl.scan_csv(path, separator=spec.format.separator))
    raise ValueError("Unknown format")


def _scan_dataframe_asset(asset: FileAsset, meta: FileMeta) -> nw.LazyFrame:
    read_spec = meta.read_spec()
    assert read_spec is not None
    return scan_dataframe(asset.path, read_spec)


def scan_dataframe_asset(asset: Asset, meta: Meta) -> nw.LazyFrame:
    """
    Use the information in an Asset's metadata to read it as a DataFrame
    """
    assert isinstance(asset, FileAsset)
    assert isinstance(meta, FileMeta)
    return _scan_dataframe_asset(asset, meta)
