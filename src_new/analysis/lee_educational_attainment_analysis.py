from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.educational_attainment.lee_et_al_2018.processed_gwas_data.lee_et_al_magma_task_generator import (
    LEE_ET_AL_2018_COMBINED_MAGMA_TASKS,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run([LEE_ET_AL_2018_COMBINED_MAGMA_TASKS.inner.bar_plot_task])


if __name__ == "__main__":
    run_initial_analysis()
