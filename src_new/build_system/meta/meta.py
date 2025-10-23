from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.meta.gwaslab_meta.gwaslab_lead_variants_meta import (
    GWASLabLeadVariantsMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_manhattan_plot_meta import (
    GWASLabManhattanQQPlotMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_region_plots_meta import (
    GWASLabRegionPlotsMeta,
)
from src_new.build_system.meta.gwaslab_meta.gwaslab_sumstats_meta import (
    GWASLabSumStatsMeta,
)
from src_new.build_system.meta.reference_meta.reference_file_meta import (
    ReferenceFileMeta,
)
from src_new.build_system.meta.simple_directory_meta import SimpleDirectoryMeta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta

"""
Meta objects are uniquely identifying metadata describing either an asset that currently exists,
or an asset that can be created by a build system.
"""
Meta = (
    SimpleFileMeta
    | SimpleDirectoryMeta
    | GWASSummaryDataFileMeta
    | FilteredGWASDataMeta
    | GWASLabSumStatsMeta
    | GWASLabLeadVariantsMeta
    | GWASLabRegionPlotsMeta
    | ReferenceFileMeta
    | GWASLabManhattanQQPlotMeta
)
