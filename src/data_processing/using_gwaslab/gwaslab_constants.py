from typing import Literal

from attrs import frozen

GWASLAB_CHROM_COL = "CHR"
GWASLAB_POS_COL = "POS"
GWASLAB_EFFECT_ALLELE_COL = "EA"
GWASLAB_NON_EFFECT_ALLELE_COL = "NEA"
GWASLAB_INFO_SCORE_COL = "INFO"
GWASLAB_EFFECT_ALLELE_FREQ_COL = "EAF"
GWASLAB_SAMPLE_SIZE_COLUMN = "N"
GWASLAB_STATUS_COL = "STATUS"
# see
# https://github.com/Cloufield/formatbook
# for column names in different file formats

GWASLAB_EUR_1K_GENOMES_NAME_38 = "1kg_eur_hg38"
GWASLAB_HUMAN_GENOME_NAME_38 = "ucsc_genome_hg38"

GWASLAB_EUR_1K_GENOMES_NAME_19 = "1kg_eur_hg19"
GWASLAB_HUMAN_GENOME_NAME_19 = "ucsc_genome_hg19"

GwaslabKnownFormat = Literal["gwaslab", "regenie"]


@frozen
class GWASLabVCFRef:
    name: str
    ref_alt_freq: str


GWASLAB_EUR_1K_GENOMES_REF_38 = GWASLabVCFRef(
    name=GWASLAB_EUR_1K_GENOMES_NAME_38, ref_alt_freq="AF"
)

GWASLAB_EUR_1K_GENOMES_REF_19 = GWASLabVCFRef(
    name=GWASLAB_EUR_1K_GENOMES_NAME_19, ref_alt_freq="AF"
)
