from src_new.analysis.runner.default_runner import DEFAULT_RUNNER
from src_new.assets.gwas.educational_attainment.lee_et_al_2018.raw_gwas_data.lee_et_al_catalog_harmonized import (
    LEE_ET_AL_2018_CATALOG_HARMONIZED_RAW,
)


def run_initial_analysis():
    DEFAULT_RUNNER.run([LEE_ET_AL_2018_CATALOG_HARMONIZED_RAW])


if __name__ == "__main__":
    run_initial_analysis()
