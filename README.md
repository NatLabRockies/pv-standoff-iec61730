<img src="tutorials\PVDeg_logo.png" width="100">

# pv-standoff-iec61730

PVDeG-based dataset, tools, and interactive resources for photovoltaic (PV) module standoff distance and T98 thermal safety mapping aligned with IEC 61730.

---

## Overview

This repository provides access to modeled PV module standoff distance and T98 thermal safety maps for the United States, along with code examples and interactive tools for querying and visualizing the data.

The datasets are derived from NSRDB weather data using the PVDeG (Photovoltaic Degradation) modeling framework and are intended to support safety classification and design considerations under :contentReference[oaicite:0]{index=0}.

---

## Contents

- `data_access/`  
  Python functions and utilities for accessing the dataset and querying values at specific latitude/longitude or nearest address.

- `notebooks/`  
  Jupyter notebooks demonstrating:
  - Example workflows for accessing and querying the dataset
  - Single-site calculations (T98 and standoff distance) using PVDeg


- `docs/`  
  Interactive calculator for querying standoff distance and T98 values based on user input (address or coordinates).

- `maps/`  
  High-resolution PNG visualizations of standoff distance and T98 metrics for the United States.

---

## Dataset

The datasets are hosted on OpenEI:

👉 https://data.openei.org/submissions/8659

They include:
- Two scenarios corresponding to T98 = 70 °C and 80 °C
- Spatial data for:
    - Standoff distance (x, cm)
    - T98 (°C): 98th percentile module temperature
    - T98_inf (°C): 98th percentile module temperature for a theoretical rack-mounted module with infinite standoff

---

## Usage

### 1. Access data programmatically

Use the functions in `data_access/` to:
- Query values at a given latitude/longitude
- Identify the nearest grid point
- Extract standoff distance and T98 metrics

### Example: Query by address

Set a Mapbox token, then run:

```bash
export MAPBOX_TOKEN="your_token_here"
python query_address.py --file standoff_USA_T98_70C.nc --address "Golden, CO"
```

### 2. Run notebook examples

See `notebooks/` for:
- Step-by-step calculations for a single site
- Example workflows for accessing the dataset and extending to regional analysis

### 3. Use the web calculator

The GitHub Pages site provides a simple interface:

- Input address or coordinates  
- Automatically converts to latitude/longitude  
- Returns:
  - Standoff distance  
  - T98 values (70 °C and 80 °C scenarios)  
- Displays location on a map  

---

## Web Tool

Interactive calculator (GitHub Pages):

https://natlabrockies.github.io/pv-standoff-iec61730/

---

## Methodology

- Weather inputs: NSRDB  
- Modeling framework: PVDeG (following IEC 61730 standard)
- Outputs:
  - T98 (98th percentile module temperature)
  - Required standoff distance to meet thermal thresholds

For detailed methodology, see:
- Jupyter notebooks in this repository
- Associated publication

---

## Intended Use

These data and tools support:
- PV module thermal safety assessment  
- Standoff distance design decisions  
- IEC 61730-related safety classification  
- Geographic comparison of thermal constraints  

---

## Repository Structure

pv-standoff-iec61730/
│
├── data_access/
├── notebooks/
├── docs/ # GitHub Pages site
├── maps/
├── README.md


---

## Citation

If you use this dataset or tool, please cite:

*To be added (dataset DOI or publication)*

---

## Contact

Michael Kempe
National Laboratory of the Rockies (NLR)

---

## Acknowledgements

This work leverages:
- NSRDB data  
- PVDeg modeling framework 
- NLR research efforts in PV reliability and safety

This work was authored [in part] by the National Laboratory of the Rockies for the U.S. Department of Energy (DOE), operated under Contract No. DE-AC36-08GO28308. Funding provided as part of the Durable Module Materials Consortium 2 (DuraMAT 2) funded by the by U.S. DOE Office of Critical Minerals and Energy Innovation (CMEI) Integrated Energy Systems Office (IESO), Agreement 38259. This research was performed using computational resources sponsored by the U.S. Department of Energy's Office of Critical Minerals and Energy Innovation and located at the National Laboratory of the Rockies. The views expressed in the article do not necessarily represent the views of the DOE or the U.S. Government. 