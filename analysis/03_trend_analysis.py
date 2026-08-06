"""
Script 03: Trend Analysis (Layer 3)

Performs Mann-Kendall trend tests, computes Theil-Sen slopes, and runs
Innovative Trend Analysis (ITA) on the time series data.
"""

import pandas as pd
import numpy as np
import pymannkendall as mk
import matplotlib.pyplot as plt
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import plot_trend_significance, save_figure


def innovative_trend_analysis(df, col, zone, save_path=None):
    """
    Perform Innovative Trend Analysis (ITA) proposed by Sen (2012).
    Compares first half of sorted data vs second half.
    """
    data = df[col].dropna().values
    if len(data) < 10:
        return None

    n = len(data)
    half = n // 2

    # Split into two halves chronologically
    first_half = data[:half]
    second_half = data[-half:] if n % 2 == 0 else data[-(half):]

    # Sort both halves ascending
    first_half_sorted = np.sort(first_half)
    second_half_sorted = np.sort(second_half)

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(first_half_sorted, second_half_sorted, alpha=0.7, edgecolors="k")

    # 1:1 line (No trend)
    min_val = min(first_half_sorted.min(), second_half_sorted.min())
    max_val = max(first_half_sorted.max(), second_half_sorted.max())

    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        "k-",
        lw=1.5,
        label="1:1 Line (No Trend)",
    )

    # +- 10% significance bands (standard ITA practice)
    ax.plot(
        [min_val, max_val],
        [min_val * 1.1, max_val * 1.1],
        "r--",
        lw=1,
        label="+10% Band",
    )
    ax.plot(
        [min_val, max_val],
        [min_val * 0.9, max_val * 0.9],
        "r--",
        lw=1,
        label="-10% Band",
    )

    ax.set_xlabel("First Half (Sorted)")
    ax.set_ylabel("Second Half (Sorted)")
    ax.set_title(f"ITA: {zone}")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)

    fig.tight_layout()
    if save_path:
        save_figure(fig, save_path)
    else:
        plt.close(fig)

    return fig


def run_trend_analysis():
    """Run MK, Theil-Sen, and ITA."""
    print("Running Trend Analysis...")

    trend_out = FIGURES_DIR / "trend_analysis"
    trend_out.mkdir(exist_ok=True)

    all_results = []

    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not file_path.exists():
            continue

        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(file_path)

        pollutant_results = []
        mean_col = f"{pol}_mean"

        for zone in df["zone"].unique():
            zone_data = df[df["zone"] == zone]

            # Annual MK Test (Hamed-Rao accounts for autocorrelation)
            try:
                mk_res = mk.hamed_rao_modification_test(zone_data[mean_col].values)

                pollutant_results.append(
                    {
                        "pollutant": pol,
                        "zone": zone,
                        "season": "Annual",
                        "trend": mk_res.trend,
                        "p_value": mk_res.p,
                        "slope": mk_res.slope,
                        "intercept": mk_res.intercept,
                    }
                )

                # ITA Plot for Annual data
                ita_path = trend_out / f"ITA_{pol}_{zone}"
                innovative_trend_analysis(zone_data, mean_col, zone, save_path=ita_path)

            except Exception as e:
                print(f"    [ERROR] MK test failed for {zone} Annual: {e}")

            # Seasonal MK Tests
            for season in df["season"].unique():
                season_data = zone_data[zone_data["season"] == season]

                if len(season_data) < 4:  # Need minimum data points
                    continue

                try:
                    # Standard MK for seasonal (less autocorrelation issue within a season across years)
                    mk_res = mk.original_test(season_data[mean_col].values)

                    pollutant_results.append(
                        {
                            "pollutant": pol,
                            "zone": zone,
                            "season": season,
                            "trend": mk_res.trend,
                            "p_value": mk_res.p,
                            "slope": mk_res.slope,
                            "intercept": mk_res.intercept,
                        }
                    )
                except Exception as e:
                    pass

        # Save results and plot heatmaps
        if pollutant_results:
            res_df = pd.DataFrame(pollutant_results)
            all_results.append(res_df)

            # Filter out 'Annual' for the seasonal heatmap
            seasonal_res = res_df[res_df["season"] != "Annual"]
            if not seasonal_res.empty:
                plot_trend_significance(
                    seasonal_res, pol, save_path=trend_out / f"MK_Significance_{pol}"
                )

    if all_results:
        final_results = pd.concat(all_results, ignore_index=True)
        out_csv = PROCESSED_DIR / "mann_kendall_results.csv"
        final_results.to_csv(out_csv, index=False)
        print(f"\nSaved trend analysis results to {out_csv}")


if __name__ == "__main__":
    run_trend_analysis()
