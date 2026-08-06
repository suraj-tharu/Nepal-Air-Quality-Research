# Spatiotemporal Dynamics and Hotspot Analysis of Atmospheric Pollutants in Nepal Using Sentinel-5P and Google Earth Engine (2019–2026)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Google Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-JavaScript-green)](https://earthengine.google.com/)

**Author:** Suraj Tharu Chaudhary  
**Contact:** [Insert Email]  
**Manuscript:** Submitted to *[Journal Name]* (Under Review)

## Project Overview

This repository contains the complete analytical pipeline—from raw satellite data extraction to final statistical visualization—for our comprehensive 8-year study on atmospheric pollutants (NO₂, SO₂, CO, O₃, HCHO, UVAI) across Nepal's five physiographic zones. 

The study leverages **Sentinel-5P TROPOMI** and **Google Earth Engine (GEE)** to identify spatial pollution gradients, temporal trends (using Mann-Kendall and Sen's Slope), structural breakpoints (e.g., the COVID-19 pandemic rebound), and meteorological drivers (using ERA5 reanalysis).

## Repository Structure

```text
├── gee_scripts/               # JavaScript code for Google Earth Engine Code Editor
│   ├── 01_no2_extraction.js   # TROPOMI NO2 extraction and zone aggregation
│   ├── ...
│   └── 10_sentinel2_ndvi.js   # Sentinel-2 NDVI processing
├── analysis/                  # Python statistical pipeline
│   ├── 01_data_preprocessing.py
│   ├── ...
│   ├── 14_validation_proxy.py # Proxy validation and ACF metrics
│   ├── config.py              # Global configurations and standard colors
│   └── utils/                 # Spatial and plotting utilities
├── data/                      # Data directories (not tracked in Git due to size)
│   ├── raw/                   # Raw CSV exports from GEE
│   └── processed/             # Cleaned and temporally aligned CSVs
├── figures/                   # Publication-ready plots (PDF/PNG)
│   ├── covid_analysis/        
│   ├── era5_analysis/         
│   ├── trend_analysis/        
│   └── validation/            
├── manuscript_draft.md        # Academic manuscript draft
├── references_apa.md          # 100+ APA formatted bibliography
├── reproducibility_guide.md   # Step-by-step instructions to reproduce the study
└── requirements.txt           # Python dependencies
```

## Key Findings

1. **Topographic Pollution Gradient:** The Terai region consistently records the highest NO₂ concentrations (26.10 µmol/m²), 3.2× higher than the High Himal zone, confirming its status as a pollution hotspot due to localized emissions and Indo-Gangetic Plain (IGP) transboundary transport.
2. **Universal O₃ Increase:** A statistically significant country-wide increasing trend in background ozone (p < 0.001) across all five physiographic zones.
3. **Wintertime NO₂ Escalation:** Significant worsening of wintertime NO₂ in all lower physiographic zones (+0.14 to 0.22 µmol/m²/yr).
4. **COVID-19 Economic Rebound:** Transient air quality improvements during the 2020 lockdown were entirely reversed by February 2021, leading to a permanent step-change increase (+12–14% vs pre-pandemic baselines) in the Terai and Siwalik zones.

## How to Reproduce

See the `reproducibility_guide.md` file for full, step-by-step instructions on running the GEE extractions and executing the Python statistical pipeline.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
