from abc import ABC, abstractmethod

# @frozen
# class Meta[S: Asset](ABC):


class FileMeta(ABC):
    @property
    @abstractmethod
    def short_name(self) -> str:
        pass


class DirMeta(ABC):
    @property
    @abstractmethod
    def short_name(self) -> str:
        pass
