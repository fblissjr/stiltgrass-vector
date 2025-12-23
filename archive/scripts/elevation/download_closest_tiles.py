#!/usr/bin/env python3
"""
Download DEM tiles closest to the search area center.
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


def find_closest_tiles(max_tiles: int = 3) -> List[Dict]:
    """Find the closest DEM tiles to the center point."""
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    tiles_with_distance = []

    for item in metadata["items"]:
        bbox = item["boundingBox"]

        # Calculate distance to tile center
        tile_center_lat = (bbox["minY"] + bbox["maxY"]) / 2
        tile_center_lon = (bbox["minX"] + bbox["maxX"]) / 2

        distance = (
            (tile_center_lat - CENTER_LAT) ** 2 + (tile_center_lon - CENTER_LON) ** 2
        ) ** 0.5

        # Check if center point overlaps with tile (with small buffer)
        overlaps = (
            bbox["minX"] - 0.05 <= CENTER_LON <= bbox["maxX"] + 0.05
            and bbox["minY"] - 0.05 <= CENTER_LAT <= bbox["maxY"] + 0.05
        )

        tiles_with_distance.append(
            {"item": item, "distance": distance, "overlaps": overlaps}
        )

    # Sort by distance
    tiles_with_distance.sort(key=lambda x: x["distance"])

    return tiles_with_distance[:max_tiles]


def download_tile(url: str, filename: str) -> bool:
    """Download a single DEM tile."""
    filepath = ELEVATION_DIR / filename

    if filepath.exists():
        print(f"  Already exists: {filename}")
        return True

    print(f"  Downloading: {filename}")

    try:
        response = requests.get(url, stream=True, timeout=180)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        print(
            f"  Downloaded: {filepath.name} ({filepath.stat().st_size / (1024 * 1024):.1f} MB)"
        )
        return True

    except Exception as e:
        print(f"  Error downloading {filename}: {e}")
        if filepath.exists():
            filepath.unlink()
        return False


def main():
    """Download the closest DEM tiles."""
    print("=" * 80)
    print("DEM TILE DOWNLOADER")
    print("=" * 80)
    print(f"\nSearch area center: {CENTER_LAT}°N, {CENTER_LON}°W\n")

    tiles = find_closest_tiles(max_tiles=3)

    print(f"Downloading {len(tiles)} closest DEM tiles:\n")

    for i, tile_info in enumerate(tiles, 1):
        item = tile_info["item"]
        bbox = item["boundingBox"]

        print(f"\n{'=' * 80}")
        print(f"TILE {i}: {item['title']}")
        print(f"{'=' * 80}")
        print(f"Distance from center: {tile_info['distance']:.4f}°")
        print(f"Bounding box:")
        print(f"  Latitude:  {bbox['minY']:.4f}° to {bbox['maxY']:.4f}°N")
        print(f"  Longitude: {bbox['minX']:.4f}° to {bbox['maxX']:.4f}°W")
        print(f"Resolution: 1 meter")
        print(f"Size: {item['sizeInBytes'] / (1024 * 1024):.1f} MB")
        print(f"Publication date: {item['publicationDate']}")
        print()

        # Download the tile
        filename = item["downloadURL"].split("/")[-1]
        success = download_tile(item["downloadURL"], filename)

        if success:
            # Also download preview image
            if "previewGraphicURL" in item and item["previewGraphicURL"]:
                preview_filename = item["previewGraphicURL"].split("/")[-1]
                print(f"  Downloading preview: {preview_filename}")
                try:
                    preview_response = requests.get(
                        item["previewGraphicURL"], timeout=30
                    )
                    preview_response.raise_for_status()
                    with open(ELEVATION_DIR / preview_filename, "wb") as f:
                        f.write(preview_response.content)
                    print(f"  Preview downloaded: {preview_filename}")
                except Exception as e:
                    print(f"  Could not download preview: {e}")

    print("\n" + "=" * 80)
    print("DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"\nFiles saved to: {ELEVATION_DIR}")


if __name__ == "__main__":
    main()
