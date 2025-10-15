"""
Reference data describing LD scores from the 1000 genomes project
See: https://zenodo.org/records/10515792
"""

from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_pull_util.data_source import (
    BasicDataSource,
    WGetDataRetriever,
    ZipDataExtractor,
)
from src.data_pull_util.data_verifier import FileSizeVerifier

THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V4 = BasicDataSource(
    retriever=WGetDataRetriever(
        url="https://zenodo.org/records/10515792/files/1000G_Phase3_baselineLD_v2.3_ldscores.zip?download=1",
        md5="39b1b619602dc1b64e676a642a933fc3",
    ),
    extractor=ZipDataExtractor(
        verifier=FileSizeVerifier(4096), sub_dir_name="baselineLD_v2.3"
    ),
    path_extension=PurePath(
        "reference_data/linkage_disequilibrium_scores/thousand_genomes_european_v2_3"
    ),
    raw_filename="1000G_Phase3_baselineLD_v2.3_ldscores.zip",
    extracted_filename="1000G_Phase3_baselineLD_v2.3_ldscores",
)


if __name__ == "__main__":
    print(
        THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V4.extracted_path(DEFAULT_DATA_CACHE_ROOT)
    )
