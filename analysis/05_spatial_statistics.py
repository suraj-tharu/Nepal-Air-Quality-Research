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
    features with sufficient neighbors (e.g., districts or grid cells).
    This script is a template designed to run on district-level data once
    exported from GEE.
    """)

    # Example workflow (commented out until district data is available):
    """
    # 1. Load District Polygons
    districts = gpd.read_file("path/to/nepal_districts.shp")
    
    # 2. Build Spatial Weights
    w = build_spatial_weights(districts, weights_type='queen')
    
    for pol in POLLUTANTS.keys():
        # Load pollutant data aggregated by district
        df = pd.read_csv(f"data/processed/{pol}_district_ts.csv")
        
        # Merge with geometry
        gdf = districts.merge(df, on='district_id')
        
        # Calculate Global Moran's I
        y = gdf[f'{pol}_mean'].values
        mi = Moran(y, w)
        print(f"Global Moran's I for {pol}: {mi.I:.3f} (p={mi.p_sim:.3f})")
        
        # Calculate Local Moran's I (LISA)
        lisa = Moran_Local(y, w)
        
        # Calculate Getis-Ord Gi*
        go = G_Local(y, w, star=True)
        
        # Plotting (using splot)
        fig, ax = plt.subplots(figsize=(10, 8))
        lisa_cluster(lisa, gdf, p=0.05, ax=ax)
        plt.savefig(spatial_out / f"{pol}_LISA_Cluster.png")
    """


if __name__ == "__main__":
    run_spatial_stats()
