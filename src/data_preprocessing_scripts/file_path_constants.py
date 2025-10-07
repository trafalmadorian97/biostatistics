from pathlib import Path

EXTRACTED_DIR = Path("data/DecodeME/extracted/osfstorage/DecodeME Summary Statistics")

GWAS_1_EXTRACTED_PATH = Path(
    "data/DecodeME/extracted/osfstorage/DecodeME Summary Statistics/gwas_1.regenie"
)

QC_FILE_PATH = Path(
    "data/DecodeME/extracted/osfstorage/DecodeME Summary Statistics/gwas_qced.var"
)


GWAS_1_QC_APPLIED_FILE_PATH = Path(
    "data/DecodeME/qc_applied/osfstorage/DecodeME Summary Statistics/gwas_1.regenie"
)

GWAS_1_QC_APPLIED_FILE_PATH_PARQUET = Path(
    "data/DecodeME/qc_applied/osfstorage/DecodeME Summary Statistics/gwas_1.regenie.parquet"
)
QC_APPLIED_DIR = Path(
    "data/DecodeME/qc_applied/osfstorage/DecodeME Summary Statistics/"
)


GWAS_1_AGWAS_PREP_PATH = Path(
    "data/DecodeME/big_a_gwas_format/osfstorage/DecodeME Summary Statistics/gwas_1.regenie"
)

GWAS_1_AGWAS_PREP_PATH_GZIPPED = Path(
    "data/DecodeME/big_a_gwas_format/osfstorage/DecodeME Summary Statistics/gwas_1.regenie.gz"
)

DECODE_ME_OUTPUT_DIR = Path("output/DecodeME")
DECODE_ME_PLOT_OUTPUT_DIR = DECODE_ME_OUTPUT_DIR / "plots"
DECODE_ME_CSV_OUTPUT_DIR = DECODE_ME_OUTPUT_DIR / "csv_tables"
DATA_DEFAULT_ROOT = Path("data")
