from pathlib import Path
import json
import numpy as np
import xarray as xr


def export_dataset(nc_file, output_dir):
    ds = xr.open_dataset(nc_file)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    lat = ds["latitude"].values.astype("float32")
    lon = ds["longitude"].values.astype("float32")

    lat.tofile(output_dir / "latitude.bin")
    lon.tofile(output_dir / "longitude.bin")

    for var in ["x", "T98_0", "T98_inf"]:
        arr = ds[var].values.astype("float32")
        arr.tofile(output_dir / f"{var}.bin")

    metadata = {
        "nlat": int(len(lat)),
        "nlon": int(len(lon)),
        "variables": ["x", "T98_0", "T98_inf"],
        "units": {
            "x": "cm",
            "T98_0": "°C",
            "T98_inf": "°C"
        }
    }

    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Exported web assets to {output_dir}")


if __name__ == "__main__":
    export_dataset(
        "TEMP/Standoff_USA_70C.nc",
        "docs/assets/70C"
    )
    export_dataset(
        "TEMP/Standoff_USA_80C.nc",
        "docs/assets/80C"
    )