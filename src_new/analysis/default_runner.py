from pathlib import Path

from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.simple_hasher import (
    SimpleHasher,
)
from src_new.build_system.runner.simple_runner import SimpleRunner

MD5_INFO_STORE_PATH = Path("build_system") / "verifying_trace_md5_info.yaml"
ASSET_ROOT = Path("assets") / "base_asset_store"

DEFAULT_RUNNER = SimpleRunner(
    tracer=SimpleHasher.md5_hasher(),
    info_store=MD5_INFO_STORE_PATH,
    asset_root=ASSET_ROOT,
)
