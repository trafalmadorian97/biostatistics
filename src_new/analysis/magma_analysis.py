from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.executable.extracted.magma_binary_extracted import (
    MAGMA_1_1_BINARY_EXTRACTED,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS, DECODE_ME_FILTER_SNPS_GWAS_1_TASK]
        # [DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING],
        # [DECODE_ME_GWAS_1_LEAD_VARIANTS]
        # [DECODE_ME_GWAS_1_REGION_PLOTS, MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_38_RAW],
        # [MAGMA_1_1_BINARY_ZIPPED]
        [MAGMA_1_1_BINARY_EXTRACTED]
    )


if __name__ == "__main__":
    run_initial_analysis()
