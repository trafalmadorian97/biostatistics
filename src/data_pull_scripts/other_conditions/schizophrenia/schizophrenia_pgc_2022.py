from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_pull_util.data_source import BasicDataSource, URLDataRetriever

SCHIZOPHRENIA_PGC_2022_EUROPEAN_DATA_SOURCE = BasicDataSource(
    retriever=URLDataRetriever(
        url="https://figshare.com/ndownloader/files/34517828",
        expected_size=239710564,
    ),
    extractor=None,
    path_extension=PurePath("other_conditions/Schizophrenia/PGC_2022_European"),
    raw_filename="PGC3_SCZ_wave3.european.autosome.public.v3.vcf.tsv.gz",
    extracted_filename=None,
)


if __name__ == "__main__":
    print(SCHIZOPHRENIA_PGC_2022_EUROPEAN_DATA_SOURCE.raw_path(DEFAULT_DATA_CACHE_ROOT))
