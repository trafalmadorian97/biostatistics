from pathlib import Path, PurePath

from src.data_preprocessing_scripts.file_path_constants import DATA_DEFAULT_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    URLDataRetriever,
    ZipGZipDataExtractor,
)

BIPOLAR_PGS_2011_GWAS_RAW_DIR = Path(
    "data/other_conditions/Bipolar_Disorder/PGS_2011/raw"
)
BIPOLAR_PGS_2011_GWAS_RAW_PATH = BIPOLAR_PGS_2011_GWAS_RAW_DIR / "14671995.zip"

BIPOLAR_PGC_2011_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url="https://figshare.com/ndownloader/articles/14671995/versions/1",
        expected_size=50060674,
    ),
    extractor=ZipGZipDataExtractor(None),
    path_extension=PurePath("other_conditions/Bipolar_Disorder/PGS_2011"),
    src_filename="14671995.zip",
    dst_filename="14671995",
)

if __name__ == "__main__":
    result = BIPOLAR_PGC_2011_DATA_SOURCE.extracted_path(DATA_DEFAULT_ROOT)
    print(result)
