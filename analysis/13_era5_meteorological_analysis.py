"""
Script 13: ERA5 Meteorological Deep Analysis
Correlates ERA5 climate variables with pollutant timeseries per zone.
Generates:
  - Heatmaps of Pearson r per zone (all pollutants x all climate vars)
  - Seasonal correlation breakdown
  - Wind rose proxy (pollution vs wind speed scatter)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import pearsonr
import warnings

warnings.filterwarnings("ignore")

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
FIGURES_DIR = Path(__file__).parent.parent / "figures" / "era5_analysis"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

POLLUTANTS = ["NO2", "SO2", "CO", "O3", "HCHO", "UVAI"]
CLIMATE_VARS = ["temperature_mean", "precip_mean", "wind_speed_mean", "rh_mean"]
CLIMATE_LABELS = {
    "temperature_mean": "Temperature (°C)",
    "precip_mean": "Precipitation (mm)",
    "wind_speed_mean": "Wind Speed (m/s)",
    "rh_mean": "Relative Humidity (%)",
}

# Load ERA5
era5_path = PROCESSED_DIR / "ERA5_climate_zonal_ts.csv"
if not era5_path.exists():
    print("ERA5 file not found. Exiting.")
    exit()

era5 = pd.read_csv(era5_path)
era5["date"] = pd.to_datetime(era5["date"])
zones = sorted(era5["zone"].unique()) if "zone" in era5.columns else ["Unknown"]

print("Running ERA5 Meteorological Deep Analysis...")

for zone in zones:
    zone_era5 = (
        era5[era5["zone"] == zone].sort_values("date").reset_index(drop=True)
        if "zone" in era5.columns
        else era5.copy()
    )

    # Build correlation matrix
    corr_data = {}
    pval_data = {}

    for pol in POLLUTANTS:
        fp = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not fp.exists():
            continue
        pol_df = pd.read_csv(fp)
        pol_df["date"] = pd.to_datetime(pol_df["date"])
        if "zone" in pol_df.columns:
            pol_df = pol_df[pol_df["zone"] == zone]
        pol_df = pol_df.sort_values("date").reset_index(drop=True)
        merged = pd.merge(
            zone_era5, pol_df[["date", f"{pol}_mean"]], on="date", how="inner"
        )

        row_r, row_p = {}, {}
        for cv in CLIMATE_VARS:
            if cv in merged.columns and f"{pol}_mean" in merged.columns:
                valid = merged[[cv, f"{pol}_mean"]].dropna()
                if len(valid) > 10:
                    r, p = pearsonr(valid[cv], valid[f"{pol}_mean"])
                    row_r[cv] = round(r, 3)
                    row_p[cv] = p
                else:
                    row_r[cv] = np.nan
                    row_p[cv] = np.nan
            else:
                row_r[cv] = np.nan
                row_p[cv] = np.nan
        corr_data[pol] = row_r
        pval_data[pol] = row_p

    if not corr_data:
        continue

    corr_df = pd.DataFrame(corr_data).T  # rows=pollutants, cols=climate vars
    pval_df = pd.DataFrame(pval_data).T

    # Build significance annotation matrix
    annot_df = corr_df.copy().astype(str)
    for i in corr_df.index:
        for j in corr_df.columns:
            r = corr_df.loc[i, j]
            p = pval_df.loc[i, j]
            if pd.isna(r):
                annot_df.loc[i, j] = "N/A"
            else:
                star = (
                    "***"
                    if p < 0.001
                    else "**" if p < 0.01 else "*" if p < 0.05 else ""
                )
                annot_df.loc[i, j] = f"{r:.2f}{star}"

    corr_df.columns = [CLIMATE_LABELS.get(c, c) for c in corr_df.columns]
    annot_df.columns = corr_df.columns

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(
        corr_df.astype(float),
        annot=annot_df,
        fmt="",
        cmap="RdYlGn",
        vmin=-1,
        vmax=1,
        linewidths=0.6,
        ax=ax,
        annot_kws={"size": 10},
    )
    ax.set_title(
        f"ERA5 Climate–Pollutant Pearson Correlation: {zone.replace('_', ' ')}\n"
        f"(* p<0.05, ** p<0.01, *** p<0.001)",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xlabel("Climate Variable", fontsize=10)
    ax.set_ylabel("Pollutant", fontsize=10)
    plt.tight_layout()
    safe_zone = zone.replace(" ", "_")
    plt.savefig(
        FIGURES_DIR / f"ERA5_Corr_{safe_zone}.png", dpi=300, bbox_inches="tight"
    )
    plt.savefig(FIGURES_DIR / f"ERA5_Corr_{safe_zone}.pdf", bbox_inches="tight")
    plt.close()
    print(f"  -> ERA5 correlation heatmap saved for {zone}")

print("\nERA5 meteorological analysis complete.")
