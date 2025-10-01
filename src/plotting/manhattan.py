from pathlib import Path

import pandas as pd
import plotly
from plotly.graph_objs import Figure
import dash_bio as dashbio

from src.data_processing.decode_me_constants import DECODE_ME_mLOGP_COL, DECODE_ME_SNP_COL, DECODE_ME_CHROM_COL


def plot_decode_me_manhattan(
    source_file: Path
) -> Figure:
    df =pd.read_csv(source_file)
    fig = dashbio.ManhattanPlot(
        chrm=DECODE_ME_CHROM_COL,
        p= DECODE_ME_mLOGP_COL,
        snp=DECODE_ME_SNP_COL ,
    )
    return fig