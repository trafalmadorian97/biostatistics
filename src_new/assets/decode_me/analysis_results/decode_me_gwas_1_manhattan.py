from src_new.assets.decode_me.processed_gwas_data.decode_me_gwas_1_sumstats_minimal_processing import (
    DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING,
)
from src_new.build_system.task.gwaslab.gwaslab_manhattan_plot_task import (
    GWASLabManhattanPlotTask,
)

DECODE_ME_GWAS_1_MANHATTAN_PLOT = GWASLabManhattanPlotTask.create(
    sumstats_task=DECODE_ME_GWAS_1_SUMSTATS_MINIMAL_FILTERING,
    asset_id="decode_me_gwas_1_manhattan_and_qq_plot",
)
