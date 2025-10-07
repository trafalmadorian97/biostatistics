from pathlib import PurePath

from attrs import frozen

from src.data_pull_util.data_source import DataSource

GWASSummaryFormat = str  # Literal

# Do we need a recommended-preprocessing step for every data source


@frozen
class GWASSummaryData:
    data_source: DataSource
    path_relative_to_source: PurePath
    summary_format: GWASSummaryFormat
