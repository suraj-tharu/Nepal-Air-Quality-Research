"""
Script 30: Publication Figures Generator

Generates high-quality, publication-ready figures for the manuscript and thesis.
Focuses on advanced visualization techniques: Ridge plots, Radar charts, Sankey diagrams.

Ensure output is 300 DPI, uses colorblind-friendly palettes (viridis, cividis),
and follows standard journal formatting (e.g., Nature, Elsevier, Science).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

try:
    import joypy
    HAS_JOYPY = True
except ImportError:
    HAS_JOYPY = False
    print("[WARNING] joypy not installed. Ridge plots will be skipped.")
    print("Run: pip install joypy")

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import save_figure

# Set global publication styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def create_ridge_plots(out_dir):
    """Creates Ridge Plots showing pollutant distribution across altitudinal zones.
    Uses pure matplotlib KDE (joypy has a bug with matplotlib >=3.9 returning a generator).
    """
    from scipy.stats import gaussian_kde

    print("  -> Generating Ridge Plots (KDE-based)...")
    zone_order = ['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(zone_order)))

    for pol in POLLUTANTS.keys():
        pol_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not pol_path.exists():
            continue

        df = pd.read_csv(pol_path)
        mean_col = f"{pol}_mean"
        df = df[['zone', mean_col]].dropna()
        if df.empty:
            continue

        n_zones = len(zone_order)
        fig, axes = plt.subplots(n_zones, 1, figsize=(10, 7), sharex=True)
        fig.suptitle(f"{pol} Altitudinal Gradient (2019–2026)", fontsize=14, fontweight='bold', y=1.01)

        for i, (zone, color) in enumerate(zip(zone_order, colors)):
            ax = axes[i]
            data = df[df['zone'] == zone][mean_col].dropna().values
            if len(data) < 5:
                ax.set_visible(False)
                continue

            kde = gaussian_kde(data, bw_method=0.4)
            x_range = np.linspace(data.min() * 0.9, data.max() * 1.1, 300)
            y_kde = kde(x_range)

            ax.fill_between(x_range, y_kde, alpha=0.7, color=color)
            ax.plot(x_range, y_kde, color=color, lw=1.5)
            ax.axvline(np.mean(data), color='white', lw=1.5, linestyle='--', alpha=0.9)
            ax.set_ylabel(zone.replace('_', '\n'), fontsize=8, rotation=0, ha='right', va='center')
            ax.yaxis.set_visible(False)
            ax.spines[['top', 'right', 'left']].set_visible(False)
            if i < n_zones - 1:
                ax.spines['bottom'].set_visible(False)
                ax.tick_params(bottom=False)

        axes[-1].set_xlabel(f"{pol} Concentration", fontsize=10)
        fig.tight_layout()
        save_figure(fig, out_dir / f"RidgePlot_{pol}")

def create_radar_charts(out_dir):
    """Creates Radar Charts showing seasonal profiles per physiographic zone."""
    print("  -> Generating Radar Charts...")
    
    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_seasonality_metrics.csv"
        if not file_path.exists():
            # Fallback if seasonality wasn't run
            continue
            
        df = pd.read_csv(file_path)
        if 'season_explicit' not in df.columns:
            continue
            
        seasonal_means = df.groupby(['zone', 'season_explicit'])[f"{pol}_mean"].mean().unstack()
        
        if seasonal_means.empty:
            continue
            
        categories = list(seasonal_means.columns)
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        colors = plt.cm.tab10.colors
        
        for i, (zone, row) in enumerate(seasonal_means.iterrows()):
            values = row.values.tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=2, linestyle='solid', label=zone, color=colors[i])
            ax.fill(angles, values, color=colors[i], alpha=0.1)
            
        plt.xticks(angles[:-1], categories)
        ax.set_rlabel_position(0)
        plt.title(f"Seasonal {pol} Profiles across Zones", size=15, y=1.1)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        save_figure(fig, out_dir / f"RadarChart_{pol}")

def generate_publication_figures():
    print("Generating Publication-Ready Figures...")
    out_dir = FIGURES_DIR / "publication_ready"
    out_dir.mkdir(exist_ok=True, parents=True)
    
    # Run specific high-end visualization functions
    create_ridge_plots(out_dir)
    create_radar_charts(out_dir)
    
    print("Publication Figures generated. Review 'figures/publication_ready/'.")

if __name__ == "__main__":
    generate_publication_figures()
