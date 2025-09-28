from invoke import task
from pathlib import Path
DECODE_ME_PROJECT_ID = "rgqs3"
DECODE_ME_RAW_DATA_PATH= Path("data/DecodeME/raw")
OSF_FILE_NAME = "osfstorage"
@task
def pull_Decode_ME(c):
    print("Pulling DecodeME data...")
    c.run(f"uv run osf -p {DECODE_ME_PROJECT_ID} clone -U {DECODE_ME_RAW_DATA_PATH}")



