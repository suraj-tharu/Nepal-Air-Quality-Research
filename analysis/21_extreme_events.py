"""
Script 21: Extreme Events Analysis

Expands upon the COVID-19 lockdown analysis to also examine:
1. Forest fire years (e.g., April 2021) using UVAI and CO.
2. Major dust events (transboundary transport) using UVAI and PM2.5/AOD.
3. Crop residue burning (post-monsoon) in the Terai using NO2 and CO.
4. Winter temperature inversions in the Kathmandu valley.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import save_figure

def run_extreme_events_analysis():
    print("Running Extreme Events Analysis...")
    out_dir = FIGURES_DIR / "extreme_events"
    out_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Forest Fire Analysis (April 2021 was a severe fire month in Nepal)
    print("  -> Analyzing Forest Fire Events (April 2021 vs Baseline)")
    
    # Load CO and UVAI
    co_path = PROCESSED_DIR / "CO_zonal_ts.csv"
    uvai_path = PROCESSED_DIR / "UVAI_zonal_ts.csv"
    
    if co_path.exists() and uvai_path.exists():
        co_df = pd.read_csv(co_path)
        uvai_df = pd.read_csv(uvai_path)
        
        # Merge
        fire_df = pd.merge(co_df, uvai_df, on=['date', 'zone', 'year', 'month'])
        fire_df['date'] = pd.to_datetime(fire_df['date'])
        
        # Baseline = April average for 2019, 2020, 2022, 2023
        aprils = fire_df[fire_df['month'] == 4]
        baseline = aprils[aprils['year'] != 2021].groupby('zone')[['CO_mean', 'UVAI_mean']].mean()
        event_2021 = aprils[aprils['year'] == 2021].groupby('zone')[['CO_mean', 'UVAI_mean']].mean()
        
        # Calculate % increase
        increase = ((event_2021 - baseline) / baseline) * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        increase['CO_mean'].plot(kind='bar', color='darkorange', ax=ax)
        ax.set_title("CO % Increase during April 2021 Forest Fires vs Baseline")
        ax.set_ylabel("% Increase")
        ax.set_xlabel("Physiographic Zone")
        plt.xticks(rotation=45)
        fig.tight_layout()
        save_figure(fig, out_dir / "Forest_Fire_CO_Increase")
        
    # 2. Crop Residue Burning (Terai, Post-Monsoon: Oct-Nov)
    print("  -> Analyzing Crop Residue Burning (Terai, Oct-Nov)")
    no2_path = PROCESSED_DIR / "NO2_zonal_ts.csv"
    if no2_path.exists():
        no2_df = pd.read_csv(no2_path)
        no2_terai = no2_df[no2_df['zone'] == 'Terai']
        
        if not no2_terai.empty:
            no2_terai['season'] = no2_terai['month'].apply(
                lambda x: 'Post-monsoon (Burning)' if x in [10, 11] else 'Other'
            )
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(data=no2_terai, x='season', y='NO2_mean',
                        hue='season', palette='Set2', legend=False, ax=ax)
            ax.set_title("Terai NO2 Concentrations: Post-Monsoon Burning vs Other Seasons")
            fig.tight_layout()
            save_figure(fig, out_dir / "Crop_Residue_Burning_NO2")
            
    # 3. Winter Temperature Inversions (Middle Mountains / Kathmandu Valley proxy)
    print("  -> Analyzing Winter Temperature Inversions")
    if no2_path.exists():
        no2_mm = no2_df[no2_df['zone'] == 'Middle_Mountains'].copy()
        
        if not no2_mm.empty:
            no2_mm['season'] = no2_mm['month'].apply(
                lambda x: 'Winter (Inversion)' if x in [12, 1, 2] else 'Other'
            )
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.violinplot(data=no2_mm, x='season', y='NO2_mean',
                           hue='season', palette='coolwarm', legend=False, ax=ax)
            ax.set_title("Middle Mountains NO2: Winter Inversions")
            fig.tight_layout()
            save_figure(fig, out_dir / "Winter_Inversion_NO2_MM")
            
    print("Extreme Events Analysis completed.")

if __name__ == "__main__":
    run_extreme_events_analysis()
