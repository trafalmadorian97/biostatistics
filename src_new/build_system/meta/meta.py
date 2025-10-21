from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.meta.simple_directory_meta import SimpleDirectoryMeta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta

"""
Classes in the Meta Union Store uniquely identifying metadata describing either an asset that currently exists,
or an asset that can be created by a build system.
"""
Meta = SimpleFileMeta | SimpleDirectoryMeta | GWASSummaryDataFileMeta |FilteredGWASDataMeta
