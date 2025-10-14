from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DATA_DEFAULT_ROOT
from src.data_processing.data_processing_pipeline.composite_pipe import CompositePipe
from src.data_processing.data_processing_pipeline.filter_freq_range_pipe import (
    FilterFreqRangePipe,
)
from src.data_processing.data_processing_pipeline.gwas_lab_pipe import (
    GWASLabColumnSpecifiers,
    GWASLabPipe,
    HarmonizationOptions,
)
from src.data_processing.data_processing_pipeline.info_filter_pipe import InfoFilterPipe
from src.data_processing.data_processing_pipeline.processed_data_source import (
    ParquetCachingProcessedDataSource,
    WhiteSpaceDelimitedDataOpener,
)
from src.data_processing.data_processing_pipeline.set_sample_size_pipe import (
    SetSampleSizePipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_EUR_1K_GENOMES_REF_19,
    GWASLAB_HUMAN_GENOME_NAME_19,
)
from src.data_pull_scripts.other_conditions.bipolar_disorder.bipolar_pgc_2011 import (
    BIPOLAR_PGC_2011_DATA_SOURCE,
)

BIPOLAR_PGC_2011_PROC_FOR_LDSC = ParquetCachingProcessedDataSource(
    data_source=BIPOLAR_PGC_2011_DATA_SOURCE,
    input_opener=WhiteSpaceDelimitedDataOpener(
        path_extension=PurePath("pgc.bip.full.2012-04.txt")
    ),
    processed_filename="14671995.parquet",
    processed_path_extension=PurePath(
        "other_conditions/Bipolar_Disorder/PGC_2011/processed_for_ldsc"
    ),
    pipe=CompositePipe(
        [
            GWASLabPipe(
                basic_check=True,
                genome_build="infer",
                filter_indels=True,
                filter_palindromic=True,
                exclude_hla=False,
                exclude_sexchr=False,
                harmonize_options=HarmonizationOptions(
                    check_ref_files=True,
                    cores=2,
                    ref_seq=GWASLAB_HUMAN_GENOME_NAME_19,
                    ref_infer=GWASLAB_EUR_1K_GENOMES_REF_19,
                    drop_missing_from_ref=True,
                ),
                liftover_to="19",
                filter_hapmap3=False,
                fmt=GWASLabColumnSpecifiers(
                    rsid="snpid",
                    snpid=None,
                    chrom="hg18chr",
                    pos="bp",
                    ea="a1",
                    nea="a2",
                    OR="or",
                    se="se",
                    p="pval",
                    info="info",
                ),
            ),
            # MinorAlleleFreqFilterPipe(
            #     min_maf=0.01
            # ),
            SetSampleSizePipe(
                sample_size=16731,  # see abstract above
            ),
            InfoFilterPipe(
                info_low_bound=0.9,
            ),
            FilterFreqRangePipe(),
        ]
    ),
)
if __name__ == "__main__":
    BIPOLAR_PGC_2011_PROC_FOR_LDSC.processed_data(DATA_DEFAULT_ROOT)
