from pathlib import Path

from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.verifying_trace_rebuilder.info import (
    VerifyingTraceInfo,
)


def test_serialization(tmp_path: Path):
    target_path = tmp_path / "dump_loc.yml"
    info = VerifyingTraceInfo(
        trace_store={
            SimpleFileMeta("file1"): (
                "fakehash",
                [(SimpleFileMeta("file2"), "fakehash2")],
            )
        }
    )
    info.serialize(target_path)
    info_recovered = VerifyingTraceInfo.deserialize(target_path)
    assert info_recovered == info
