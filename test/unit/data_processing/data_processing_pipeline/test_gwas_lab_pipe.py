from pathlib import Path

import narwhals
import pandas as pd

from src.data_processing.data_processing_pipeline.gwas_lab_pipe import GWASLabPipe
from src.data_processing.decode_me_constants import DECODE_ME_EA
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_EFFECT_ALLELE_COL,
)
from test.unit.data_processing.path_constants import DUMMY_DATA_PATH


def test_pipe_rename(tmp_path: Path):
    """
    Test that Gwaslab pipe appropriately renames the effect allele columns
    """
    df = pd.read_csv(DUMMY_DATA_PATH, sep=" ")
    nlf = narwhals.from_native(df).lazy()
    pipe = GWASLabPipe(
        basic_check=True,
        genome_build="38",
        filter_hapmap3=False,
        filter_indels=True,
        filter_palindromic=True,
        exclude_hla=False,
        exclude_sexchr=False,
        harmonize_options=None,
        fmt="regenie",
        liftover_to=None,
    )
    result = pipe.process(x=nlf, data_cache_root=tmp_path)
    pd_result = result.collect().to_pandas()
    assert (pd_result[GWASLAB_EFFECT_ALLELE_COL] == df[DECODE_ME_EA]).all()
