import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patches as mpatches
import os

def create_study_area_map():
    print("Generating Study Area Map for Nepal...")
    
    # 1. Ensure output directory exists
    os.makedirs('figures/spatial_maps', exist_ok=True)
    
    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)
    nepal = world[world.NAME == 'Nepal']
    
    # Convert to Web Mercator (EPSG:3857) for Contextily basemaps
    nepal_wm = nepal.to_crs(epsg=3857)
    
    # 3. Setup Figure
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Plot Nepal boundary with thick black edge and transparent face
    nepal_wm.plot(ax=ax, edgecolor='black', facecolor='none', linewidth=2.5, zorder=5)
    
    # Add a buffer to zoom out slightly
    bounds = nepal_wm.total_bounds
    buffer_x = (bounds[2] - bounds[0]) * 0.1
    buffer_y = (bounds[3] - bounds[1]) * 0.1
    ax.set_xlim(bounds[0] - buffer_x, bounds[2] + buffer_x)
    ax.set_ylim(bounds[1] - buffer_y, bounds[3] + buffer_y)
    
    # 4. Add High-Resolution Physical Terrain Basemap
    # OpenStreetMap or Stamen Terrain (now Stadia)
    try:
        cx.add_basemap(ax, crs=nepal_wm.crs.to_string(), source=cx.providers.Esri.WorldTerrain)
    except:
        cx.add_basemap(ax, crs=nepal_wm.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik)
    
    # 5. Add Map Design Elements
    # Scale Bar (assuming EPSG:3857 units are meters, which they mostly are at the equator, but we need correct scale)
    # matplotlib-scalebar calculates based on the axes coordinates
    scalebar = ScaleBar(dx=1, units="m", length_fraction=0.2, location="lower right", box_alpha=0.8)
    ax.add_artist(scalebar)
    
    # North Arrow
    x, y, arrow_length = 0.05, 0.95, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=20, weight='bold',
                xycoords='axes fraction')
                
    # 6. Aesthetic Formatting
    ax.set_title("Study Area: Nepal and Physiographic Terrain", fontsize=16, weight='bold', pad=20)
    ax.set_xlabel("Longitude (Web Mercator)", fontsize=12)
    ax.set_ylabel("Latitude (Web Mercator)", fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Add an approximate text annotation for zones
    ax.text(bounds[0] + buffer_x, bounds[1] + buffer_y*1.5, "Terai (Lowlands)", fontsize=12, style='italic', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    ax.text(bounds[2] - buffer_x*2.5, bounds[3] - buffer_y*1.5, "High Himal", fontsize=12, style='italic', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Save the professional map
    plt.tight_layout()
    plt.savefig('figures/spatial_maps/Figure_1_Study_Area.png', dpi=300, bbox_inches='tight')
    plt.savefig('figures/spatial_maps/Figure_1_Study_Area.pdf', bbox_inches='tight')
    plt.close()
    print("Map saved to figures/spatial_maps/Figure_1_Study_Area.png")

if __name__ == "__main__":
    create_study_area_map()
