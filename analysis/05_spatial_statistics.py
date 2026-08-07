"""
Script 05: Spatial Statistics (Layer 5)

Performs Global and Local Moran's I, and Getis-Ord Gi* hotspot analysis.
Note: Requires raster to vector conversion of the pollutant maps, or processing
at the district/municipality level. This script simulates the analytical workflow.
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import warnings

# Try importing spatial stats libraries
try:
    import libpysal
    from esda.moran import Moran, Moran_Local
    from esda.getisord import G_Local
    from splot.esda import moran_scatterplot, lisa_cluster, plot_local_autocorrelation
    import matplotlib.pyplot as plt

    HAS_PYSAL = True
except ImportError:
    HAS_PYSAL = False
    print("[WARNING] Spatial statistics packages (libpysal, esda, splot) not found.")
    print("Run: pip install libpysal esda splot")

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.spatial_utils import build_spatial_weights


def run_spatial_stats():
    """Run spatial statistics."""
    print("Running Spatial Statistics...")

    if not HAS_PYSAL:
        print("Cannot run spatial stats without PySAL stack. Exiting layer.")
        return

    spatial_out = FIGURES_DIR / "spatial_stats"
    spatial_out.mkdir(exist_ok=True)

    # ---------------------------------------------------------
    # Note: In a full pipeline, you would load the district-level
    # aggregated data or a grid (vectorized pixels) to run these tests.
    # The current CSVs are aggregated at the physiographic zone level,
    # which has only 5 polygons (too few for Moran's I).
    #
    # This script provides the template for when you aggregate by
    # district (77 polygons) or a custom grid (e.g., 10x10km).
    # ---------------------------------------------------------

    print("""
    [INFO] Spatial statistics (Moran's I, Getis-Ord Gi*) require vector 
    features with sufficient neighbors. This script assumes district-level 
    or grid-level data exported from GEE.
    """)

    # 1. Load spatial polygons (e.g., Districts)
    # Note: Replace with actual path to Nepal districts shapefile when available
    shapefile_path = RAW_DIR / "shapefiles" / "nepal_districts.shp"
    
    if not shapefile_path.exists():
        print(f"[WARNING] Shapefile not found at {shapefile_path}. Skipping spatial stats execution.")
        print("Please ensure the shapefile and district-level CSVs are present.")
        return

    districts = gpd.read_file(shapefile_path)
    
    # 2. Build Spatial Weights
    w = build_spatial_weights(districts, weights_type='queen')
    
    for pol in POLLUTANTS.keys():
        # Load pollutant data aggregated by district (assumes this is exported from GEE)
        csv_path = PROCESSED_DIR / f"{pol}_district_ts.csv"
        
        if not csv_path.exists():
            print(f"  -> Skipping {pol}, district data not found.")
            continue
            
        print(f"  -> Running Spatial Stats for {pol}")
        df = pd.read_csv(csv_path)
        
        # Merge with geometry
        # Assumes a common key like 'DISTRICT' or 'ADM2_NAME'
        merge_col = 'DISTRICT' if 'DISTRICT' in df.columns else df.columns[0]
        gdf = districts.merge(df, left_on='DISTRICT', right_on=merge_col)
        
        mean_col = f'{pol}_mean'
        if mean_col not in gdf.columns:
            continue
            
        y = gdf[mean_col].values
        
        # Calculate Global Moran's I
        mi = Moran(y, w)
        print(f"    Global Moran's I: {mi.I:.3f} (p={mi.p_sim:.3f})")
        
        # Calculate Local Moran's I (LISA)
        lisa = Moran_Local(y, w)
        
        # Calculate Getis-Ord Gi* (Hotspot Analysis)
        go = G_Local(y, w, star=True)
        
        # Add results to GeoDataFrame
        gdf['lisa_I'] = lisa.Is
        gdf['lisa_q'] = lisa.q
        gdf['lisa_p'] = lisa.p_sim
        gdf['gi_star'] = go.Gs
        gdf['gi_p'] = go.p_sim
        
        # Save results
        gdf.drop(columns='geometry').to_csv(spatial_out / f"{pol}_spatial_stats_results.csv", index=False)
        
        # Plotting (using splot)
        fig, ax = plt.subplots(figsize=(10, 8))
        lisa_cluster(lisa, gdf, p=0.05, ax=ax)
        ax.set_title(f"Local Moran's I (LISA) Cluster Map - {pol}")
        plt.savefig(spatial_out / f"{pol}_LISA_Cluster.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        # Plot Getis-Ord Gi*
        fig, ax = plt.subplots(figsize=(10, 8))
        # Significance filter
        sig = gdf['gi_p'] < 0.05
        hotspots = gdf[sig & (gdf['gi_star'] > 0)]
        coldspots = gdf[sig & (gdf['gi_star'] < 0)]
        
        gdf.plot(color='lightgrey', edgecolor='white', ax=ax)
        hotspots.plot(color='red', ax=ax, label='Hot Spot (95%)')
        coldspots.plot(color='blue', ax=ax, label='Cold Spot (95%)')
        ax.set_title(f"Getis-Ord Gi* Hotspot Analysis - {pol}")
        plt.savefig(spatial_out / f"{pol}_Getis_Ord_Hotspots.png", dpi=300, bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    run_spatial_stats()
