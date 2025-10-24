from src_new.assets.gwas.systemic_lupus_erythematosus.bentham_et_al_2015.raw_gwas_data.bentham_2015_raw_build_37 import (
    BENTHAM_2015_RAW_BUILD_37,
)
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabColumnSpecifiers,
    GWASLabCreateSumstatsTask,
)

"""
Hmm. These sumstats seem a bit messed up
For instance the variant rs887369 has a p value but no beta.
"""
BENTHAM_2015_SUMSTATS_MINIMAL_PROCESSING_FROM_RAW_BUILD_37 = GWASLabCreateSumstatsTask(
    df_source_task=BENTHAM_2015_RAW_BUILD_37,
    asset_id=AssetId("bentham_2015_raw_build_37_sumstats_minimal_processing"),
    basic_check=True,
    genome_build="infer",
    fmt=GWASLabColumnSpecifiers(
        rsid="rsid",
        snpid=None,
        chrom="chrom",
        pos="pos",
        ea="effect_allele",
        nea="other_allele",
        OR="OR",
        se="se",
        p="p",
        info=None,
        beta="beta",
    ),
)
