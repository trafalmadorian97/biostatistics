from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.base_meta import Meta

# from src_new.build_system.meta.remote_file_meta import RemoteFileMeta


class GWASSummaryDataFileMeta(Meta[FileAsset]):
    short_id: str
    trait: str
