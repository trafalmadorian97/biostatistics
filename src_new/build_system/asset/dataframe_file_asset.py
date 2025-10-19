from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset


@frozen
class DataFrameTextFileFormat:
    delimiter: str


@frozen
class DataFrameParquetFileFormat:
    pass


FrameFormat = DataFrameTextFileFormat | DataFrameParquetFileFormat

@frozen
class DataFrameFileAsset(Asset):
    path: Path
    format: FrameFormat
    compression: str
    def __attrs_post_init__(self):
        assert self.path.is_file()
