import polars as pl
from src.data_preprocessing_scripts.file_path_constants import QC_APPLIED_DIR
from src.data_processing.find_significant_snps import find_significant_snps


def print_sig_snps():
    for file in sorted(QC_APPLIED_DIR.glob("*.regenie.parquet")):
        frame = pl.scan_parquet(file)
        sig = find_significant_snps(frame).collect()
        print(f"Significant snps in {file}")
        print(sig)

if __name__ == "__main__":
    print_sig_snps()
