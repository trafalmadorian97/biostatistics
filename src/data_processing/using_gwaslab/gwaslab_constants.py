from typing import Literal

GWASLAB_CHROM_COL = "CHR"
GWASLAB_POS_COL = "POS"
GWASLAB_EFFECT_ALLELE_COL = "EA"
GWASLAB_NON_EFFECT_ALLELE_COL = "NEA"
GWASLAB_INFO_SCORE_COL = "INFO"
GWASLAB_EFFECT_ALLELE_FREQ_COL = "EAF"
# see
# https://github.com/Cloufield/formatbook
# for column names in different file formats

GWASLAB_EUR_1K_GENOMES_NAME = "1kg_eur_hg38"

GwaslabKnownFormat = Literal["gwaslab", "regenie"]
