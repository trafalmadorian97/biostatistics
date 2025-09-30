import gzip
import shutil

from invoke import task
from pathlib import Path

DECODE_ME_PROJECT_ID = "rgqs3"
DECODE_ME_RAW_DATA_PATH = Path("data/DecodeME/raw")
DECODE_ME_EXTRACTED_DATA_PATH = Path("data/DecodeME/extracted")
OSF_FILE_NAME = "osfstorage"
DECODE_ME_RAW_OSF_DATA_PATH = DECODE_ME_RAW_DATA_PATH / OSF_FILE_NAME
UNIT_TEST_PATH = Path("test/unit")


@task
def test(c):
    print("Running unit and integration tests with pytest")
    c.run(f"uv run -m pytest {UNIT_TEST_PATH}", pty=True)


@task
def format(c):
    """
    Format code
    """
    print("Formatting with ruff...")
    c.run("uv run ruff format", pty=True)


@task(pre=[format, test])
def green(c):
    pass


@task
def pull_Decode_ME(c):
    print("Pulling DecodeME data...")
    c.run(f"uv run osf -p {DECODE_ME_PROJECT_ID} clone -U {DECODE_ME_RAW_DATA_PATH}")


@task
def extract_Decode_ME(c):
    print("Extracting DecodeME data...")
    copy_extract(DECODE_ME_RAW_DATA_PATH, DECODE_ME_EXTRACTED_DATA_PATH)


def copy_extract(source_root: Path, dest_root: Path):
    for item in source_root.iterdir():
        if item.is_dir():
            copy_extract(item, dest_root / item.name)
        if item.suffix == ".gz":
            dest_root.mkdir(exist_ok=True, parents=True)
            print(f"Extracting {item}")
            with gzip.open(item, "rb") as fp_src:
                with open(dest_root / item.stem, "wb") as fp_dst:
                    shutil.copyfileobj(fp_src, fp_dst)
