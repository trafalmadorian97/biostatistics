from src_new.assets.me_cfs.decode_me.analysis_results.decode_me_gwas_1_lead_variants import (
    DECODE_ME_GWAS_1_LEAD_VARIANTS,
)
from src_new.assets.me_cfs.decode_me.processed_gwas_data.decode_me_gwas_1_sumstats_minimal_processing import (
    DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING,
)
from src_new.build_system.task.gwaslab.gwaslab_region_plots_task import (
    GwasLabRegionPlotsFromLeadVariantsTask,
)

DECODE_ME_GWAS_1_REGION_PLOTS = GwasLabRegionPlotsFromLeadVariantsTask(
    lead_variants_task=DECODE_ME_GWAS_1_LEAD_VARIANTS,
    sumstats_task=DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING,
    vcf_name_for_ld=None,
    short_id="decode_me_gwas_1_lead_variant_region_plots",
)
