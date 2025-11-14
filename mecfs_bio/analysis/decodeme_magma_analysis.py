from mecfs_bio.analysis.runner.default_runner import DEFAULT_RUNNER
from mecfs_bio.assets.gwas.me_cfs.decode_me.analysis_results.magma.magma_specific_tissue_bar_plot import (
    MAGMA_DECODE_ME_SPECIFIC_TISSUE_ANALYSIS_BAR_PLOT,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        [MAGMA_DECODE_ME_SPECIFIC_TISSUE_ANALYSIS_BAR_PLOT],
    )


if __name__ == "__main__":
    run_initial_analysis()
