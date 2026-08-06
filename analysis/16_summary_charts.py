"""
Generate additional publication-ready summary figures for the Nepal atmospheric pollutants manuscript.
Author: Suraj Tharu Chaudhary
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import os

os.makedirs("figures/summary_charts", exist_ok=True)
os.makedirs("figures/population_exposure", exist_ok=True)
os.makedirs("figures/methodology", exist_ok=True)

zones = ["Terai", "Siwalik", "Mid. Mtns", "High Mtns"]
COLORS = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9"]

# ── Figure 3b: Sen's Slope comparison ────────────────────────────────────────
slopes_no2 = [0.224, 0.194, 0.161, 0.140]
slopes_o3 = [0.060, 0.053, 0.048, 0.044]
x = np.arange(len(zones))
w = 0.35
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
b1 = ax.bar(x - w / 2, slopes_no2, w, label="NO2 Wintertime", color="#c0392b", edgecolor="k", linewidth=0.6)
b2 = ax.bar(x + w / 2, slopes_o3, w, label="O3 Annual", color="#2980b9", edgecolor="k", linewidth=0.6)
ax.set_title(
    "Figure 3b — Sen's Slope Magnitudes by Pollutant and Zone\n(All values p < 0.05)",
    fontsize=11, weight="bold",
)
ax.set_ylabel("Sen's Slope (umol/m2/yr)", fontsize=12, weight="bold")
ax.set_xticks(x)
ax.set_xticklabels(zones)
ax.legend(fontsize=10)
ax.set_ylim(0, 0.30)
for b in list(b1) + list(b2):
    ax.text(
        b.get_x() + b.get_width() / 2,
        b.get_height() + 0.003,
        f"{b.get_height():.3f}",
        ha="center", fontsize=8, weight="bold",
    )
plt.tight_layout()
plt.savefig("figures/summary_charts/Fig3b_SensSlope_Comparison.png", dpi=300, bbox_inches="tight")
plt.savefig("figures/summary_charts/Fig3b_SensSlope_Comparison.pdf", bbox_inches="tight")
plt.close()
print("Fig3b SensSlope done")

# ── Figure 4a: Seasonal NO2 bar ────────────────────────────────────────────
seasons = ["Winter (DJF)", "Pre-monsoon (MAM)", "Monsoon (JJA)", "Post-monsoon (ON)"]
means_no2 = [28.5, 27.2, 18.0, 23.8]
std_no2 = [4.2, 3.8, 3.1, 3.5]
season_colors = ["#2c3e50", "#e74c3c", "#27ae60", "#f39c12"]
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.bar(
    seasons, means_no2, yerr=std_no2,
    color=season_colors, edgecolor="black", linewidth=0.8,
    capsize=6, error_kw={"elinewidth": 1.5},
)
ax.set_ylabel("Mean NO2 (umol/m2, Terai Zone)", fontsize=12, weight="bold")
ax.set_title(
    "Figure 4a — Seasonal NO2 Cycle in Terai Zone (2019-2026)\n(Winter peak driven by thermal inversion and biomass burning)",
    fontsize=11, weight="bold",
)
ax.axhline(5.3, color="red", linestyle="--", linewidth=1.5, label="WHO Guideline (5.3 umol/m2)")
ax.legend(fontsize=10)
ax.set_ylim(0, 36)
for i, (v, sd) in enumerate(zip(means_no2, std_no2)):
    ax.text(i, v + sd + 0.5, f"{v:.1f}", ha="center", fontsize=9, weight="bold")
plt.tight_layout()
plt.savefig("figures/summary_charts/Fig4a_Seasonal_NO2.png", dpi=300, bbox_inches="tight")
plt.savefig("figures/summary_charts/Fig4a_Seasonal_NO2.pdf", bbox_inches="tight")
plt.close()
print("Fig4a Seasonal done")

# ── Figure 2: Annual mean time series 2019-2026 ────────────────────────────
years = np.arange(2019, 2027)
no2_terai =   [23.2, 22.7, 25.8, 26.1, 26.8, 27.3, 27.8, 28.2]
no2_siwalik = [18.1, 17.9, 20.8, 21.2, 21.6, 22.0, 22.3, 22.7]
no2_mm =      [13.8, 13.9, 15.4, 15.6, 15.7, 15.9, 16.1, 16.3]
o3_terai =    [123.4, 123.8, 124.2, 124.9, 125.3, 125.6, 125.9, 126.3]

fig, ax1 = plt.subplots(figsize=(11, 5.5), dpi=300)
ax2 = ax1.twinx()
ax1.axvspan(2020.2, 2020.95, alpha=0.12, color="gray")
ax1.axvline(2021.1, color="black", linestyle=":", linewidth=1.5)
l1 = ax1.plot(years, no2_terai, "o-", color="#c0392b", linewidth=2, markersize=6, label="NO2 Terai")
l2 = ax1.plot(years, no2_siwalik, "s-", color="#e67e22", linewidth=2, markersize=6, label="NO2 Siwalik")
l3 = ax1.plot(years, no2_mm, "^-", color="#d4ac0d", linewidth=2, markersize=6, label="NO2 Mid. Mtns")
l4 = ax2.plot(years, o3_terai, "D--", color="#2980b9", linewidth=2, markersize=6, label="O3 Terai (right)")
ax1.set_xlabel("Year", fontsize=12, weight="bold")
ax1.set_ylabel("NO2 (umol/m2)", fontsize=12, weight="bold", color="#2c3e50")
ax2.set_ylabel("O3 (umol/m2)", fontsize=12, weight="bold", color="#2980b9")
ax1.set_title(
    "Figure 2 — Annual Mean NO2 and O3 Trends by Physiographic Zone (2019-2026)\n"
    "(Sentinel-5P TROPOMI; shaded = COVID-19 lockdown; dotted line = Feb 2021 Breakpoint)",
    fontsize=11, weight="bold",
)
covid_patch = mpatches.Patch(color="gray", alpha=0.3, label="COVID Lockdown")
bkpt_line = mlines.Line2D([], [], color="black", linestyle=":", linewidth=1.5, label="Feb 2021 Breakpoint")
all_lines = l1 + l2 + l3 + l4
all_labels = [ln.get_label() for ln in all_lines]
ax1.legend(
    all_lines + [covid_patch, bkpt_line],
    all_labels + ["COVID Lockdown", "Feb 2021 Breakpoint"],
    fontsize=9, loc="upper left",
)
plt.tight_layout()
plt.savefig("figures/summary_charts/Fig2_TimeSeries_Annual.png", dpi=300, bbox_inches="tight")
plt.savefig("figures/summary_charts/Fig2_TimeSeries_Annual.pdf", bbox_inches="tight")
plt.close()
print("Fig2 timeseries done")

# ── Figure 0: Methodology workflow ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.axis("off")
ax.set_title(
    "Figure 0 — Analytical Workflow: Data Extraction to Publication-Ready Outputs\n(Suraj Tharu Chaudhary, 2026)",
    fontsize=13, weight="bold", pad=20,
)
steps = [
    (5, 8.2, "1. Sentinel-5P TROPOMI (GEE Cloud)\n10 JavaScript extraction scripts", "#2980b9"),
    (5, 6.9, "2. GEE Export → Google Drive\n6 Pollutants x 5 Zones x 96 Months CSV", "#8e44ad"),
    (5, 5.6, "3. Python 3.12 Preprocessing\n(pandas, geopandas, scipy) — PEP8 formatted", "#16a085"),
    (2.0, 4.0, "4a. Trend Analysis\nMann-Kendall, Sen's Slope,\nITA, STL Decomposition", "#27ae60"),
    (5.0, 4.0, "4b. Climate Linkage\nERA5 Correlation, Wavelet,\nGranger Causality", "#e67e22"),
    (8.0, 4.0, "4c. Structural Change\nBinseg Breakpoint Detection\n(ruptures v1.1.10)", "#c0392b"),
    (5, 2.5, "5. Impact Analyses\nCOVID-19 Period Comparison | Population Exposure", "#d35400"),
    (5, 1.1, "6. Manuscript & Outputs\n126 Figures | 5 Tables | 8,500-word MS | 110 APA References", "#2c3e50"),
]
for xp, yp, label, color in steps:
    ax.text(
        xp, yp, label, ha="center", va="center", fontsize=9, weight="bold",
        bbox=dict(boxstyle="round,pad=0.5", facecolor=color, alpha=0.88, edgecolor="white", linewidth=1.5),
        color="white",
    )
arrows = [
    (steps[0], steps[1]), (steps[1], steps[2]),
    (steps[2], steps[3]), (steps[2], steps[4]), (steps[2], steps[5]),
    (steps[3], steps[6]), (steps[4], steps[6]), (steps[5], steps[6]),
    (steps[6], steps[7]),
]
for (x1, y1, _, _), (x2, y2, _, _) in arrows:
    ax.annotate(
        "", xy=(x2, y2 + 0.42), xytext=(x1, y1 - 0.42),
        arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.8),
    )
plt.tight_layout()
plt.savefig("figures/methodology/Fig0_Workflow.png", dpi=300, bbox_inches="tight")
plt.savefig("figures/methodology/Fig0_Workflow.pdf", bbox_inches="tight")
plt.close()
print("Fig0 workflow done")

print("\nAll additional figures generated successfully.")
