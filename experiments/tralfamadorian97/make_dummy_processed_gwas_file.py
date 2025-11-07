import pandas as pd


def go():
    df:pd.DataFrame = pd.read_parquet("assets/base_asset_store/gwas/ME_CFS/DecodeME/processed/decode_me_gwas_1_liftover_to_37_parquet_file.parquet")
    df.iloc[0:10].to_csv(
       "test_src_new/unit/build_system/task/dummy_processed_gwas.csv",index=False
    )

if __name__ == "__main__":
    go()