from pathlib import Path

from invoke import task

from src.data_processing_util.gzip_util import copy_extract

DECODE_ME_PROJECT_ID = "rgqs3"
DECODE_ME_RAW_DATA_PATH = Path("data/DecodeME/raw")
DECODE_ME_EXTRACTED_DATA_PATH = Path("data/DecodeME/extracted")
OSF_FILE_NAME = "osfstorage"
DECODE_ME_RAW_OSF_DATA_PATH = DECODE_ME_RAW_DATA_PATH / OSF_FILE_NAME
UNIT_TEST_PATH = Path("test/unit")
NEW_UNIT_TEST_PATH = Path("test_src_new/unit")


# dev tasks
@task
def test(c):
    print("Running unit and integration tests with pytest")
    c.run(f"pixi r python  -m pytest {UNIT_TEST_PATH} {NEW_UNIT_TEST_PATH}", pty=True)


@task
def format(c):
    """
    Format code
    """
    print("Formatting with ruff...")
    c.run("pixi r  ruff format", pty=True)


@task
def formatcheck(c):
    """
    Check for format errors
    """
    print("Checking format with black...")
    c.run("pixi r ruff format --check .")


@task
def lintfix(c):
    print("linting and applying lint auto-fixes using ruff...")
    c.run(" pixi r  ruff check --fix --unsafe-fixes")


@task
def lintcheck(c):
    print("linting using ruff...")
    c.run("pixi r ruff check")


@task
def typecheck(c):
    """
    Check for type errors
    """
    print("Typechecking with mypy...")
    c.run("pixi r  mypy .", pty=True)


@task(pre=[lintfix, format, typecheck, test])
def green(c):
    pass


## Library setup tasks


@task
def get_eur_1k_genomes_gwaslab(c):
    import gwaslab as gl

    from src.data_processing.using_gwaslab.gwaslab_constants import (
        GWASLAB_EUR_1K_GENOMES_NAME_38,
    )

    gl.download_ref(GWASLAB_EUR_1K_GENOMES_NAME_38)


@task
def install_tabix_ubuntu(c):
    c.run("sudo apt-get install tabix")


## Data tasks


@task
def pull_Decode_ME(c):
    print("Pulling DecodeME data...")
    c.run(f"pixi r python -p {DECODE_ME_PROJECT_ID} clone -U {DECODE_ME_RAW_DATA_PATH}")


@task
def extract_Decode_ME(c):
    print("Extracting DecodeME data...")
    copy_extract(DECODE_ME_RAW_DATA_PATH, DECODE_ME_EXTRACTED_DATA_PATH)
