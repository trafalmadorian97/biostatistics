from src_new.analysis.default_runner import DEFAULT_RUNNER
from src_new.assets.decode_me.processed_gwas_data.decode_me_gwas_1_sumstats_minimal_processing import (
    DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS, DECODE_ME_FILTER_SNPS_GWAS_1_TASK]
        [DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING]
    )


if __name__ == "__main__":
    run_initial_analysis()
