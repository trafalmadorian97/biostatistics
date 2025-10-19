from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.meta.simple_directory_meta import SimpleDirectoryMeta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta

AnyMeta = SimpleFileMeta | SimpleDirectoryMeta | GWASSummaryDataFileMeta
