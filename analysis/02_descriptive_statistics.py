"""
Script 02: Descriptive Statistics (Layer 2)

Generates descriptive statistics tables, seasonal boxplots, and multi-pollutant
time series plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import plot_seasonal_boxplot, plot_multi_pollutant_panel


def run_descriptive_stats():
    """Run descriptive statistics layer."""
    print("Running Descriptive Statistics Analysis...")

    stats_out = FIGURES_DIR / "descriptive_stats"
    stats_out.mkdir(exist_ok=True)

    summary_stats = []
    multi_data = {}

    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"

        if not file_path.exists():
            print(f"  [SKIPPING] {pol} data not found.")
            continue

        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])

        # 1. Summary table (Mean, Std, Min, Max, CV by Zone & Season)
        mean_col = f"{pol}_mean"

        # Overall zone stats
        zone_stats = df.groupby("zone")[mean_col].agg(["mean", "std", "min", "max"])
        zone_stats["CV"] = (zone_stats["std"] / zone_stats["mean"]) * 100
        zone_stats["Pollutant"] = pol
        zone_stats["Level"] = "Annual"
        summary_stats.append(zone_stats.reset_index())

        # Seasonal stats
        seasonal_stats = df.groupby(["zone", "season"])[mean_col].agg(["mean", "std"])
        seasonal_stats["CV"] = (seasonal_stats["std"] / seasonal_stats["mean"]) * 100
        seasonal_stats["Pollutant"] = pol
        seasonal_stats["Level"] = "Seasonal"
        summary_stats.append(seasonal_stats.reset_index())

        # 2. Seasonal Boxplots
        plot_seasonal_boxplot(
            df,
            pol,
            group_by="season",
            title=f"Seasonal {POLLUTANTS[pol]['full_name']} Distribution",
            save_path=stats_out / f"{pol}_seasonal_boxplot",
        )

        # 3. Store for multi-panel
        multi_data[pol] = df

    # Combine and save summary stats
    if summary_stats:
        final_stats = pd.concat(summary_stats, ignore_index=True)
        final_stats.to_csv(PROCESSED_DIR / "descriptive_summary_stats.csv", index=False)
        print(
            f"\nSaved summary statistics to {PROCESSED_DIR / 'descriptive_summary_stats.csv'}"
        )

    # 4. Multi-pollutant panel
    if multi_data:
        zones_to_plot = [
            "Terai",
            "Middle_Mountains",
            "High_Himal",
        ]  # Plot subset for clarity
        plot_multi_pollutant_panel(
            multi_data,
            zones_to_plot,
            title="Multi-Pollutant Time Series (Selected Zones)",
            save_path=stats_out / "multi_pollutant_timeseries",
        )
        print(f"\nSaved multi-pollutant figure to {stats_out}")


if __name__ == "__main__":
    run_descriptive_stats()
