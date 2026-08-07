"""
Script 03b: Advanced Trend Analysis (Pixel-Level)

Performs pixel-wise Mann-Kendall Trend Test, Sen's Slope, and Theil-Sen Regression
on the spatial GeoTIFF stacks to generate trend maps.
"""

import pandas as pd
import numpy as np
import xarray as xr
import rioxarray
import pymannkendall as mk
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from config import RAW_DIR, PROCESSED_DIR, FIGURES_DIR, POLLUTANTS

def pixel_mann_kendall(x):
    """
    Apply Mann-Kendall to a 1D array (pixel time series).
    Returns [trend_slope, p_value]
    """
    if np.isnan(x).all() or len(x[~np.isnan(x)]) < 10:
        return np.array([np.nan, np.nan])
    
    try:
        # standard MK
        res = mk.original_test(x)
        return np.array([res.slope, res.p])
    except:
        return np.array([np.nan, np.nan])

def theil_sen_regression(x):
    """
    Apply Theil-Sen regression to a 1D array.
    """
    if np.isnan(x).all() or len(x[~np.isnan(x)]) < 10:
        return np.array([np.nan, np.nan])
    
    try:
        # Use scipy stats for Theil-Sen
        t = np.arange(len(x))
        mask = ~np.isnan(x)
        res = stats.mstats.theilslopes(x[mask], t[mask], 0.95)
        # res returns (slope, intercept, low_slope, high_slope)
        return np.array([res[0], res[1]])
    except:
        return np.array([np.nan, np.nan])

def run_advanced_trend_analysis():
    print("Running Advanced Pixel-Level Trend Analysis...")
    trend_out = PROCESSED_DIR / "spatial_trends"
    trend_out.mkdir(exist_ok=True, parents=True)

    # For each pollutant, we assume a stacked NetCDF or a folder of GeoTIFFs
    # Note: In a real run, you need to stack the monthly GeoTIFFs exported from GEE
    # Here we outline the pipeline using xarray
    
    for pol in POLLUTANTS.keys():
        print(f"  -> Processing {pol} pixel trends")
        
        # Placeholder for loading stacked rasters
        # Example: stack = xr.open_mfdataset(f'data/raw/Sentinel5P_{pol}/*.tif')
        # Since data isn't stacked locally yet, this is the functional framework:
        
        """
        # --- CODE TO UNCOMMENT WHEN GEOTIFFS ARE DOWNLOADED ---
        
        tif_files = sorted(list((RAW_DIR / f"{pol}_monthly").glob("*.tif")))
        if not tif_files:
            print(f"    [SKIP] No GeoTIFFs found for {pol}")
            continue
            
        time_index = pd.to_datetime([f.stem.split('_')[-1] for f in tif_files], format='%Y%m')
        
        # Load as a data array
        da = xr.concat([rioxarray.open_rasterio(f).squeeze() for f in tif_files], dim=pd.Index(time_index, name='time'))
        
        print(f"    Computing Mann-Kendall and Sen's slope for {pol}...")
        mk_res = xr.apply_ufunc(
            pixel_mann_kendall, 
            da, 
            input_core_dims=[['time']], 
            output_core_dims=[['mk_stats']],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[float],
            output_sizes={'mk_stats': 2}
        )
        
        slope_da = mk_res.isel(mk_stats=0).rename('sen_slope')
        p_val_da = mk_res.isel(mk_stats=1).rename('p_value')
        
        # Mask non-significant trends (p > 0.05)
        sig_slope = slope_da.where(p_val_da < 0.05)
        
        # Save to disk
        sig_slope.rio.to_raster(trend_out / f"{pol}_significant_trend_slope.tif")
        p_val_da.rio.to_raster(trend_out / f"{pol}_p_value.tif")
        """
        pass
        
    print("Advanced Trend Analysis scripts prepared.")

if __name__ == "__main__":
    run_advanced_trend_analysis()
