from src_new.analysis.default_runner import DEFAULT_RUNNER
from src_new.assets.raw_gwas_data.decode_me_gwas_1 import DECODE_ME_GWAS_1_TASK
from src_new.assets.raw_gwas_data.decode_me_quality_control_snps import DECODE_ME_QC_SNPS
from src_new.build_system.rebuilder.verifying_trace_rebuilder.tracer.simple_hasher import (
    SimpleHasher,
)
from src_new.build_system.rebuilder.verifying_trace_rebuilder.verifying_trace_rebuilder_core import (
    VerifyingTraceRebuilder,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS]
    )


if __name__ == "__main__":
    run_initial_analysis()
