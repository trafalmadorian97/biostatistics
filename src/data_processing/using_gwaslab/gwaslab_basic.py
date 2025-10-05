from pathlib import Path
from typing import Sequence

import gwaslab as gl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from src.data_processing.using_gwaslab.gwaslab_constants import (
    GWASLAB_EUR_1K_GENOMES_NAME,
)
from src.data_types.variant import Variant, df_to_variants
from src.general.timing_util import time_this
from src.plotting.save_fig import write_plots_to_dir


def load_sumstats(pth: Path):
    sumstats = gl.Sumstats(
        str(pth),
        tab_fmt="parquet",
        fmt="regenie",
    )
    sumstats.basic_check()
    sumstats.infer_build(verbose=True)
    return sumstats


CSV_DIR_NAME = "csv_tables"
PLOT_DIR_NAME = "plots"

LEAD_VARIANT_DIR_NAME = "lead_variants"


def plot_manhattan_and_qq(sumstats: gl.Sumstats) -> Figure:
    fig, (ax1, ax2) = plt.subplots(figsize=(24, 16), ncols=2, nrows=1)
    sumstats.plot_mqq(figax=[fig, ax1, ax2], skip=2, cut=20, mode="mqq", scaled=True)
    return fig


def plot_manhattan_and_qq_anno(sumstats: gl.Sumstats, sig_level: float) -> Figure:
    fig, (ax1, ax2) = plt.subplots(figsize=(24, 16), ncols=2, nrows=1)
    sumstats.plot_mqq(
        figax=[fig, ax1, ax2],
        skip=2,
        cut=20,
        mode="mqq",
        scaled=True,
        anno="GENENAME",
        sig_level_lead=sig_level,
    )
    return fig


def plot_regional_around_variant(
    sumstats: gl.Sumstats,
    chrom: int,
    pos: int,
    buffer: int,
    output_dir: Path,
    with_ld: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with time_this("generating regional plot"):
        vcf_path = gl.get_path(GWASLAB_EUR_1K_GENOMES_NAME) if with_ld else None
        sumstats.plot_mqq(
            mode="r",
            skip=2,
            cut=20,
            scaled=True,
            region_grid=True,
            region=(chrom, max(pos - buffer, 0), pos + buffer),
            save=str(
                output_dir / "regional_plot.png",
            ),
            save_args={"dpi": 400, "facecolor": "white"},
            vcf_path=vcf_path,
        )


def plot_regional_around_sig_variants(
    sumstats: gl.Sumstats,
    sig_variants: Sequence[Variant],
    output_dir: Path,
    with_ld: bool,
    buffer: int = 500_000,
) -> None:
    for item in sig_variants:
        print(f"plotting around  {item.id}")
        plot_regional_around_variant(
            sumstats=sumstats,
            chrom=item.chromosome,
            pos=item.position,
            buffer=buffer,
            output_dir=output_dir / item.id_normalized,
            with_ld=with_ld,
        )


def apply_gwaslab_to_gwas(
    qc_datafile_parquet: Path,
    root_output_dir: Path,
    ld_regional_plots: bool,
    sig_level=5e-8,
):
    csv_output_dir = root_output_dir / CSV_DIR_NAME
    csv_output_dir.mkdir(parents=True, exist_ok=True)
    plot_output_Dir = root_output_dir / PLOT_DIR_NAME
    print(f"Loading data from {qc_datafile_parquet}...")
    sumstats = load_sumstats(qc_datafile_parquet)
    print("Getting lead variants with gwaslab...")
    lead_variants: pd.DataFrame = sumstats.get_lead(
        anno=True, sig_level=sig_level
    )  # Interestingly, some the gene annotations here are inconsistent with those in the paper. May be they used different databases
    print("Done getting lead variants with gwaslab")
    lead_variants.to_csv(csv_output_dir / "gwaslab_lead_variants.csv", index=False)
    print("plotting regional plots around significant variants...")
    plot_regional_around_sig_variants(
        sumstats=sumstats,
        sig_variants=df_to_variants(lead_variants),
        output_dir=root_output_dir / LEAD_VARIANT_DIR_NAME,
        with_ld=ld_regional_plots,
    )
    print("plotting with gwaslab...")
    figs = {}
    figs["gwaslab_manhattan_qq"] = plot_manhattan_and_qq(
        sumstats=sumstats,
    )

    figs["gwaslab_manhattan_qq_with_annotations"] = plot_manhattan_and_qq_anno(
        sumstats=sumstats, sig_level=sig_level
    )
    write_plots_to_dir(path=plot_output_Dir, plots=figs)
    print("done plotting with gwaslab")
    print(sumstats)
