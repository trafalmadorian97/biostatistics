from src.data_preprocessing_scripts.file_path_constants import (
    GWAS_1_QC_APPLIED_FILE_PATH,
)
from src.plotting.manhattan import plot_decode_me_manhattan_geneview

from pathlib import Path

from src.plotting.save_fig import write_plots_to_dir

DECODE_ME_OUTPUT_DIR = Path("output/DecodeME")


def go():
    figs = {}
    figs["geneview_manhattan"] = plot_decode_me_manhattan_geneview(
        GWAS_1_QC_APPLIED_FILE_PATH
    )
    write_plots_to_dir(plots=figs, path=DECODE_ME_OUTPUT_DIR)


if __name__ == "__main__":
    go()
