from pathlib import PurePath

from src_new.build_system.meta.reference_meta.reference_file_meta import (
    ReferenceFileMeta,
)
from src_new.build_system.task.reference.download_file_task import DownloadFileTask

THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1_RAW = DownloadFileTask(
    meta=ReferenceFileMeta(
        asset_id="thousand_genomes_phase_3_v1_eur_ld_scores_tar_gzip",
        group="linkage_disequilibrium_scores",
        sub_group="thousand_genomes_phase_3_v1",
        sub_folder=PurePath("raw"),
        extension="tar.gz",
    ),
    url="https://zenodo.org/records/7768714/files/1000G_Phase3_ldscores.tgz?download=1",
    md5_hash="e4352ccf778f296835d73985350a863b",
)
