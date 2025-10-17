#!/usr/bin/env python3
"""
Search Area Analysis for Treasure Hunt
Agent A2: Satellite Imagery & Elevation Data Collector

This script analyzes the Day 8 search area and provides information about:
- Search area boundaries
- Elevation characteristics
- Data source URLs
- File download instructions
"""

import math
from typing import Tuple, Dict, List

# Search area parameters
CENTER_LAT = 35.705  # Day 8 center latitude
CENTER_LON = -82.83  # Day 8 center longitude
RADIUS_MILES = 43.5  # Day 8 radius (87 mile diameter / 2)

def miles_to_degrees(miles: float, latitude: float) -> Tuple[float, float]:
    """
    Convert miles to degrees at a given latitude.
    Returns (lat_degrees, lon_degrees)
    """
    # 1 degree latitude is approximately 69 miles
    lat_degrees = miles / 69.0

    # 1 degree longitude varies by latitude
    # At equator: 69 miles, at poles: 0 miles
    lon_miles_per_degree = 69.0 * math.cos(math.radians(latitude))
    lon_degrees = miles / lon_miles_per_degree if lon_miles_per_degree > 0 else 0

    return lat_degrees, lon_degrees

def calculate_bounding_box() -> Dict[str, float]:
    """Calculate the bounding box for the search area."""
    lat_deg, lon_deg = miles_to_degrees(RADIUS_MILES, CENTER_LAT)

    return {
        'north': CENTER_LAT + lat_deg,
        'south': CENTER_LAT - lat_deg,
        'east': CENTER_LON + lon_deg,
        'west': CENTER_LON - lon_deg,
        'center_lat': CENTER_LAT,
        'center_lon': CENTER_LON
    }

def get_data_sources() -> Dict[str, Dict]:
    """Return information about available data sources."""
    bbox = calculate_bounding_box()

    sources = {
        'satellite_imagery': {
            'NAIP (USGS)': {
                'description': 'National Agriculture Imagery Program - 1m resolution aerial imagery',
                'resolution': '1 meter',
                'url': 'https://earthexplorer.usgs.gov/',
                'update_frequency': '3-year cycle',
                'format': 'GeoTIFF, JPEG2000',
                'notes': 'Highest resolution freely available imagery. Latest NC coverage likely 2021-2023.'
            },
            'Sentinel-2': {
                'description': 'European Space Agency satellite imagery',
                'resolution': '10 meters (visible bands)',
                'url': 'https://dataspace.copernicus.eu/',
                'alternative_url': 'https://apps.sentinel-hub.com/eo-browser/',
                'update_frequency': '5 days (both satellites combined)',
                'format': 'JP2, GeoTIFF',
                'notes': 'Free, recent imagery. Good for general reconnaissance.'
            },
            'Landsat 8/9': {
                'description': 'USGS/NASA satellite imagery',
                'resolution': '30 meters (visible bands), 15m (panchromatic)',
                'url': 'https://earthexplorer.usgs.gov/',
                'update_frequency': '8 days (combined)',
                'format': 'GeoTIFF',
                'notes': 'Long historical record, moderate resolution.'
            },
            'Google Earth': {
                'description': 'Web-based satellite imagery viewer',
                'resolution': 'Varies, often <1m in populated areas',
                'url': f'https://earth.google.com/web/@{CENTER_LAT},{CENTER_LON},1000a,50000d,35y,0h,0t,0r',
                'notes': 'Best for visual reconnaissance, no easy download. Can take screenshots.'
            }
        },
        'elevation_data': {
            'USGS 3DEP 1m': {
                'description': '1-meter resolution lidar-derived DEM',
                'resolution': '1 meter',
                'url': 'https://apps.nationalmap.gov/downloader/',
                'format': 'Cloud Optimized GeoTIFF (COG)',
                'coverage': 'Varies by area, excellent coverage in NC mountains',
                'notes': 'Best available elevation data. Check availability for specific area.'
            },
            'USGS 3DEP 10m': {
                'description': '1/3 arc-second (10m) DEM',
                'resolution': '~10 meters',
                'url': 'https://apps.nationalmap.gov/downloader/',
                'format': 'Cloud Optimized GeoTIFF (COG)',
                'coverage': 'Complete coverage of NC',
                'notes': 'Fallback if 1m not available. Adequate for slope analysis.'
            },
            'SRTM': {
                'description': 'Shuttle Radar Topography Mission',
                'resolution': '30 meters (1 arc-second for USA)',
                'url': 'https://earthexplorer.usgs.gov/',
                'alternative_url': 'https://dwtkns.com/srtm30m/',
                'format': 'GeoTIFF, HGT',
                'notes': 'Global coverage, older data (2000), lower resolution.'
            },
            'OpenTopography': {
                'description': 'High-resolution topography data portal',
                'resolution': 'Varies, often <1m lidar',
                'url': 'https://portal.opentopography.org/',
                'notes': 'Academic/research access. May have high-res lidar for this area.'
            }
        }
    }

    return sources

def print_search_area_info():
    """Print comprehensive information about the search area."""
    bbox = calculate_bounding_box()
    sources = get_data_sources()

    print("=" * 80)
    print("TREASURE HUNT SEARCH AREA ANALYSIS - AGENT A2")
    print("=" * 80)
    print()

    print("SEARCH AREA PARAMETERS:")
    print(f"  Center: {CENTER_LAT}°N, {CENTER_LON}°W")
    print(f"  Radius: {RADIUS_MILES} miles")
    print(f"  Diameter: {RADIUS_MILES * 2} miles")
    print()

    print("BOUNDING BOX (for data downloads):")
    print(f"  North: {bbox['north']:.4f}°")
    print(f"  South: {bbox['south']:.4f}°")
    print(f"  East:  {bbox['east']:.4f}°")
    print(f"  West:  {bbox['west']:.4f}°")
    print()

    area_sq_miles = math.pi * RADIUS_MILES ** 2
    print(f"TOTAL AREA: {area_sq_miles:,.0f} square miles")
    print()

    print("=" * 80)
    print("SATELLITE IMAGERY SOURCES")
    print("=" * 80)
    print()

    for name, info in sources['satellite_imagery'].items():
        print(f"{name}:")
        print(f"  Description: {info['description']}")
        print(f"  Resolution: {info['resolution']}")
        print(f"  URL: {info['url']}")
        if 'alternative_url' in info:
            print(f"  Alternative URL: {info['alternative_url']}")
        if 'update_frequency' in info:
            print(f"  Update Frequency: {info['update_frequency']}")
        print(f"  Format: {info['format']}")
        print(f"  Notes: {info['notes']}")
        print()

    print("=" * 80)
    print("ELEVATION DATA SOURCES")
    print("=" * 80)
    print()

    for name, info in sources['elevation_data'].items():
        print(f"{name}:")
        print(f"  Description: {info['description']}")
        print(f"  Resolution: {info['resolution']}")
        print(f"  URL: {info['url']}")
        if 'alternative_url' in info:
            print(f"  Alternative URL: {info['alternative_url']}")
        if 'coverage' in info:
            print(f"  Coverage: {info['coverage']}")
        print(f"  Format: {info['format']}")
        print(f"  Notes: {info['notes']}")
        print()

    print("=" * 80)
    print("RECOMMENDED DOWNLOAD WORKFLOW")
    print("=" * 80)
    print()
    print("1. SATELLITE IMAGERY (Priority: NAIP):")
    print("   a. Visit https://earthexplorer.usgs.gov/")
    print("   b. Create free USGS account (required for downloads)")
    print(f"   c. Search by coordinates: {CENTER_LAT}, {CENTER_LON}")
    print("   d. Or use polygon: N/S/E/W from bounding box above")
    print("   e. Select 'Aerial Imagery' > 'NAIP'")
    print("   f. Filter by date: 2021-2024 for latest imagery")
    print("   g. Preview tiles, download GeoTIFF format")
    print()
    print("2. ELEVATION DATA (Priority: 3DEP 1m or 10m):")
    print("   a. Visit https://apps.nationalmap.gov/downloader/")
    print("   b. Click 'Elevation Products (3DEP)'")
    print(f"   c. Enter coordinates or draw polygon around {CENTER_LAT}, {CENTER_LON}")
    print("   d. Select '1 meter DEM' first, if not available try '1/3 arc-second DEM'")
    print("   e. Download as Cloud Optimized GeoTIFF")
    print("   f. No account required for download!")
    print()
    print("3. QUICK VISUAL RECONNAISSANCE (Google Earth):")
    print(f"   Visit: https://earth.google.com/web/@{CENTER_LAT},{CENTER_LON},1000a,50000d,35y,0h,0t,0r")
    print("   Take screenshots of interesting areas that match aerial photos")
    print()

    print("=" * 80)
    print("EXPECTED TERRAIN CHARACTERISTICS")
    print("=" * 80)
    print()
    print("Based on coordinates 35.705°N, 82.83°W:")
    print("  - Region: Blue Ridge Mountains, near Asheville, NC")
    print("  - Typical elevation range: 2,000 - 4,500 feet")
    print("  - Terrain: Moderate to steep mountain slopes")
    print("  - Vegetation: Deciduous forest (oak, maple, hickory)")
    print("  - Public lands: Pisgah National Forest, Blue Ridge Parkway area")
    print()
    print("Search area likely includes:")
    print("  - Pisgah National Forest (western portion)")
    print("  - Blue Ridge Parkway corridor")
    print("  - Possible Great Smoky Mountains NP (far western edge)")
    print("  - DuPont State Forest (southern edge)")
    print()

def generate_dem_analysis_info():
    """Generate information about DEM analysis."""
    print("=" * 80)
    print("ELEVATION DATA ANALYSIS PLAN")
    print("=" * 80)
    print()
    print("Once DEM data is downloaded, analyze for:")
    print()
    print("1. ELEVATION RANGE:")
    print("   - Min/max elevation in search area")
    print("   - Histogram of elevation distribution")
    print("   - Identify areas at 2,000-4,000 ft (optimal for treasure location)")
    print()
    print("2. SLOPE ANALYSIS:")
    print("   - Calculate slope (rise/run) for entire area")
    print("   - Filter for moderate slopes (10-30 degrees)")
    print("   - Identify accessible hiking terrain vs. too steep")
    print()
    print("3. ASPECT ANALYSIS (CRITICAL):")
    print("   - Calculate aspect (direction slope faces)")
    print("   - Filter for SOUTH-FACING slopes (135° - 225°)")
    print("   - This eliminates ~50% of search area!")
    print()
    print("4. TERRAIN FEATURES:")
    print("   - Identify ridgelines (local elevation maxima)")
    print("   - Identify valleys and drainages")
    print("   - Look for saddles, benches, and flat areas")
    print()
    print("Python libraries needed:")
    print("   - rasterio: Read/write GeoTIFF files")
    print("   - numpy: Array operations")
    print("   - richdem or scipy: Calculate slope/aspect")
    print("   - matplotlib: Visualization")
    print()

if __name__ == "__main__":
    print_search_area_info()
    generate_dem_analysis_info()

    # Save bounding box to file for later use
    bbox = calculate_bounding_box()

    import json
    with open('/Users/fredbliss/workspace/treasure/data/search_area_bbox.json', 'w') as f:
        json.dump(bbox, f, indent=2)

    print("=" * 80)
    print(f"Bounding box saved to: /Users/fredbliss/workspace/treasure/data/search_area_bbox.json")
    print("=" * 80)
