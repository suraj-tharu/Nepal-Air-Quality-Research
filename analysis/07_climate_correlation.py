"""
Script 07: Climate-Pollution Correlation Analysis (Layer 6)

Calculates Pearson, Spearman, and Partial correlations between
pollutants and ERA5 climate variables.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

try:
    import pingouin as pg

    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False
    print("[WARNING] pingouin not found. Partial correlations will be skipped.")
    print("Run: pip install pingouin")

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS, ERA5_VARIABLES
from utils.plotting import plot_correlation_heatmap


def run_correlation_analysis():
    """Calculate and plot correlations."""
    print("Running Climate-Pollution Correlation Analysis...")

    corr_out = FIGURES_DIR / "climate_correlation"
    corr_out.mkdir(exist_ok=True)

    # Load climate data
    clim_path = PROCESSED_DIR / "ERA5_climate_zonal_ts.csv"
    if not clim_path.exists():
        print("  [ERROR] Climate data not found.")
        return

    clim_df = pd.read_csv(clim_path)
    clim_df["date"] = pd.to_datetime(clim_df["date"])

    # Analyze by zone
    zones = clim_df["zone"].unique()

    for zone in zones:
        print(f"  -> Analyzing Zone: {zone}")

        zone_clim = clim_df[clim_df["zone"] == zone].set_index("date")

        # Collect pollutant data for this zone
        pol_data = {}
        for pol in POLLUTANTS.keys():
            pol_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
            if pol_path.exists():
                df = pd.read_csv(pol_path)
                df["date"] = pd.to_datetime(df["date"])
                z_df = df[df["zone"] == zone].set_index("date")
                pol_data[f"{pol}"] = z_df[f"{pol}_mean"]

        if not pol_data:
            continue

        pol_df = pd.DataFrame(pol_data)

        # Merge climate and pollutants
        merged = pd.merge(
            pol_df, zone_clim, left_index=True, right_index=True, how="inner"
        )

        # Select variables for correlation
        pol_cols = list(pol_data.keys())
        clim_cols = ["temp_mean", "precip_mean", "wind_speed_mean", "rh_mean"]

        # Keep only available columns
        clim_cols = [c for c in clim_cols if c in merged.columns]

        if not clim_cols:
            continue

        # 1. Pearson Correlation
        corr_matrix = merged[pol_cols + clim_cols].corr(method="pearson")

        # Extract the pol vs clim sub-matrix
        sub_corr = corr_matrix.loc[pol_cols, clim_cols]

        # Calculate p-values manually for the sub-matrix
        p_matrix = pd.DataFrame(index=pol_cols, columns=clim_cols)
        for p in pol_cols:
            for c in clim_cols:
                mask = ~merged[p].isna() & ~merged[c].isna()
                if mask.sum() > 2:
                    r, pval = stats.pearsonr(merged.loc[mask, p], merged.loc[mask, c])
                    p_matrix.loc[p, c] = pval
                else:
                    p_matrix.loc[p, c] = 1.0  # Not sig

        p_matrix = p_matrix.astype(float)

        # Plot
        plot_correlation_heatmap(
            sub_corr,
            title=f"Pearson Correlation: Pollutants vs Climate ({zone})",
            p_matrix=p_matrix,
            mask_insignificant=True,
            save_path=corr_out / f"Corr_Pearson_{zone}",
        )

        # 2. Partial Correlation (controlling for other climate vars)
        if HAS_PINGOUIN:
            partial_results = []
            for p in pol_cols:
                for c in clim_cols:
                    covar = [x for x in clim_cols if x != c]
                    try:
                        res = pg.partial_corr(data=merged, x=p, y=c, covar=covar)
                        partial_results.append(
                            {
                                "Zone": zone,
                                "Pollutant": p,
                                "Climate_Var": c,
                                "Partial_r": res["r"].values[0],
                                "p_val": res["p-val"].values[0],
                            }
                        )
                    except Exception as e:
                        pass

            if partial_results:
                part_df = pd.DataFrame(partial_results)
                part_df.to_csv(corr_out / f"Partial_Corr_{zone}.csv", index=False)


if __name__ == "__main__":
    run_correlation_analysis()
