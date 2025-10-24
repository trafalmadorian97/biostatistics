from src_new.analysis.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.systemic_lupus_erythematosus.bentham_et_al_2015.analysis_results.bentham_2015_raw_37_lead_variant_region_plots import (
    BENTHAM_2105_RAW_LEAD_VARIANT_REGION_PLOTS,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [DECODE_ME_GWAS_1_TASK, DECODE_ME_QC_SNPS, DECODE_ME_FILTER_SNPS_GWAS_1_TASK]
        # [DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING],
        # [DECODE_ME_GWAS_1_LEAD_VARIANTS]
        # [DECODE_ME_GWAS_1_REGION_PLOTS, MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_38_RAW],
        # [DECODE_ME_GWAS_1_MANHATTAN_AND_QQ_PLOT, DECODE_ME_GWAS_1_MANHATTAN_PLOT],
        # [BENTHAM_2015_HARMONIZED_BUILD_38]
        # [BENTHAM_2015_SUMSTATS_MINIMAL_PROCESSING],
        # [BENTHAM_2015_SUMSTATS_MINIMAL_PROCESSING_FROM_RAW_BUILD_37]
        [BENTHAM_2105_RAW_LEAD_VARIANT_REGION_PLOTS]
        # [BENTHAM_2015_RAW_LEAD_VARIANTS]
    )


if __name__ == "__main__":
    run_initial_analysis()
