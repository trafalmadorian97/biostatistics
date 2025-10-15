import os
import re
from pathlib import Path

import requests
from tqdm import tqdm


def _check_filename(response, expected_filename: str | None):
    if expected_filename is None:
        return
    if "Content-Disposition" not in response.headers:
        return

    content_disposition = response.headers["Content-Disposition"]
    # Use regex to extract filename from the header
    match = re.search(r'filename="([^"]+)"', content_disposition)
    if match:
        filename = match.group(1)
        matches = expected_filename == filename
        if matches:
            print(f"Returned file matched expected filename: {filename}")

        else:
            print(
                f"Expected downloaded file to have name {expected_filename}, but it instead had filename {filename}"
            )


def download_file(url: str, local_path: Path, expected_filename: str | None):
    """
    Modified from Google AI
    """
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        _check_filename(response, expected_filename)

        print(f"Downloading from {url}")
        with open(local_path, "wb") as f:
            for chunk in tqdm(
                response.iter_content(chunk_size=8192),
            ):
                f.write(chunk)
        print(f"File '{local_path}' downloaded successfully.")
        print(f"Filesize is {os.path.getsize(local_path)} bytes.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


def download_file_if_missing(url: str, local_path: Path, expected_filename: str | None):
    if local_path.exists():
        print("File already exists.  Skipping")
        return
    download_file(url, local_path, expected_filename)
