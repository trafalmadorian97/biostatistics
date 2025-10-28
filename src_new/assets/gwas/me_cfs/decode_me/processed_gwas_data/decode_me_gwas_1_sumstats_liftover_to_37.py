from src_new.assets.gwas.me_cfs.decode_me.processed_gwas_data.filtered_snps_gwas_1 import (
    DECODE_ME_FILTER_SNPS_GWAS_1_TASK,
)
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.task.gwaslab.gwaslab_create_sumstats_task import (
    GWASLabCreateSumstatsTask,
)

DECODE_ME_GWAS_1_SUMSTATS_LIFTOVER_TO_37 = GWASLabCreateSumstatsTask(
    df_source_task=DECODE_ME_FILTER_SNPS_GWAS_1_TASK,
    asset_id=AssetId("decode_me_gwas_1_sumstats_liftover_to_37"),
    basic_check=True,
    genome_build="infer",
    liftover_to="19",
)
