"""
Publication-quality plotting utilities for Nepal atmospheric pollutants analysis.

All figures follow journal requirements:
- 300 DPI minimum
- Arial font family
- Consistent color schemes per pollutant
- Proper axis labels with units
"""

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Try to import cartopy for map plotting
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    HAS_CARTOPY = True
except ImportError:
    HAS_CARTOPY = False
    print("[WARNING] cartopy not installed. Map plots will use basic matplotlib.")


# =============================================================================
# GLOBAL STYLE SETTINGS
# =============================================================================
def set_publication_style():
    """Set matplotlib rcParams for publication-quality figures."""
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.1,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "lines.linewidth": 1.5,
            "axes.grid": False,
            "figure.facecolor": "white",
        }
    )


# Call on module import
set_publication_style()

# =============================================================================
# COLOR PALETTES
# =============================================================================
POLLUTANT_COLORS = {
    "NO2": "#E53935",
    "SO2": "#8E24AA",
    "CO": "#FF6F00",
    "O3": "#1565C0",
    "HCHO": "#2E7D32",
    "UVAI": "#D84315",
}

ZONE_COLORS = {
    "Terai": "#2E7D32",
    "Siwalik": "#66BB6A",
    "Middle_Mountains": "#FDD835",
    "High_Mountains": "#FF8F00",
    "High_Himal": "#BDBDBD",
}

SEASON_COLORS = {
    "Pre-monsoon": "#FF6B35",
    "Monsoon": "#1E88E5",
    "Post-monsoon": "#43A047",
    "Winter": "#8E24AA",
}

# Significance level markers
SIG_MARKERS = {
    0.01: "***",
    0.05: "**",
    0.10: "*",
    1.00: "ns",
}


def save_figure(fig, filepath, formats=None):
    """
    Save figure in multiple formats for journal submission.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    filepath : str or Path
        Base filepath (without extension).
    formats : list
        List of formats to save (default: ['png', 'pdf']).
    """
    filepath = Path(filepath)
    formats = formats or ["png", "pdf"]

    filepath.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        fig.savefig(
            filepath.with_suffix(f".{fmt}"),
            format=fmt,
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(fig)
    print(f"  -> Saved: {filepath.stem} ({', '.join(formats)})")


# =============================================================================
# TIME SERIES PLOTS
# =============================================================================
def plot_monthly_timeseries(
    df, pollutant, zones=None, events=None, title=None, save_path=None
):
    """
    Plot monthly time series of a pollutant by physiographic zone.

    Parameters
    ----------
    df : pd.DataFrame
        Must have columns: 'date', 'zone', '{pollutant}_mean'
    pollutant : str
        Pollutant name (e.g., 'NO2')
    zones : list, optional
        Zones to plot. Default: all.
    events : dict, optional
        {date_str: label} for annotation lines.
    title : str, optional
    save_path : str or Path, optional
    """
    fig, ax = plt.subplots(figsize=(12, 5))

    col = f"{pollutant}_mean"
    zones = zones or df["zone"].unique()

    for zone in zones:
        zone_data = df[df["zone"] == zone].sort_values("date")
        color = ZONE_COLORS.get(zone, "#333333")
        ax.plot(
            zone_data["date"],
            zone_data[col],
            label=zone.replace("_", " "),
            color=color,
            alpha=0.85,
        )

    # Add event annotations
    if events:
        for date_str, label in events.items():
            event_date = pd.to_datetime(date_str)
            ax.axvline(
                event_date, color="gray", linestyle="--", alpha=0.6, linewidth=0.8
            )
            ax.text(
                event_date,
                ax.get_ylim()[1] * 0.95,
                label,
                rotation=90,
                fontsize=7,
                va="top",
                ha="right",
                color="gray",
            )

    ax.set_xlabel("Date")
    ax.set_ylabel(f"{pollutant} Concentration")
    ax.set_title(title or f"Monthly {pollutant} by Physiographic Zone")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xticks(rotation=45)

    fig.tight_layout()

    if save_path:
        save_figure(fig, save_path)
    return fig, ax


def plot_seasonal_boxplot(df, pollutant, group_by="season", title=None, save_path=None):
    """
    Create seasonal boxplot comparison across zones.

    Parameters
    ----------
    df : pd.DataFrame
        Must have 'season', 'zone', '{pollutant}_mean' columns.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    col = f"{pollutant}_mean"
    season_order = ["Pre-monsoon", "Monsoon", "Post-monsoon", "Winter"]

    if group_by == "season":
        sns.boxplot(
            data=df,
            x="season",
            y=col,
            hue="zone",
            order=season_order,
            palette=ZONE_COLORS,
            ax=ax,
            linewidth=0.8,
            fliersize=3,
        )
    else:
        sns.boxplot(
            data=df,
            x="zone",
            y=col,
            hue="season",
            order=list(ZONE_COLORS.keys()),
            palette=SEASON_COLORS,
            ax=ax,
            linewidth=0.8,
            fliersize=3,
        )

    ax.set_xlabel(group_by.capitalize())
    ax.set_ylabel(f"{pollutant} Concentration")
    ax.set_title(title or f"Seasonal {pollutant} Distribution")
    ax.legend(title=group_by.capitalize(), loc="upper right")

    fig.tight_layout()
    if save_path:
        save_figure(fig, save_path)
    return fig, ax


# =============================================================================
# TREND ANALYSIS PLOTS
# =============================================================================
def plot_trend_significance(trend_results, pollutant, title=None, save_path=None):
    """
    Create a heatmap of Mann-Kendall trend significance by zone and season.

    Parameters
    ----------
    trend_results : pd.DataFrame
        Columns: zone, season, trend (increasing/decreasing/no trend),
        p_value, slope
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Heatmap of Theil-Sen slopes
    slope_pivot = trend_results.pivot_table(
        values="slope", index="zone", columns="season"
    )
    season_order = ["Pre-monsoon", "Monsoon", "Post-monsoon", "Winter"]
    slope_pivot = slope_pivot.reindex(columns=season_order)

    sns.heatmap(
        slope_pivot,
        annot=True,
        fmt=".2e",
        cmap="RdYlGn_r",
        center=0,
        ax=axes[0],
        cbar_kws={"label": "Theil-Sen Slope"},
    )
    axes[0].set_title(f"{pollutant} Trend Slope (per year)")
    axes[0].set_ylabel("Physiographic Zone")

    # Heatmap of p-values
    pval_pivot = trend_results.pivot_table(
        values="p_value", index="zone", columns="season"
    )
    pval_pivot = pval_pivot.reindex(columns=season_order)

    # Custom annotation with significance stars
    annot_matrix = pval_pivot.map(
        lambda p: next((v for k, v in SIG_MARKERS.items() if p <= k), "ns")
    )

    sns.heatmap(
        pval_pivot,
        annot=annot_matrix,
        fmt="",
        cmap="RdYlGn",
        vmin=0,
        vmax=0.1,
        ax=axes[1],
        cbar_kws={"label": "p-value"},
    )
    axes[1].set_title(f"{pollutant} Trend Significance")
    axes[1].set_ylabel("Physiographic Zone")

    fig.suptitle(title or f"Mann-Kendall Trend Analysis: {pollutant}", y=1.02)
    fig.tight_layout()

    if save_path:
        save_figure(fig, save_path)
    return fig, axes


# =============================================================================
# CORRELATION PLOTS
# =============================================================================
def plot_correlation_heatmap(
    corr_matrix, title=None, save_path=None, mask_insignificant=True, p_matrix=None
):
    """
    Plot correlation heatmap between pollutants and climate variables.

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Correlation coefficients (pollutants × climate variables).
    p_matrix : pd.DataFrame, optional
        P-values for masking insignificant correlations.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    mask = None
    if mask_insignificant and p_matrix is not None:
        mask = p_matrix > 0.05

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        vmin=-1,
        vmax=1,
        mask=mask,
        ax=ax,
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Correlation Coefficient", "shrink": 0.8},
    )

    ax.set_title(title or "Pollutant–Climate Correlation Matrix")

    if mask_insignificant:
        ax.text(
            0.5,
            -0.05,
            "× = not significant (p > 0.05)",
            transform=ax.transAxes,
            ha="center",
            fontsize=8,
            color="gray",
        )

    fig.tight_layout()
    if save_path:
        save_figure(fig, save_path)
    return fig, ax


# =============================================================================
# STL DECOMPOSITION PLOTS
# =============================================================================
def plot_stl_decomposition(result, dates, pollutant, zone, save_path=None):
    """
    Plot STL decomposition results (observed, trend, seasonal, residual).

    Parameters
    ----------
    result : statsmodels STL result object
    dates : array-like
        Date index for x-axis.
    pollutant : str
    zone : str
    """
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    components = [
        ("Observed", result.observed, POLLUTANT_COLORS.get(pollutant, "#333")),
        ("Trend", result.trend, "#1565C0"),
        ("Seasonal", result.seasonal, "#2E7D32"),
        ("Residual", result.resid, "#757575"),
    ]

    for ax, (label, data, color) in zip(axes, components):
        ax.plot(dates, data, color=color, linewidth=1.2)
        ax.set_ylabel(label)
        ax.axhline(0, color="gray", linewidth=0.5, linestyle="-")

        if label == "Residual":
            ax.fill_between(dates, data, 0, alpha=0.3, color=color)

    axes[0].set_title(
        f'STL Decomposition: {pollutant} — {zone.replace("_", " ")}',
        fontsize=12,
        fontweight="bold",
    )
    axes[-1].set_xlabel("Date")
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    fig.tight_layout()
    if save_path:
        save_figure(fig, save_path)
    return fig, axes


# =============================================================================
# HOTSPOT CLASSIFICATION LEGEND
# =============================================================================
EHSA_COLORS = {
    "New": "#FF0000",
    "Consecutive": "#FF4500",
    "Intensifying": "#DC143C",
    "Persistent": "#8B0000",
    "Diminishing": "#FF8C00",
    "Sporadic": "#FFD700",
    "Oscillating": "#9370DB",
    "Historical": "#FFA07A",
    "No Pattern": "#D3D3D3",
    "New Cold Spot": "#0000FF",
    "Persistent Cold Spot": "#00008B",
    "Intensifying Cold Spot": "#4169E1",
}


def plot_multi_pollutant_panel(data_dict, zones, title=None, save_path=None):
    """
    Create a multi-panel figure showing all pollutants across zones.

    Parameters
    ----------
    data_dict : dict
        {pollutant: DataFrame} with 'date', 'zone', '{pollutant}_mean'
    zones : list
        Zones to include.
    """
    n_pollutants = len(data_dict)
    fig, axes = plt.subplots(
        n_pollutants, 1, figsize=(14, 3 * n_pollutants), sharex=True
    )

    if n_pollutants == 1:
        axes = [axes]

    for ax, (pollutant, df) in zip(axes, data_dict.items()):
        col = f"{pollutant}_mean"
        for zone in zones:
            zone_data = df[df["zone"] == zone].sort_values("date")
            ax.plot(
                zone_data["date"],
                zone_data[col],
                color=ZONE_COLORS.get(zone, "#333"),
                alpha=0.8,
                linewidth=1,
            )

        ax.set_ylabel(
            pollutant, fontweight="bold", color=POLLUTANT_COLORS.get(pollutant, "#333")
        )
        ax.tick_params(axis="y", labelcolor=POLLUTANT_COLORS.get(pollutant, "#333"))

    # Common legend
    legend_elements = [
        Line2D([0], [0], color=c, label=z.replace("_", " "))
        for z, c in ZONE_COLORS.items()
        if z in zones
    ]
    axes[0].legend(handles=legend_elements, loc="upper right", ncol=len(zones))

    axes[-1].set_xlabel("Date")
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.suptitle(
        title or "Multi-Pollutant Time Series by Physiographic Zone",
        y=1.01,
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout()

    if save_path:
        save_figure(fig, save_path)
    return fig, axes
