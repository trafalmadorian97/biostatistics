from pathlib import Path

from attrs import frozen

from src_new.build_system.meta.filtered_gwas_data_meta import FilteredGWASDataMeta
from src_new.build_system.meta.gwas_summary_file_meta import GWASSummaryDataFileMeta
from src_new.build_system.meta.gwaslab_sumstats_meta import GWASLabSumStatsMeta
from src_new.build_system.meta.meta import Meta
from src_new.build_system.meta.simple_file_meta import SimpleFileMeta
from src_new.build_system.rebuilder.metadata_to_path.base_meta_to_path import MetaToPath


@frozen
class SimpleMetaToPath(MetaToPath):
    root: Path

    def __call__(self, m: Meta) -> Path:
        if isinstance(m, SimpleFileMeta):
            return self.root / "other_files" / m.short_id
        if isinstance(m, GWASSummaryDataFileMeta):
            pth = self.root / "gwas_summary" / m.trait / m.project / m.sub_dir
            if m.project_path is not None:
                pth = pth / m.project_path
            else:
                pth = pth / m.short_id
            return pth
        if isinstance(m, FilteredGWASDataMeta):
            pth = (
                self.root
                / "gwas_summary"
                / m.trait
                / m.project
                / m.sub_dir
                / str(m.short_id + m.extension)
            )
            return pth
        if isinstance(m, GWASLabSumStatsMeta):
            pth = (
                self.root
                / "gwas_summary"
                / m.trait
                / m.project
                / m.sub_dir
                / (m.asset_id + ".pickle")
            )
            return pth

        raise ValueError(f"Unknown meta {m} of type {type(m)}.")
