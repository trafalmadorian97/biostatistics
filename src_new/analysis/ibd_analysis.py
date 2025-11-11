from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.inflammatory_bowel_disease.Liu_et_al_2023_meta import (
    LIU_ET_AL_2023_IBD_META,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        [LIU_ET_AL_2023_IBD_META],
    )


if __name__ == "__main__":
    run_initial_analysis()
