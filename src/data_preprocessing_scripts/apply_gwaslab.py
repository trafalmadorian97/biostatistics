from src.data_preprocessing_scripts.file_path_constants import (
    DECODE_ME_OUTPUT_DIR,
    GWAS_1_QC_APPLIED_FILE_PATH_PARQUET,
)
from src.data_processing.using_gwaslab.gwaslab_basic import (
    apply_gwaslab_to_gwas,
)

GWAS_1_SUBDIR = "gwas_1"


def apply_gwaslab_gwas1():
    apply_gwaslab_to_gwas(
        qc_datafile_parquet=GWAS_1_QC_APPLIED_FILE_PATH_PARQUET,
        root_output_dir=DECODE_ME_OUTPUT_DIR / GWAS_1_SUBDIR,
        ld_regional_plots=True,
    )


if __name__ == "__main__":
    apply_gwaslab_gwas1()
