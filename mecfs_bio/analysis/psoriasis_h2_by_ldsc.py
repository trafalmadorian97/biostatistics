from mecfs_bio.analysis.runner.default_runner import DEFAULT_RUNNER
from mecfs_bio.assets.gwas.psoriasis.million_veterans.analysis.million_veterans_psoriasis_h2_by_ldsc import (
    MILLION_VETERAN_PSORIASIS_H2_BY_LDSC,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run(
        [MILLION_VETERAN_PSORIASIS_H2_BY_LDSC],
        incremental_save=True,
    )


if __name__ == "__main__":
    run_initial_analysis()
