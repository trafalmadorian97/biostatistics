import gwaslab

from src_new.build_system.asset.base_asset import Asset
from src_new.build_system.asset.file_asset import FileAsset


def read_sumstats(asset: Asset) -> gwaslab.Sumstats:
    assert isinstance(asset, FileAsset)
    return gwaslab.load_pickle(asset.path)
