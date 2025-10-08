from pathlib import PurePath

import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import DataProcessingPipe
from src.data_processing.using_gwaslab.gwaslab_constants import GWASLAB_EFFECT_ALLELE_COL, \
    GWASLAB_EFFECT_ALLELE_FREQ_COL


@frozen
class MinorAlleleFreqFilterPipe(DataProcessingPipe):
    min_maf: float
    eaf_column_name: str = GWASLAB_EFFECT_ALLELE_FREQ_COL
    def process(self, x: narwhals.LazyFrame, data_cache_root: PurePath) -> narwhals.LazyFrame:
        return x.filter(
            (narwhals.col(self.eaf_column_name) >= self.min_maf) & (
            (1- narwhals.col(self.eaf_column_name) ) >= self.min_maf
            )
        )
