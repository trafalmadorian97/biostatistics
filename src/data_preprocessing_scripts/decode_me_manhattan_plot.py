from src.data_preprocessing_scripts.file_path_constants import GWAS_1_QC_APPLIED_FILE_PATH
from src.plotting.manhattan import plot_decode_me_manhattan


def go():
    figs = {}
    figs["dash_bio_manhattan"] = plot_decode_me_manhattan(GWAS_1_QC_APPLIED_FILE_PATH)