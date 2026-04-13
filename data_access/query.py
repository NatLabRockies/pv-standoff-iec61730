from __future__ import annotations

from pathlib import Path
from typing import Any

import xarray as xr


def open_dataset(nc_path: str | Path) -> xr.Dataset:
    """
    Open a NetCDF dataset with xarray.

    Parameters
    ----------
    nc_path : str or Path
        Path to the NetCDF file.

    Returns
    -------
    xr.Dataset
        Opened dataset.
    """
    nc_path = Path(nc_path)
    if not nc_path.exists():
        raise FileNotFoundError(f"Dataset not found: {nc_path}")

    return xr.open_dataset(nc_path, engine="netcdf4")


def _validate_coords(ds: xr.Dataset) -> None:
    """
    Ensure expected latitude/longitude coordinates exist.
    """
    required = {"latitude", "longitude"}
    missing = required - set(ds.coords)
    if missing:
        raise KeyError(
            f"Dataset is missing required coordinates: {sorted(missing)}"
        )


def get_value_at_latlon(
    ds: xr.Dataset,
    lat: float,
    lon: float,
) -> dict[str, Any]:
    """
    Return values from the nearest grid point to the requested latitude/longitude.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset with latitude and longitude coordinates.
    lat : float
        Latitude in decimal degrees.
    lon : float
        Longitude in decimal degrees.

    Returns
    -------
    dict
        Dictionary with nearest coordinates and variable values.
    """
    _validate_coords(ds)

    nearest = ds.sel(latitude=lat, longitude=lon, method="nearest")

    result: dict[str, Any] = {
        "requested_latitude": float(lat),
        "requested_longitude": float(lon),
        "nearest_latitude": float(nearest["latitude"].values),
        "nearest_longitude": float(nearest["longitude"].values),
    }

    for var_name in nearest.data_vars:
        value = nearest[var_name].values

        try:
            result[var_name] = float(value)
        except (TypeError, ValueError):
            result[var_name] = value.item() if hasattr(value, "item") else value

    return result


def summarize_point(
    ds: xr.Dataset,
    lat: float,
    lon: float,
) -> str:
    """
    Return a human-readable summary for a given point.
    """
    point = get_value_at_latlon(ds, lat, lon)

    lines = [
        f"Requested point: ({point['requested_latitude']:.4f}, {point['requested_longitude']:.4f})",
        f"Nearest grid point: ({point['nearest_latitude']:.4f}, {point['nearest_longitude']:.4f})",
    ]

    if "x" in point:
        lines.append(f"Standoff distance x: {point['x']:.2f} cm")
    if "T98_0" in point:
        lines.append(f"T98_0: {point['T98_0']:.2f} °C")
    if "T98_inf" in point:
        lines.append(f"T98_inf: {point['T98_inf']:.2f} °C")

    return "\n".join(lines)