from abc import ABC
from pathlib import Path

import py3_wget


class WF(ABC):
    """
    An interface to the external world.
    """

    def download_from_url(
        self, url: str, md5_hash: str | None, local_path: Path
    ) -> None:
        pass


class SimpleWF(WF):
    def download_from_url(
        self, url: str, md5_hash: str | None, local_path: Path
    ) -> None:
        py3_wget.download_file(
            url=url,
            output_path=local_path,
            md5=md5_hash,
        )
