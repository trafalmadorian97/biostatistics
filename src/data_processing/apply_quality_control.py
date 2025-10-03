from pathlib import Path
from typing import Literal

import polars as pl

from src.data_processing.decode_me_constants import DECODE_ME_SNP_COL

OutputMode = Literal["csv","parquet"]

def apply_decodeme_qc(regenie_file: Path, qced_file: Path, out_path: Path, output_mode:OutputMode ):
    print(f"Filtering regenie file: {regenie_file} using qced file: {qced_file}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    regenie_df = pl.scan_csv(regenie_file, separator=" ")
    print(f"rows before filtering: {regenie_df.select(pl.len()).collect().item()}")
    qced_df = pl.scan_csv(qced_file, separator=" ")
    filtered = regenie_df.join(qced_df, on=[DECODE_ME_SNP_COL])
    print(f"rows after filtering{filtered.select(pl.len()).collect().item()}")
    if output_mode == "csv":
        filtered.sink_csv(out_path, separator=" ")
    elif output_mode == "parquet":
        filtered.sink_parquet(out_path)
    else:
        raise ValueError("unknown output mode")
    print(f"wrote to {out_path}")


def apply_decodeme_qc_to_all_regenie_files_in_dir(regenie_dir:Path, out_dir:Path, qced_file: Path, output_mode:OutputMode ):
    out_dir.mkdir(parents=True, exist_ok=True)
    for regenie_file in sorted(regenie_dir.glob("*.regenie")):
        filename = regenie_file.name
        if output_mode == "parquet":
            filename += ".parquet"
        apply_decodeme_qc(regenie_file=regenie_file, qced_file=qced_file, out_path=out_dir/filename, output_mode=output_mode)
