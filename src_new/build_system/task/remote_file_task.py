from abc import ABC

from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.remote_file_meta import RemoteFileMeta
from src_new.build_system.task.base_task import Task


class RemoteFileTask(Task[FileAsset], ABC):
    pass
