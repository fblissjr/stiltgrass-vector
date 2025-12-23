#!/usr/bin/env python3
"""
Calculate drive times from Charlotte to major trailheads in Pisgah/Asheville area
Uses simple distance calculations and typical mountain driving speeds
"""

import csv
import math

# Charlotte coordinates
CHARLOTTE = (35.227, -80.843)

# Major trailheads with coordinates
TRAILHEADS = [
    {
        "name": "Looking Glass Rock Trailhead",
        "lat": 35.290991,
        "lon": -82.776671,
        "elevation_gain": "moderate",
        "access_road": "US 276 + FR 475",
        "popularity": "high",
    },
    {
        "name": "Graveyard Fields Trailhead",
        "lat": 35.320310,
        "lon": -82.847057,
        "elevation_gain": "low",
        "access_road": "Blue Ridge Parkway MP 418.8",
        "popularity": "very high",
    },
    {
        "name": "Mount Pisgah Trailhead",
        "lat": 35.40278,
        "lon": -82.75667,
        "elevation_gain": "moderate",
        "access_road": "Blue Ridge Parkway MP 407.6",
        "popularity": "very high",
    },
    {
        "name": "Bent Creek - Hard Times Trailhead",
        "lat": 35.500,
        "lon": -82.600,  # Approximate - south Asheville
        "elevation_gain": "low",
        "access_road": "I-26 to NC 191 to Bent Creek Ranch Rd",
        "popularity": "high",
    },
    {
        "name": "Craggy Gardens",
        "lat": 35.700,
        "lon": -82.380,  # Approximate - BRP MP 364-365
        "elevation_gain": "moderate",
        "access_road": "Blue Ridge Parkway MP 364-365",
        "popularity": "very high",
    },
    {
        "name": "Craggy Pinnacle",
        "lat": 35.698,
        "lon": -82.380,  # Approximate - BRP MP 364.1
        "elevation_gain": "moderate",
        "access_road": "Blue Ridge Parkway MP 364.1",
        "popularity": "high",
    },
    {
        "name": "Downtown Asheville",
        "lat": 35.595,
        "lon": -82.551,
        "elevation_gain": "n/a",
        "access_road": "I-40",
        "popularity": "reference point",
    },
]


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance between two points in miles"""
    R = 3959  # Earth's radius in miles

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def estimate_drive_time(distance_miles, route_type="interstate"):
    """
    Estimate drive time based on distance and route type

    Route types:
    - interstate: I-40 corridor, average 65 mph
    - highway: US highways, average 55 mph
    - mountain: Blue Ridge Parkway, average 40 mph
    - mixed: typical route mix, average 50 mph
    """
    speeds = {"interstate": 65, "highway": 55, "mountain": 40, "mixed": 50}

    speed = speeds.get(route_type, 50)
    time_hours = distance_miles / speed

    # Add time for stops, traffic, etc (15% buffer)
    time_hours *= 1.15

    return time_hours


def categorize_route(trailhead):
    """Determine route type based on access road"""
    access = trailhead.get("access_road", "").lower()

    if "blue ridge parkway" in access or "brp" in access:
        return "mountain"
    elif "i-40" in access or "i-26" in access:
        return "interstate"
    elif "us" in access:
        return "highway"
    else:
        return "mixed"


def main():
    results = []

    print("Calculating drive times from Charlotte to Pisgah/Asheville trailheads...")
    print(f"Charlotte: {CHARLOTTE[0]:.4f}°N, {CHARLOTTE[1]:.4f}°W\n")

    for trailhead in TRAILHEADS:
        # Calculate straight-line distance
        straight_distance = haversine_distance(
            CHARLOTTE[0], CHARLOTTE[1], trailhead["lat"], trailhead["lon"]
        )

        # Estimate actual driving distance (typically 1.3-1.5x straight line in mountains)
        driving_distance = straight_distance * 1.35

        # Determine route type
        route_type = categorize_route(trailhead)

        # Calculate drive time
        drive_time_hours = estimate_drive_time(driving_distance, route_type)
        drive_time_minutes = drive_time_hours * 60

        result = {
            "trailhead": trailhead["name"],
            "latitude": trailhead["lat"],
            "longitude": trailhead["lon"],
            "straight_distance_miles": round(straight_distance, 1),
            "estimated_driving_distance_miles": round(driving_distance, 1),
            "estimated_drive_time_hours": round(drive_time_hours, 2),
            "estimated_drive_time_minutes": round(drive_time_minutes, 0),
            "route_type": route_type,
            "access_road": trailhead["access_road"],
            "popularity": trailhead["popularity"],
        }

        results.append(result)

        # Print result
        hours = int(drive_time_hours)
        minutes = int((drive_time_hours - hours) * 60)
        print(
            f"{trailhead['name']:35s} | {driving_distance:5.1f} mi | {hours}h {minutes:02d}m | {route_type}"
        )

    # Sort by drive time
    results.sort(key=lambda x: x["estimated_drive_time_hours"])

    # Write to CSV
    output_file = "data/drive_times.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults written to: {output_file}")

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Closest trailhead: {results[0]['trailhead']}")
    print(f"  Distance: {results[0]['estimated_driving_distance_miles']} miles")
    print(
        f"  Time: {int(results[0]['estimated_drive_time_hours'])}h {int((results[0]['estimated_drive_time_hours'] % 1) * 60)}m"
    )
    print(f"\nFarthest trailhead: {results[-1]['trailhead']}")
    print(f"  Distance: {results[-1]['estimated_driving_distance_miles']} miles")
    print(
        f"  Time: {int(results[-1]['estimated_drive_time_hours'])}h {int((results[-1]['estimated_drive_time_hours'] % 1) * 60)}m"
    )

    # Show 1-3 hour range
    print("\n=== TRAILHEADS WITHIN 1-3 HOUR DRIVE FROM CHARLOTTE ===")
    for r in results:
        if 1.0 <= r["estimated_drive_time_hours"] <= 3.0:
            hours = int(r["estimated_drive_time_hours"])
            minutes = int((r["estimated_drive_time_hours"] - hours) * 60)
            print(
                f"  {r['trailhead']:35s} | {hours}h {minutes:02d}m | {r['popularity']:10s}"
            )


if __name__ == "__main__":
    main()
