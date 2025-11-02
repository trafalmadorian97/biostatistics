from src_new.assets.reference_data.magma_gene_locations.raw.magma_gene_location_reference_data_build_37 import (
    MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_37_RAW,
)
from src_new.build_system.task.extraction_from_zip_task import ExtractFromZipTask

MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_37_EXTRACTED = (
    ExtractFromZipTask.create_from_zipped_reference_file(
        source_task=MAGMA_GENE_LOCATION_REFERENCE_DATA_BUILD_37_RAW,
        asset_id="magma_gene_location_reference_data_build_37_extracted",
        file_to_extract="NCBI37.3.gene.loc",
    )
)
