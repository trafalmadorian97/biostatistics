from pathlib import Path
from typing import Mapping

import gwaslab as gl
import narwhals as nw
from attrs import frozen

from src.data_preprocessing_scripts.file_path_constants import DEFAULT_DATA_CACHE_ROOT
from src.data_processing.data_processing_pipeline.processed_data_source import (
    ProcessedDataSource,
)
from src.data_pull_scripts.reference_data.thousand_genome_ld_reference_data_v1 import (
    THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1,
)
from src.data_pull_util.data_source import DataSource
from src.processed_data_source_library.other_conditions.bipolar_disorder.bipolar_pgc_2011_preprocessed_for_ldsc import (
    BIPOLAR_PGC_2011_PROC_FOR_LDSC,
)
from src.processed_data_source_library.other_conditions.schizophrenia.schizophrenia_pgc_european_2022_preprocessed_for_ldsc import (
    SCHIZOPHRENIA_EUROPEAN_PGC_2022_PROC_FOR_LDSC,
)


@frozen
class GeneticCorrelationGwaslab:
    sources: Mapping[str, ProcessedDataSource]
    ld_reference_data: DataSource
    filename_pattern: str = "/LDscore.@"

    def run(self, data_cache_root: Path) -> nw.LazyFrame:
        if len(self.sources) <= 1:
            raise ValueError("Not Enough inputs")
        first_key = list(self.sources.keys())[0]
        first_sumstats = gl.Sumstats(
            self.sources[first_key]
            .processed_data(data_cache_root=data_cache_root)
            .collect()
            .to_pandas(),
            fmt="gwaslab",
        )
        first_sumstats.basic_check()
        first_sumstats.infer_build()
        other_sumstats = []
        sumstats_names = [first_key]
        for key, source in self.sources.items():
            if key == first_key:
                continue
            cur_ss = gl.Sumstats(
                source.processed_data(data_cache_root=data_cache_root)
                .collect()
                .to_pandas(),
                fmt="gwaslab",
            )
            cur_ss.basic_check()
            cur_ss.infer_build()
            other_sumstats.append(cur_ss)
            sumstats_names.append(key)
        first_sumstats.estimate_rg_by_ldsc(
            other_traits=other_sumstats,
            rg=",".join(sumstats_names),
            ref_ld_chr=str(
                self.ld_reference_data.extracted_path(data_cache_root=data_cache_root)
            )
            + self.filename_pattern,
            w_ld_chr=str(
                self.ld_reference_data.extracted_path(data_cache_root=data_cache_root)
            )
            + self.filename_pattern,
        )
        result = first_sumstats.ldsc_rg
        print("yo")
        return nw.from_native(result).lazy()


if __name__ == "__main__":
    corr_computer = GeneticCorrelationGwaslab(
        sources={
            "Schizophrenia_2022": SCHIZOPHRENIA_EUROPEAN_PGC_2022_PROC_FOR_LDSC,
            "Bipolar_211": BIPOLAR_PGC_2011_PROC_FOR_LDSC,
        },
        ld_reference_data=THOUSAND_GENOME_EUR_LD_REFERENCE_DATA_V1,
    )
    corr_computer.run(DEFAULT_DATA_CACHE_ROOT)
    """
    Result:                 p1          p2       rg       se        z            p   h2_obs  h2_obs_se   h2_int  h2_int_se  gcov_int  gcov_int_se
Schizophrenia_2022 Bipolar_211 0.792362 0.043371 18.26942 1.449823e-74 0.357247   0.041441 1.047737   0.011539  0.157771     0.011309
    """
