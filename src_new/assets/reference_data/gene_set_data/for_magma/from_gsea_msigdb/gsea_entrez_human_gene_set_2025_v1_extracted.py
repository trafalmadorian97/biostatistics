from src_new.assets.reference_data.gene_set_data.for_magma.from_gsea_msigdb.gsea_entrez_human_gene_set_2025_v1 import (
    GSEA_HUMAN_GENE_SET_2025_V1,
)
from src_new.build_system.task.extract_all_from_zip_task import ExtractAllFromZipTask

"""
Official page:
https://www.gsea-msigdb.org/gsea/downloads.jsp
File is labeled "Human Gene Set GMT
file set (ZIPped)"
Official page does not provide a direct download link, so hosted on Dropbox.
"""
GSEA_HUMAN_GENE_SET_2025_V1_EXTRACTED = (
    ExtractAllFromZipTask.create_from_zipped_reference_file(
        source_task=GSEA_HUMAN_GENE_SET_2025_V1,
        asset_id="gsea_human_data_2025_v1_extracted",
    )
)
