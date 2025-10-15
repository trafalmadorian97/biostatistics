from abc import ABC, abstractmethod
from pathlib import Path

from attrs import frozen


class DataVerifier(ABC):
    """
    Abstract class representing a method to verify that correct data already present, and so
    does not need to be re-acquired.
    """

    @abstractmethod
    def verify(self, data_path: Path) -> bool:
        pass

    def report_on_data_path(self, data_path: Path):
        pass


@frozen
class FileSizeInDirVerifier(DataVerifier):
    """
    Verifier that works by checking that total of all files in the directory of a given type have the expected size
    """

    suffix_to_check: str
    expected_size: int

    def _measure_size_of_dir(self, data_path: Path) -> int:
        return sum(
            item.stat().st_size
            for item in data_path.iterdir()
            if item.suffix == self.suffix_to_check
        )

    def verify(self, data_path: Path) -> bool:
        if not data_path.is_dir():
            return False
        return self.expected_size == self._measure_size_of_dir(data_path)

    def report_on_data_path(self, data_path: Path):
        print(
            f"Total Size of relevant files in dir: {self._measure_size_of_dir(data_path)}"
        )


@frozen
class FileSizeVerifier(DataVerifier):
    """
    Verifier that works by checking file size
    """

    expected_size: int | None

    def _measure_size(self, data_path: Path) -> int:
        return data_path.stat().st_size

    def verify(self, data_path: Path) -> bool:
        if not data_path.exists():
            return False
        if self.expected_size is None:
            return False
        return self.expected_size == self._measure_size(data_path)

    def report_on_data_path(self, data_path: Path):
        print(f"Size of extracted file: {self._measure_size(data_path)}")
