from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.reference_data.magma_ld_reference.magma_eur_build_37_1k_genomes_ref import (
    MAGMA_EUR_BUILD_37_1k_GENOMES_REF,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS, DECODE_ME_FILTER_SNPS_GWAS_1_TASK]
        # [DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING],
        # [DECODE_ME_GWAS_1_LEAD_VARIANTS]
        # [DECODE_ME_GWAS_1_REGION_PLOTS, MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_38_RAW],
        # [MAGMA_1_1_BINARY_ZIPPED]
        # [MAGMA_1_1_BINARY_EXTRACTED]
        # [DECODE_ME_GWAS_1_LIFTOVER_TO_37_WITH_RSID],
        # must_rebuild_transitive=[DECODE_ME_GWAS_1_LIFTOVER_TO_37_WITH_RSID],
        # [
        #     DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_P_VALUES,
        #     DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_LOCS,
        # ],
        # [MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_37_EXTRACTED]
        [MAGMA_EUR_BUILD_37_1k_GENOMES_REF]
        # [DECODE_ME_GWAS_1_MAGMA_ANNOTATIONS],
        # must_rebuild_transitive=[DECODE_ME_GWAS_1_MAGMA_ANNOTATIONS]
        # must_rebuild_transitive=[
        #     DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_P_VALUES,
        #     DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_LOCS,
        # ],
    )


if __name__ == "__main__":
    run_initial_analysis()
