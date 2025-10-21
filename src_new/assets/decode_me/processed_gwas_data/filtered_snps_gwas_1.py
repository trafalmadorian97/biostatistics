from src_new.assets.decode_me.raw_gwas_data.decode_me_gwas_1 import (
    DECODE_ME_GWAS_1_TASK,
)
from src_new.assets.decode_me.raw_gwas_data.decode_me_quality_control_snps import (
    DECODE_ME_QC_SNPS,
)
from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.read_spec.dataframe_read_spec import DataFrameReadSpec, DataFrameParquetFormat
from src_new.build_system.task.filter_snps_task import FilterSNPsTask

DECODE_ME_FILTER_SNPS_GWAS_1_TASK = FilterSNPsTask(
    raw_gwas_task=DECODE_ME_GWAS_1_TASK,
    snp_list_task=DECODE_ME_QC_SNPS,
    meta=FilteredGWASDataMeta(
        short_id=AssetId("decode_me_gwas_1_filtered_for_quality_control"),
        trait="ME_CFS",
        project="DecodeME",
        sub_dir="processed",
        read_spec=DataFrameReadSpec(
            format=DataFrameParquetFormat()
        )
    ),
)
