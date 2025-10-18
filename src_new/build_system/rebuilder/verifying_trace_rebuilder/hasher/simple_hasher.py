import hashlib
from pathlib import Path
from typing import Callable

from attrs import frozen

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset
from src_new.build_system.rebuilder.verifying_trace_rebuilder.hasher.base_hasher import (
    Hasher,
)

HashConstructor = Callable[[], hashlib._Hash]


@frozen
class SimpleHasher(Hasher):
    hash_constructor: HashConstructor
    chunk_size: int = 8192

    def compute_hash(self, a: Asset) -> str:
        if isinstance(a, FileAsset):
            file_hash = self.hash_constructor()
            with open(Path(a.path), "rb") as f:
                while chunk := f.read(self.chunk_size):
                    file_hash.update(chunk)
            return file_hash.hexdigest()
        raise ValueError(f"Unknown asset {a} of type{type(a)}")
