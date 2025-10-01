from pathlib import Path

import polars

from src.data_processing.decode_me_constants import DECODE_ME_SNP_COL, DECODE_ME_CHROM_COL, DECODE_ME_mLOGP_COL

_BIG_A_GWAS_REANAME_MAPPING = {
    DECODE_ME_CHROM_COL: "chr",
    "GENPOS": "position",
    DECODE_ME_SNP_COL: "snp",
    "ALLELE0": "a1",
    "ALLELE1": "a2",
    "BETA": "beta",
    "SE": "se",
    "A1FREQ": "eaf",
    "N": "n",
}
BIG_A_GWAS_PVALUE_COL = "pvalue"

_NO_LOWERCASE_REGEX = "^[^a-z]*$"


def prep_for_big_agwas(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    polars.scan_csv(src, separator=" ").rename(
        _BIG_A_GWAS_REANAME_MAPPING
    ).with_columns((10 ** (-polars.col(DECODE_ME_mLOGP_COL))).alias(BIG_A_GWAS_PVALUE_COL)).drop(
        polars.selectors.matches(_NO_LOWERCASE_REGEX)
    ).sink_csv(dst, separator=" ")
