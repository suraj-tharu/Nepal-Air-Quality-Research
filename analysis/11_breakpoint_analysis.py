"""
Script 11: Breakpoint Analysis
Replaces the R BFAST script by performing structural breakpoint detection
on the pollutant timeseries using Python's `ruptures` library.

Identifies abrupt shifts in the timeseries trend (e.g., COVID-19 lockdown drops).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ruptures as rpt
import os
from statsmodels.tsa.seasonal import STL

# Import from config
from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS

BREAKPOINT_DIR = FIGURES_DIR / "breakpoint_analysis"
BREAKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def detect_breakpoints():
    print("Running Python Breakpoint Analysis (replacing R-BFAST)...")

    results = []

    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not file_path.exists():
            continue

        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])

        for zone in df["zone"].unique():
            zone_data = (
                df[df["zone"] == zone].sort_values("date").reset_index(drop=True)
            )

            if len(zone_data) < 36:
                print(f"    [WARNING] Not enough data for {zone}")
                continue

            ts_values = zone_data[f"{pol}_mean"].values
            dates = zone_data["date"]

            # Decompose the time series to isolate the trend component
            stl = STL(ts_values, period=12, robust=True)
            res = stl.fit()
            trend = res.trend

            # Change point detection on the trend using Binary Segmentation (Binseg)
            # More robust than Pelt for these types of environmental time series
            algo = rpt.Binseg(model="l2", min_size=6).fit(trend)
            # Find change points using penalty
            penalty = 3.0 * np.log(len(trend)) * np.var(trend)
            # If variance is tiny, Binseg might return no breakpoints (which is correct)
            try:
                breakpoints = algo.predict(pen=penalty)
            except Exception:
                breakpoints = []

            # Remove the last breakpoint which is just the end of the array
            if len(breakpoints) > 0 and breakpoints[-1] == len(trend):
                breakpoints = breakpoints[:-1]

            # Plotting
            plt.figure(figsize=(12, 6))
            plt.plot(dates, ts_values, label="Raw Data", color="gray", alpha=0.5)
            plt.plot(dates, trend, label="STL Trend", color="blue", linewidth=2)

            bp_dates = []
            for bp in breakpoints:
                bp_idx = min(bp, len(dates) - 1)
                bp_date = dates.iloc[bp_idx]
                bp_dates.append(bp_date.strftime("%Y-%m"))
                plt.axvline(x=bp_date, color="red", linestyle="--", linewidth=2)

            plt.title(f"Structural Breakpoint Analysis: {pol} in {zone}")
            plt.xlabel("Date")
            plt.ylabel("Concentration (mol/m²)")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            # Save plot
            safe_zone = zone.replace(" ", "_")
            plt.savefig(BREAKPOINT_DIR / f"Breakpoint_{pol}_{safe_zone}.png", dpi=300)
            plt.savefig(BREAKPOINT_DIR / f"Breakpoint_{pol}_{safe_zone}.pdf")
            plt.close()

            # Store results
            results.append(
                {
                    "Pollutant": pol,
                    "Zone": zone,
                    "Trend_Breakpoints": ", ".join(bp_dates) if bp_dates else "None",
                }
            )

    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(PROCESSED_DIR / "breakpoint_results.csv", index=False)
        print(
            f"\nSaved Breakpoint results to {PROCESSED_DIR / 'breakpoint_results.csv'}"
        )


if __name__ == "__main__":
    detect_breakpoints()
