"""
Setuptools configuration for pv-standoff-iec61730.

This package provides Python functions and example workflows for accessing
IEC 61730-related PV standoff and T98 thermal safety datasets, along with
supporting notebooks and web resources.

Usage:
    pip install -e .
"""

from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).resolve().parent
README = HERE / "README.md"

long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="pv-standoff-iec61730",
    version="0.1.0",
    description="Functions and tools for accessing PV standoff and T98 IEC 61730 safety datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NatLabRockies/pv-standoff-iec61730",
    author="Silvana Ovaitt",
    author_email="Silvana.Ovaitt@nlr.gov",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords=(
        "photovoltaics PV IEC61730 standoff T98 thermal safety "
        "NSRDB PVDeG reliability"
    ),
    packages=find_packages(exclude=["docs", "notebooks", "maps", "tests"]),
    include_package_data=True,
    install_requires=[
        "xarray",
        "netCDF4",
        "numpy",
        "pandas",
        "matplotlib",
    ],
    extras_require={
        "notebooks": [
            "jupyter",
        ],
        "dev": [
            "pytest",
            "ipython",
        ],
        "all": [
            "jupyter",
            "pytest",
            "ipython",
        ],
    },
    python_requires=">=3.10",
)