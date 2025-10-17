#!/usr/bin/env python3
"""
Download elevation data and satellite imagery for the treasure hunt search area.
Search area: 35.705°N, 82.83°W (Asheville, NC) with 43.5 mile radius
"""

import os
import requests
import json
from pathlib import Path
import numpy as np
from typing import Tuple, Dict, Any

# Search area parameters
CENTER_LAT = 35.705
CENTER_LON = -82.83
RADIUS_MILES = 43.5
RADIUS_DEGREES = RADIUS_MILES / 69.0  # Approximate conversion

# Calculate bounding box
LAT_MIN = CENTER_LAT - RADIUS_DEGREES
LAT_MAX = CENTER_LAT + RADIUS_DEGREES
LON_MIN = CENTER_LON - RADIUS_DEGREES
LON_MAX = CENTER_LON + RADIUS_DEGREES

# Directory setup
BASE_DIR = Path("/Users/fredbliss/workspace/treasure")
ELEVATION_DIR = BASE_DIR / "data" / "elevation"
SATELLITE_DIR = BASE_DIR / "data" / "satellite_imagery"

def get_bounding_box() -> Dict[str, float]:
    """Return the bounding box for the search area."""
    return {
        "lat_min": LAT_MIN,
        "lat_max": LAT_MAX,
        "lon_min": LON_MIN,
        "lon_max": LON_MAX
    }

def download_srtm_elevation() -> bool:
    """
    Download SRTM elevation data for the search area.
    SRTM provides 30m resolution elevation data globally.
    """
    print("Attempting to download SRTM elevation data...")

    # We'll use OpenTopography API for SRTM data
    # This requires registration but provides programmatic access
    url = "https://portal.opentopography.org/API/globaldem"

    params = {
        "demtype": "SRTMGL1",  # SRTM GL1 (30m resolution)
        "south": LAT_MIN,
        "north": LAT_MAX,
        "west": LON_MIN,
        "east": LON_MAX,
        "outputFormat": "GTiff"
    }

    print(f"Bounding box: {LAT_MIN:.3f}°N to {LAT_MAX:.3f}°N, {LON_MIN:.3f}°W to {LON_MAX:.3f}°W")
    print("Note: OpenTopography API requires an API key for downloads.")
    print("Visit: https://opentopography.org/blog/introducing-api-keys-access-opentopography-global-datasets")

    return False

def download_usgs_3dep_metadata() -> Dict[str, Any]:
    """
    Get metadata about available USGS 3DEP elevation data for the area.
    """
    print("\nQuerying USGS 3DEP data availability...")

    # The National Map API endpoint
    url = "https://tnmaccess.nationalmap.gov/api/v1/products"

    params = {
        "datasets": "Digital Elevation Model (DEM) 1 meter",
        "bbox": f"{LON_MIN},{LAT_MIN},{LON_MAX},{LAT_MAX}",
        "outputFormat": "JSON",
        "max": 50
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data.get('total', 0)} DEM tiles available")

            # Save metadata
            metadata_file = ELEVATION_DIR / "usgs_3dep_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Metadata saved to: {metadata_file}")

            return data
        else:
            print(f"API request failed with status code: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error querying USGS API: {e}")
        return {}

def get_elevation_profile() -> None:
    """
    Get elevation profile information for the search area.
    Uses Open-Elevation API for spot elevation queries.
    """
    print("\nQuerying elevation at key points in search area...")

    # Sample points across the search area
    sample_points = [
        (CENTER_LAT, CENTER_LON, "Center"),
        (LAT_MIN, LON_MIN, "Southwest corner"),
        (LAT_MIN, LON_MAX, "Southeast corner"),
        (LAT_MAX, LON_MIN, "Northwest corner"),
        (LAT_MAX, LON_MAX, "Northeast corner"),
        (CENTER_LAT, LON_MIN, "West edge"),
        (CENTER_LAT, LON_MAX, "East edge"),
        (LAT_MIN, CENTER_LON, "South edge"),
        (LAT_MAX, CENTER_LON, "North edge"),
    ]

    # Open-Elevation API (free, no key required)
    url = "https://api.open-elevation.com/api/v1/lookup"

    locations = [{"latitude": lat, "longitude": lon} for lat, lon, _ in sample_points]

    try:
        response = requests.post(url, json={"locations": locations}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            elevations = []

            print("\nElevation samples:")
            for point, result in zip(sample_points, data['results']):
                lat, lon, name = point
                elevation = result['elevation']
                elevations.append(elevation)
                print(f"  {name:20s}: {elevation:6.1f}m ({elevation * 3.28084:.1f}ft) at {lat:.3f}°N, {lon:.3f}°W")

            # Calculate statistics
            elevations = np.array(elevations)
            print(f"\nElevation statistics:")
            print(f"  Minimum: {elevations.min():.1f}m ({elevations.min() * 3.28084:.1f}ft)")
            print(f"  Maximum: {elevations.max():.1f}m ({elevations.max() * 3.28084:.1f}ft)")
            print(f"  Range: {elevations.max() - elevations.min():.1f}m ({(elevations.max() - elevations.min()) * 3.28084:.1f}ft)")
            print(f"  Mean: {elevations.mean():.1f}m ({elevations.mean() * 3.28084:.1f}ft)")

            # Save elevation data
            elevation_file = ELEVATION_DIR / "elevation_samples.json"
            elevation_data = {
                "samples": [
                    {
                        "location": name,
                        "latitude": lat,
                        "longitude": lon,
                        "elevation_meters": result['elevation'],
                        "elevation_feet": result['elevation'] * 3.28084
                    }
                    for (lat, lon, name), result in zip(sample_points, data['results'])
                ],
                "statistics": {
                    "min_meters": float(elevations.min()),
                    "max_meters": float(elevations.max()),
                    "range_meters": float(elevations.max() - elevations.min()),
                    "mean_meters": float(elevations.mean()),
                    "min_feet": float(elevations.min() * 3.28084),
                    "max_feet": float(elevations.max() * 3.28084),
                    "range_feet": float((elevations.max() - elevations.min()) * 3.28084),
                    "mean_feet": float(elevations.mean() * 3.28084)
                }
            }

            with open(elevation_file, 'w') as f:
                json.dump(elevation_data, f, indent=2)
            print(f"\nElevation data saved to: {elevation_file}")

        else:
            print(f"Elevation API request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error querying elevation API: {e}")

def get_sentinel2_info() -> None:
    """
    Get information about Sentinel-2 satellite coverage for the area.
    """
    print("\n" + "="*80)
    print("SENTINEL-2 SATELLITE IMAGERY INFORMATION")
    print("="*80)

    print(f"\nSearch area coordinates: {CENTER_LAT:.3f}°N, {CENTER_LON:.3f}°W")
    print(f"Bounding box: {LAT_MIN:.3f}° to {LAT_MAX:.3f}°N, {LON_MIN:.3f}° to {LON_MAX:.3f}°W")

    print("\nSentinel-2 Coverage:")
    print("  - Resolution: 10m (multispectral)")
    print("  - Revisit time: 5 days (with both satellites)")
    print("  - Coverage: Global (83°N to 56°S)")
    print("  - Your area IS covered by Sentinel-2")

    print("\nDownload Sources:")
    print("  1. Copernicus Data Space Ecosystem: https://dataspace.copernicus.eu/")
    print("  2. USGS Sentinel2Look Viewer: https://landsatlook.usgs.gov/sentinel2/viewer.html")
    print("  3. Google Earth Engine (requires account)")

    print("\nNote: Direct download requires authentication and manual tile selection.")
    print("Consider using Google Earth Engine Python API for programmatic access.")

def main():
    """Main execution function."""
    print("="*80)
    print("TREASURE HUNT - ELEVATION & SATELLITE DATA COLLECTOR")
    print("="*80)
    print(f"\nSearch Area:")
    print(f"  Center: {CENTER_LAT}°N, {CENTER_LON}°W (Asheville, NC)")
    print(f"  Radius: {RADIUS_MILES} miles")
    print(f"  Region: Blue Ridge Mountains")
    print(f"\nBounding Box:")
    print(f"  Latitude: {LAT_MIN:.3f}° to {LAT_MAX:.3f}°N")
    print(f"  Longitude: {LON_MIN:.3f}° to {LON_MAX:.3f}°W")

    # Create directories
    ELEVATION_DIR.mkdir(parents=True, exist_ok=True)
    SATELLITE_DIR.mkdir(parents=True, exist_ok=True)

    # Get elevation profile
    get_elevation_profile()

    # Get USGS 3DEP metadata
    usgs_metadata = download_usgs_3dep_metadata()

    # Get Sentinel-2 info
    get_sentinel2_info()

    # SRTM info
    print("\n" + "="*80)
    print("SRTM ELEVATION DATA")
    print("="*80)
    download_srtm_elevation()

    print("\n" + "="*80)
    print("DATA COLLECTION SUMMARY")
    print("="*80)
    print("\nFiles created:")
    print(f"  - {ELEVATION_DIR / 'elevation_samples.json'}")
    print(f"  - {ELEVATION_DIR / 'usgs_3dep_metadata.json'}")
    print("\nFor full resolution data, you'll need to:")
    print("  1. Visit The National Map: https://apps.nationalmap.gov/downloader/")
    print("  2. Select 'Elevation Products (3DEP)'")
    print("  3. Draw your search area or enter coordinates")
    print("  4. Download 1m or 1/3 arc-second DEM tiles")

if __name__ == "__main__":
    main()
