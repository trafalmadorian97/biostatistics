from typing import Literal

from attrs import frozen

GWASLAB_CHROM_COL = "CHR"
GWASLAB_POS_COL = "POS"
GWASLAB_EFFECT_ALLELE_COL = "EA"
GWASLAB_NON_EFFECT_ALLELE_COL = "NEA"
GWASLAB_INFO_SCORE_COL = "INFO"
GWASLAB_EFFECT_ALLELE_FREQ_COL = "EAF"
GWASLAB_SAMPLE_SIZE_COLUMN = "N"
# see
# https://github.com/Cloufield/formatbook
# for column names in different file formats

GWASLAB_EUR_1K_GENOMES_NAME = "1kg_eur_hg38"
GWASLAB_HUMAN_GENOME_HG38_NAME = "ucsc_genome_hg38"

GwaslabKnownFormat = Literal["gwaslab", "regenie"]


@frozen
class GWASLabVCFRef:
    name: str
    ref_alt_freq: str


GWASLAB_EUR_1K_GENOMES_REF = GWASLabVCFRef(
    name=GWASLAB_EUR_1K_GENOMES_NAME, ref_alt_freq="AF"
)
