from src.data_preprocessing_scripts.file_path_constants import (
    GWAS_1_EXTRACTED_PATH,
    QC_FILE_PATH,
    GWAS_1_QC_APPLIED_FILE_PATH,
)
from src.data_processing.apply_quality_control import apply_decodeme_qc


def go():
    apply_decodeme_qc(
        regenie_file=GWAS_1_EXTRACTED_PATH,
        qced_file=QC_FILE_PATH,
        out_path=GWAS_1_QC_APPLIED_FILE_PATH,
    )


if __name__ == "__main__":
    go()
