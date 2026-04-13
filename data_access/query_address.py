from __future__ import annotations

import argparse

from data_access import geocode_address, open_dataset, summarize_point


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Geocode an address and query nearest standoff/T98 values."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to NetCDF file, e.g. standoff_USA_T98_70C.nc",
    )
    parser.add_argument(
        "--address",
        required=True,
        help='Address or place string, e.g. "Golden, CO"',
    )
    parser.add_argument(
        "--mapbox-token",
        default=None,
        help="Optional Mapbox token. If omitted, uses MAPBOX_TOKEN env var.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    geo = geocode_address(args.address, access_token=args.mapbox_token)
    ds = open_dataset(args.file)

    print(f"Geocoded address: {geo['label']}")
    print(
        summarize_point(
            ds,
            lat=geo["latitude"],
            lon=geo["longitude"],
        )
    )


if __name__ == "__main__":
    main()