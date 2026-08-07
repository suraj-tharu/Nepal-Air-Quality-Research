"""
Script 04b: Seasonality and Climatology Analysis

Calculates seasonal anomalies, monthly climatologies, and seasonal indices
from the extracted time series data.

Seasons in Nepal:
- Winter (Dec, Jan, Feb)
- Pre-monsoon (Mar, Apr, May)
- Monsoon (Jun, Jul, Aug, Sep)
- Post-monsoon (Oct, Nov)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import save_figure

def get_season(month):
    if month in [12, 1, 2]: return 'Winter'
    elif month in [3, 4, 5]: return 'Pre-monsoon'
    elif month in [6, 7, 8, 9]: return 'Monsoon'
    elif month in [10, 11]: return 'Post-monsoon'
    return 'Unknown'

def run_seasonality_analysis():
    print("Running Seasonality and Climatology Analysis...")
    out_dir = FIGURES_DIR / "seasonality"
    out_dir.mkdir(exist_ok=True, parents=True)

    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if not file_path.exists():
            continue

        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(file_path)
        
        # Ensure we have month and year
        if 'date' in df.columns and 'month' not in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            df['year'] = df['date'].dt.year
            
        df['season_explicit'] = df['month'].apply(get_season)
        
        mean_col = f"{pol}_mean"
        
        # 1. Monthly Climatology (Long-term average for each month)
        climatology = df.groupby(['zone', 'month'])[mean_col].mean().reset_index()
        climatology = climatology.rename(columns={mean_col: 'climatology_mean'})
        
        # Merge back to calculate anomalies
        df = df.merge(climatology, on=['zone', 'month'], how='left')
        df['anomaly'] = df[mean_col] - df['climatology_mean']
        df['anomaly_percent'] = (df['anomaly'] / df['climatology_mean']) * 100
        
        # 2. Seasonal Index (ratio of monthly to annual average)
        annual_avg = df.groupby(['zone', 'year'])[mean_col].mean().reset_index()
        annual_avg = annual_avg.rename(columns={mean_col: 'annual_mean'})
        df = df.merge(annual_avg, on=['zone', 'year'], how='left')
        df['seasonal_index'] = df[mean_col] / df['annual_mean']
        
        # Plot Monthly Climatology
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='month', y=mean_col, hue='zone', marker='o', ax=ax)
        ax.set_title(f"{pol} Monthly Climatology (2019-2026)")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
        ax.set_ylabel(f"Concentration")
        save_figure(fig, out_dir / f"climatology_{pol}")
        
        # Plot Seasonal Anomalies over time
        for zone in df['zone'].unique():
            zone_data = df[df['zone'] == zone].sort_values(['year', 'month'])
            # Create a string for x-axis
            x_labels = zone_data['year'].astype(str) + "-" + zone_data['month'].astype(str).str.zfill(2)
            
            fig, ax = plt.subplots(figsize=(12, 4))
            colors = ['red' if x > 0 else 'blue' for x in zone_data['anomaly']]
            ax.bar(x_labels, zone_data['anomaly'], color=colors)
            ax.set_title(f"{pol} Monthly Anomaly - {zone}")
            ax.set_xticks(range(0, len(x_labels), 6)) # Show every 6th tick
            ax.set_ylabel("Anomaly")
            plt.xticks(rotation=45)
            fig.tight_layout()
            save_figure(fig, out_dir / f"anomaly_{pol}_{zone}")
            
        # Save extended dataframe
        df.to_csv(PROCESSED_DIR / f"{pol}_seasonality_metrics.csv", index=False)
        
    print("Seasonality Analysis completed.")

if __name__ == "__main__":
    run_seasonality_analysis()
