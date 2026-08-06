"""
Script 04: STL Decomposition (Layer 4)

Performs Seasonal-Trend decomposition using LOESS (STL) on the time series.
Separates data into Trend, Seasonal, and Residual components.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import plot_stl_decomposition


def run_stl_decomposition():
    """Run STL on all pollutants."""
    print("Running STL Decomposition...")

    stl_out = FIGURES_DIR / "stl_decomposition"
    stl_out.mkdir(exist_ok=True)

    # Store components for potential later use (e.g., breakpoint detection)
    components_db = []

    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not file_path.exists():
            continue

        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])

        mean_col = f"{pol}_mean"

        for zone in df["zone"].unique():
            zone_data = df[df["zone"] == zone].sort_values("date").set_index("date")

            # Need regular frequency for STL
            # Monthly data -> period=12
            ts_data = zone_data[mean_col].asfreq("MS")

            # Handle missing values via interpolation if necessary
            if ts_data.isna().any():
                ts_data = ts_data.interpolate(method="time")

            if len(ts_data.dropna()) < 24:
                print(f"    [WARNING] Not enough data for STL in {zone}")
                continue

            try:
                # STL parameters:
                # period=12 (monthly),
                # seasonal=13 (odd number, controls stiffness of seasonal component)
                # robust=True (handles outliers like wildfire spikes)
                stl = STL(ts_data, period=12, seasonal=13, robust=True)
                res = stl.fit()

                # Plot
                save_path = stl_out / f"STL_{pol}_{zone}"
                plot_stl_decomposition(
                    res, ts_data.index, pol, zone, save_path=save_path
                )

                # Save components
                comp_df = pd.DataFrame(
                    {
                        "date": ts_data.index,
                        "pollutant": pol,
                        "zone": zone,
                        "observed": res.observed,
                        "trend": res.trend,
                        "seasonal": res.seasonal,
                        "residual": res.resid,
                    }
                )
                components_db.append(comp_df)

            except Exception as e:
                print(f"    [ERROR] STL failed for {pol} {zone}: {e}")

    if components_db:
        final_db = pd.concat(components_db, ignore_index=True)
        out_csv = PROCESSED_DIR / "stl_components.csv"
        final_db.to_csv(out_csv, index=False)
        print(f"\nSaved STL components to {out_csv}")


if __name__ == "__main__":
    run_stl_decomposition()
