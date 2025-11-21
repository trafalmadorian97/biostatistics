from mecfs_bio.assets.gwas.psoriasis.million_veterans.processed_gwas_data.million_veterans_eur_magma_task_generator import (
    MILLION_VETERANS_EUR_PSORIASIS_COMBINED_MAGMA_TASKS,
)
from mecfs_bio.assets.reference_data.linkage_disequilibrium_score_reference_data.extracted.eur_ld_scores_thousand_genome_phase_3_v1_extracted import (
    THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1_EXTRACTED,
)
from mecfs_bio.build_system.task.gwaslab.gwaslab_snp_heritability_by_ldsc_task import (
    SNPHeritabilityByLDSCTask,
)
from mecfs_bio.build_system.task.pipes.composite_pipe import CompositePipe
from mecfs_bio.build_system.task.pipes.compute_beta_pipe import ComputeBetaPipe
from mecfs_bio.build_system.task.pipes.compute_se_pip import ComputeSEPipe

MILLION_VETERAN_PSORIASIS_H2_BY_LDSC = SNPHeritabilityByLDSCTask.create(
    asset_id="million_veterans_psoriasis_h2_by_ldsc",
    source_sumstats_task=MILLION_VETERANS_EUR_PSORIASIS_COMBINED_MAGMA_TASKS.sumstats_task,
    ld_ref_task=THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1_EXTRACTED,
    set_sample_size=443794,
    pipe=CompositePipe([ComputeBetaPipe(), ComputeSEPipe()]),
)
