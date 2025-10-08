from pathlib import Path

import narwhals
import pandas as pd

from src.data_processing.data_processing_pipeline.maf_filer_pipe import MinorAlleleFreqFilterPipe
from src.data_processing.using_gwaslab.gwaslab_constants import GWASLAB_EFFECT_ALLELE_FREQ_COL


def test_maf_filter_pipe(tmp_path: Path):
    """
    Verify we can filter a row that does not meet the minor allele frequency threshold
    """
    df = pd.DataFrame(
        {GWASLAB_EFFECT_ALLELE_FREQ_COL: [0.001, 0.01, 0.5, 0.99, 0.999]}
    )
    pipe = MinorAlleleFreqFilterPipe(
        min_maf=0.01
    )
    result = pipe.process( narwhals.from_native(df).lazy()  , data_cache_root=tmp_path).collect().to_pandas()
    assert result[GWASLAB_EFFECT_ALLELE_FREQ_COL].tolist() == [0.01, 0.5, 0.99]
