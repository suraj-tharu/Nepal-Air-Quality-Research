"""
Script 12: COVID-19 Lockdown Impact Analysis
Quantifies the difference in pollutant concentrations between:
  - Pre-lockdown (Jan 2019 – Feb 2020)
  - Lockdown (Mar–Jun 2020)
  - Post-lockdown recovery (Jul 2020 – Dec 2020)
  - Post-rebound (Jan 2021 – Dec 2026)

Computes percentage change and generates comparison bar charts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Paths
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
FIGURES_DIR = Path(__file__).parent.parent / "figures" / "covid_analysis"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

POLLUTANTS = ["NO2", "SO2", "CO", "O3", "HCHO", "UVAI"]

# -------------------------------------------------------------------
# Period definitions (Nepal lockdown: 24 Mar – 21 Jul 2020)
# -------------------------------------------------------------------
PERIODS = {
    "Pre-Lockdown\n(Jan 2019–Feb 2020)": ("2019-01-01", "2020-02-28"),
    "Lockdown\n(Mar–Jun 2020)": ("2020-03-01", "2020-06-30"),
    "Post-Lockdown 2020\n(Jul–Dec 2020)": ("2020-07-01", "2020-12-31"),
    "Rebound 2021\n(Jan–Dec 2021)": ("2021-01-01", "2021-12-31"),
    "Post-Rebound\n(2022–2026)": ("2022-01-01", "2026-12-31"),
}

COLORS = ["#2196F3", "#FF5722", "#4CAF50", "#FF9800", "#9C27B0"]


def compute_period_means(df, pollutant, zones):
    """Return mean concentration per period per zone."""
    df["date"] = pd.to_datetime(df["date"])
    col = f"{pollutant}_mean"
    records = []
    for period_name, (start, end) in PERIODS.items():
        mask = (df["date"] >= start) & (df["date"] <= end)
        for zone in zones:
            zone_mask = mask & (df["zone"] == zone)
            val = df.loc[zone_mask, col].mean()
            records.append({"Period": period_name, "Zone": zone, "Mean": val})
    return pd.DataFrame(records)


summary_all = []

for pol in POLLUTANTS:
    fp = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
    if not fp.exists():
        print(f"  [SKIP] {pol} not found")
        continue

    df = pd.read_csv(fp)
    df["date"] = pd.to_datetime(df["date"])
    zones = sorted(df["zone"].unique())

    period_df = compute_period_means(df, pol, zones)

    # --- compute % change vs Pre-Lockdown baseline
    baseline_map = (
        period_df[period_df["Period"] == list(PERIODS.keys())[0]]
        .set_index("Zone")["Mean"]
        .to_dict()
    )
    period_df["Baseline"] = period_df["Zone"].map(baseline_map)
    period_df["PctChange"] = (
        (period_df["Mean"] - period_df["Baseline"]) / period_df["Baseline"].abs()
    ) * 100

    # --- grouped bar chart per zone
    fig, axes = plt.subplots(1, len(zones), figsize=(18, 5), sharey=False)
    if len(zones) == 1:
        axes = [axes]

    for ax, zone in zip(axes, zones):
        zdata = period_df[period_df["Zone"] == zone]
        periods_ordered = list(PERIODS.keys())
        means = [zdata[zdata["Period"] == p]["Mean"].values[0] for p in periods_ordered]
        pcts = [
            zdata[zdata["Period"] == p]["PctChange"].values[0] for p in periods_ordered
        ]

        bars = ax.bar(
            range(len(periods_ordered)),
            means,
            color=COLORS,
            alpha=0.85,
            edgecolor="white",
            linewidth=0.8,
        )

        # annotate % change above each bar
        for i, (bar, pct) in enumerate(zip(bars, pcts)):
            if not np.isnan(pct):
                txt = f"{pct:+.1f}%" if i > 0 else "baseline"
                color = "red" if pct > 0 else "green"
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() * 1.02,
                    txt,
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    color=color,
                    fontweight="bold",
                )

        ax.set_xticks(range(len(periods_ordered)))
        ax.set_xticklabels(
            [p.replace("\n", "\n") for p in periods_ordered],
            fontsize=6.5,
            rotation=15,
            ha="right",
        )
        ax.set_title(zone.replace("_", " "), fontsize=9, fontweight="bold")
        ax.set_ylabel(f"{pol} mean concentration", fontsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.suptitle(
        f"COVID-19 Lockdown Impact on {pol} — Nepal Physiographic Zones",
        fontsize=13,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"COVID_Impact_{pol}.png", dpi=300, bbox_inches="tight")
    plt.savefig(FIGURES_DIR / f"COVID_Impact_{pol}.pdf", bbox_inches="tight")
    plt.close()
    print(f"  -> {pol} COVID analysis saved.")

    # collect stats for summary table
    for _, row in period_df.iterrows():
        summary_all.append(
            {
                "Pollutant": pol,
                "Zone": row["Zone"],
                "Period": row["Period"].replace("\n", " "),
                "Mean": round(row["Mean"], 4) if not np.isnan(row["Mean"]) else np.nan,
                "PctChange_vs_Baseline": (
                    round(row["PctChange"], 2)
                    if not np.isnan(row["PctChange"])
                    else np.nan
                ),
            }
        )

summary_df = pd.DataFrame(summary_all)
summary_df.to_csv(PROCESSED_DIR / "covid_lockdown_analysis.csv", index=False)
print(f"\nSaved COVID summary to {PROCESSED_DIR / 'covid_lockdown_analysis.csv'}")
print("\nLockdown period (Mar–Jun 2020) mean NO2 change vs. baseline:")
lockdown_no2 = summary_df[
    (summary_df["Pollutant"] == "NO2")
    & (summary_df["Period"].str.contains("Lockdown\(Mar"))
]
print(lockdown_no2[["Zone", "Mean", "PctChange_vs_Baseline"]].to_string(index=False))
