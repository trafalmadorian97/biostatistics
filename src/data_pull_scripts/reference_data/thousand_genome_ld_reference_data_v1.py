from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    TarGzipDataExtractor,
    WGetDataRetriever,
)
from src.data_pull_util.data_verifier import FileSizeVerifier


THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1 = BasicDataSource(
    retriever=WGetDataRetriever(
        url="https://zenodo.org/records/7768714/files/1000G_Phase3_ldscores.tgz?download=1",
        md5="e4352ccf778f296835d73985350a863b",
    ),
    extractor=TarGzipDataExtractor(
        verifier=FileSizeVerifier(4096), sub_dir_name="LDscore"
    ),
    path_extension=PurePath(
        "reference_data/linkage_disequilibrium_scores/thousand_genomes_european_v1"
    ),
    raw_filename="1000G_Phase3_ldscores",
    extracted_filename="1000G_Phase3_ldscores",
)


if __name__ == "__main__":
    print(
        THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1.extracted_path(DEFAULT_DATA_CACHE_ROOT)
    )
