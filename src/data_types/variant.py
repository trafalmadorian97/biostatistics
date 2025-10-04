import pandas as pd
from attr import frozen

from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_CHROM_COL,
    GWASLAB_EFFECT_ALLELE_COL,
    GWASLAB_NON_EFFECT_ALLELE_COL,
    GWASLAB_POS_COL,
)
from src.plotting.save_fig import normalize_filename


@frozen
class Variant:
    """
    Represents a genetic variant.
    """

    chromosome: int
    position: int
    effect_allele: str
    non_effect_allele: str

    @property
    def id(self) -> str:
        return f"{self.chromosome}:{self.position}:{self.non_effect_allele}:{self.effect_allele}"

    @property
    def id_normalized(self) -> str:
        return normalize_filename(self.id).replace(":", "_")


def df_to_variants(df: pd.DataFrame) -> list[Variant]:
    return [
        Variant(
            chromosome=df[GWASLAB_CHROM_COL].iloc[i],
            position=df[GWASLAB_POS_COL].iloc[i],
            effect_allele=df[GWASLAB_EFFECT_ALLELE_COL].iloc[i],
            non_effect_allele=df[GWASLAB_NON_EFFECT_ALLELE_COL].iloc[i],
        )
        for i in range(len(df))
    ]
