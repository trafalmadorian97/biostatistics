from pathlib import Path

import gwaslab as gl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def load_sumstats(pth: Path):
    sumstats = gl.Sumstats(
        str(pth),
        tab_fmt="parquet",
        fmt="regenie",
    )
    sumstats.basic_check()
    sumstats.infer_build(verbose=True)
    return sumstats


def plot_manhattan_and_qq(sumstats: gl.Sumstats) -> Figure:
    fig, (ax1, ax2) = plt.subplots(figsize=(24, 16), ncols=2, nrows=1)
    sumstats.plot_mqq(figax=[fig, ax1, ax2], skip=2, cut=20, mode="mqq", scaled=True)
    return fig
