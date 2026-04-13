from __future__ import annotations

from typing import Any
import requests

from .config import MAPBOX_TOKEN


MAPBOX_GEOCODE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"


def geocode_address(
    query: str,
    country: str = "US",
    limit: int = 1,
) -> dict[str, Any]:
    if not MAPBOX_TOKEN:
        raise ValueError("Missing Mapbox token in data_access/config.py")

    url = (
        f"{MAPBOX_GEOCODE_URL}{requests.utils.quote(query)}.json"
        f"?access_token={MAPBOX_TOKEN}"
        f"&country={country}"
        f"&limit={limit}"
        f"&types=address,place,postcode"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    if not data.get("features"):
        raise ValueError(f"No geocoding result found for: {query}")

    feature = data["features"][0]
    lon, lat = feature["center"]

    return {
        "query": query,
        "label": feature.get("place_name", query),
        "latitude": float(lat),
        "longitude": float(lon),
    }