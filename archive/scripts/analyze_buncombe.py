#!/usr/bin/env python3
"""
Detailed analysis of Buncombe County trails and investigation of "Unknown" counties
"""

import csv
import json
from collections import Counter

# Load the CSV data
trails = []
with open("data/trails_summary.csv", "r") as f:
    reader = csv.DictReader(f)
    trails = list(reader)

# Filter Buncombe County trails
buncombe_trails = [t for t in trails if t["county"] == "Buncombe"]
unknown_trails = [t for t in trails if t["county"] == "Unknown"]

print("=" * 70)
print("BUNCOMBE COUNTY TRAILS ANALYSIS")
print("=" * 70)

# Sort by distance
buncombe_trails.sort(key=lambda x: float(x["distance_miles"]), reverse=True)

print(f"\nTotal Buncombe County Trails: {len(buncombe_trails)}")
print(f"Total Miles: {sum(float(t['distance_miles']) for t in buncombe_trails):.2f}")

print("\n--- Top 20 Buncombe County Trails by Distance ---")
for i, trail in enumerate(buncombe_trails[:20], 1):
    print(
        f"{i:2d}. {trail['name'][:50]:<50} {trail['distance_miles']:>6} mi | {trail['highway_type']:<8} | {trail['surface']:<12} | {trail['difficulty']}"
    )

# Analyze highway types
highway_types = Counter([t["highway_type"] for t in buncombe_trails])
print("\n--- Buncombe County Highway Types ---")
for hwy_type, count in highway_types.most_common():
    total_miles = sum(
        float(t["distance_miles"])
        for t in buncombe_trails
        if t["highway_type"] == hwy_type
    )
    print(f"  {hwy_type}: {count} trails, {total_miles:.2f} miles")

# Analyze surfaces
surfaces = Counter([t["surface"] for t in buncombe_trails if t["surface"] != "unknown"])
print("\n--- Buncombe County Trail Surfaces ---")
for surface, count in surfaces.most_common():
    print(f"  {surface}: {count} trails")

# Analyze difficulty
difficulties = Counter(
    [t["difficulty"] for t in buncombe_trails if t["difficulty"] != "unknown"]
)
print("\n--- Buncombe County Difficulty Levels ---")
for diff, count in difficulties.most_common():
    print(f"  {diff}: {count} trails")

# Forest Service roads
fs_trails = [t for t in buncombe_trails if t["ref"] and "FS" in t["ref"]]
print(f"\n--- Forest Service Roads in Buncombe County ---")
print(f"Total: {len(fs_trails)}")
for trail in fs_trails[:10]:
    print(
        f"  {trail['name'][:45]:<45} {trail['ref']:<10} {trail['distance_miles']:>6} mi"
    )

print("\n" + "=" * 70)
print("UNKNOWN COUNTY INVESTIGATION")
print("=" * 70)

# Sample some unknown trails to understand why they're unknown
print("\nSample of 'Unknown' County Trails (showing longest):")
unknown_trails.sort(key=lambda x: float(x["distance_miles"]), reverse=True)
for i, trail in enumerate(unknown_trails[:15], 1):
    print(
        f"{i:2d}. {trail['name'][:50]:<50} {trail['distance_miles']:>6} mi | {trail['highway_type']}"
    )

# Check if there are patterns
print("\nHypothesis: 'Unknown' trails might be missing tiger:county tag in OSM data")
print(f"Total Unknown trails: {len(unknown_trails):,}")
print(
    f"Total Unknown miles: {sum(float(t['distance_miles']) for t in unknown_trails):.2f}"
)

print("\n" + "=" * 70)
