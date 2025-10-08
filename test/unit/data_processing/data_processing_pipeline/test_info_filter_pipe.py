from pathlib import Path

import pandas as pd
import narwhals

from src.data_processing.data_processing_pipeline.info_filter_pipe import InfoFilterPipe
from src.data_processing.using_gwaslab.gwaslab_constants import GWASLAB_INFO_SCORE_COL


def test_info_filter_pipe(tmp_path: Path):
    """
    Verify we can filter a row that does not meet the info score threshold
    """
    df = pd.DataFrame(
        {GWASLAB_INFO_SCORE_COL: [0.1, 0.95]}
    )
    pipe = InfoFilterPipe(
        info_low_bound=0.9
    )
    result = pipe.process( narwhals.from_native(df).lazy()  , data_cache_root=tmp_path).collect()
    assert len(result) == 1