#!/usr/bin/env python3
"""
Download specific DEM tiles that cover the center of the search area.
"""

import json
from pathlib import Path
from typing import Dict, List

import requests

BASE_DIR = Path(".")
ELEVATION_DIR = BASE_DIR / "data" / "elevation"
METADATA_FILE = ELEVATION_DIR / "usgs_3dep_metadata.json"

# Search area center
CENTER_LAT = 35.705
CENTER_LON = -82.83


def find_tiles_near_center() -> List[Dict]:
    """Find DEM tiles that cover or are near the center point."""
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    tiles_near_center = []

    for item in metadata["items"]:
        bbox = item["boundingBox"]

        # Check if center point is within this tile
        if (
            bbox["minX"] <= CENTER_LON <= bbox["maxX"]
            and bbox["minY"] <= CENTER_LAT <= bbox["maxY"]
        ):
            distance = 0  # Center is inside tile
            tiles_near_center.append(
                {"item": item, "distance": distance, "contains_center": True}
            )
        else:
            # Calculate approximate distance to tile center
            tile_center_lat = (bbox["minY"] + bbox["maxY"]) / 2
            tile_center_lon = (bbox["minX"] + bbox["maxX"]) / 2

            distance = (
                (tile_center_lat - CENTER_LAT) ** 2
                + (tile_center_lon - CENTER_LON) ** 2
            ) ** 0.5

            tiles_near_center.append(
                {"item": item, "distance": distance, "contains_center": False}
            )

    # Sort by distance
    tiles_near_center.sort(key=lambda x: x["distance"])

    return tiles_near_center


def download_tile(url: str, filename: str) -> bool:
    """Download a single DEM tile."""
    filepath = ELEVATION_DIR / filename

    if filepath.exists():
        print(f"  Already exists: {filename}")
        return True

    print(f"  Downloading: {filename}")
    print(f"    URL: {url}")

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r    Progress: {percent:.1f}%", end="", flush=True)

        print()  # New line after progress
        print(f"  Downloaded successfully: {filepath.name}")
        print(f"  Size: {filepath.stat().st_size / (1024 * 1024):.1f} MB")
        return True

    except Exception as e:
        print(f"  Error downloading {filename}: {e}")
        if filepath.exists():
            filepath.unlink()  # Remove partial download
        return False


def main():
    """Download DEM tiles covering the search area center."""
    print("Finding DEM tiles near search area center...")
    print(f"Center: {CENTER_LAT}°N, {CENTER_LON}°W\n")

    tiles = find_tiles_near_center()

    # Find tiles that contain the center
    center_tiles = [t for t in tiles if t["contains_center"]]

    if center_tiles:
        print(f"Found {len(center_tiles)} tile(s) containing the center point:\n")

        for i, tile_info in enumerate(center_tiles[:5], 1):  # Limit to 5 tiles
            item = tile_info["item"]
            print(f"Tile {i}: {item['title']}")
            print(
                f"  Bounding box: {item['boundingBox']['minY']:.3f}°N to {item['boundingBox']['maxY']:.3f}°N"
            )
            print(
                f"               {item['boundingBox']['minX']:.3f}°W to {item['boundingBox']['maxX']:.3f}°W"
            )
            print(f"  Size: {item['sizeInBytes'] / (1024 * 1024):.1f} MB")
            print(f"  Format: {item['format']}")
            print()

            # Download the tile
            filename = item["downloadURL"].split("/")[-1]
            download_tile(item["downloadURL"], filename)
            print()
    else:
        print("No tiles found containing the center point.")
        print(f"\nClosest tiles:")
        for i, tile_info in enumerate(tiles[:3], 1):
            item = tile_info["item"]
            print(f"\nTile {i}: {item['title']}")
            print(f"  Distance: {tile_info['distance']:.4f}°")
            print(
                f"  Bounding box: {item['boundingBox']['minY']:.3f}°N to {item['boundingBox']['maxY']:.3f}°N"
            )
            print(
                f"               {item['boundingBox']['minX']:.3f}°W to {item['boundingBox']['maxX']:.3f}°W"
            )


if __name__ == "__main__":
    main()
