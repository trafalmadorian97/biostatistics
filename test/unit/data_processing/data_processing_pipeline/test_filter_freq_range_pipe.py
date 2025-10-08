from pathlib import Path

import narwhals
import pandas as pd

from src.data_processing.data_processing_pipeline.filter_freq_range_pipe import (
    FilterFreqRangePipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_SAMPLE_SIZE_COLUMN,
)


def test_skip_with_constant_n(tmp_path: Path):
    df = pd.DataFrame({GWASLAB_SAMPLE_SIZE_COLUMN: [100, 100, 100, 100]})
    result = (
        FilterFreqRangePipe()
        .process(narwhals.from_native(df).lazy(), data_cache_root=tmp_path)
        .collect()
        .to_pandas()
    )
    pd.testing.assert_frame_equal(result, df)


def test_filter(tmp_path: Path):
    df = pd.DataFrame(
        {GWASLAB_SAMPLE_SIZE_COLUMN: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}
    )

    df_expected = pd.DataFrame({GWASLAB_SAMPLE_SIZE_COLUMN: [0.7, 0.8, 0.9, 1]})
    result = (
        FilterFreqRangePipe()
        .process(narwhals.from_native(df).lazy(), data_cache_root=tmp_path)
        .collect()
        .to_pandas()
    )
    pd.testing.assert_frame_equal(result.reset_index(drop=True), df_expected)
