import polars as pl
from pathlib import Path

from src.data_processing.decode_me_constants import DECODE_ME_mLOGP_COL, DECODE_ME_POS_COL, DECODE_ME_CHROM_COL, \
    DECODE_ME_SNP_COL, DECODE_ME_BETA_COL
from src.data_processing.preprocess_for_big_agwas import BIG_A_GWAS_PVALUE_COL


def find_significant_snps(frame: pl.LazyFrame, p_value_thresh:float=1e-8)  ->pl.LazyFrame:
    return frame.with_columns(
        (10 ** (-pl.col(DECODE_ME_mLOGP_COL))).alias(BIG_A_GWAS_PVALUE_COL)
    ).select(DECODE_ME_CHROM_COL,
        DECODE_ME_POS_COL,
        DECODE_ME_SNP_COL,
        DECODE_ME_BETA_COL,
        BIG_A_GWAS_PVALUE_COL,
        ).filter(pl.col(BIG_A_GWAS_PVALUE_COL)  < p_value_thresh)

