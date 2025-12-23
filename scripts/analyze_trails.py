#!/usr/bin/env python3
"""
Trail Data Analyzer - Agent A1
Parses KML trail data and generates comprehensive analysis
"""

import csv
import json
import math
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple

# KML namespace
NS = {"kml": "http://www.opengis.net/kml/2.2"}


def parse_description(description: str) -> Dict[str, str]:
    """Parse the CDATA description field to extract OSM tags"""
    tags = {}
    if not description:
        return tags

    # Extract content from CDATA
    cdata_match = re.search(r"<!\[CDATA\[(.*?)\]\]>", description, re.DOTALL)
    if not cdata_match:
        return tags

    content = cdata_match.group(1)

    # Parse HTML tags
    tag_pattern = r"<b>(.*?):</b>\s*(.*?)(?:<br/>|$)"
    matches = re.findall(tag_pattern, content)

    for key, value in matches:
        tags[key] = value.strip()

    return tags


def parse_coordinates(coord_string: str) -> List[Tuple[float, float]]:
    """Parse KML coordinate string into list of (lon, lat) tuples"""
    coords = []
    for coord in coord_string.strip().split():
        parts = coord.split(",")
        if len(parts) >= 2:
            lon, lat = float(parts[0]), float(parts[1])
            coords.append((lon, lat))
    return coords


def calculate_distance(coords: List[Tuple[float, float]]) -> float:
    """Calculate total distance in miles using Haversine formula"""
    if len(coords) < 2:
        return 0.0

    total_miles = 0.0
    for i in range(len(coords) - 1):
        lon1, lat1 = coords[i]
        lon2, lat2 = coords[i + 1]

        # Haversine formula
        R = 3959  # Earth radius in miles
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        total_miles += R * c

    return total_miles


def extract_county(tags: Dict[str, str]) -> str:
    """Extract county from tiger:county tag"""
    county_raw = tags.get("tiger:county", "Unknown")
    # Parse "Buncombe, NC" -> "Buncombe"
    if "," in county_raw:
        return county_raw.split(",")[0].strip()
    return county_raw


def main():
    print("Starting KML trail data analysis...")
    print(f"Parsing: trails.kml")

    # Parse KML
    tree = ET.parse("trails.kml")
    root = tree.getroot()

    # Storage
    trails = []
    geojson_features = []

    # Statistics
    stats = {
        "total_trails": 0,
        "total_miles": 0.0,
        "named_trails": 0,
        "unnamed_trails": 0,
        "county_counts": Counter(),
        "county_miles": defaultdict(float),
        "highway_types": Counter(),
        "surface_types": Counter(),
        "difficulty_levels": Counter(),
        "forest_service_roads": 0,
        "has_surface_tag": 0,
        "has_difficulty_tag": 0,
    }

    # Parse each Placemark
    for placemark in root.findall(".//kml:Placemark", NS):
        stats["total_trails"] += 1

        # Extract name
        name_elem = placemark.find("kml:name", NS)
        name = (
            name_elem.text
            if name_elem is not None
            else f"Trail {stats['total_trails']}"
        )

        # Extract description (contains OSM tags)
        desc_elem = placemark.find("kml:description", NS)
        description = desc_elem.text if desc_elem is not None else ""
        tags = parse_description(description)

        # Extract coordinates
        linestring = placemark.find(".//kml:LineString/kml:coordinates", NS)
        if linestring is None:
            continue

        coords = parse_coordinates(linestring.text)
        if not coords:
            continue

        # Calculate distance
        distance_miles = calculate_distance(coords)
        stats["total_miles"] += distance_miles

        # Extract metadata
        county = extract_county(tags)
        highway_type = tags.get("highway", "unknown")
        surface = tags.get("surface", "unknown")
        difficulty = tags.get("sac_scale", tags.get("tracktype", "unknown"))
        osm_id = tags.get("OSM ID", "unknown")
        ref = tags.get("ref", "")

        # Update statistics
        stats["county_counts"][county] += 1
        stats["county_miles"][county] += distance_miles
        stats["highway_types"][highway_type] += 1

        if surface != "unknown":
            stats["surface_types"][surface] += 1
            stats["has_surface_tag"] += 1

        if difficulty != "unknown":
            stats["difficulty_levels"][difficulty] += 1
            stats["has_difficulty_tag"] += 1

        if "Trail " in name and name.startswith("Trail "):
            stats["unnamed_trails"] += 1
        else:
            stats["named_trails"] += 1

        if ref and "FS " in ref:
            stats["forest_service_roads"] += 1

        # Build trail record
        trail_record = {
            "name": name,
            "osm_id": osm_id,
            "county": county,
            "distance_miles": round(distance_miles, 3),
            "highway_type": highway_type,
            "surface": surface,
            "difficulty": difficulty,
            "ref": ref,
            "num_coordinates": len(coords),
            "all_tags": tags,
        }
        trails.append(trail_record)

        # Build GeoJSON feature
        geojson_coords = [[lon, lat] for lon, lat in coords]
        feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "osm_id": osm_id,
                "county": county,
                "distance_miles": round(distance_miles, 3),
                "highway_type": highway_type,
                "surface": surface,
                "difficulty": difficulty,
                "ref": ref,
                **tags,  # Include all OSM tags
            },
            "geometry": {"type": "LineString", "coordinates": geojson_coords},
        }
        geojson_features.append(feature)

        # Progress indicator
        if stats["total_trails"] % 1000 == 0:
            print(f"  Processed {stats['total_trails']} trails...")

    print(f"\nParsing complete! Processed {stats['total_trails']} trails")
    print(f"Total trail miles: {stats['total_miles']:.2f}")

    # Sort trails by distance (longest first)
    trails.sort(key=lambda x: x["distance_miles"], reverse=True)

    # Write GeoJSON
    geojson = {"type": "FeatureCollection", "features": geojson_features}

    geojson_path = "data/trails.geojson"
    print(f"\nWriting GeoJSON to: {geojson_path}")
    with open(geojson_path, "w") as f:
        json.dump(geojson, f, indent=2)
    print(f"  GeoJSON written: {len(geojson_features)} features")

    # Write CSV
    csv_path = "data/trails_summary.csv"
    print(f"\nWriting CSV to: {csv_path}")
    with open(csv_path, "w", newline="") as f:
        fieldnames = [
            "name",
            "osm_id",
            "county",
            "distance_miles",
            "highway_type",
            "surface",
            "difficulty",
            "ref",
            "num_coordinates",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for trail in trails:
            row = {k: trail[k] for k in fieldnames}
            writer.writerow(row)
    print(f"  CSV written: {len(trails)} rows")

    # Prepare statistics JSON
    stats_export = {
        "summary": {
            "total_trails": stats["total_trails"],
            "total_miles": round(stats["total_miles"], 2),
            "named_trails": stats["named_trails"],
            "unnamed_trails": stats["unnamed_trails"],
            "forest_service_roads": stats["forest_service_roads"],
            "trails_with_surface_tag": stats["has_surface_tag"],
            "trails_with_difficulty_tag": stats["has_difficulty_tag"],
        },
        "by_county": {
            county: {
                "trail_count": stats["county_counts"][county],
                "total_miles": round(stats["county_miles"][county], 2),
                "avg_miles_per_trail": round(
                    stats["county_miles"][county] / stats["county_counts"][county], 2
                ),
            }
            for county in sorted(stats["county_counts"].keys())
        },
        "by_highway_type": dict(stats["highway_types"].most_common()),
        "by_surface": dict(stats["surface_types"].most_common()),
        "by_difficulty": dict(stats["difficulty_levels"].most_common()),
        "top_10_longest_trails": [
            {
                "name": t["name"],
                "county": t["county"],
                "distance_miles": t["distance_miles"],
                "highway_type": t["highway_type"],
            }
            for t in trails[:10]
        ],
        "buncombe_county_summary": {
            "trail_count": stats["county_counts"]["Buncombe"],
            "total_miles": round(stats["county_miles"]["Buncombe"], 2),
            "percentage_of_total": round(
                100 * stats["county_counts"]["Buncombe"] / stats["total_trails"], 2
            ),
        },
    }

    stats_path = "data/trails_statistics.json"
    print(f"\nWriting statistics to: {stats_path}")
    with open(stats_path, "w") as f:
        json.dump(stats_export, f, indent=2)
    print(f"  Statistics written")

    # Print summary
    print("\n" + "=" * 70)
    print("TRAIL DATA SUMMARY")
    print("=" * 70)
    print(f"\nTotal Trails: {stats['total_trails']:,}")
    print(f"Total Miles: {stats['total_miles']:,.2f}")
    print(
        f"Average Trail Length: {stats['total_miles'] / stats['total_trails']:.2f} miles"
    )
    print(f"\nNamed Trails: {stats['named_trails']:,}")
    print(f"Unnamed Trails: {stats['unnamed_trails']:,}")
    print(f"Forest Service Roads: {stats['forest_service_roads']}")

    print(f"\n--- Top 5 Counties by Trail Count ---")
    for county, count in stats["county_counts"].most_common(5):
        miles = stats["county_miles"][county]
        print(f"  {county}: {count:,} trails ({miles:,.2f} miles)")

    print(f"\n--- Highway Types ---")
    for hwy_type, count in stats["highway_types"].most_common():
        print(f"  {hwy_type}: {count:,} trails")

    print(f"\n--- Top 10 Longest Trails ---")
    for i, trail in enumerate(trails[:10], 1):
        print(
            f"  {i}. {trail['name']} ({trail['county']} County): {trail['distance_miles']:.2f} miles"
        )

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
