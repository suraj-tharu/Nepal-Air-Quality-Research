"""
Script 01: Data Preprocessing

Loads exported GEE data (CSVs), cleans it, applies scaling factors,
adds season labels, and saves as processed DataFrames for downstream analysis.
"""

import os
import glob
import pandas as pd
from pathlib import Path

# Import from config
from config import RAW_DIR, PROCESSED_DIR, POLLUTANTS, ERA5_VARIABLES, SEASONS
from utils.spatial_utils import assign_season


def load_and_clean_gee_export(file_pattern, val_col, scale_factor=1.0):
    """
    Load GEE exported CSV, clean dates, scale values, and add seasons.
    Handles multiple CSVs if export was split.
    """
    files = glob.glob(str(RAW_DIR / file_pattern))
    if not files:
        print(f"[WARNING] No files found for {file_pattern}. Run GEE exports first.")
        return pd.DataFrame()

    df_list = []
    for f in files:
        df_list.append(pd.read_csv(f))

    df = pd.concat(df_list, ignore_index=True)

    # Required columns: year, month, zone, and the variable column(s)
    req_cols = ["year", "month", "zone"]
    if not all(c in df.columns for c in req_cols):
        print(f"[ERROR] Missing required columns in {file_pattern}")
        return pd.DataFrame()

    # Drop system:index and .geo if they exist
    df = df.drop(columns=["system:index", ".geo"], errors="ignore")

    # Create datetime column
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(DAY=1))

    # Add season
    df["season"] = df["month"].apply(assign_season)

    # Scale values if needed (e.g., mol/m2 -> umol/m2)
    if isinstance(val_col, str):
        if val_col in df.columns:
            df[val_col] = df[val_col] * scale_factor
    elif isinstance(val_col, list):
        for col in val_col:
            if col in df.columns:
                df[col] = df[col] * scale_factor

    # Sort
    df = df.sort_values(["zone", "date"]).reset_index(drop=True)

    return df


def preprocess_pollutants():
    """Process all pollutant data."""
    print("Processing Pollutant Data...")

    all_data = {}

    for pol, params in POLLUTANTS.items():
        pattern = f"{pol}_monthly_zonal_physiographic*.csv"
        mean_col = f"{pol}_mean"

        df = load_and_clean_gee_export(
            pattern,
            val_col=[mean_col, f"{pol}_median", f"{pol}_stdDev"],
            scale_factor=params["scale_factor"],
        )

        if not df.empty:
            out_file = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
            df.to_csv(out_file, index=False)
            all_data[pol] = df
            print(f"  -> Saved {pol} data: {len(df)} records")

    return all_data


def preprocess_climate():
    """Process ERA5 climate data."""
    print("Processing ERA5 Climate Data...")

    pattern = "ERA5_monthly_zonal_physiographic*.csv"

    df = load_and_clean_gee_export(pattern, val_col=None)

    if not df.empty:
        out_file = PROCESSED_DIR / "ERA5_climate_zonal_ts.csv"
        df.to_csv(out_file, index=False)
        print(f"  -> Saved ERA5 data: {len(df)} records")

    return df


def preprocess_population():
    """Process population data."""
    print("Processing Population Data...")

    pattern = "Population_zonal_physiographic*.csv"

    df = load_and_clean_gee_export(pattern, val_col=None)

    if not df.empty:
        out_file = PROCESSED_DIR / "Population_zonal_ts.csv"
        df.to_csv(out_file, index=False)
        print(f"  -> Saved Population data: {len(df)} records")

    return df


if __name__ == "__main__":
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    print("-" * 40)

    preprocess_pollutants()
    preprocess_climate()
    print("Preprocessing complete.")
