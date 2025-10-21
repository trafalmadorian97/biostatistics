from typing import Literal

from attrs import frozen

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
