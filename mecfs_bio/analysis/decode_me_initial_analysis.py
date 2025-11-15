"""
Script to run initial analysis on DecodeME data.
"""
from mecfs_bio.analysis.runner.default_runner import DEFAULT_RUNNER
from mecfs_bio.assets.gwas.me_cfs.decode_me.analysis.decode_me_gwas_1_lead_variants import \
    DECODE_ME_GWAS_1_LEAD_VARIANTS
from mecfs_bio.assets.gwas.me_cfs.decode_me.analysis.decode_me_gwas_1_manhattan import (
    DECODE_ME_GWAS_1_MANHATTAN_PLOT,
)
from mecfs_bio.assets.gwas.me_cfs.decode_me.analysis.decode_me_gwas_1_manhattan_and_qq import (
    DECODE_ME_GWAS_1_MANHATTAN_AND_QQ_PLOT,
)
from mecfs_bio.assets.reference_data.linkage_disequilibrium_score_reference_data.extracted.eur_ld_scores_thousand_genome_phase_3_v1_extracted import (
    THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1_EXTRACTED,
)


def run_initial_analysis():
    """
    Function to run initial analysis on DecodeME data.  Includes generation of manhattan plot,
    as well as extraction of lead variants.
    """
    DEFAULT_RUNNER.run(
        [
            DECODE_ME_GWAS_1_MANHATTAN_AND_QQ_PLOT,
            DECODE_ME_GWAS_1_MANHATTAN_PLOT,
            DECODE_ME_GWAS_1_LEAD_VARIANTS
        ]
    )


if __name__ == "__main__":
    run_initial_analysis()
