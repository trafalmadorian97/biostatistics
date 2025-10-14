from pathlib import Path

from src.data_pull_util.data_verifier import FileSizeInDirVerifier


def test_file_size_in_dir_verifier(tmp_path: Path):
    """
    Check that FileSizeInDirVerifier only counts the size of files with the correct extension
    """
    file_1 = tmp_path / "file1.txt"
    file_2 = tmp_path / "file1.test"
    file_1.write_text("123")
    file_2.write_text("4567891011121314151617181920")
    sz_1 = file_1.stat().st_size
    sz_2 = file_2.stat().st_size
    verifier_1 = FileSizeInDirVerifier(suffix_to_check=".txt", expected_size=sz_1)
    verifier_2 = FileSizeInDirVerifier(suffix_to_check=".txt", expected_size=sz_2)
    assert verifier_1.verify(tmp_path)
    assert not verifier_2.verify(tmp_path)
