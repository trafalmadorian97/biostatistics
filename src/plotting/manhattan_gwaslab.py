from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_decode_me_manhattan_geneview(source_file: Path) -> Figure:
    fig, ax = plt.subplots(figsize=(12, 8))

    # df = pd.read_csv(
    #     source_file,
    #     sep=" ",
    #     usecols=[
    #         DECODE_ME_CHROM_COL,
    #         DECODE_ME_POS_COL,
    #         DECODE_ME_SNP_COL,
    #         DECODE_ME_mLOGP_COL,
    #     ],
    # ).sort_values(by=[DECODE_ME_CHROM_COL, DECODE_ME_POS_COL])
    # df["P"] = 10 ** (-df[DECODE_ME_mLOGP_COL])
    # gv.manhattanplot(
    #     data=df,
    #     chrom=DECODE_ME_CHROM_COL,
    #     pos=DECODE_ME_POS_COL,
    #     snp=DECODE_ME_SNP_COL,
    #     ax=ax,
    # )
    return fig
    # fig = dashbio.ManhattanPlot(
    #     dataframe=df,
    #     chrm=DECODE_ME_CHROM_COL,
    #     p= DECODE_ME_mLOGP_COL,
    #     snp=DECODE_ME_SNP_COL ,
    # )
    # return fig
