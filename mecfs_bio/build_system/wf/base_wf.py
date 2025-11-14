from abc import ABC
from pathlib import Path

import py3_wget


class WF(ABC):
    """
    An interface to the external world.
    Currently only used for downloading files.
    May be extended in the future .
    """

    def download_from_url(self, url: str, local_path: Path) -> None:
        pass


class SimpleWF(WF):
    def download_from_url(self, url: str, local_path: Path) -> None:
        # py3_wget attempts to read the while file to check md5.  doesn't work for large files.  So implement my own check
        py3_wget.download_file(
            url=url,
            output_path=local_path,
        )
