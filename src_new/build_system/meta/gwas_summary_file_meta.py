from pathlib import PurePath

from attrs import frozen

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.base_meta import FileMeta
from src_new.build_system.meta.read_spec.read_spec import ReadSpec

# from src_new.build_system.meta.remote_file_meta import RemoteFileMeta


@frozen
class GWASSummaryDataFileMeta(FileMeta):
    @property
    def asset_id(self) -> AssetId:
        return self.short_id

    short_id: AssetId
    trait: str
    project: str
    sub_dir: str
    project_path: PurePath | None
    _read_spec: ReadSpec | None = None

    def read_spec(self) -> ReadSpec | None:
        return self._read_spec
