from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.inflammatory_bowel_disease.liu_et_al_2023.processed_gwas_data.liu_et_al_2023_eur_liftover_to_37 import (
    LIU_ET_AL_2023_IBD_EUR_LIFTOVER_37_SUMSTATS,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        # [LIU_ET_AL_2023_IBD_META],
        # [LIU_ET_AL_2023_IBD_META_EUR_ONLY]
        [LIU_ET_AL_2023_IBD_EUR_LIFTOVER_37_SUMSTATS]
    )


if __name__ == "__main__":
    run_initial_analysis()
