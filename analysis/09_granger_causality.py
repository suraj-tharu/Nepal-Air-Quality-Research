"""
Script 09: Granger Causality (Layer 6)

Tests if past values of climate variables provide statistically significant
information to predict current values of pollutants (and vice versa).
"""

import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS


def run_granger():
    """Run Granger Causality Tests."""
    print("Running Granger Causality Tests...")

    gc_out = FIGURES_DIR / "granger_causality"
    gc_out.mkdir(exist_ok=True)

    clim_path = PROCESSED_DIR / "ERA5_climate_zonal_ts.csv"
    if not clim_path.exists():
        return

    clim_df = pd.read_csv(clim_path)
    clim_df["date"] = pd.to_datetime(clim_df["date"])

    maxlag = 6  # Check up to 6 months lag
    results = []

    zones = clim_df["zone"].unique()

    for zone in zones:
        zone_clim = clim_df[clim_df["zone"] == zone].set_index("date")

        for pol in POLLUTANTS.keys():
            pol_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
            if not pol_path.exists():
                continue

            df = pd.read_csv(pol_path)
            df["date"] = pd.to_datetime(df["date"])
            zone_pol = df[df["zone"] == zone].set_index("date")

            merged = pd.merge(
                zone_pol[[f"{pol}_mean"]],
                zone_clim[["temp_mean", "precip_mean"]],
                left_index=True,
                right_index=True,
            )
            merged = merged.dropna()

            if len(merged) < 30:  # Need enough data points
                continue

            # 1. Does Climate Granger-cause Pollutant?
            for clim_var in ["temp_mean", "precip_mean"]:
                try:
                    # format: [Y, X] -> does X cause Y?
                    data = merged[[f"{pol}_mean", clim_var]]
                    # Suppress output, we just want the p-values
                    gc_res = grangercausalitytests(data, maxlag=maxlag, verbose=False)

                    # Extract min p-value across lags (using SSR F-test)
                    min_p = min(
                        [gc_res[lag][0]["ssr_ftest"][1] for lag in range(1, maxlag + 1)]
                    )
                    best_lag = [
                        lag
                        for lag in range(1, maxlag + 1)
                        if gc_res[lag][0]["ssr_ftest"][1] == min_p
                    ][0]

                    results.append(
                        {
                            "Zone": zone,
                            "Target (Y)": pol,
                            "Predictor (X)": clim_var,
                            "Direction": "Climate -> Pollutant",
                            "Best_Lag": best_lag,
                            "Min_p_value": min_p,
                            "Significant": min_p < 0.05,
                        }
                    )
                except Exception as e:
                    pass

    if results:
        res_df = pd.DataFrame(results)
        res_df.to_csv(gc_out / "granger_results.csv", index=False)
        print(f"Saved Granger results to {gc_out / 'granger_results.csv'}")


if __name__ == "__main__":
    run_granger()
