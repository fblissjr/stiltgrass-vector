#!/usr/bin/env python3
"""
Quick Satellite Image Downloader
Downloads satellite tiles for top trail candidates
No API key required - uses open ESRI World Imagery
"""

import time
from io import BytesIO
from pathlib import Path

import numpy as np
import requests
from PIL import Image

OUTPUT_DIR = Path("data/satellite_imagery")
OUTPUT_DIR.mkdir(exist_ok=True)

# Top trail coordinates (from analysis)
TRAILS = [
    {"name": "Bent_Creek_Trail", "lat": 35.4999, "lon": -82.6031, "rank": 1},
    {"name": "Old_Trestle_Road_Seg1", "lat": 35.6397, "lon": -82.2944, "rank": 2},
    {"name": "Old_Trestle_Road_Seg2", "lat": 35.6390, "lon": -82.2950, "rank": 3},
    {"name": "Rainbow_Road", "lat": 35.639, "lon": -82.294, "rank": 4},
    {"name": "Old_Trestle_Road_Seg3", "lat": 35.640, "lon": -82.295, "rank": 5},
]


def deg2num(lat_deg, lon_deg, zoom):
    """Convert lat/lon to tile coordinates"""
    lat_rad = np.radians(lat_deg)
    n = 2.0**zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n
    )
    return (xtile, ytile)


def download_tile(lat, lon, zoom=17):
    """Download satellite tile from ESRI World Imagery"""
    x, y = deg2num(lat, lon, zoom)

    # ESRI World Imagery (free, no API key)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"  Error: {e}")

    return None


def download_multi_tile(lat, lon, zoom=17, tile_range=1):
    """Download multiple tiles and stitch together for larger view"""
    center_x, center_y = deg2num(lat, lon, zoom)

    tiles = []
    for dy in range(-tile_range, tile_range + 1):
        row = []
        for dx in range(-tile_range, tile_range + 1):
            x = center_x + dx
            y = center_y + dy

            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    row.append(Image.open(BytesIO(response.content)))
                else:
                    row.append(None)
            except:
                row.append(None)

            time.sleep(0.2)  # Rate limiting

        tiles.append(row)

    # Stitch tiles together
    if tiles and tiles[0] and tiles[0][0]:
        tile_size = tiles[0][0].size[0]
        full_size = tile_size * (2 * tile_range + 1)

        result = Image.new("RGB", (full_size, full_size))

        for i, row in enumerate(tiles):
            for j, tile in enumerate(row):
                if tile:
                    result.paste(tile, (j * tile_size, i * tile_size))

        return result

    return None


def main():
    print("=== Quick Satellite Image Download ===\n")
    print("Downloading from ESRI World Imagery (free, no API key required)\n")

    for trail in TRAILS:
        print(f"Rank {trail['rank']}: {trail['name']}")
        print(f"  Location: {trail['lat']:.4f}, {trail['lon']:.4f}")

        # Download single tile (256x256 @ zoom 17)
        print("  Downloading single tile...")
        img = download_tile(trail["lat"], trail["lon"], zoom=17)

        if img:
            output_file = OUTPUT_DIR / f"rank{trail['rank']}_{trail['name']}_single.jpg"
            img.save(output_file)
            print(f"  ✓ Saved: {output_file}")

        # Download 3x3 tile grid for larger view
        print("  Downloading 3x3 tile grid (larger view)...")
        img_large = download_multi_tile(
            trail["lat"], trail["lon"], zoom=17, tile_range=1
        )

        if img_large:
            output_file = OUTPUT_DIR / f"rank{trail['rank']}_{trail['name']}_3x3.jpg"
            img_large.save(output_file)
            print(f"  ✓ Saved: {output_file}")

        print()
        time.sleep(1)

    print("=== Download Complete ===")
    print(f"\nImages saved to: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Open images in data/satellite_imagery/")
    print("2. Look for brown/tan trails through green forest")
    print("3. Compare to aerial photos 04-06.jpg")
    print("4. Rate trails: HIGH/MEDIUM/LOW confidence")


if __name__ == "__main__":
    main()
