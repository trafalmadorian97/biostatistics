from src_new.assets.executable.extracted.magma_binary_extracted import (
    MAGMA_1_1_BINARY_EXTRACTED,
)
from src_new.assets.gwas.me_cfs.decode_me.processed_gwas_data.magma.decode_me_gwas_1_build_37_magma_entrez_annotations import (
    DECODE_ME_GWAS_1_MAGMA_ENTREZ_ANNOTATIONS,
)
from src_new.assets.gwas.me_cfs.decode_me.processed_gwas_data.magma.decode_me_gwas_1_build_37_magma_snp_p_values import (
    DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_P_VALUES,
)
from src_new.assets.reference_data.magma_ld_reference.magma_eur_build_37_1k_genomes_ref_extracted import (
    MAGMA_EUR_BUILD_37_1K_GENOMES_EXTRACTED,
)
from src_new.build_system.task.magma.magma_gene_analysis_task import (
    MagmaGeneAnalysisTask,
)

DECODE_ME_GWAS_1_MAGMA_ENTREZ_GENE_ANALYSIS = MagmaGeneAnalysisTask.create(
    asset_id="decode_me_gwas_1_build_37_magma_gene_analysis",
    magma_annotation_task=DECODE_ME_GWAS_1_MAGMA_ENTREZ_ANNOTATIONS,
    magma_p_value_task=DECODE_ME_GWAS_1_BUILD_37_MAGMA_SNP_P_VALUES,
    magma_binary_task=MAGMA_1_1_BINARY_EXTRACTED,
    magma_ld_ref_task=MAGMA_EUR_BUILD_37_1K_GENOMES_EXTRACTED,
    ld_ref_file_stem="g1000_eur",
    sample_size=275488,  # source: add up cases and controls column in raw gwas data file
)
