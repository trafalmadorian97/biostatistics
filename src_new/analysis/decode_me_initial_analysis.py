from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.simple_hasher import (
    SimpleHasher,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_rebuilder_core import (
    VerifyingTraceRebuilder,
)


def run_initial_analysis():
    rebuilder = VerifyingTraceRebuilder(SimpleHasher.md5_hasher())
