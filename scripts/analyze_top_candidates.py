#!/usr/bin/env python3
"""
Analyze geographic clustering and patterns in top candidates
"""

import json
import csv
from collections import defaultdict

# Load top candidates
with open('/Users/fredbliss/workspace/treasure/data/top_50_candidates.csv', 'r') as f:
    reader = csv.DictReader(f)
    candidates = list(reader)

# Analyze geographic clustering
clusters = defaultdict(list)

for c in candidates:
    lat = float(c['latitude'])
    lon = float(c['longitude'])

    # Round to 2 decimal places to identify clusters
    cluster_key = f"{lat:.2f},{lon:.2f}"
    clusters[cluster_key].append(c)

print("Geographic Clustering Analysis")
print("=" * 60)
print()

# Sort clusters by size
sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

print(f"Found {len(sorted_clusters)} distinct geographic clusters")
print()

print("Top 5 Largest Clusters:")
print("-" * 60)

for i, (cluster_key, trails) in enumerate(sorted_clusters[:5], 1):
    lat, lon = cluster_key.split(',')
    print(f"\nCluster {i}: {lat}, {lon}")
    print(f"  Trails: {len(trails)}")
    print(f"  Average score: {sum(int(t['score']) for t in trails) / len(trails):.1f}")
    print(f"  Drive time: ~{trails[0]['drive_time_min']} min")
    print(f"  Elevation: ~{trails[0]['elevation_ft']} ft")

    # List first few trail names
    named_trails = [t['name'] for t in trails if not t['name'].startswith('Trail ')]
    if named_trails:
        print(f"  Named trails: {', '.join(named_trails[:3])}")

print()
print()

# Analyze elevation distribution
print("Elevation Distribution:")
print("-" * 60)

elevation_bins = defaultdict(int)
for c in candidates:
    elev = int(float(c['elevation_ft']))
    bin_key = (elev // 500) * 500
    elevation_bins[bin_key] += 1

for bin_key in sorted(elevation_bins.keys()):
    print(f"  {bin_key}-{bin_key+499} ft: {elevation_bins[bin_key]} trails")

print()
print()

# Analyze score distribution
print("Score Distribution:")
print("-" * 60)

score_bins = defaultdict(int)
for c in candidates:
    score = int(c['score'])
    score_bins[score] = score_bins.get(score, 0) + 1

for score in sorted(score_bins.keys(), reverse=True):
    print(f"  Score {score}: {score_bins[score]} trails")

print()
print()

# Analyze surface types
print("Surface Type Distribution (Top 50):")
print("-" * 60)

surface_counts = defaultdict(int)
for c in candidates:
    surface_counts[c['surface']] += 1

for surface in sorted(surface_counts.keys(), key=lambda x: surface_counts[x], reverse=True):
    print(f"  {surface}: {surface_counts[surface]} trails")

print()
print()

# Key insights
print("KEY INSIGHTS:")
print("-" * 60)

# Top cluster
top_cluster = sorted_clusters[0]
top_lat, top_lon = top_cluster[0].split(',')
print(f"1. MAJOR CONCENTRATION near {top_lat}, {top_lon}")
print(f"   - {len(top_cluster[1])} of top 50 candidates in this area")
print(f"   - Likely a specific trail system or recreation area")

# Elevation pattern
most_common_elev = max(elevation_bins.items(), key=lambda x: x[1])
print(f"\n2. ELEVATION SWEET SPOT: {most_common_elev[0]}-{most_common_elev[0]+499} ft")
print(f"   - {most_common_elev[1]} of 50 trails in this range")
print(f"   - Matches temperature constraint (55°F at night)")

# Surface preference
most_common_surface = max(surface_counts.items(), key=lambda x: x[1])
print(f"\n3. SURFACE TYPE: {most_common_surface[0]}")
print(f"   - {most_common_surface[1]} of 50 trails have this surface")
print(f"   - Ideal for treasure concealment")

# Location identification
top_trails = candidates[:5]
avg_lat = sum(float(t['latitude']) for t in top_trails) / len(top_trails)
avg_lon = sum(float(t['longitude']) for t in top_trails) / len(top_trails)

print(f"\n4. TOP 5 CANDIDATES CENTROID: {avg_lat:.4f}, {avg_lon:.4f}")
print(f"   - Research this exact area for trail system identification")
print(f"   - Drive time: {top_trails[0]['drive_time_min']} minutes from Charlotte")
