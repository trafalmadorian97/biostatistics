import os.path
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path, PurePath
from zipfile import ZipFile

from attrs import frozen

from src.data_processing_util.gzip_util import apply_gzip, copy_extract_all
from src.data_pull_util.data_verifier import DataVerifier
from src.data_pull_util.get_miscl import download_file

RAW_DIR_NAME = "raw"
EXTRACTED_DIR_NAME = "extracted"


class DataRetriever(ABC):
    @abstractmethod
    def retrieve(self, local_dst: Path, expected_name: str | None = None):
        pass


@frozen
class URLDataRetriever(DataRetriever):
    url: str
    expected_size: int | None

    def _already_exists(self, local_dst: Path) -> bool:
        if self.expected_size is None:
            return False
        if (
            Path(local_dst).exists()
            and os.path.getsize(local_dst) == self.expected_size
        ):
            print(
                f"File of correct size already exists at {local_dst}. Skipping download."
            )
            return True
        return False

    def retrieve(self, local_dst: Path, expected_name: str | None = None):
        if self._already_exists(local_dst):
            return
        local_dst.parent.mkdir(parents=True, exist_ok=True)
        download_file(
            url=self.url,
            local_path=local_dst,
            expected_filename=expected_name,
        )


@frozen
class CopyDataRetriever(DataRetriever):
    src_path: Path

    def retrieve(self, local_dst: Path, expected_name: str | None = None):
        local_dst.parent.mkdir(parents=True, exist_ok=True)
        local_dst.write_bytes(self.src_path.read_bytes())


class DataExtractor(ABC):
    @abstractmethod
    def extract(self, src: Path, dst: Path):
        pass


@frozen
class ZipDataExtractor(DataExtractor):
    verifier: DataVerifier

    def _already_exists(self, local_dst: Path) -> bool:
        if self.verifier.verify(data_path=local_dst):
            return True
        return False

    def extract(self, src: Path, dst: Path):
        assert src.suffix == ".zip"
        if self._already_exists(dst):
            print(
                f"File of correct size already exists at {dst}. Skipping extractions."
            )
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        print(f"Extracting from {src} to {dst}...")
        with ZipFile(src, "r") as zip_object:
            zip_object.extractall(dst)
        self.verifier.report_on_data_path(dst)


@frozen
class ZipGZipDataExtractor(DataExtractor):
    verifier: DataVerifier

    def _already_exists(self, local_dst: Path) -> bool:
        if self.verifier.verify(data_path=local_dst):
            return True
        return False

    def extract(self, src: Path, dst: Path):
        if self._already_exists(local_dst=dst):
            print(f"{dst} already exists. Skipping extraction.")
            return
        assert src.suffix == ".zip"
        dst.parent.mkdir(parents=True, exist_ok=True)
        print(f"Extracting from {src} to {dst}...")
        with tempfile.TemporaryDirectory() as tmp_dir:
            with ZipFile(src, "r") as zip_object:
                zip_object.extractall(tmp_dir)
            copy_extract_all(Path(tmp_dir), dst)
        self.verifier.report_on_data_path(dst)


@frozen
class GZipDataExtractor(DataExtractor):
    verifier: DataVerifier

    def _already_exists(self, local_dst: Path) -> bool:
        if self.verifier.verify(data_path=local_dst):
            return True
        return False

    def extract(self, src: Path, dst: Path):
        if self._already_exists(local_dst=dst):
            print(f"{dst} already exists. Skipping extraction.")
            return
        assert src.suffix in [".gzip", ".gz"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        print(f"Extracting from {src} to {dst}...")
        apply_gzip(src=src, dst=dst)
        self.verifier.report_on_data_path(dst)


class DataSource(ABC):
    @abstractmethod
    def raw_path(self, data_cache_root: Path) -> Path:
        pass

    @abstractmethod
    def extracted_path(self, data_cache_root: Path) -> Path:
        pass


@frozen
class BasicDataSource(DataSource):
    retriever: DataRetriever
    extractor: DataExtractor | None
    path_extension: PurePath
    raw_filename: str
    extracted_filename: str | None

    def __attrs_post_init__(self):
        assert (self.extractor is None) == (self.extracted_filename is None)

    def raw_path(self, data_cache_root: Path) -> Path:
        rpath = data_cache_root / self.path_extension / RAW_DIR_NAME / self.raw_filename
        self.retriever.retrieve(rpath, expected_name=self.raw_filename)
        return rpath

    def extracted_path(self, data_cache_root: Path) -> Path:
        rpath = self.raw_path(data_cache_root)
        if self.extractor is None:
            return rpath
        assert self.extracted_filename is not None
        xpath = (
            data_cache_root
            / self.path_extension
            / EXTRACTED_DIR_NAME
            / self.extracted_filename
        )
        self.extractor.extract(rpath, xpath)
        return xpath
