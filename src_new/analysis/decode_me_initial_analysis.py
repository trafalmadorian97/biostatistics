from src_new.analysis.default_runner import DEFAULT_RUNNER
from src_new.assets.decode_me.analysis_results.decode_me_gwas_1_manhattan import (
    DECODE_ME_GWAS_1_MANHATTAN_PLOT,
)
from src_new.assets.decode_me.analysis_results.decode_me_gwas_1_manhattan_and_qq import (
    DECODE_ME_GWAS_1_MANHATTAN_AND_QQ_PLOT,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS, DECODE_ME_FILTER_SNPS_GWAS_1_TASK]
        # [DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING],
        # [DECODE_ME_GWAS_1_LEAD_VARIANTS]
        # [DECODE_ME_GWAS_1_REGION_PLOTS, MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_38_RAW],
        [DECODE_ME_GWAS_1_MANHATTAN_AND_QQ_PLOT, DECODE_ME_GWAS_1_MANHATTAN_PLOT],
    )


if __name__ == "__main__":
    run_initial_analysis()
