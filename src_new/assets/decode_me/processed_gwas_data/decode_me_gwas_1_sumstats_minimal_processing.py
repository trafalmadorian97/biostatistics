from src_new.assets.decode_me.processed_gwas_data.filtered_snps_gwas_1 import (
    DECODE_ME_FILTER_SNPS_GWAS_1_TASK,
)
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)

DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING = GWASLabCreateSumstatsTask(
    df_source_task=DECODE_ME_FILTER_SNPS_GWAS_1_TASK,
    asset_id=AssetId("decode_me_gwas_1_sumstats_minimal_processing"),
    basic_check=True,
    genome_build="infer",
)
