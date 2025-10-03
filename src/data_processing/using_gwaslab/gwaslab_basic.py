from pathlib import Path

import gwaslab as gl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

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


def plot_manhattan_and_qq(sumstats: gl.Sumstats) -> Figure:
    fig, (ax1, ax2) = plt.subplots(figsize=(24, 16), ncols=2, nrows=1)
    sumstats.plot_mqq(figax=[fig, ax1, ax2], skip=2, cut=20, mode="mqq", scaled=True)
    return fig


def apply_gwaslab_to_gwas(
    qc_datafile_parquet: Path,
    root_output_dir: Path,
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
    print("plotting with gwaslab")
    figs = {}
    figs["gwaslab_manhattan_qq"] = plot_manhattan_and_qq(
        sumstats=sumstats,
    )
    write_plots_to_dir(path=plot_output_Dir, plots=figs)
    print("done plotting with gwaslab")
    print(sumstats)
