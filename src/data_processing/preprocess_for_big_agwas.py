from pathlib import Path

import polars

_BIG_A_GWAS_REANAME_MAPPING = {
    "CHROM": "chr",
    "GENPOS": "position",
    "ID": "snp",
    "ALLELE0": "a1",
    "ALLELE1": "a2",
    "BETA": "beta",
    "SE": "se",
    "A1FREQ": "eaf",
    "N": "n",
}

_NO_LOWERCASE_REGEX = "^[^a-z]*$"


def rename_columns_for_big_agwas(src: Path, dst: Path):
    polars.scan_csv(src, separator=" ").rename(
        _BIG_A_GWAS_REANAME_MAPPING
    ).with_columns((10 ** (-polars.col("LOG10P"))).alias("pvalue")).drop(
        polars.selectors.matches(_NO_LOWERCASE_REGEX)
    ).sink_csv(dst, separator=" ")
