#!/usr/bin/env python3
"""
Elevation Data Processor for Treasure Hunt
Downloads SRTM data and creates slope, aspect, and south-facing slope masks
"""

import os
import sys
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import calculate_default_transform, reproject, Resampling
from scipy.ndimage import generic_filter
import subprocess
from pathlib import Path

# Search area parameters
CENTER_LAT = 35.635
CENTER_LON = -82.875
RADIUS_MILES = 37.5
RADIUS_KM = RADIUS_MILES * 1.60934

# Convert radius to approximate degrees (rough approximation)
# At this latitude: 1 degree lat ~ 111 km, 1 degree lon ~ 91 km
RADIUS_DEG_LAT = RADIUS_KM / 111.0
RADIUS_DEG_LON = RADIUS_KM / 91.0

# Bounding box
SOUTH = CENTER_LAT - RADIUS_DEG_LAT
NORTH = CENTER_LAT + RADIUS_DEG_LAT
WEST = CENTER_LON - RADIUS_DEG_LON
EAST = CENTER_LON + RADIUS_DEG_LON

# Output directory
OUTPUT_DIR = Path('/Users/fredbliss/workspace/treasure/data/elevation')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Search Area Configuration:")
print(f"  Center: {CENTER_LAT}°N, {CENTER_LON}°W")
print(f"  Radius: {RADIUS_MILES} miles ({RADIUS_KM:.2f} km)")
print(f"  Bounding Box:")
print(f"    North: {NORTH:.4f}°")
print(f"    South: {SOUTH:.4f}°")
print(f"    East: {EAST:.4f}°")
print(f"    West: {WEST:.4f}°")
print()

def download_srtm_data():
    """Download SRTM data using the elevation library"""
    print("=" * 60)
    print("STEP 1: Downloading SRTM 30m DEM data")
    print("=" * 60)

    dem_path = OUTPUT_DIR / 'dem.tif'

    # Use elevation library to download data
    cmd = [
        'eio',
        'clip',
        '-o', str(dem_path),
        '--bounds', str(WEST), str(SOUTH), str(EAST), str(NORTH)
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error downloading DEM: {result.stderr}")
        return None

    print(f"DEM downloaded successfully to: {dem_path}")

    # Verify the file
    with rasterio.open(dem_path) as src:
        print(f"  Shape: {src.shape}")
        print(f"  CRS: {src.crs}")
        print(f"  Bounds: {src.bounds}")
        print(f"  Resolution: {src.res}")

        # Get elevation statistics
        data = src.read(1, masked=True)
        print(f"  Elevation range: {data.min():.1f}m to {data.max():.1f}m")
        print(f"  Mean elevation: {data.mean():.1f}m")

    print()
    return dem_path

def calculate_slope_aspect(dem_path):
    """Calculate slope and aspect from DEM"""
    print("=" * 60)
    print("STEP 2: Calculating Slope and Aspect")
    print("=" * 60)

    with rasterio.open(dem_path) as src:
        dem = src.read(1, masked=True)
        transform = src.transform
        profile = src.profile

        # Get cell size in meters (approximate for this latitude)
        cell_size_x = abs(transform[0]) * 91000  # degrees to meters at ~36°N
        cell_size_y = abs(transform[4]) * 111000  # degrees to meters

        print(f"Cell size: {cell_size_x:.1f}m x {cell_size_y:.1f}m")

        # Calculate gradients using numpy gradient
        dy, dx = np.gradient(dem.filled(np.nan))

        # Convert to slope in degrees
        # rise / run, then to degrees
        slope_rad = np.arctan(np.sqrt((dy/cell_size_y)**2 + (dx/cell_size_x)**2))
        slope_deg = np.degrees(slope_rad)

        # Calculate aspect (direction of slope)
        # atan2(dx, -dy) gives aspect in radians, convert to degrees
        # 0° = North, 90° = East, 180° = South, 270° = West
        aspect_rad = np.arctan2(dx, -dy)
        aspect_deg = np.degrees(aspect_rad)
        # Convert from -180:180 to 0:360
        aspect_deg = (aspect_deg + 360) % 360

        # Mask no-data values
        if isinstance(dem, np.ma.MaskedArray):
            slope_deg = np.ma.masked_where(dem.mask, slope_deg)
            aspect_deg = np.ma.masked_where(dem.mask, aspect_deg)

        # Save slope
        slope_path = OUTPUT_DIR / 'slope.tif'
        profile.update(dtype=rasterio.float32, nodata=-9999)

        with rasterio.open(slope_path, 'w', **profile) as dst:
            dst.write(slope_deg.filled(-9999).astype(np.float32), 1)

        print(f"Slope saved to: {slope_path}")
        print(f"  Slope range: {np.nanmin(slope_deg):.1f}° to {np.nanmax(slope_deg):.1f}°")
        print(f"  Mean slope: {np.nanmean(slope_deg):.1f}°")

        # Save aspect
        aspect_path = OUTPUT_DIR / 'aspect.tif'
        with rasterio.open(aspect_path, 'w', **profile) as dst:
            dst.write(aspect_deg.filled(-9999).astype(np.float32), 1)

        print(f"Aspect saved to: {aspect_path}")
        print(f"  Aspect range: 0° to 360° (0°=N, 90°=E, 180°=S, 270°=W)")
        print()

        return slope_path, aspect_path, slope_deg, aspect_deg

def create_south_facing_mask(aspect_path, slope_path):
    """Create binary mask of south-facing slopes (135° to 225° aspect)"""
    print("=" * 60)
    print("STEP 3: Creating South-Facing Slope Mask")
    print("=" * 60)

    with rasterio.open(aspect_path) as aspect_src:
        aspect = aspect_src.read(1, masked=True)
        profile = aspect_src.profile

    with rasterio.open(slope_path) as slope_src:
        slope = slope_src.read(1, masked=True)

    # South-facing: 135° to 225° (SE to SW)
    # Also require moderate slope (not flat, not too steep)
    MIN_ASPECT = 135
    MAX_ASPECT = 225
    MIN_SLOPE = 5  # degrees (not too flat)
    MAX_SLOPE = 35  # degrees (not too steep for hiking)

    south_facing = (
        (aspect >= MIN_ASPECT) &
        (aspect <= MAX_ASPECT) &
        (slope >= MIN_SLOPE) &
        (slope <= MAX_SLOPE)
    )

    # Convert to 0/1 mask
    mask = south_facing.astype(np.uint8)

    # Save mask
    mask_path = OUTPUT_DIR / 'south_facing_mask.tif'
    profile.update(dtype=rasterio.uint8, nodata=255)

    with rasterio.open(mask_path, 'w', **profile) as dst:
        dst.write(mask, 1)

    print(f"South-facing mask saved to: {mask_path}")
    print(f"  Criteria: Aspect {MIN_ASPECT}°-{MAX_ASPECT}°, Slope {MIN_SLOPE}°-{MAX_SLOPE}°")

    total_pixels = mask.size
    south_pixels = np.sum(mask == 1)
    percentage = (south_pixels / total_pixels) * 100

    print(f"  South-facing pixels: {south_pixels:,} ({percentage:.2f}%)")
    print()

    return mask_path

def terrain_analysis():
    """Perform comprehensive terrain analysis"""
    print("=" * 60)
    print("STEP 4: Terrain Analysis Summary")
    print("=" * 60)

    dem_path = OUTPUT_DIR / 'dem.tif'
    slope_path = OUTPUT_DIR / 'slope.tif'
    aspect_path = OUTPUT_DIR / 'aspect.tif'
    mask_path = OUTPUT_DIR / 'south_facing_mask.tif'

    with rasterio.open(dem_path) as src:
        dem = src.read(1, masked=True)

    with rasterio.open(slope_path) as src:
        slope = src.read(1, masked=True)

    with rasterio.open(aspect_path) as src:
        aspect = src.read(1, masked=True)

    with rasterio.open(mask_path) as src:
        mask = src.read(1)

    print("ELEVATION STATISTICS:")
    print(f"  Minimum: {np.nanmin(dem):.1f}m ({np.nanmin(dem)*3.28084:.0f}ft)")
    print(f"  Maximum: {np.nanmax(dem):.1f}m ({np.nanmax(dem)*3.28084:.0f}ft)")
    print(f"  Mean: {np.nanmean(dem):.1f}m ({np.nanmean(dem)*3.28084:.0f}ft)")
    print(f"  Std Dev: {np.nanstd(dem):.1f}m")
    print(f"  Relief: {np.nanmax(dem) - np.nanmin(dem):.1f}m ({(np.nanmax(dem) - np.nanmin(dem))*3.28084:.0f}ft)")
    print()

    print("SLOPE STATISTICS:")
    print(f"  Mean slope: {np.nanmean(slope):.1f}°")
    print(f"  Median slope: {np.nanmedian(slope):.1f}°")
    print(f"  Max slope: {np.nanmax(slope):.1f}°")

    # Slope categories
    flat = np.sum((slope >= 0) & (slope < 5))
    gentle = np.sum((slope >= 5) & (slope < 15))
    moderate = np.sum((slope >= 15) & (slope < 25))
    steep = np.sum((slope >= 25) & (slope < 35))
    very_steep = np.sum(slope >= 35)
    total = slope.size

    print(f"  Flat (0-5°): {flat/total*100:.1f}%")
    print(f"  Gentle (5-15°): {gentle/total*100:.1f}%")
    print(f"  Moderate (15-25°): {moderate/total*100:.1f}%")
    print(f"  Steep (25-35°): {steep/total*100:.1f}%")
    print(f"  Very Steep (>35°): {very_steep/total*100:.1f}%")
    print()

    print("ASPECT DISTRIBUTION:")
    # Aspect categories (N, NE, E, SE, S, SW, W, NW)
    directions = [
        ('North', 337.5, 22.5),
        ('Northeast', 22.5, 67.5),
        ('East', 67.5, 112.5),
        ('Southeast', 112.5, 157.5),
        ('South', 157.5, 202.5),
        ('Southwest', 202.5, 247.5),
        ('West', 247.5, 292.5),
        ('Northwest', 292.5, 337.5)
    ]

    for name, min_a, max_a in directions:
        if min_a > max_a:  # North wraps around
            count = np.sum((aspect >= min_a) | (aspect < max_a))
        else:
            count = np.sum((aspect >= min_a) & (aspect < max_a))
        pct = count / total * 100
        print(f"  {name:12s}: {pct:5.1f}%")

    print()
    print("SOUTH-FACING SLOPE ANALYSIS:")
    south_pixels = np.sum(mask == 1)
    print(f"  Total area matching criteria: {south_pixels/total*100:.2f}%")
    print(f"  Criteria: 135°-225° aspect, 5°-35° slope")

    # Get elevation stats for south-facing areas
    south_dem = dem[mask == 1]
    if len(south_dem) > 0:
        print(f"  Elevation range on south slopes: {np.nanmin(south_dem):.1f}m to {np.nanmax(south_dem):.1f}m")
        print(f"  Mean elevation on south slopes: {np.nanmean(south_dem):.1f}m")

    print()
    print("=" * 60)
    print("DATA FILES CREATED:")
    print("=" * 60)
    print(f"  {dem_path}")
    print(f"  {slope_path}")
    print(f"  {aspect_path}")
    print(f"  {mask_path}")
    print()

def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print("ELEVATION DATA PROCESSOR - TREASURE HUNT")
    print("Agent A2: Satellite Imagery & Elevation Data")
    print("=" * 60)
    print()

    try:
        # Step 1: Download DEM
        dem_path = download_srtm_data()
        if not dem_path:
            print("Failed to download DEM data")
            sys.exit(1)

        # Step 2: Calculate slope and aspect
        slope_path, aspect_path, slope_deg, aspect_deg = calculate_slope_aspect(dem_path)

        # Step 3: Create south-facing mask
        mask_path = create_south_facing_mask(aspect_path, slope_path)

        # Step 4: Terrain analysis
        terrain_analysis()

        print("=" * 60)
        print("SUCCESS! All elevation data processed.")
        print("=" * 60)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
