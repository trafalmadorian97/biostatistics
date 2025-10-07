import gzip
import shutil
from pathlib import Path


def apply_gzip(src: Path, dst: Path):
    with open(src, "rb") as f_in:
        with gzip.open(dst, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def copy_extract(source_root: Path, dest_root: Path):
    for item in source_root.iterdir():
        if item.is_dir():
            copy_extract(item, dest_root / item.name)
        if item.suffix == ".gz":
            dest_root.mkdir(exist_ok=True, parents=True)
            print(f"Extracting {item} to {dest_root / item.stem}")
            with gzip.open(item, "rb") as fp_src:
                with open(dest_root / item.stem, "wb") as fp_dst:
                    shutil.copyfileobj(fp_src, fp_dst)


def copy_extract_all(source_root: Path, dest_root: Path):
    for item in source_root.iterdir():
        if item.is_dir():
            copy_extract(item, dest_root / item.name)
        if item.suffix == ".gz":
            dest_root.mkdir(exist_ok=True, parents=True)
            print(f"Extracting {item} to {dest_root / item.stem}")
            with gzip.open(item, "rb") as fp_src:
                with open(dest_root / item.stem, "wb") as fp_dst:
                    shutil.copyfileobj(fp_src, fp_dst)
        else:
            dest_root.mkdir(exist_ok=True, parents=True)
            print(f"copying {item} to {dest_root / item}")
            with open(item, "rb") as fp_src:
                with open(dest_root / item.stem, "wb") as fp_dst:
                    shutil.copyfileobj(fp_src, fp_dst)
