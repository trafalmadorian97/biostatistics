from pathlib import Path

import requests
from tqdm import tqdm


def download_file(url: str, local_path: Path):
    """
    Modified from Google AI
    """
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        print(f"Downloading from {url}")
        with open(local_path, "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size=8192)):
                f.write(chunk)
        print(f"File '{local_path}' downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


def download_file_if_missing(url: str, local_path: Path):
    if local_path.exists():
        print("File already exists.  Skipping")
        return
    download_file(url, local_path)
