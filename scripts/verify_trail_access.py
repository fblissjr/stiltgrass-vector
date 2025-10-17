#!/usr/bin/env python3
"""
Comprehensive trail verification script to identify access restrictions
and filter out private trails from the candidate list.
"""

import xml.etree.ElementTree as ET
import pandas as pd
import re
from pathlib import Path
import json

def parse_kml_description(description):
    """Parse CDATA description field to extract OSM tags."""
    tags = {}

    # Extract CDATA content
    cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', description, re.DOTALL)
    if not cdata_match:
        return tags

    cdata_content = cdata_match.group(1)

    # Parse each tag from the HTML-encoded format
    # Format: <b>tag_name:</b> tag_value<br/>
    tag_pattern = r'<b>(.*?):</b>\s*(.*?)(?:<br/>|$)'
    matches = re.findall(tag_pattern, cdata_content)

    for key, value in matches:
        tags[key.strip()] = value.strip()

    return tags

def parse_kml_file(kml_path):
    """Parse KML file and extract trail information with all tags."""
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Define namespace
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    trails = []

    for placemark in root.findall('.//kml:Placemark', ns):
        name_elem = placemark.find('kml:name', ns)
        desc_elem = placemark.find('kml:description', ns)

        if name_elem is None or desc_elem is None:
            continue

        trail_name = name_elem.text
        description = desc_elem.text

        # Parse tags from description
        tags = parse_kml_description(description)

        if 'OSM ID' not in tags:
            continue

        trail_info = {
            'trail_name': trail_name,
            'osm_id': tags.get('OSM ID', ''),
            'access': tags.get('access', ''),
            'motor_vehicle': tags.get('motor_vehicle', ''),
            'foot': tags.get('foot', ''),
            'bicycle': tags.get('bicycle', ''),
            'horse': tags.get('horse', ''),
            'highway': tags.get('highway', ''),
            'surface': tags.get('surface', ''),
            'tracktype': tags.get('tracktype', ''),
            'ref': tags.get('ref', ''),
            'tiger:county': tags.get('tiger:county', ''),
            'sac_scale': tags.get('sac_scale', ''),
        }

        trails.append(trail_info)

    return pd.DataFrame(trails)

def identify_access_restrictions(df):
    """Identify trails with access restrictions."""
    # Flag trails with various access restrictions
    df['has_private_access'] = df['access'] == 'private'
    df['has_private_motor_vehicle'] = df['motor_vehicle'] == 'private'
    df['has_any_restriction'] = df['has_private_access'] | df['has_private_motor_vehicle']

    # Categorize access level
    def categorize_access(row):
        if row['access'] == 'private':
            return 'PRIVATE'
        elif row['motor_vehicle'] == 'private' and row['foot'] in ['yes', 'designated']:
            return 'FOOT_ONLY'
        elif row['motor_vehicle'] == 'private':
            return 'NO_MOTOR_VEHICLE'
        elif row['foot'] == 'designated':
            return 'PUBLIC_DESIGNATED'
        elif row['access'] == 'yes' or row['access'] == 'permissive':
            return 'PUBLIC'
        else:
            return 'UNKNOWN'

    df['access_category'] = df.apply(categorize_access, axis=1)

    return df

def main():
    # Paths
    base_dir = Path('/Users/fredbliss/workspace/treasure')
    kml_path = base_dir / 'trails.kml'
    top_20_path = base_dir / 'data' / 'final_top_20.csv'
    output_dir = base_dir / 'data'
    output_dir.mkdir(exist_ok=True)

    print("Step 1: Parsing KML file...")
    kml_df = parse_kml_file(kml_path)
    print(f"Parsed {len(kml_df)} trails from KML")

    print("\nStep 2: Identifying access restrictions...")
    kml_df = identify_access_restrictions(kml_df)

    # Statistics
    total_trails = len(kml_df)
    private_access = kml_df['has_private_access'].sum()
    private_motor_vehicle = kml_df['has_private_motor_vehicle'].sum()
    any_restriction = kml_df['has_any_restriction'].sum()

    print(f"\nAccess Statistics:")
    print(f"  Total trails: {total_trails}")
    print(f"  Trails with access=private: {private_access} ({private_access/total_trails*100:.1f}%)")
    print(f"  Trails with motor_vehicle=private: {private_motor_vehicle} ({private_motor_vehicle/total_trails*100:.1f}%)")
    print(f"  Trails with any restriction: {any_restriction} ({any_restriction/total_trails*100:.1f}%)")

    print("\nAccess categories:")
    print(kml_df['access_category'].value_counts())

    # Save trails with restrictions
    restricted_df = kml_df[kml_df['has_any_restriction']]
    restricted_path = output_dir / 'private_trails_flagged.csv'
    restricted_df.to_csv(restricted_path, index=False)
    print(f"\nSaved {len(restricted_df)} restricted trails to {restricted_path}")

    print("\nStep 3: Loading top 20 candidates...")
    top_20_df = pd.read_csv(top_20_path)
    print(f"Loaded {len(top_20_df)} top candidates")

    # Merge with access information
    print("\nStep 4: Cross-referencing top candidates with access tags...")
    top_20_df['osm_id'] = top_20_df['osm_id'].astype(str)
    kml_df['osm_id'] = kml_df['osm_id'].astype(str)

    merged_df = top_20_df.merge(
        kml_df[['osm_id', 'access', 'motor_vehicle', 'foot', 'bicycle', 'access_category', 'has_any_restriction']],
        on='osm_id',
        how='left'
    )

    # Check for access issues in top 20
    print("\nTop 20 candidates with access restrictions:")
    restricted_top = merged_df[merged_df['has_any_restriction'] == True]
    if len(restricted_top) > 0:
        print(restricted_top[['trail_name', 'osm_id', 'total_score', 'access', 'motor_vehicle', 'access_category']])
    else:
        print("None found")

    # Filter out trails with full private access (not just motor vehicle)
    print("\nStep 5: Filtering out PRIVATE access trails...")
    public_df = merged_df[merged_df['access_category'] != 'PRIVATE']

    removed_count = len(merged_df) - len(public_df)
    print(f"Removed {removed_count} trails with private access")

    if removed_count > 0:
        print("\nRemoved trails:")
        removed = merged_df[merged_df['access_category'] == 'PRIVATE']
        print(removed[['trail_name', 'osm_id', 'total_score', 'access', 'motor_vehicle']])

    # Re-rank remaining trails
    print("\nStep 6: Re-ranking remaining trails...")
    public_df = public_df.sort_values('total_score', ascending=False).reset_index(drop=True)
    public_df.insert(0, 'new_rank', range(1, len(public_df) + 1))

    # Save verified public trails
    verified_path = output_dir / 'public_trails_verified.csv'
    public_df.to_csv(verified_path, index=False)
    print(f"\nSaved {len(public_df)} verified public trails to {verified_path}")

    # Save updated top 20
    top_20_verified = public_df.head(20)
    top_20_verified_path = output_dir / 'top_20_verified.csv'
    top_20_verified.to_csv(top_20_verified_path, index=False)
    print(f"Saved updated top 20 to {top_20_verified_path}")

    print("\n" + "="*80)
    print("NEW TOP 10 AFTER REMOVING PRIVATE TRAILS:")
    print("="*80)
    for idx, row in top_20_verified.head(10).iterrows():
        print(f"\n{row['new_rank']}. {row['trail_name']} (OSM ID: {row['osm_id']})")
        print(f"   Score: {row['total_score']}")
        print(f"   Access: {row['access_category']}")
        print(f"   Distance: {row['distance_miles']:.2f} miles")
        print(f"   Surface: {row['surface']}, Difficulty: {row['difficulty']}")
        if pd.notna(row['ref']):
            print(f"   Ref: {row['ref']}")

if __name__ == '__main__':
    main()
