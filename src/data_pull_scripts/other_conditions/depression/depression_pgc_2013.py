from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DATA_DEFAULT_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    URLDataRetriever,
    ZipDataExtractor,
)
from src.data_pull_util.data_verifier import FileSizeInDirVerifier

DEPRESSION_PGC_2011_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url="https://figshare.com/ndownloader/files/28169499",
        expected_size=29116287,
    ),
    extractor=ZipDataExtractor(
        FileSizeInDirVerifier(".txt", expected_size=6639416 + 77410286)
    ),
    path_extension=PurePath("other_conditions/Depression/PGC_2011"),
    raw_filename="pgc.mdd.2012-04.zip",
    extracted_filename="pgc.mdd.2012-04",
)

if __name__ == "__main__":
    result = DEPRESSION_PGC_2011_DATA_SOURCE.extracted_path(DATA_DEFAULT_ROOT)
    # print(result)
