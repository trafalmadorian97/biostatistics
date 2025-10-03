from src.data_preprocessing_scripts.file_path_constants import (
    DECODE_ME_OUTPUT_DIR,
    GWAS_1_QC_APPLIED_FILE_PATH_PARQUET,
)
from src.data_processing.using_gwaslab.gwaslab_basic import (
    load_sumstats,
    plot_manhattan_and_qq,
)
from src.plotting.save_fig import write_plots_to_dir


def apply_gwaslab():
    sumstats = load_sumstats(GWAS_1_QC_APPLIED_FILE_PATH_PARQUET)
    print("plotting")
    figs = {}
    figs["gwaslab_manhattan_qq"] = plot_manhattan_and_qq(
        sumstats=sumstats,
    )
    write_plots_to_dir(path=DECODE_ME_OUTPUT_DIR, plots=figs)
    print("done plotting")
    print(sumstats)


if __name__ == "__main__":
    apply_gwaslab()
