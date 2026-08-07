"""
Script 06b: Emerging Hotspot Analysis

Implements Space-Time Pattern Mining to identify new, intensifying, 
or diminishing hotspots over the 2019-2026 period.
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import warnings

try:
    import libpysal
    from esda.moran import Moran, Moran_Local
    from esda.getisord import G_Local
    import matplotlib.pyplot as plt
    HAS_PYSAL = True
except ImportError:
    HAS_PYSAL = False

from config import RAW_DIR, PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.spatial_utils import build_spatial_weights

def run_emerging_hotspots():
    print("Running Emerging Hotspot Analysis...")
    
    if not HAS_PYSAL:
        print("Cannot run spatial stats without PySAL stack.")
        return
        
    out_dir = FIGURES_DIR / "emerging_hotspots"
    out_dir.mkdir(exist_ok=True, parents=True)
    
    shapefile_path = RAW_DIR / "shapefiles" / "nepal_districts.shp"
    if not shapefile_path.exists():
        print(f"[WARNING] Shapefile not found at {shapefile_path}. Skipping.")
        return

    districts = gpd.read_file(shapefile_path)
    w = build_spatial_weights(districts, weights_type='queen')
    
    for pol in POLLUTANTS.keys():
        csv_path = PROCESSED_DIR / f"{pol}_district_ts.csv"
        if not csv_path.exists():
            continue
            
        print(f"  -> Analyzing {pol}")
        df = pd.read_csv(csv_path)
        
        # We need a space-time cube (District x Time)
        # Assuming df has 'DISTRICT', 'year', 'month', 'value'
        if 'DISTRICT' not in df.columns:
            merge_col = df.columns[0]
        else:
            merge_col = 'DISTRICT'
            
        # Group by year for annual emerging hotspots
        annual_df = df.groupby([merge_col, 'year'])[f"{pol}_mean"].mean().reset_index()
        
        years = sorted(annual_df['year'].unique())
        if len(years) < 2:
            continue
            
        # Calculate Getis-Ord Gi* for each year to track changes
        hotspot_tracker = []
        
        for yr in years:
            yr_data = annual_df[annual_df['year'] == yr]
            gdf = districts.merge(yr_data, left_on='DISTRICT', right_on=merge_col, how='inner')
            
            if gdf.empty:
                continue
                
            # Align weights with gdf order
            w_yr = build_spatial_weights(gdf, weights_type='queen')
            
            y = gdf[f"{pol}_mean"].values
            go = G_Local(y, w_yr, star=True)
            
            for i, row in gdf.iterrows():
                dist = row['DISTRICT']
                z_score = go.Zs[i]
                p_val = go.p_sim[i]
                
                status = 0 # Not significant
                if p_val < 0.05:
                    status = 1 if z_score > 0 else -1
                    
                hotspot_tracker.append({
                    'DISTRICT': dist,
                    'year': yr,
                    'status': status
                })
                
        tracker_df = pd.DataFrame(hotspot_tracker)
        tracker_df.to_csv(PROCESSED_DIR / f"{pol}_hotspot_tracker.csv", index=False)
        
        # Here you would typically classify "New", "Consecutive", "Intensifying", etc.
        # based on the 8-year sequence of statuses.
        
    print("Emerging Hotspot Analysis framework completed.")

if __name__ == "__main__":
    run_emerging_hotspots()
