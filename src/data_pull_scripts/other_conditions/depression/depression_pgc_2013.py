from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DATA_DEFAULT_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    URLDataRetriever,
    ZipDataExtractor,
)

DEPRESSION_PGC_2011_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url="https://figshare.com/ndownloader/files/28169499",
        expected_size=29116287,
    ),
    extractor=ZipDataExtractor(None),
    path_extension=PurePath("other_conditions/Depression/PGC_2011"),
    src_filename="pgc.mdd.2012-04.zip",
    dst_filename="pgc.mdd.2012-04",
)

if __name__ == "__main__":
    result = DEPRESSION_PGC_2011_DATA_SOURCE.extracted_path(DATA_DEFAULT_ROOT)
    print(result)
