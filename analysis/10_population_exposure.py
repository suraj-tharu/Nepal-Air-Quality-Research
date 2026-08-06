"""
Script 10: Population Exposure Analysis (Layer 7)

Calculates population-weighted exposure to pollutants and evaluates
exceedances of WHO Air Quality Guidelines.
"""

import pandas as pd
import numpy as np
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS


def run_exposure_analysis():
    """Run Population Exposure Analysis."""
    print("Running Population Exposure Analysis...")

    exp_out = FIGURES_DIR / "population_exposure"
    exp_out.mkdir(exist_ok=True)

    pop_path = PROCESSED_DIR / "Population_zonal_ts.csv"
    if not pop_path.exists():
        print("  [ERROR] Population data not found.")
        return

    pop_df = pd.read_csv(pop_path)
    # Use latest available population year
    latest_yr = pop_df["year"].max()
    pop_latest = pop_df[pop_df["year"] == latest_yr].set_index("zone")

    results = []

    for pol in POLLUTANTS.keys():
        pol_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not pol_path.exists():
            continue

        df = pd.read_csv(pol_path)

        # Calculate annual mean per zone
        annual_mean = df.groupby(["year", "zone"])[f"{pol}_mean"].mean().reset_index()

        # Merge with population
        merged = pd.merge(
            annual_mean,
            pop_latest[["population_total"]],
            left_on="zone",
            right_index=True,
        )

        # Calculate Population-Weighted Concentration (PWC)
        # PWC = sum(C_i * P_i) / sum(P_i)
        for yr in merged["year"].unique():
            yr_data = merged[merged["year"] == yr]
            total_pop = yr_data["population_total"].sum()

            pwc = (
                yr_data[f"{pol}_mean"] * yr_data["population_total"]
            ).sum() / total_pop

            results.append({"Year": yr, "Pollutant": pol, "Pop_Weighted_Mean": pwc})

    if results:
        res_df = pd.DataFrame(results)
        res_df.to_csv(exp_out / "population_weighted_exposure.csv", index=False)
        print(
            f"Saved exposure results to {exp_out / 'population_weighted_exposure.csv'}"
        )


if __name__ == "__main__":
    run_exposure_analysis()
