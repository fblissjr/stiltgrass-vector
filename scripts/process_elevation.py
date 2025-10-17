#!/usr/bin/env python3
"""
Process elevation data to create slope, aspect, and south-facing masks
"""

import numpy as np
import rasterio
from pathlib import Path

OUTPUT_DIR = Path('/Users/fredbliss/workspace/treasure/data/elevation')

def calculate_slope_aspect(dem_path):
    """Calculate slope and aspect from DEM"""
    print("=" * 70)
    print("CALCULATING SLOPE AND ASPECT")
    print("=" * 70)
    print()

    with rasterio.open(dem_path) as src:
        dem = src.read(1, masked=True)
        transform = src.transform
        profile = src.profile

        # Get cell size in meters
        # At ~36°N latitude: 1 degree lat ~ 111km, 1 degree lon ~ 91km
        cell_size_x = abs(transform[0]) * 91000  # degrees to meters
        cell_size_y = abs(transform[4]) * 111000  # degrees to meters

        print(f"DEM Info:")
        print(f"  Shape: {dem.shape}")
        print(f"  Cell size: {cell_size_x:.1f}m x {cell_size_y:.1f}m")
        print(f"  Elevation range: {dem.min():.1f}m to {dem.max():.1f}m")
        print()

        # Calculate gradients
        dy, dx = np.gradient(dem.filled(np.nan))

        # Convert to slope in degrees
        slope_rad = np.arctan(np.sqrt((dy/cell_size_y)**2 + (dx/cell_size_x)**2))
        slope_deg = np.degrees(slope_rad)

        # Calculate aspect (0° = North, 90° = East, 180° = South, 270° = West)
        aspect_rad = np.arctan2(dx, -dy)
        aspect_deg = np.degrees(aspect_rad)
        aspect_deg = (aspect_deg + 360) % 360  # Convert to 0-360

        # Handle no-data
        if isinstance(dem, np.ma.MaskedArray):
            slope_deg = np.ma.masked_where(dem.mask, slope_deg)
            aspect_deg = np.ma.masked_where(dem.mask, aspect_deg)

        # Save slope
        slope_path = OUTPUT_DIR / 'slope.tif'
        profile.update(dtype=rasterio.float32, nodata=-9999)

        with rasterio.open(slope_path, 'w', **profile) as dst:
            dst.write(slope_deg.filled(-9999).astype(np.float32), 1)

        print(f"Slope Statistics:")
        print(f"  Range: {np.nanmin(slope_deg):.1f}° to {np.nanmax(slope_deg):.1f}°")
        print(f"  Mean: {np.nanmean(slope_deg):.1f}°")
        print(f"  Median: {np.nanmedian(slope_deg):.1f}°")
        print(f"  Saved to: {slope_path}")
        print()

        # Save aspect
        aspect_path = OUTPUT_DIR / 'aspect.tif'
        with rasterio.open(aspect_path, 'w', **profile) as dst:
            dst.write(aspect_deg.filled(-9999).astype(np.float32), 1)

        print(f"Aspect Statistics:")
        print(f"  Range: 0° to 360° (0°=N, 90°=E, 180°=S, 270°=W)")
        print(f"  Saved to: {aspect_path}")
        print()

        return slope_path, aspect_path, slope_deg, aspect_deg

def create_south_facing_mask(aspect_path, slope_path):
    """Create binary mask of south-facing slopes"""
    print("=" * 70)
    print("CREATING SOUTH-FACING SLOPE MASK")
    print("=" * 70)
    print()

    with rasterio.open(aspect_path) as aspect_src:
        aspect = aspect_src.read(1, masked=True)
        profile = aspect_src.profile

    with rasterio.open(slope_path) as slope_src:
        slope = slope_src.read(1, masked=True)

    # South-facing criteria
    MIN_ASPECT = 135  # Southeast
    MAX_ASPECT = 225  # Southwest
    MIN_SLOPE = 5     # degrees (not too flat)
    MAX_SLOPE = 35    # degrees (not too steep for hiking)

    south_facing = (
        (aspect >= MIN_ASPECT) &
        (aspect <= MAX_ASPECT) &
        (slope >= MIN_SLOPE) &
        (slope <= MAX_SLOPE)
    )

    mask = south_facing.astype(np.uint8)

    # Save mask
    mask_path = OUTPUT_DIR / 'south_facing_mask.tif'
    profile.update(dtype=rasterio.uint8, nodata=255)

    with rasterio.open(mask_path, 'w', **profile) as dst:
        dst.write(mask, 1)

    total_pixels = mask.size
    south_pixels = np.sum(mask == 1)
    percentage = (south_pixels / total_pixels) * 100

    print(f"South-Facing Mask Criteria:")
    print(f"  Aspect: {MIN_ASPECT}° to {MAX_ASPECT}° (SE through S to SW)")
    print(f"  Slope: {MIN_SLOPE}° to {MAX_SLOPE}° (moderate slopes)")
    print()
    print(f"Results:")
    print(f"  Matching pixels: {south_pixels:,} ({percentage:.2f}%)")
    print(f"  Saved to: {mask_path}")
    print()

    return mask_path

def terrain_analysis():
    """Comprehensive terrain analysis"""
    print("=" * 70)
    print("COMPREHENSIVE TERRAIN ANALYSIS")
    print("=" * 70)
    print()

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

    # Elevation statistics
    print("ELEVATION ANALYSIS:")
    print(f"  Minimum: {np.nanmin(dem):.0f}m ({np.nanmin(dem)*3.28084:.0f}ft)")
    print(f"  Maximum: {np.nanmax(dem):.0f}m ({np.nanmax(dem)*3.28084:.0f}ft)")
    print(f"  Mean: {np.nanmean(dem):.0f}m ({np.nanmean(dem)*3.28084:.0f}ft)")
    print(f"  Median: {np.nanmedian(dem):.0f}m ({np.nanmedian(dem)*3.28084:.0f}ft)")
    print(f"  Relief: {np.nanmax(dem) - np.nanmin(dem):.0f}m ({(np.nanmax(dem) - np.nanmin(dem))*3.28084:.0f}ft)")
    print()

    # Elevation zones
    print("ELEVATION ZONES:")
    zones = [
        ("Low valleys", 0, 500),
        ("Mid elevations", 500, 1000),
        ("Mountain slopes", 1000, 1500),
        ("High peaks", 1500, 3000)
    ]
    for name, min_e, max_e in zones:
        count = np.sum((dem >= min_e) & (dem < max_e))
        pct = count / dem.size * 100
        print(f"  {name:20s} ({min_e:4d}-{max_e:4d}m): {pct:5.1f}%")
    print()

    # Slope statistics
    print("SLOPE ANALYSIS:")
    print(f"  Mean: {np.nanmean(slope):.1f}°")
    print(f"  Median: {np.nanmedian(slope):.1f}°")
    print(f"  Max: {np.nanmax(slope):.1f}°")
    print()

    # Slope categories
    print("SLOPE CATEGORIES:")
    categories = [
        ("Flat", 0, 5),
        ("Gentle", 5, 15),
        ("Moderate", 15, 25),
        ("Steep", 25, 35),
        ("Very Steep", 35, 90)
    ]
    for name, min_s, max_s in categories:
        count = np.sum((slope >= min_s) & (slope < max_s))
        pct = count / slope.size * 100
        print(f"  {name:12s} ({min_s:2d}-{max_s:2d}°): {pct:5.1f}%")
    print()

    # Aspect distribution
    print("ASPECT DISTRIBUTION:")
    directions = [
        ('North (N)', 337.5, 22.5),
        ('Northeast (NE)', 22.5, 67.5),
        ('East (E)', 67.5, 112.5),
        ('Southeast (SE)', 112.5, 157.5),
        ('South (S)', 157.5, 202.5),
        ('Southwest (SW)', 202.5, 247.5),
        ('West (W)', 247.5, 292.5),
        ('Northwest (NW)', 292.5, 337.5)
    ]

    for name, min_a, max_a in directions:
        if min_a > max_a:  # North wraps around
            count = np.sum((aspect >= min_a) | (aspect < max_a))
        else:
            count = np.sum((aspect >= min_a) & (aspect < max_a))
        pct = count / aspect.size * 100
        print(f"  {name:18s}: {pct:5.1f}%")
    print()

    # South-facing analysis
    print("SOUTH-FACING SLOPES (135°-225°, 5°-35° slope):")
    south_pixels = np.sum(mask == 1)
    print(f"  Area: {south_pixels/dem.size*100:.2f}% of total")

    if south_pixels > 0:
        south_dem = dem[mask == 1]
        south_slope = slope[mask == 1]

        print(f"  Elevation range: {np.nanmin(south_dem):.0f}m to {np.nanmax(south_dem):.0f}m")
        print(f"  Mean elevation: {np.nanmean(south_dem):.0f}m ({np.nanmean(south_dem)*3.28084:.0f}ft)")
        print(f"  Mean slope: {np.nanmean(south_slope):.1f}°")

        # Count by elevation zone
        print()
        print("  Distribution by elevation:")
        for name, min_e, max_e in zones:
            count = np.sum((south_dem >= min_e) & (south_dem < max_e))
            pct = count / south_pixels * 100 if south_pixels > 0 else 0
            print(f"    {name:20s}: {pct:5.1f}%")

    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print("Output files created:")
    print(f"  {OUTPUT_DIR / 'dem.tif'}")
    print(f"  {OUTPUT_DIR / 'slope.tif'}")
    print(f"  {OUTPUT_DIR / 'aspect.tif'}")
    print(f"  {OUTPUT_DIR / 'south_facing_mask.tif'}")
    print()

def main():
    dem_path = OUTPUT_DIR / 'dem.tif'

    if not dem_path.exists():
        print(f"ERROR: DEM file not found at {dem_path}")
        print("Please run download_srtm.py first.")
        return

    # Calculate slope and aspect
    slope_path, aspect_path, _, _ = calculate_slope_aspect(dem_path)

    # Create south-facing mask
    mask_path = create_south_facing_mask(aspect_path, slope_path)

    # Terrain analysis
    terrain_analysis()

if __name__ == '__main__':
    main()
