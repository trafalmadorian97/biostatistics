from src_new.assets.reference_data.rna_seq_data.gtex_v10_median_tissue_expression_rna_seq_raw import (
    GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ,
)
from src_new.build_system.task.pipe_dataframe_task import (
    CSVOutFormat,
    PipeDataFrameTask,
)
from src_new.build_system.task.pipes.drop_col_pipe import DropColPipe
from src_new.build_system.task.pipes.shifted_log_pip import ShiftedLogPipe
from src_new.build_system.task.pipes.winsorize_all import WinsorizeAllPipe

GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ_PREP_FOR_MAGMA = PipeDataFrameTask.create(
    source_task=GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ,  # GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ_EXTRACTED,
    asset_id="gtex_v10_rna_seq_median_tissue_expression_prep_for_magma",
    out_format=CSVOutFormat(sep="\t"),
    pipes=[
        DropColPipe(cols_to_drop=["Description"]),
        WinsorizeAllPipe(max_value=50, cols_to_exclude="Name"),
        ShiftedLogPipe(cols_to_exclude="Name", base=2),
    ],
)
