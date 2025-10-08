from pathlib import PurePath

import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_SAMPLE_SIZE_COLUMN,
)


@frozen
class FilterFreqRangePipe(DataProcessingPipe):
    """
    Implements a data-processing rule described in
    Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.

    "
    If sample size varies from SNP to SNP, remove SNPs with effective sample size
    less than 0.67 times the 90th percentile of sample size.
    "
    """

    sample_size_col: str = GWASLAB_SAMPLE_SIZE_COLUMN

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        if self.sample_size_col not in x.columns:
            return x
        min_count = x.select(narwhals.min(self.sample_size_col)).collect().item()
        max_count = x.select(narwhals.max(self.sample_size_col)).collect().item()
        if min_count == max_count:
            return x
        percentile_90 = float(
            x.select(
                narwhals.col(self.sample_size_col).quantile(
                    0.9, interpolation="nearest"
                )
            )
            .collect()
            .item()
        )
        return x.filter(narwhals.col(self.sample_size_col) >= 0.67 * percentile_90)
