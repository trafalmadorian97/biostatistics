import gzip
import shutil
from pathlib import Path, PurePath

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.read_spec.read_path import read_file_asset_path
from src_new.build_system.meta.reference_meta.reference_file_meta import (
    ReferenceFileMeta,
)
from src_new.build_system.rebuilder.fetch.base_fetch import Fetch
from src_new.build_system.task.base_task import Task
from src_new.build_system.wf.base_wf import WF


@frozen
class ExtractGzipTextFileTask(Task):
    _meta: Meta
    _source_file_task: Task

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def deps(self) -> list["Task"]:
        return [self._source_file_task]

    @property
    def _source_file_id(self) -> AssetId:
        return self._source_file_task.asset_id

    def execute(self, scratch_dir: Path, fetch: Fetch, wf: WF) -> Asset:
        out_path = scratch_dir / "extracted_file"
        src_asset = fetch(self._source_file_id)
        src_path = read_file_asset_path(src_asset)
        apply_gzip(src_path, out_path)
        return FileAsset(out_path)

    @classmethod
    def create_for_reference_file(cls, source_file_task: Task, asset_id: str):
        src_meta = source_file_task.meta
        assert isinstance(src_meta, ReferenceFileMeta)
        meta = ReferenceFileMeta(
            group=src_meta.group,
            sub_group=src_meta.sub_group,
            sub_folder=PurePath("extracted"),
            asset_id=AssetId(asset_id),
            filename=src_meta.filename,
            extension="",
        )
        return cls(
            meta=meta,
            source_file_task=source_file_task,
        )


def apply_gzip(src: Path, dst: Path):
    with gzip.open(src, "rb") as f_in:
        with open(dst, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
