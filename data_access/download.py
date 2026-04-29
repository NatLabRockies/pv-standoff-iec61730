from __future__ import annotations

from pathlib import Path
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


DATASET_URLS = {
    "70C": "https://data.openei.org/files/8659/Standoff_USA_70C.nc",
    "80C": "https://data.openei.org/files/8659/Standoff_USA_80C.nc",
}


def download_dataset(
    scenario: str,
    output_dir: str = "TEMP",
    overwrite: bool = False,
):
    """
    Download a dataset from OpenEI into the TEMP folder.

    Parameters
    ----------
    scenario : str
        Either "70C" or "80C"
    output_dir : str
        Folder to save the file
    overwrite : bool
        Re-download even if file already exists
    """

    if scenario not in DATASET_URLS:
        raise ValueError(
            f"Invalid scenario '{scenario}'. Use '70C' or '80C'."
        )

    url = DATASET_URLS[scenario]

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    filename = output_path / Path(url).name

    if filename.exists() and not overwrite:
        print(f"Dataset already exists: {filename}")
        return filename

    print(f"Downloading {scenario} dataset...")
    print(url)

    response = requests.get(
        url,
        stream=True,
        timeout=120,
        verify=False
    )
    
    response.raise_for_status()

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print(f"Saved to: {filename}")

    return filename