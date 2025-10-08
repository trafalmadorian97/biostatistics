from pathlib import Path

import polars
import polars.testing

from src.data_processing.preprocess_for_big_agwas import prep_for_big_agwas
from test.unit.data_processing.path_constants import DUMMY_DATA_PATH

_EXPECTED_RENAMED_DATA = Path("test/unit/data_processing/dummy_data_renamed.regenie")


def test_preprocess_for_big_a_gwas(tmp_path: Path):
    out_path = tmp_path / "output.txt"
    prep_for_big_agwas(DUMMY_DATA_PATH, out_path)
    frame_1 = polars.read_csv(out_path, separator=" ")
    frame_2 = polars.read_csv(_EXPECTED_RENAMED_DATA, separator=" ")
    polars.testing.assert_frame_equal(frame_1, frame_2, check_column_order=False)
