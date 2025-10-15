from pathlib import Path, PurePath

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    GZipDataExtractor,
    URLDataRetriever,
)
from src.data_pull_util.data_verifier import FileSizeVerifier

SCHIZOPHRENIA_PGC_2014_GWAS_RAW_DIR = Path(
    "data/other_conditions/Schizophrenia/PGC_2014/raw/"
)
SCHIZOPHRENIA_PGC_2014_GWAS_PATH = (
    SCHIZOPHRENIA_PGC_2014_GWAS_RAW_DIR / "daner_PGC_SCZ52_0513a.hq2.gz"
)
SCHIZOPHRENIA_PGC_2014_GWAS_EXTRACTED_DIR = Path(
    "data/other_conditions/Schizophrenia/PGC_2014/extracted/"
)
SCHIZOPHRENIA_PGC_2014_URL = "https://figshare.com/ndownloader/files/28570554"


SCHIZOPHRENIA_PGC_2014_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url=SCHIZOPHRENIA_PGC_2014_URL,
        expected_size=498641959,
    ),
    extractor=GZipDataExtractor(verifier=FileSizeVerifier(expected_size=498794088)),
    path_extension=PurePath("other_conditions/Schizophrenia/PGC_2014"),
    raw_filename="daner_PGC_SCZ52_0513a.hq2.gz",
    extracted_filename="daner_PGC_SCZ52_0513a.hq2",
)


# def pull():
#     download_file_if_missing(
#         SCHIZOPHRENIA_PGS_2014_URL, SCHIZOPHRENIA_PGS_2014_GWAS_PATH
#     )
#     copy_extract(
#         SCHIZOPHRENIA_PGS_2014_GWAS_RAW_DIR, SCHIZOPHRENIA_PGS_2014_GWAS_EXTRACTED_DIR
#     )


if __name__ == "__main__":
    SCHIZOPHRENIA_PGC_2014_DATA_SOURCE.extracted_path(DEFAULT_DATA_CACHE_ROOT)
