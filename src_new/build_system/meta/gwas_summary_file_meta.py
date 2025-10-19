from pathlib import PurePath

from attrs import frozen

from src_new.build_system.meta.base_meta import FileMeta

# from src_new.build_system.meta.remote_file_meta import RemoteFileMeta


@frozen
class GWASSummaryDataFileMeta(FileMeta):
    @property
    def short_name(self) -> str:
        return self.short_id

    short_id: str
    trait: str
    project: str
    sub_dir: str
    project_path: PurePath | None
