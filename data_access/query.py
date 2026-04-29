from __future__ import annotations

from pathlib import Path
from typing import Any
import math
import xarray as xr


def open_dataset(nc_path):
    """
    Open a NetCDF dataset from either:
    - local file path
    - remote URL
    """

    if str(nc_path).startswith("http"):
        return xr.open_dataset(nc_path)

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

    nearest_lat = float(nearest["latitude"].values)
    nearest_lon = float(nearest["longitude"].values)
    
    result: dict[str, Any] = {
        "requested_latitude": float(lat),
        "requested_longitude": float(lon),
        "nearest_latitude": nearest_lat,
        "nearest_longitude": nearest_lon,
        "nearest_distance_km": haversine_km(lat, lon, nearest_lat, nearest_lon),
    }

    for var_name in nearest.data_vars:
        value = nearest[var_name].values

        try:
            result[var_name] = float(value)
        except (TypeError, ValueError):
            result[var_name] = value.item() if hasattr(value, "item") else value

    return result

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Calculate great-circle distance between two lat/lon points in km.
    """
    radius_km = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius_km * c

def summarize_point(
    ds: xr.Dataset,
    lat: float,
    lon: float,
) -> str:
    """
    Return a human-readable summary for a given point.
    """
    point = get_value_at_latlon(ds, lat, lon)

    # Too far from valid grid
    if point["nearest_distance_km"] > 25:
        return (
            f"Requested point: ({point['requested_latitude']:.4f}, "
            f"{point['requested_longitude']:.4f})\n"
            f"No valid grid point found within 10 km.\n"
            f"Nearest available grid point is "
            f"{point['nearest_distance_km']:.2f} km away."
        )

    # Grid point exists but values are NaN
    if any(
        key in point and isinstance(point[key], float) and math.isnan(point[key])
        for key in ["x", "T98_0", "T98_inf"]
    ):
        return (
            f"Requested point: ({point['requested_latitude']:.4f}, "
            f"{point['requested_longitude']:.4f})\n"
            f"Nearest grid point: ({point['nearest_latitude']:.4f}, "
            f"{point['nearest_longitude']:.4f})\n"
            f"Nearest grid point distance: {point['nearest_distance_km']:.2f} km\n"
            "No valid dataset values found for this location."
        )

    # Normal successful output
    lines = [
        f"Requested point: ({point['requested_latitude']:.4f}, {point['requested_longitude']:.4f})",
        f"Nearest grid point: ({point['nearest_latitude']:.4f}, {point['nearest_longitude']:.4f})",
        f"Nearest grid point distance: {point['nearest_distance_km']:.2f} km",
    ]


    if "x" in point:
        lines.append(f"Standoff distance x: {point['x']:.2f} cm")
    if "T98_0" in point:
        lines.append(f"T98_0: {point['T98_0']:.2f} °C")
    if "T98_inf" in point:
        lines.append(f"T98_inf: {point['T98_inf']:.2f} °C")

    return "\n".join(lines)