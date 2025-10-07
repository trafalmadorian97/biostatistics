from pathlib import Path

from src.data_processing_util.gzip_util import copy_extract
from src.data_pull_util.get_miscl import download_file_if_missing

SCHIZOPHRENIA_PGS_2014_GWAS_RAW_DIR = Path(
    "data/other_conditions/Schizophrenia/PGS_2014/raw/"
)
SCHIZOPHRENIA_PGS_2014_GWAS_PATH = (
    SCHIZOPHRENIA_PGS_2014_GWAS_RAW_DIR / "daner_PGC_SCZ52_0513a.hq2.gz"
)
SCHIZOPHRENIA_PGS_2014_GWAS_EXTRACTED_DIR = Path(
    "data/other_conditions/Schizophrenia/PGS_2014/extracted/"
)
SCHIZOPHRENIA_PGS_2014_URL = "https://figshare.com/ndownloader/files/28570554"


def pull():
    download_file_if_missing(
        SCHIZOPHRENIA_PGS_2014_URL, SCHIZOPHRENIA_PGS_2014_GWAS_PATH
    )
    copy_extract(
        SCHIZOPHRENIA_PGS_2014_GWAS_RAW_DIR, SCHIZOPHRENIA_PGS_2014_GWAS_EXTRACTED_DIR
    )


if __name__ == "__main__":
    pull()
