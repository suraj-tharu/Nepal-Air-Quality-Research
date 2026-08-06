"""
Spatial utility functions for Nepal atmospheric pollutants analysis.

Handles loading boundaries, creating spatial grids, coordinate transformations,
and spatial weight matrix construction.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box, Point
from pathlib import Path
import warnings

# Suppress shapely deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def load_nepal_boundary(filepath=None):
    """
    Load Nepal country boundary as a GeoDataFrame.

    If no file provided, creates an approximate boundary from bounding box.
    For production use, supply a proper shapefile.

    Parameters
    ----------
    filepath : str or Path, optional
        Path to Nepal boundary shapefile/GeoJSON.

    Returns
    -------
    gpd.GeoDataFrame
        Nepal boundary polygon.
    """
    if filepath and Path(filepath).exists():
        gdf = gpd.read_file(filepath)
        return gdf

    # Approximate bounding box (use proper shapefile in production)
    print(
        "[WARNING] Using approximate Nepal boundary. "
        "Please provide a proper shapefile for actual analysis."
    )
    from shapely.geometry import Polygon

    # Simplified Nepal polygon (approximate)
    nepal_coords = [
        (80.06, 28.83),
        (80.09, 28.29),
        (80.48, 28.60),
        (81.11, 28.34),
        (81.63, 28.20),
        (82.10, 27.87),
        (83.29, 27.36),
        (84.09, 27.33),
        (85.01, 26.63),
        (85.82, 26.57),
        (86.95, 26.77),
        (87.23, 26.40),
        (88.06, 26.41),
        (88.17, 27.86),
        (87.99, 28.09),
        (86.98, 27.95),
        (85.72, 28.20),
        (84.23, 28.84),
        (83.90, 29.32),
        (82.99, 29.13),
        (82.09, 29.66),
        (81.18, 30.00),
        (80.88, 30.34),
        (80.40, 30.18),
        (80.06, 28.83),
    ]
    poly = Polygon(nepal_coords)
    gdf = gpd.GeoDataFrame({"name": ["Nepal"]}, geometry=[poly], crs="EPSG:4326")
    return gdf


def create_physiographic_zones(dem_path=None):
    """
    Create physiographic zone classification from DEM.

    Zones based on elevation:
        1 = Terai (< 300m)
        2 = Siwalik (300–1500m)
        3 = Middle Mountains (1500–3000m)
        4 = High Mountains (3000–5000m)
        5 = High Himal (> 5000m)

    Parameters
    ----------
    dem_path : str or Path, optional
        Path to DEM GeoTIFF. If None, returns zone definitions only.

    Returns
    -------
    dict
        Zone definitions with elevation ranges.
    """
    zones = {
        1: {"name": "Terai", "min_elev": 0, "max_elev": 300},
        2: {"name": "Siwalik", "min_elev": 300, "max_elev": 1500},
        3: {"name": "Middle_Mountains", "min_elev": 1500, "max_elev": 3000},
        4: {"name": "High_Mountains", "min_elev": 3000, "max_elev": 5000},
        5: {"name": "High_Himal", "min_elev": 5000, "max_elev": 9000},
    }

    if dem_path and Path(dem_path).exists():
        import rasterio

        with rasterio.open(dem_path) as src:
            dem_data = src.read(1)
            profile = src.profile

        zone_raster = np.zeros_like(dem_data, dtype=np.int8)
        for zone_id, params in zones.items():
            mask = (dem_data >= params["min_elev"]) & (dem_data < params["max_elev"])
            zone_raster[mask] = zone_id

        return zone_raster, zones, profile

    return zones


def create_spatial_grid(boundary_gdf, cell_size_deg=0.05):
    """
    Create a regular spatial grid over the study area.

    Parameters
    ----------
    boundary_gdf : gpd.GeoDataFrame
        Boundary polygon.
    cell_size_deg : float
        Grid cell size in degrees (default 0.05° ≈ 5km).

    Returns
    -------
    gpd.GeoDataFrame
        Grid of square polygons covering the study area.
    """
    bounds = boundary_gdf.total_bounds  # [minx, miny, maxx, maxy]

    xmin, ymin, xmax, ymax = bounds

    # Create grid cells
    grid_cells = []
    x = xmin
    while x < xmax:
        y = ymin
        while y < ymax:
            cell = box(x, y, x + cell_size_deg, y + cell_size_deg)
            grid_cells.append(cell)
            y += cell_size_deg
        x += cell_size_deg

    grid = gpd.GeoDataFrame(geometry=grid_cells, crs="EPSG:4326")

    # Keep only cells that intersect the boundary
    grid = gpd.sjoin(grid, boundary_gdf, how="inner", predicate="intersects")
    grid = grid.drop(columns=["index_right"]).reset_index(drop=True)
    grid["grid_id"] = range(len(grid))

    # Add centroid coordinates
    centroids = grid.geometry.centroid
    grid["center_lon"] = centroids.x
    grid["center_lat"] = centroids.y

    return grid


def build_spatial_weights(gdf, weights_type="queen", k=None, distance_band=None):
    """
    Build spatial weight matrix for spatial autocorrelation analysis.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with polygon geometries.
    weights_type : str
        'queen', 'rook', 'knn', or 'distance'
    k : int, optional
        Number of neighbors for KNN weights.
    distance_band : float, optional
        Distance threshold for distance-based weights (in CRS units).

    Returns
    -------
    libpysal.weights.W
        Spatial weights matrix.
    """
    from libpysal.weights import Queen, Rook, KNN, DistanceBand

    if weights_type == "queen":
        w = Queen.from_dataframe(gdf)
    elif weights_type == "rook":
        w = Rook.from_dataframe(gdf)
    elif weights_type == "knn":
        k = k or 8
        w = KNN.from_dataframe(gdf, k=k)
    elif weights_type == "distance":
        if distance_band is None:
            raise ValueError("distance_band required for distance-based weights")
        w = DistanceBand.from_dataframe(gdf, threshold=distance_band)
    else:
        raise ValueError(f"Unknown weights type: {weights_type}")

    w.transform = "r"  # Row-standardize
    return w


def assign_season(month):
    """
    Assign Nepal-specific season based on month number.

    Parameters
    ----------
    month : int
        Month number (1-12).

    Returns
    -------
    str
        Season name.
    """
    if month in [3, 4, 5]:
        return "Pre-monsoon"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month in [10, 11]:
        return "Post-monsoon"
    else:
        return "Winter"


def raster_to_points(raster_path, band=1, nodata=None):
    """
    Convert a raster GeoTIFF to a GeoDataFrame of points.

    Parameters
    ----------
    raster_path : str or Path
        Path to GeoTIFF file.
    band : int
        Band number to read (1-indexed).
    nodata : float, optional
        No-data value to mask out.

    Returns
    -------
    gpd.GeoDataFrame
        Point features with raster values.
    """
    import rasterio

    with rasterio.open(raster_path) as src:
        data = src.read(band)
        transform = src.transform
        crs = src.crs

        if nodata is None:
            nodata = src.nodata

    rows, cols = np.where(data != nodata if nodata else np.ones_like(data, dtype=bool))
    values = data[rows, cols]

    # Convert row, col to coordinates
    xs, ys = rasterio.transform.xy(transform, rows, cols)

    points = [Point(x, y) for x, y in zip(xs, ys)]

    gdf = gpd.GeoDataFrame({"value": values}, geometry=points, crs=crs)

    return gdf
