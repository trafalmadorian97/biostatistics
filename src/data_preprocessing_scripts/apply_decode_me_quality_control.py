from src.data_preprocessing_scripts.file_path_constants import (
    EXTRACTED_DIR,
    QC_APPLIED_DIR,
    QC_FILE_PATH,
)
from src.data_processing.apply_quality_control import (
    apply_decodeme_qc_to_all_regenie_files_in_dir,
)


def go():
    apply_decodeme_qc_to_all_regenie_files_in_dir(
        qced_file=QC_FILE_PATH,
        out_dir=QC_APPLIED_DIR,
        regenie_dir=EXTRACTED_DIR,
        output_mode="parquet",
    )
    # apply_decodeme_qc(
    #     regenie_file=GWAS_1_EXTRACTED_PATH,
    #     qced_file=QC_FILE_PATH,
    #     out_path=GWAS_1_QC_APPLIED_FILE_PATH,
    # )


if __name__ == "__main__":
    go()
