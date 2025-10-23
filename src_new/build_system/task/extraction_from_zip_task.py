import zipfile
from pathlib import Path

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.meta import Meta
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class ExtractFromZipTask(Task):
    """
    Task to extract a single file from a zip archive
    """

    _meta: Meta
    _source_file_task: Task
    _file_to_extract: str

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return [self._source_file_task]

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        asset = fetch(self._source_file_task.asset_id)
        assert isinstance(asset, FileAsset)
        extract_single_file_from_zip(
            zip_path=asset.path,
            file_to_extract=self._file_to_extract,
            destination_dir=scratch_dir,
        )
        result_path = scratch_dir / self._file_to_extract
        return FileAsset(result_path)


def extract_single_file_from_zip(
    zip_path: Path, file_to_extract: str, destination_dir: Path
):
    destination_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        if file_to_extract in zip_ref.namelist():
            zip_ref.extract(file_to_extract, destination_dir)
            print(f"Successfully extracted '{file_to_extract}' to '{destination_dir}'")
        else:
            raise ValueError(f"File '{file_to_extract}' not found in '{zip_path}'")
