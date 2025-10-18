from pathlib import Path

from attrs import frozen

from src_new.build_system.meta.base_meta import Meta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath


@frozen
class SimpleMetaToPath(MetaToPath):
    root: Path

    def __call__(self, m: Meta) -> Path:
        if isinstance(m, SimpleFileMeta):
            return self.root / m.short_id
        raise ValueError(f"Unknown meta {m} of type {type(m)}.")
