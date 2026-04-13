from __future__ import annotations

import argparse

from data_access import open_dataset, summarize_point


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query nearest standoff/T98 values from an IEC 61730 NetCDF map."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to NetCDF file, e.g. standoff_USA_T98_70C.nc",
    )
    parser.add_argument(
        "--lat",
        type=float,
        required=True,
        help="Latitude in decimal degrees",
    )
    parser.add_argument(
        "--lon",
        type=float,
        required=True,
        help="Longitude in decimal degrees",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    ds = open_dataset(args.file)
    print(summarize_point(ds, args.lat, args.lon))


if __name__ == "__main__":
    main()