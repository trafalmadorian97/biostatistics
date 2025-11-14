from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.psoriasis.million_veterans.processed_gwas_data.million_veterans_eur_magma_task_generator import \
    MILLION_VETERANS_EUR_PSORIASIS_COMBINED_MAGMA_TASKS
from src_new.assets.gwas.psoriasis.million_veterans.raw_gwas_data.raw_psoriasis_data import \
    MILLION_VETERAN_PSORIASIS_EUR_DATA_RAW


def run_initial_analysis():
    DEFAULT_RUNNER.run([MILLION_VETERANS_EUR_PSORIASIS_COMBINED_MAGMA_TASKS.inner.bar_plot_task])



if __name__ == "__main__":
    run_initial_analysis()
