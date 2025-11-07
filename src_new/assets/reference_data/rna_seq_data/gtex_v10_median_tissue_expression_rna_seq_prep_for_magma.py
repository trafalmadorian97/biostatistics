from src_new.assets.reference_data.rna_seq_data.gtex_v10_median_tissue_expression_rna_seq_raw import (
    GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ,
)
from src_new.build_system.task.pipe_dataframe_task import (
    CSVOutFormat,
    PipeDataFrameTask,
)
from src_new.build_system.task.pipes.drop_col_pipe import DropColPipe
from src_new.build_system.task.pipes.filter_rows_by_min import FilterRowsByMin
from src_new.build_system.task.pipes.move_col_to_front_pipe import MoveColToFrontPipe
from src_new.build_system.task.pipes.shifted_log_pipe import ShiftedLogPipe
from src_new.build_system.task.pipes.split_col import SplitColPipe
from src_new.build_system.task.pipes.winsorize_all import WinsorizeAllPipe

GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ_PREP_FOR_MAGMA = PipeDataFrameTask.create(
    source_task=GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ,  # GTEx_V10_MEDIAN_TISSUE_EXPRESSION_RNA_SEQ_EXTRACTED,
    asset_id="gtex_v10_rna_seq_median_tissue_expression_prep_for_magma",
    out_format=CSVOutFormat(sep="\t"),
    pipes=[
        DropColPipe(cols_to_drop=["Description"]),
        FilterRowsByMin(min_value=1, exclude_columns=["Name"]),
        WinsorizeAllPipe(max_value=50, cols_to_exclude=["Name"]),
        SplitColPipe(
            col_to_split="Name", split_by=".", new_col_names=("Gene", "Version")
        ),
        DropColPipe(cols_to_drop=["Version", "Name"]),
        ShiftedLogPipe(cols_to_exclude=["Gene"], base=2, pseudocount=1),
        MoveColToFrontPipe(target_col="Gene"),
    ],
)
