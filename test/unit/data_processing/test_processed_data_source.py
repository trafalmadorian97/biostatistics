from pathlib import Path, PurePath

from src.data_processing.data_processing_pipeline.gwas_lab_pipe import GWASLabPipe
from src.data_processing.data_processing_pipeline.processed_data_source import (
    ParquetCachingProcessedDataSource,
    TSVDataOpener,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_EFFECT_ALLELE_COL,
    GWASLAB_NON_EFFECT_ALLELE_COL,
)
from src.data_pull_util.data_source import BasicDataSource, CopyDataRetriever
from test.unit.data_processing.path_constants import DUMMY_DATA_PATH_WITH_INDEL


def test_preprocess_and_drop_indel(tmp_path: Path):
    """
    source data contains two variants, one of which is an indel
    verify that preprocessing can drop the indel.
    """
    source = BasicDataSource(
        retriever=CopyDataRetriever(src_path=DUMMY_DATA_PATH_WITH_INDEL),
        extractor=None,
        path_extension=PurePath("my_data"),
        extracted_filename=None,
        raw_filename="my_file.regenie",
    )
    processed_source = ParquetCachingProcessedDataSource(
        data_source=source,
        processed_filename="processed_data.parquet",
        input_opener=TSVDataOpener(),
        processed_path_extension_from_root=PurePath("my_processed_data"),
        pipe=GWASLabPipe(
            basic_check=True,
            genome_build="38",
            filter_indels=True,
            filter_hapmap3=False,
            filter_palindromic=False,
            exclude_hla=False,
            exclude_sexchr=False,
            harmonize_options=None,
        ),
    )
    frame = (
        processed_source.processed_data(data_cache_root=tmp_path).collect().to_pandas()
    )
    assert len(frame) == 1
    # check no indels
    assert (frame[GWASLAB_EFFECT_ALLELE_COL].str.len() == 1).all()
    assert (frame[GWASLAB_NON_EFFECT_ALLELE_COL].str.len() == 1).all()
