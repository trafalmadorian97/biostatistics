from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.inflammatory_bowel_disease.liu_et_al_2023.processed_gwas_data.analysis.magma.liu_et_al_2023_eur_37_specific_tissue_bar_plot import (
    LIU_ET_AL_IBD_EUR_37_SPECIFIC_TISSUE_ANALYSIS_BAR_PLOT,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        [LIU_ET_AL_IBD_EUR_37_SPECIFIC_TISSUE_ANALYSIS_BAR_PLOT], incremental_save=True
    )


if __name__ == "__main__":
    run_initial_analysis()
