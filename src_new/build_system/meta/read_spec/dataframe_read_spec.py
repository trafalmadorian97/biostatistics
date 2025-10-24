from typing import Literal, Mapping, Sequence

import polars as pl
from attrs import field, frozen

Compression = Literal["gzip"]


@frozen
class DataFrameTextFormat:
    separator: str
    null_values: Sequence[str] = tuple()
    schema_overrides: Mapping[str, pl.DataType] = field(factory=dict)


@frozen
class DataFrameParquetFormat:
    pass


DataFrameFormat = DataFrameTextFormat | DataFrameParquetFormat


@frozen
class DataFrameReadSpec:
    """
    Specifies how a file containing a dataframe should be read.
    Allows client code to operate without concern for the specifics of the dataframe format.
    """

    format: DataFrameFormat
