from pathlib import Path

import polars
import polars.testing

from src.data_processing.preprocess_for_big_agwas import rename_columns_for_big_agwas

_DUMMY_DATA_PATH = Path("test/unit/data_processing/dummy_data.regenie")
_EXPECTED_RENAMED_DATA = Path("test/unit/data_processing/dummy_data_renamed.regenie")


def test_preprocess_for_big_a_gwas(tmp_path: Path):
    out_path = tmp_path / "output.txt"
    rename_columns_for_big_agwas(_DUMMY_DATA_PATH, out_path)
    frame_1 = polars.read_csv(out_path, separator=" ")
    frame_2 = polars.read_csv(_EXPECTED_RENAMED_DATA, separator=" ")
    polars.testing.assert_frame_equal(frame_1, frame_2, check_column_order=False)
