from pathlib import PurePath

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_processing.data_processing_pipeline.composite_pipe import CompositePipe
from src.data_processing.data_processing_pipeline.estimate_n_pipe import EstimateNPipe
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
from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_EUR_1K_GENOMES_REF_19,
    GWASLAB_HUMAN_GENOME_NAME_19,
    GWASLAB_SAMPLE_SIZE_COLUMN,
)
from src.data_pull_scripts.other_conditions.schizophrenia.schizophrenia_pgc_2022 import (
    SCHIZOPHRENIA_PGC_2022_EUROPEAN_DATA_SOURCE,
)

"""
Abstract:
Schizophrenia has a heritability of 60–80%1, much of which is attributable to common risk alleles. 
Here, in a two-stage genome-wide association study of up to 76,755 individuals with schizophrenia and 243,649 control
 individuals, we report common variant associations at 287 distinct genomic loci. Associations were concentrated in genes 
 that are expressed in excitatory and inhibitory neurons of the central nervous system, but not in other tissues or cell types. 
 Using fine-mapping and functional genomic data, we identify 120 genes (106 protein-coding) that are likely to underpin associations at
  some of these loci, including 16 genes with credible causal non-synonymous or untranslated region variation. We also implicate fundamental 
  processes related to neuronal function, including synaptic organization, differentiation and transmission. Fine-mapped 
  candidates were enriched for genes associated with rare disruptive coding variants in people with schizophrenia, including the 
  glutamate receptor subunit GRIN2A and transcription factor SP4, and were also enriched for genes implicated by such variants in neurodevelopmental disorders. 
  We identify biological processes relevant to schizophrenia pathophysiology; show convergence of common and rare variant associations in schizophrenia and
   neurodevelopmental disorders; and provide a resource of prioritized genes and variants to advance mechanistic studies.

https://www.nature.com/articles/s41586-022-04434-5
"""
SCHIZOPHRENIA_EUROPEAN_PGC_2022_PROC_FOR_LDSC = ParquetCachingProcessedDataSource(
    data_source=SCHIZOPHRENIA_PGC_2022_EUROPEAN_DATA_SOURCE,
    input_opener=WhiteSpaceDelimitedDataOpener(
        skip_rows=73,  # file contains a long header
    ),
    processed_filename="processed.parquet",
    processed_path_extension=PurePath(
        "other_conditions/Schizophrenia/PGC_2022_European/processed_for_ldsc"
    ),
    pipe=CompositePipe(
        [
            EstimateNPipe(),
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
                    rsid="ID",
                    chrom="CHROM",
                    pos="POS",
                    ea="A1",
                    nea="A2",
                    info="IMPINFO",
                    beta="BETA",
                    se="SE",
                    p="PVAL",
                    ncase="NCAS",
                    ncontrol="NCON",
                    neff="NEFF",
                    snpid=None,
                    OR=None,
                    n=GWASLAB_SAMPLE_SIZE_COLUMN,
                ),
            ),
            # MinorAlleleFreqFilterPipe(
            #     min_maf=0.01
            # ),
            InfoFilterPipe(
                info_low_bound=0.9,
            ),
            FilterFreqRangePipe(),
        ]
    ),
)
if __name__ == "__main__":
    SCHIZOPHRENIA_EUROPEAN_PGC_2022_PROC_FOR_LDSC.processed_data(
        DEFAULT_DATA_CACHE_ROOT
    )
