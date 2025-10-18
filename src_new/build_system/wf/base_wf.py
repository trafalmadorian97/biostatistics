from abc import ABC

from pathlib_abc import WritablePath


class WF(ABC):
    """
    An interface to the external world.
    """

    def download_from_url(
        self, url: str, md5_hash: str | None, local_path: WritablePath
    ) -> None:
        pass


class DummyWF(WF):
    def download_from_url(
        self, url: str, md5_hash: str | None, local_path: WritablePath
    ) -> None:
        raise NotImplementedError("Not implemented")
