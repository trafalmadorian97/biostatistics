from pathlib import PurePath

from src_new.build_system.reference.schemas.hg19_sn151_schema import HG19_SNP151_SCHEMA

from src_new.build_system.meta.read_spec.dataframe_read_spec import (
    DataFrameReadSpec,
    DataFrameTextFormat,
)
from src_new.build_system.meta.reference_meta.reference_file_meta import (
    ReferenceFileMeta,
)
from src_new.build_system.task.reference.download_file_task import DownloadFileTask

"""
See
https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/
"""
GENOME_ANNOTATION_DATABASE_BUILD_37 = DownloadFileTask(
    meta=ReferenceFileMeta(
        group="genome_annotations",
        sub_group="build_37",
        sub_folder=PurePath("raw"),
        asset_id="genome_annotation_database_build_37",
        extension=".gz",
        filename="snp151.txt",
        read_spec=DataFrameReadSpec(
            format=DataFrameTextFormat(
                separator="\t",
                column_names=HG19_SNP151_SCHEMA,
                has_header=False,
            )
        ),
    ),
    url="https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/snp151.txt.gz",
    md5_hash=None,
)
