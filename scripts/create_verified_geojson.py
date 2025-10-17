#!/usr/bin/env python3
"""
Create GeoJSON file for verified public trails by extracting coordinates from KML.
"""

import xml.etree.ElementTree as ET
import pandas as pd
import json
from pathlib import Path
import re

def parse_kml_description(description):
    """Parse CDATA description field to extract OSM tags."""
    tags = {}
    cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', description, re.DOTALL)
    if not cdata_match:
        return tags

    cdata_content = cdata_match.group(1)
    tag_pattern = r'<b>(.*?):</b>\s*(.*?)(?:<br/>|$)'
    matches = re.findall(tag_pattern, cdata_content)

    for key, value in matches:
        tags[key.strip()] = value.strip()

    return tags

def parse_coordinates(coord_string):
    """Parse KML coordinate string into list of [lon, lat] pairs."""
    if not coord_string:
        return []

    coords = []
    points = coord_string.strip().split()
    for point in points:
        parts = point.split(',')
        if len(parts) >= 2:
            lon, lat = float(parts[0]), float(parts[1])
            coords.append([lon, lat])
    return coords

def create_geojson_from_kml(kml_path, verified_csv_path, output_path):
    """Create GeoJSON from KML for verified trails."""
    # Load verified trails
    verified_df = pd.read_csv(verified_csv_path)
    verified_osm_ids = set(verified_df['osm_id'].astype(str))

    # Parse KML
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    features = []

    for placemark in root.findall('.//kml:Placemark', ns):
        name_elem = placemark.find('kml:name', ns)
        desc_elem = placemark.find('kml:description', ns)
        linestring_elem = placemark.find('.//kml:LineString/kml:coordinates', ns)

        if name_elem is None or desc_elem is None or linestring_elem is None:
            continue

        # Parse tags
        tags = parse_kml_description(desc_elem.text)
        osm_id = tags.get('OSM ID', '')

        # Only include verified trails
        if osm_id not in verified_osm_ids:
            continue

        # Get trail info from verified df
        trail_info = verified_df[verified_df['osm_id'].astype(str) == osm_id].iloc[0]

        # Parse coordinates
        coordinates = parse_coordinates(linestring_elem.text)

        if not coordinates:
            continue

        # Create GeoJSON feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {
                "trail_name": trail_info['trail_name'],
                "osm_id": osm_id,
                "rank": int(trail_info['new_rank']),
                "total_score": int(trail_info['total_score']),
                "distance_miles": float(trail_info['distance_miles']),
                "surface": trail_info['surface'],
                "difficulty": trail_info['difficulty'],
                "highway_type": trail_info['highway_type'],
                "county": trail_info['county'],
                "ref": trail_info['ref'] if pd.notna(trail_info['ref']) else None,
                "access_category": trail_info['access_category'],
                "foot": tags.get('foot', ''),
                "bicycle": tags.get('bicycle', ''),
                "horse": tags.get('horse', ''),
            }
        }

        features.append(feature)

    # Create GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Save
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Created GeoJSON with {len(features)} trails")
    return geojson

def main():
    base_dir = Path('/Users/fredbliss/workspace/treasure')
    kml_path = base_dir / 'trails.kml'
    verified_csv = base_dir / 'data' / 'top_20_verified.csv'
    output_path = base_dir / 'data' / 'top_20_verified.geojson'

    create_geojson_from_kml(kml_path, verified_csv, output_path)
    print(f"Saved GeoJSON to {output_path}")

if __name__ == '__main__':
    main()
