from pathlib import PurePath

from src_new.build_system.meta.asset_id import AssetId
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.task.osf_retrieve_task import OSFRetrievalTask



DECODE_ME_QC_SNPS = OSFRetrievalTask(
    meta=GWASSummaryDataFileMeta(
        short_id=AssetId("decode_me_snps_passing_quality_control"),
        trait="ME_CFS",
        project="DecodeME",
        sub_dir="raw",
        project_path=PurePath("DecodeME Summary Statistics") / "gwas_qced.var.gz",
    ),
    osf_project_id="rgqs3",
)
