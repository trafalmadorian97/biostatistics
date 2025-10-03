from pathlib import Path

import polars

from src.data_processing.decode_me_constants import (
    DECODE_ME_BETA_COL,
    DECODE_ME_CHROM_COL,
    DECODE_ME_POS_COL,
    DECODE_ME_mLOGP_COL,
)

_BIG_A_GWAS_REANAME_MAPPING = {
    DECODE_ME_CHROM_COL: "chr",
    DECODE_ME_POS_COL: "position",
    "ALLELE0": "a2",  # Since  Allele0 is the non-effect Alelle according to DecodeME readme, and a2 is the non-effect allele according to https://bigagwas.org/documentation#input_file
    "ALLELE1": "a1",  #
    DECODE_ME_BETA_COL: "beta",
    "SE": "se",
    "A1FREQ": "eaf",  # Since a1 is the effect allele according to the readme
    "N": "n",
}
BIG_A_GWAS_PVALUE_COL = "pvalue"

_NO_LOWERCASE_REGEX = "^[^a-z]*$"


def prep_for_big_agwas(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    polars.scan_csv(src, separator=" ").rename(
        _BIG_A_GWAS_REANAME_MAPPING
    ).with_columns(
        (10 ** (-polars.col(DECODE_ME_mLOGP_COL))).alias(BIG_A_GWAS_PVALUE_COL)
    ).drop(polars.selectors.matches(_NO_LOWERCASE_REGEX)).sink_csv(dst, separator=" ")
