from pathlib import Path

from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.imohash import (
    ImoHasher,
)
from src_new.build_system.runner.simple_runner import SimpleRunner

# MD5_INFO_STORE_PATH = Path("build_system")  /"verifying_trace_md5_info.yaml"
# IMO_32_INFO_STORE_PATH = Path("build_system") / "verifying_trace_imo_xxh_info.yaml"
IMO_128_INFO_STORE_PATH = Path("build_system") / "verifying_trace_imo_xxh_128_info.yaml"
ASSET_ROOT = Path("assets") / "base_asset_store"
# _imo_hasher_32 = ImoHasher.with_xxhash_32()
_imo_hasher_128 = ImoHasher.with_xxhash_128()
# _md5_hash = SimpleHasher.md5_hasher()

DEFAULT_RUNNER = SimpleRunner(
    tracer=_imo_hasher_128,  # _imo_hasher_32,#SimpleHasher.md5_hasher(),
    info_store=IMO_128_INFO_STORE_PATH,  # IMO_32_INFO_STORE_PATH,#MD5_INFO_STORE_PATH,
    asset_root=ASSET_ROOT,
)
