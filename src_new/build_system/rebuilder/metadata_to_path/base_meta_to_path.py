from abc import ABC, abstractmethod
from pathlib import Path


from src_new.build_system.meta.base_meta import Meta


class MetaToPath(ABC):
    @abstractmethod
    def __call__(self, m: Meta) -> Path:
        pass
