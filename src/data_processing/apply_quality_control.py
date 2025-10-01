import polars as pl
from pathlib import Path

from src.data_processing.decode_me_constants import DECODE_ME_SNP_COL


def apply_decodeme_qc(regenie_file: Path, qced_file: Path, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    regenie_df = pl.scan_csv(regenie_file, separator=" ")
    print(f"rows before filtering: {regenie_df.select(pl.len()).collect().item()}")
    qced_df = pl.scan_csv(qced_file, separator=" ")
    filtered = regenie_df.join(qced_df, on=[DECODE_ME_SNP_COL])
    print(f"rows after filtering{filtered.select(pl.len()).collect().item()}")
    filtered.sink_csv(out_path,separator=" ")
