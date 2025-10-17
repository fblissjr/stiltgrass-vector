#!/usr/bin/env python3
"""
Automated Satellite Imagery Analysis for Treasure Hunt
Downloads and analyzes satellite imagery for top trail candidates
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import requests
from PIL import Image
from io import BytesIO
import cv2
import time

# Paths
DATA_DIR = Path("/Users/fredbliss/workspace/treasure/data")
PHOTO_DIR = Path("/Users/fredbliss/workspace/treasure/photos")
OUTPUT_DIR = DATA_DIR / "satellite_imagery"
CANDIDATES_FILE = DATA_DIR / "top_20_verified.csv"

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

def download_google_static_map(lat, lon, zoom=18, size="640x640", maptype="satellite"):
    """
    Download satellite imagery from Google Static Maps API
    Note: Requires API key for production use, but can try without for testing
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap"

    params = {
        'center': f'{lat},{lon}',
        'zoom': zoom,
        'size': size,
        'maptype': maptype,
        'scale': 2,  # Higher resolution
    }

    # For demo without API key - use a different approach
    # Option 1: Use OpenStreetMap tiles
    # Option 2: Use Sentinel Hub (requires account)
    # Option 3: Use Google Earth Engine (requires setup)

    print(f"Note: Google Static Maps requires API key")
    print(f"Alternative: Manually visit https://www.google.com/maps/@{lat},{lon},{zoom}z/data=!3m1!1e3")
    return None

def download_osm_satellite(lat, lon, zoom=17):
    """
    Download from OpenStreetMap tiles (no API key needed)
    Uses ESRI World Imagery which is free
    """
    # ESRI World Imagery tiles
    # Format: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}

    # Convert lat/lon to tile coordinates
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = np.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n)
        return (xtile, ytile)

    x, y = deg2num(lat, lon, zoom)

    # Download tile
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading tile: {e}")

    return None

def download_sentinel_hub(lat, lon, bbox_size=0.01):
    """
    Download from Sentinel Hub (requires account and API key)
    High quality satellite imagery
    """
    print("Sentinel Hub requires API key - see https://www.sentinel-hub.com/")
    return None

def extract_trail_coordinates(csv_file):
    """
    Extract GPS coordinates from trail data
    Note: Our CSV doesn't have explicit lat/lon columns, need to parse from trails.geojson
    """
    import geopandas as gpd

    # Load GeoJSON with trail geometries
    trails_gj = DATA_DIR / "top_20_verified.geojson"

    if not trails_gj.exists():
        print(f"GeoJSON file not found: {trails_gj}")
        return []

    gdf = gpd.read_file(trails_gj)

    coordinates = []
    for idx, row in gdf.iterrows():
        # Get centroid of trail
        centroid = row.geometry.centroid
        coordinates.append({
            'name': row.get('trail_name', row.get('name', f'Trail {idx+1}')),
            'lat': centroid.y,
            'lon': centroid.x,
            'rank': idx + 1
        })

    return coordinates

def analyze_trail_visibility(sat_image, reference_photos):
    """
    Analyze if trail is visible in satellite imagery
    Compare against aerial photos 4-6 features
    """
    if sat_image is None:
        return {'visible': False, 'confidence': 0, 'num_lines': 0,
                'orientation_match': False, 'color_match': False,
                'brown_percent': 0.0, 'green_percent': 0.0}

    # Convert to numpy array
    sat_np = np.array(sat_image)

    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(sat_np, cv2.COLOR_RGB2GRAY)

    # Edge detection to find linear features
    edges = cv2.Canny(gray, 50, 150)

    # Hough line detection for trails
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                            minLineLength=30, maxLineGap=10)

    if lines is None:
        return {'visible': False, 'confidence': 0, 'num_lines': 0,
                'orientation_match': False, 'color_match': False,
                'brown_percent': 0.0, 'green_percent': 0.0}

    # Analyze line orientations
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2-y1, x2-x1))
        if angle < 0:
            angle += 180
        angles.append(angle)

    # Check for dominant N-S (0-15° or 165-180°) or NW-SE orientations
    ns_angles = [a for a in angles if a < 15 or a > 165]
    nwse_angles = [a for a in angles if 135 < a < 180 or 0 < a < 45]

    matches_orientation = len(ns_angles) > len(angles) * 0.3 or len(nwse_angles) > len(angles) * 0.3

    # Color analysis for brown/tan trail vs green forest
    hsv = cv2.cvtColor(sat_np, cv2.COLOR_RGB2HSV)

    # Brown/tan trail color range
    lower_brown = np.array([10, 50, 50])
    upper_brown = np.array([30, 255, 200])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    brown_percent = np.sum(brown_mask > 0) / brown_mask.size

    # Green forest color range
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_percent = np.sum(green_mask > 0) / green_mask.size

    # Trail should have some brown and lots of green (forest context)
    has_trail_colors = brown_percent > 0.05 and green_percent > 0.4

    # Calculate confidence
    confidence = 0
    if len(lines) > 10:  # Linear features present
        confidence += 30
    if matches_orientation:  # Correct orientation
        confidence += 30
    if has_trail_colors:  # Color match
        confidence += 40

    return {
        'visible': bool(confidence > 50),
        'confidence': int(min(confidence, 100)),
        'num_lines': int(len(lines)),
        'orientation_match': bool(matches_orientation),
        'color_match': bool(has_trail_colors),
        'brown_percent': float(round(brown_percent * 100, 2)),
        'green_percent': float(round(green_percent * 100, 2))
    }

def compare_to_aerial_photos(sat_image, photo_nums=[4, 5, 6]):
    """
    Compare satellite imagery to aerial photos using feature matching
    """
    if sat_image is None:
        return {'match_score': 0}

    sat_np = np.array(sat_image)
    sat_gray = cv2.cvtColor(sat_np, cv2.COLOR_RGB2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=500)
    kp_sat, des_sat = orb.detectAndCompute(sat_gray, None)

    if des_sat is None:
        return {'match_score': 0}

    best_score = 0

    for photo_num in photo_nums:
        photo_path = PHOTO_DIR / f"{photo_num:02d}_aerial.jpg"
        if not photo_path.exists():
            continue

        aerial = cv2.imread(str(photo_path))
        aerial_gray = cv2.cvtColor(aerial, cv2.COLOR_BGR2GRAY)

        # Resize to similar scale
        scale = sat_gray.shape[0] / aerial_gray.shape[0]
        aerial_resized = cv2.resize(aerial_gray, None, fx=scale, fy=scale)

        kp_aerial, des_aerial = orb.detectAndCompute(aerial_resized, None)

        if des_aerial is None:
            continue

        # BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des_sat, des_aerial)

        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Calculate match score
        good_matches = [m for m in matches if m.distance < 50]
        score = len(good_matches) / max(len(kp_sat), len(kp_aerial)) * 100

        best_score = max(best_score, score)

    return {
        'match_score': float(round(best_score, 2)),
        'match_quality': str('HIGH' if best_score > 20 else 'MEDIUM' if best_score > 10 else 'LOW')
    }

def main():
    """
    Main automated analysis pipeline
    """
    print("=== Automated Satellite Imagery Analysis ===\n")

    # Load trail candidates
    print("Loading trail candidates...")
    try:
        coordinates = extract_trail_coordinates(CANDIDATES_FILE)
        print(f"Found {len(coordinates)} trail candidates\n")
    except Exception as e:
        print(f"Error loading coordinates: {e}")
        print("\nManual coordinates for top 3 trails:")
        coordinates = [
            {'name': 'Bent Creek Trail', 'lat': 35.4999, 'lon': -82.6031, 'rank': 1},
            {'name': 'Old Trestle Road Seg1', 'lat': 35.6397, 'lon': -82.2944, 'rank': 2},
            {'name': 'Old Trestle Road Seg2', 'lat': 35.6390, 'lon': -82.2950, 'rank': 3},
        ]

    results = []

    # Analyze top 5 trails
    for trail in coordinates[:5]:
        print(f"\n--- Analyzing: {trail['name']} (Rank {trail['rank']}) ---")
        print(f"Location: {trail['lat']:.4f}, {trail['lon']:.4f}")

        # Try downloading satellite imagery
        print("Downloading satellite imagery...")
        sat_image = download_osm_satellite(trail['lat'], trail['lon'], zoom=17)

        if sat_image:
            # Save image
            output_file = OUTPUT_DIR / f"rank{trail['rank']}_{trail['name'].replace(' ', '_')}_satellite.jpg"
            sat_image.save(output_file)
            print(f"✓ Saved: {output_file}")

            # Analyze visibility
            print("Analyzing trail visibility...")
            visibility = analyze_trail_visibility(sat_image, None)
            print(f"  Visibility: {'YES' if visibility['visible'] else 'NO'}")
            print(f"  Confidence: {visibility['confidence']}%")
            print(f"  Linear features: {visibility['num_lines']}")
            print(f"  Orientation match: {visibility['orientation_match']}")
            print(f"  Color match: {visibility['color_match']}")

            # Compare to aerial photos
            print("Comparing to aerial photos...")
            comparison = compare_to_aerial_photos(sat_image, [4, 5, 6])
            print(f"  Match score: {comparison['match_score']}")
            print(f"  Match quality: {comparison['match_quality']}")

            results.append({
                **trail,
                **visibility,
                **comparison
            })
        else:
            print("✗ Could not download imagery")
            print(f"  Manual check: https://www.google.com/maps/@{trail['lat']},{trail['lon']},17z/data=!3m1!1e3")

        time.sleep(1)  # Rate limiting

    # Save results
    if results:
        results_file = OUTPUT_DIR / "automated_analysis_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to: {results_file}")

        # Create summary
        print("\n=== SUMMARY ===")
        for r in sorted(results, key=lambda x: x['confidence'], reverse=True):
            print(f"\n{r['name']} (Rank {r['rank']}):")
            print(f"  Confidence: {r['confidence']}%")
            print(f"  Match Quality: {r.get('match_quality', 'N/A')}")
            print(f"  Recommendation: {'HIGH PRIORITY' if r['confidence'] > 70 else 'MEDIUM' if r['confidence'] > 50 else 'LOW'}")

    print("\n=== Analysis Complete ===")
    print(f"Images saved to: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Review satellite images in data/satellite_imagery/")
    print("2. Manually verify top candidates in Google Earth")
    print("3. Use automated_analysis_results.json for rankings")

if __name__ == "__main__":
    main()
