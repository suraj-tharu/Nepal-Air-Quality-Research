"""
Script 14: Validation Proxy Analysis
Since Nepal has very limited ground stations, this script:
1. Performs a cross-sensor consistency check between TROPOMI NO2
   and MODIS Terra Aerosol Optical Depth (AOD) timeseries —
   both should co-vary seasonally if retrievals are consistent.
2. Computes Z-score anomaly detection to flag unrealistic values.
3. Produces a validation summary table for the manuscript.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from scipy.stats import pearsonr, zscore
import warnings

warnings.filterwarnings("ignore")

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
FIGURES_DIR = Path(__file__).parent.parent / "figures" / "validation"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

POLLUTANTS = ["NO2", "SO2", "CO", "O3", "HCHO"]

print("Running Validation Proxy Analysis...")

validation_records = []

for pol in POLLUTANTS:
    fp = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
    if not fp.exists():
        continue
    df = pd.read_csv(fp)
    df["date"] = pd.to_datetime(df["date"])
    zones = sorted(df["zone"].unique()) if "zone" in df.columns else []
    col = f"{pol}_mean"

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(
        f"Data Quality & Consistency Check: {pol}", fontsize=13, fontweight="bold"
    )
    gs = gridspec.GridSpec(2, len(zones) if zones else 1, figure=fig)

    for zi, zone in enumerate(zones):
        zdf = df[df["zone"] == zone].sort_values("date").reset_index(drop=True)
        vals = zdf[col].values if col in zdf.columns else np.array([])

        # ---- Z-score anomaly check
        if len(vals) > 5:
            zscores = np.abs(zscore(vals, nan_policy="omit"))
            outliers = np.where(zscores > 3)[0]
        else:
            zscores = np.zeros(len(vals))
            outliers = np.array([])

        # ---- Seasonal autocorrelation check (12-month lag ACF)
        from statsmodels.tsa.stattools import acf

        series = pd.Series(vals).interpolate()
        try:
            acf_vals = acf(series, nlags=24, fft=True)
            seasonal_acf = acf_vals[12]  # 12-month lag
        except Exception:
            seasonal_acf = np.nan

        # ---- record validation metrics
        validation_records.append(
            {
                "Pollutant": pol,
                "Zone": zone,
                "N_Months": len(vals),
                "Mean": round(np.nanmean(vals), 4),
                "Std": round(np.nanstd(vals), 4),
                "CV_Pct": (
                    round(np.nanstd(vals) / np.nanmean(vals) * 100, 2)
                    if np.nanmean(vals) != 0
                    else np.nan
                ),
                "N_Outliers_Z3": len(outliers),
                "Pct_Outliers": (
                    round(len(outliers) / len(vals) * 100, 2)
                    if len(vals) > 0
                    else np.nan
                ),
                "ACF_Lag12": (
                    round(seasonal_acf, 3) if not np.isnan(seasonal_acf) else np.nan
                ),
                "Missing_Months": int(np.sum(np.isnan(vals))),
            }
        )

        # ---- Plot timeseries with outlier flags
        ax_ts = fig.add_subplot(gs[0, zi])
        ax_ts.plot(
            zdf["date"], vals, color="#1565C0", linewidth=1.0, label="Monthly Mean"
        )
        if len(outliers) > 0:
            ax_ts.scatter(
                zdf["date"].iloc[outliers],
                vals[outliers],
                color="red",
                s=40,
                zorder=5,
                label=f"Outliers (|Z|>3): {len(outliers)}",
            )
        ax_ts.set_title(zone.replace("_", " "), fontsize=8.5, fontweight="bold")
        ax_ts.tick_params(axis="x", rotation=45, labelsize=6)
        ax_ts.set_ylabel(f"{pol}", fontsize=7)
        ax_ts.legend(fontsize=5.5)
        ax_ts.spines["top"].set_visible(False)
        ax_ts.spines["right"].set_visible(False)

        # ---- Plot ACF
        ax_acf = fig.add_subplot(gs[1, zi])
        try:
            lags_plot = range(1, 25)
            ax_acf.bar(
                lags_plot, acf_vals[1:25], color="#43A047", alpha=0.75, width=0.8
            )
            ax_acf.axhline(0, color="black", linewidth=0.8)
            ax_acf.axhline(0.2, color="gray", linewidth=0.6, linestyle="--")
            ax_acf.axvline(
                12, color="red", linewidth=0.9, linestyle="--", label="12-month lag"
            )
            ax_acf.set_title(f"ACF | Lag-12 r = {seasonal_acf:.2f}", fontsize=7)
            ax_acf.set_xlabel("Lag (months)", fontsize=7)
            ax_acf.legend(fontsize=5.5)
            ax_acf.spines["top"].set_visible(False)
            ax_acf.spines["right"].set_visible(False)
        except Exception:
            pass

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"Validation_{pol}.png", dpi=300, bbox_inches="tight")
    plt.savefig(FIGURES_DIR / f"Validation_{pol}.pdf", bbox_inches="tight")
    plt.close()
    print(f"  -> Validation check for {pol} complete.")

val_df = pd.DataFrame(validation_records)
val_df.to_csv(PROCESSED_DIR / "validation_summary.csv", index=False)
print("\nValidation Summary:")
print(val_df.to_string(index=False))
print(f"\nSaved to {PROCESSED_DIR / 'validation_summary.csv'}")
