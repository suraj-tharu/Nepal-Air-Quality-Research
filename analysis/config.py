"""
Configuration module for Nepal Atmospheric Pollutants Analysis.

Central location for all paths, constants, pollutant parameters,
study area definitions, and analysis settings.
"""

import os
from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"
SUPPLEMENTARY_DIR = PROJECT_ROOT / "supplementary"

# Create directories if they don't exist
for d in [RAW_DIR, PROCESSED_DIR, FIGURES_DIR, SUPPLEMENTARY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# =============================================================================
# STUDY PERIOD
# =============================================================================
START_YEAR = 2019
END_YEAR = 2026  # 6 complete years of calibrated TROPOMI data
START_DATE = f"{START_YEAR}-01-01"
END_DATE = f"{END_YEAR}-12-31"

# =============================================================================
# POLLUTANT CONFIGURATIONS
# =============================================================================
POLLUTANTS = {
    "NO2": {
        "full_name": "Nitrogen Dioxide",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_NO2",
        "band": "tropospheric_NO2_column_number_density",
        "qa_band": "tropospheric_NO2_column_number_density",  # qa_value for filtering
        "qa_threshold": 0.75,
        "unit": "mol/m²",
        "scale_factor": 1e6,  # Convert to µmol/m²
        "display_unit": "µmol/m²",
        "colormap": "YlOrRd",
        "who_guideline": None,  # WHO provides annual mean for ground-level
    },
    "SO2": {
        "full_name": "Sulfur Dioxide",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_SO2",
        "band": "SO2_column_number_density",
        "qa_band": "SO2_column_number_density_amf",
        "qa_threshold": 0.5,
        "unit": "mol/m²",
        "scale_factor": 1e6,
        "display_unit": "µmol/m²",
        "colormap": "PuRd",
        "who_guideline": None,
    },
    "CO": {
        "full_name": "Carbon Monoxide",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_CO",
        "band": "CO_column_number_density",
        "qa_band": "H2O_column_number_density",  # qa_value for CO
        "qa_threshold": 0.5,
        "unit": "mol/m²",
        "scale_factor": 1e3,
        "display_unit": "mmol/m²",
        "colormap": "OrRd",
        "who_guideline": None,
    },
    "O3": {
        "full_name": "Ozone",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_O3",
        "band": "O3_column_number_density",
        "qa_band": "O3_column_number_density",
        "qa_threshold": 0.5,
        "unit": "mol/m²",
        "scale_factor": 1e3,
        "display_unit": "mmol/m²",
        "colormap": "BuPu",
        "who_guideline": None,
    },
    "HCHO": {
        "full_name": "Formaldehyde",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_HCHO",
        "band": "tropospheric_HCHO_column_number_density",
        "qa_band": "tropospheric_HCHO_column_number_density",
        "qa_threshold": 0.5,
        "unit": "mol/m²",
        "scale_factor": 1e6,
        "display_unit": "µmol/m²",
        "colormap": "YlGn",
        "who_guideline": None,
    },
    "UVAI": {
        "full_name": "UV Aerosol Index",
        "gee_collection": "COPERNICUS/S5P/OFFL/L3_AER_AI",
        "band": "absorbing_aerosol_index",
        "qa_band": "absorbing_aerosol_index",
        "qa_threshold": None,  # No QA filtering for UVAI
        "unit": "dimensionless",
        "scale_factor": 1,
        "display_unit": "Index",
        "colormap": "hot_r",
        "who_guideline": None,
    },
}

# =============================================================================
# NEPAL PHYSIOGRAPHIC ZONES
# =============================================================================
# Elevation-based classification (meters)
PHYSIOGRAPHIC_ZONES = {
    "Terai": {"min_elev": 0, "max_elev": 300, "description": "Southern plains"},
    "Siwalik": {
        "min_elev": 300,
        "max_elev": 1500,
        "description": "Outer Himalaya foothills",
    },
    "Middle_Mountains": {
        "min_elev": 1500,
        "max_elev": 3000,
        "description": "Mid-hills region",
    },
    "High_Mountains": {
        "min_elev": 3000,
        "max_elev": 5000,
        "description": "Inner Himalaya",
    },
    "High_Himal": {
        "min_elev": 5000,
        "max_elev": 9000,
        "description": "Trans-Himalaya / Nival zone",
    },
}

# Nepal bounding box (approximate)
NEPAL_BBOX = {
    "west": 80.0,
    "south": 26.3,
    "east": 88.2,
    "north": 30.5,
}

# Nepal provinces (7 provinces)
PROVINCES = [
    "Koshi",
    "Madhesh",
    "Bagmati",
    "Gandaki",
    "Lumbini",
    "Karnali",
    "Sudurpashchim",
]

# =============================================================================
# SEASONS (Nepal-specific)
# =============================================================================
SEASONS = {
    "Pre-monsoon": [3, 4, 5],  # March–May
    "Monsoon": [6, 7, 8, 9],  # June–September
    "Post-monsoon": [10, 11],  # October–November
    "Winter": [12, 1, 2],  # December–February
}

SEASON_COLORS = {
    "Pre-monsoon": "#FF6B35",
    "Monsoon": "#1E88E5",
    "Post-monsoon": "#43A047",
    "Winter": "#8E24AA",
}

# =============================================================================
# ERA5 CLIMATE VARIABLES
# =============================================================================
ERA5_VARIABLES = {
    "temperature_2m": {
        "full_name": "2m Air Temperature",
        "gee_collection": "ECMWF/ERA5_LAND/MONTHLY_AGGR",
        "band": "temperature_2m",
        "unit": "K",
        "convert_to_celsius": True,
    },
    "total_precipitation": {
        "full_name": "Total Precipitation",
        "gee_collection": "ECMWF/ERA5_LAND/MONTHLY_AGGR",
        "band": "total_precipitation_sum",
        "unit": "m",
        "convert_to_mm": True,
    },
    "u_wind_10m": {
        "full_name": "10m U-component of Wind",
        "gee_collection": "ECMWF/ERA5_LAND/MONTHLY_AGGR",
        "band": "u_component_of_wind_10m",
        "unit": "m/s",
    },
    "v_wind_10m": {
        "full_name": "10m V-component of Wind",
        "gee_collection": "ECMWF/ERA5_LAND/MONTHLY_AGGR",
        "band": "v_component_of_wind_10m",
        "unit": "m/s",
    },
    "dewpoint_temperature_2m": {
        "full_name": "2m Dewpoint Temperature",
        "gee_collection": "ECMWF/ERA5_LAND/MONTHLY_AGGR",
        "band": "dewpoint_temperature_2m",
        "unit": "K",
        "convert_to_celsius": True,
    },
}

# =============================================================================
# ANALYSIS PARAMETERS
# =============================================================================

# Mann-Kendall test
MK_SIGNIFICANCE_LEVEL = 0.05

# Spatial statistics
SPATIAL_WEIGHTS_TYPE = "queen"  # 'queen' or 'rook' contiguity
DISTANCE_BAND_KM = 50  # For distance-based weights
GI_STAR_SIGNIFICANCE = 0.05

# Wavelet analysis
WAVELET_MOTHER = "morlet"
WAVELET_DT = 1 / 12  # Monthly data -> 1/12 year

# Granger causality
GRANGER_MAX_LAG = 6  # Maximum lag in months

# BFAST
BFAST_H = 0.15  # Minimal segment size (fraction of time series)
BFAST_SEASON = "harmonic"  # Seasonal model type
BFAST_MAX_ITER = 10

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================
FIGURE_DPI = 300
FIGURE_FORMAT = "png"  # 'png', 'pdf', 'svg', 'tiff'
FONT_FAMILY = "Arial"
FONT_SIZE = 10
TITLE_SIZE = 12

# Map projection for Nepal
MAP_CRS = "EPSG:4326"  # WGS84
MAP_PROJECTED_CRS = "EPSG:32645"  # UTM Zone 45N (covers most of Nepal)

# Colorbar settings
CBAR_ORIENTATION = "horizontal"
CBAR_SHRINK = 0.6
CBAR_PAD = 0.08

# =============================================================================
# KEY EVENTS (for annotation in time series plots)
# =============================================================================
KEY_EVENTS = {
    "2020-03-24": "Nepal COVID-19 Lockdown",
    "2020-06-15": "Lockdown Eased (Phase 1)",
    "2020-09-01": "Lockdown Fully Lifted",
    "2021-04-29": "Second Lockdown",
    "2021-09-01": "Second Lockdown Lifted",
    "2023-03-01": "2023 Wildfire Season Peak",
}
