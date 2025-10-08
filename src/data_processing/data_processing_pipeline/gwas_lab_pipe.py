from pathlib import PurePath
from typing import Literal

import gwaslab as gl
import narwhals
from attrs import frozen

from src.data_processing.data_processing_pipeline.data_processing_pipe import (
    DataProcessingPipe,
)
from src.data_processing.using_gwaslab.gwaslab_constants import GwaslabKnownFormat

GenomeBuildMode = Literal["infer", "19", "38"]


@frozen
class GWASLabPipe(DataProcessingPipe):
    basic_check: bool
    genome_build: GenomeBuildMode
    filter_hapmap3: bool
    fmt: GwaslabKnownFormat = "regenie"

    def process(
        self, x: narwhals.LazyFrame, data_cache_root: PurePath
    ) -> narwhals.LazyFrame:
        sumstats = gl.Sumstats(
            x.collect().to_pandas(),
            fmt=self.fmt,
        )
        if self.basic_check:
            sumstats.basic_check()
        if self.genome_build == "infer":
            sumstats.infer_build()
            forced_build = None
            print(f"Build is {sumstats.meta['gwaslab']['genome_build']}")
        else:
            forced_build = self.genome_build
        if self.filter_hapmap3:
            sumstats.filter_hapmap3(inplace=True, build=forced_build)
        return narwhals.from_native(sumstats.data).lazy()
