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
    """
    Specifies how a file containing a dataframe should be read.
    Allows client code to operate without concern for the specifics of the dataframe format.
    """

    format: DataFrameFormat
