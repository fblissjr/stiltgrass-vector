#!/usr/bin/env python3
"""
Download SRTM elevation data using srtm.py library
"""

from pathlib import Path

import numpy as np
import rasterio
import srtm
from rasterio.transform import from_bounds

# Search area parameters
CENTER_LAT = 35.635
CENTER_LON = -82.875
RADIUS_MILES = 37.5
RADIUS_KM = RADIUS_MILES * 1.60934

# Convert radius to approximate degrees
RADIUS_DEG_LAT = RADIUS_KM / 111.0
RADIUS_DEG_LON = RADIUS_KM / 91.0

# Bounding box
SOUTH = CENTER_LAT - RADIUS_DEG_LAT
NORTH = CENTER_LAT + RADIUS_DEG_LAT
WEST = CENTER_LON - RADIUS_DEG_LON
EAST = CENTER_LON + RADIUS_DEG_LON

OUTPUT_DIR = Path("data/elevation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Downloading SRTM data for area:")
print(f"  North: {NORTH:.4f}°, South: {SOUTH:.4f}°")
print(f"  East: {EAST:.4f}°, West: {WEST:.4f}°")
print()

# Initialize SRTM data handler
elevation_data = srtm.get_data()

# Create a grid of points
resolution = 0.001  # approximately 100m at this latitude
lats = np.arange(SOUTH, NORTH, resolution)
lons = np.arange(WEST, EAST, resolution)

print(f"Creating DEM grid: {len(lats)} x {len(lons)} pixels")
print(f"Approximate resolution: ~100m")
print()

# Create elevation grid
print("Downloading elevation data from SRTM...")
dem = np.zeros((len(lats), len(lons)), dtype=np.float32)

# Sample elevations (this will download SRTM tiles as needed)
for i, lat in enumerate(lats):
    if i % 100 == 0:
        print(f"  Progress: {i}/{len(lats)} rows ({i / len(lats) * 100:.1f}%)")
    for j, lon in enumerate(lons):
        elev = elevation_data.get_elevation(lat, lon)
        dem[i, j] = elev if elev is not None else -9999

print("Download complete!")
print()

# Flip the array vertically (SRTM returns data in different orientation than GeoTIFF)
dem = np.flipud(dem)

# Create GeoTIFF
dem_path = OUTPUT_DIR / "dem.tif"

# Define transform
transform = from_bounds(WEST, SOUTH, EAST, NORTH, dem.shape[1], dem.shape[0])

# Create profile
profile = {
    "driver": "GTiff",
    "height": dem.shape[0],
    "width": dem.shape[1],
    "count": 1,
    "dtype": rasterio.float32,
    "crs": "EPSG:4326",
    "transform": transform,
    "nodata": -9999,
    "compress": "lzw",
}

# Write DEM
with rasterio.open(dem_path, "w", **profile) as dst:
    dst.write(dem, 1)

print(f"DEM saved to: {dem_path}")
print(f"  Shape: {dem.shape}")
print(
    f"  Elevation range: {dem[dem != -9999].min():.1f}m to {dem[dem != -9999].max():.1f}m"
)
print(f"  Mean elevation: {dem[dem != -9999].mean():.1f}m")
print()
