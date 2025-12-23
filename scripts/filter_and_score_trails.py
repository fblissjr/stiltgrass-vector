#!/usr/bin/env python3
"""
Agent C1: Multi-Constraint Filter and Location Scorer
Systematically apply all constraints to 11,954 trail segments
"""

import csv
import json
import sys
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
from typing import Dict, List, Tuple

# Charlotte coordinates (search origin)
CHARLOTTE_LAT = 35.227
CHARLOTTE_LON = -80.843

# Constraint thresholds
MIN_ELEVATION = 3000  # feet
MAX_ELEVATION = 4500  # feet
MIN_DRIVE_TIME = 60  # minutes
MAX_DRIVE_TIME = 180  # minutes

# Scoring weights
SCORE_SURFACE_SUITABLE = 40
SCORE_DIFFICULTY_MODERATE = 30
SCORE_BUNCOMBE_COUNTY = 20
SCORE_STILT_GRASS = 15
SCORE_FOREST_SERVICE = 10
SCORE_NAMED_TRAIL = 10
SCORE_GOOD_CELL_COVERAGE = 10
SCORE_OPTIMAL_ELEVATION = 10

# Suitable surfaces
SUITABLE_SURFACES = {"ground", "gravel", "dirt", "unpaved"}

# Moderate difficulties
MODERATE_DIFFICULTIES = {"grade2", "grade3", "hiking"}

# Buncombe County variations
BUNCOMBE_VARIATIONS = {"buncombe", "buncombe county"}


@dataclass
class TrailScore:
    name: str
    osm_id: str
    score: int
    distance_miles: float
    drive_time_minutes: float
    latitude: float
    longitude: float
    elevation_est: float
    county: str
    surface: str
    difficulty: str
    highway_type: str
    ref: str
    score_breakdown: Dict[str, int]


def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calculate great circle distance in miles"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3959  # Radius of earth in miles
    return c * r


def estimate_drive_time(straight_line_miles: float) -> float:
    """
    Estimate drive time based on straight-line distance.
    Use 1.4x multiplier for mountain roads (more winding than typical 1.3x)
    Assume average speed of 45 mph for mountain roads
    """
    road_miles = straight_line_miles * 1.4
    drive_time_minutes = (road_miles / 45.0) * 60
    return drive_time_minutes


def get_trail_center(coordinates: List[List[float]]) -> Tuple[float, float]:
    """Calculate center point of trail from coordinates"""
    if not coordinates:
        return 0.0, 0.0

    # Simple average of all coordinates
    avg_lon = sum(coord[0] for coord in coordinates) / len(coordinates)
    avg_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    return avg_lat, avg_lon


def estimate_elevation_from_lat_lon(lat: float, lon: float) -> float:
    """
    Rough elevation estimation based on known mountain geography
    More accurate would require DEM data, but this gives reasonable estimates

    Based on Blue Ridge Mountain patterns:
    - Areas north of Asheville (lat > 35.6): generally higher (3000-5000 ft)
    - Closer to Boone area (lat > 36.0): 3000-4500 ft
    - Western areas (lon < -82.0): higher elevations
    """
    base_elevation = 2000

    # Northern areas are higher
    if lat > 36.2:
        base_elevation += 1500  # High country (Boone area)
    elif lat > 35.8:
        base_elevation += 1200  # Northern mountains
    elif lat > 35.5:
        base_elevation += 800  # Asheville area

    # Western areas are higher
    if lon < -82.5:
        base_elevation += 500
    elif lon < -82.0:
        base_elevation += 300

    return base_elevation


def is_forest_service_road(ref: str, name: str) -> bool:
    """Check if trail is a Forest Service road"""
    if not ref and not name:
        return False

    ref_upper = (ref or "").upper()
    name_upper = (name or "").upper()

    # Check for FS, FR, NF patterns
    forest_indicators = ["FS ", "FR ", "NF ", "FOREST SERVICE", "NATIONAL FOREST"]

    for indicator in forest_indicators:
        if indicator in ref_upper or indicator in name_upper:
            return True

    return False


def is_buncombe_county(county: str, lat: float, lon: float) -> bool:
    """
    Check if trail is in Buncombe County
    Use county tag if available, otherwise estimate from coordinates

    Buncombe County approximate bounds:
    - Lat: 35.45 to 35.75
    - Lon: -82.85 to -82.25
    """
    if county and any(var in county.lower() for var in BUNCOMBE_VARIATIONS):
        return True

    # Rough geographic check
    if 35.45 <= lat <= 35.75 and -82.85 <= lon <= -82.25:
        return True

    return False


def has_japanese_stilt_grass_habitat(
    surface: str, difficulty: str, elevation: float
) -> bool:
    """
    Japanese stilt grass (Microstegium vimineum) habitat:
    - Prefers disturbed areas, trail edges
    - Elevations typically below 4000 ft
    - Moist, shaded areas
    - Ground/dirt surfaces more likely
    """
    if elevation > 4000:
        return False

    if surface in {"ground", "dirt", "unpaved"}:
        return True

    if difficulty in {"grade2", "grade3"}:
        return True

    return False


def calculate_cell_coverage_score(lat: float, lon: float, elevation: float) -> int:
    """
    Estimate cellular coverage quality based on location

    Good coverage areas:
    - Near Boone/Blowing Rock (lat > 36.1, lon > -81.8)
    - Ridge tops (higher elevation)
    - Near populated areas

    Poor coverage:
    - Deep valleys
    - Very remote areas
    - Near TN border (lon < -82.8)
    """
    score = 0

    # Boone/Banner Elk area has excellent dual-carrier coverage
    if 36.0 <= lat <= 36.3 and -82.0 <= lon <= -81.6:
        score += 10
    # Asheville area has good coverage
    elif 35.5 <= lat <= 35.7 and -82.7 <= lon <= -82.4:
        score += 8
    # Northern mountains generally good
    elif lat > 35.8:
        score += 6

    # Ridge tops get better signal
    if elevation > 3500:
        score += 2

    # Penalize areas near TN border (known dead zones)
    if lon < -82.8:
        score -= 10

    return max(0, min(score, 10))


def score_trail(feature: Dict) -> TrailScore:
    """Calculate composite score for a trail based on all constraints"""
    props = feature["properties"]
    coords = feature["geometry"]["coordinates"]

    # Extract basic properties
    name = props.get("name", f"Trail {props.get('osm_id', 'Unknown')}")
    osm_id = str(props.get("osm_id", ""))
    county = props.get("county", "Unknown")
    distance_miles = float(props.get("distance_miles", 0))
    surface = props.get("surface", "unknown").lower()
    difficulty = props.get("difficulty", "unknown").lower()
    highway_type = props.get("highway_type", "unknown")
    ref = props.get("ref", "")

    # Calculate center point
    center_lat, center_lon = get_trail_center(coords)

    # Calculate distance and drive time from Charlotte
    straight_distance = haversine_distance(
        CHARLOTTE_LON, CHARLOTTE_LAT, center_lon, center_lat
    )
    drive_time = estimate_drive_time(straight_distance)

    # Estimate elevation
    elevation_est = estimate_elevation_from_lat_lon(center_lat, center_lon)

    # Initialize score and breakdown
    score = 0
    breakdown = {}

    # Apply scoring criteria

    # 1. Surface type (40 points)
    if surface in SUITABLE_SURFACES:
        score += SCORE_SURFACE_SUITABLE
        breakdown["surface"] = SCORE_SURFACE_SUITABLE
    else:
        breakdown["surface"] = 0

    # 2. Difficulty (30 points)
    if difficulty in MODERATE_DIFFICULTIES:
        score += SCORE_DIFFICULTY_MODERATE
        breakdown["difficulty"] = SCORE_DIFFICULTY_MODERATE
    else:
        breakdown["difficulty"] = 0

    # 3. Buncombe County (20 points)
    if is_buncombe_county(county, center_lat, center_lon):
        score += SCORE_BUNCOMBE_COUNTY
        breakdown["buncombe"] = SCORE_BUNCOMBE_COUNTY
    else:
        breakdown["buncombe"] = 0

    # 4. Japanese stilt grass habitat (15 points)
    if has_japanese_stilt_grass_habitat(surface, difficulty, elevation_est):
        score += SCORE_STILT_GRASS
        breakdown["stilt_grass"] = SCORE_STILT_GRASS
    else:
        breakdown["stilt_grass"] = 0

    # 5. Forest Service road (10 points)
    if is_forest_service_road(ref, name):
        score += SCORE_FOREST_SERVICE
        breakdown["forest_service"] = SCORE_FOREST_SERVICE
    else:
        breakdown["forest_service"] = 0

    # 6. Named trail (10 points)
    if name and not name.startswith("Trail ") and name != "unknown":
        score += SCORE_NAMED_TRAIL
        breakdown["named"] = SCORE_NAMED_TRAIL
    else:
        breakdown["named"] = 0

    # 7. Cell coverage (10 points)
    cell_score = calculate_cell_coverage_score(center_lat, center_lon, elevation_est)
    score += cell_score
    breakdown["cell_coverage"] = cell_score

    # 8. Optimal elevation (10 points)
    if MIN_ELEVATION <= elevation_est <= MAX_ELEVATION:
        score += SCORE_OPTIMAL_ELEVATION
        breakdown["elevation"] = SCORE_OPTIMAL_ELEVATION
    else:
        breakdown["elevation"] = 0

    return TrailScore(
        name=name,
        osm_id=osm_id,
        score=score,
        distance_miles=distance_miles,
        drive_time_minutes=drive_time,
        latitude=center_lat,
        longitude=center_lon,
        elevation_est=elevation_est,
        county=county,
        surface=surface,
        difficulty=difficulty,
        highway_type=highway_type,
        ref=ref,
        score_breakdown=breakdown,
    )


def apply_hard_constraints(trail_score: TrailScore) -> bool:
    """
    Check if trail passes all hard constraints
    Returns True if trail should be kept, False if eliminated
    """
    # 1. Elevation constraint (3,000-4,500 ft based on temperature)
    if not (MIN_ELEVATION <= trail_score.elevation_est <= MAX_ELEVATION):
        return False

    # 2. Drive time constraint (1-3 hours from Charlotte)
    if not (MIN_DRIVE_TIME <= trail_score.drive_time_minutes <= MAX_DRIVE_TIME):
        return False

    # 3. Basic cellular coverage (must have some score)
    if trail_score.score_breakdown.get("cell_coverage", 0) < 3:
        return False

    return True


def main():
    print("Agent C1: Multi-Constraint Filter and Location Scorer")
    print("=" * 60)
    print()

    # Load trails data
    print("Loading trails.geojson...")
    with open("data/trails.geojson", "r") as f:
        trails_data = json.load(f)

    total_trails = len(trails_data["features"])
    print(f"Loaded {total_trails:,} trail segments")
    print()

    # Score all trails
    print("Scoring all trails with composite criteria...")
    all_scored_trails = []

    for i, feature in enumerate(trails_data["features"]):
        if (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1:,} / {total_trails:,} trails...")

        trail_score = score_trail(feature)
        all_scored_trails.append(trail_score)

    print(f"  Completed scoring {len(all_scored_trails):,} trails")
    print()

    # Apply hard constraints
    print("Applying hard constraints...")
    filtered_trails = [t for t in all_scored_trails if apply_hard_constraints(t)]

    eliminated_count = total_trails - len(filtered_trails)
    print(f"  Hard constraints eliminated {eliminated_count:,} trails")
    print(f"  {len(filtered_trails):,} trails pass all hard constraints")
    print()

    # Sort by score
    filtered_trails.sort(key=lambda x: x.score, reverse=True)

    # Statistics
    print("Filter Statistics:")
    print(f"  Total trails: {total_trails:,}")
    print(f"  Passed hard constraints: {len(filtered_trails):,}")
    print(f"  Elimination rate: {(eliminated_count / total_trails) * 100:.1f}%")
    print()

    # Top 50 candidates
    top_50 = filtered_trails[:50]

    print("Top 10 Candidates:")
    print("-" * 60)
    for i, trail in enumerate(top_50[:10], 1):
        print(f"{i}. {trail.name}")
        print(
            f"   Score: {trail.score} | Drive time: {trail.drive_time_minutes:.0f} min | Elevation: {trail.elevation_est:.0f} ft"
        )
        print(f"   Location: {trail.latitude:.4f}, {trail.longitude:.4f}")
        print(f"   Surface: {trail.surface} | Difficulty: {trail.difficulty}")
        print()

    # Save filtered trails GeoJSON
    print("Saving filtered trails...")
    filtered_features = []
    for trail_score in filtered_trails:
        # Find original feature
        for feature in trails_data["features"]:
            if str(feature["properties"].get("osm_id", "")) == trail_score.osm_id:
                # Add score to properties
                feature["properties"]["composite_score"] = trail_score.score
                feature["properties"]["drive_time_minutes"] = (
                    trail_score.drive_time_minutes
                )
                feature["properties"]["elevation_est"] = trail_score.elevation_est
                filtered_features.append(feature)
                break

    filtered_geojson = {"type": "FeatureCollection", "features": filtered_features}

    with open("data/filtered_trails.geojson", "w") as f:
        json.dump(filtered_geojson, f, indent=2)
    print(f"  Saved {len(filtered_features):,} trails to filtered_trails.geojson")

    # Save top 50 CSV
    print("Saving top 50 candidates CSV...")
    with open("data/top_50_candidates.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "rank",
                "name",
                "score",
                "osm_id",
                "latitude",
                "longitude",
                "elevation_ft",
                "drive_time_min",
                "distance_miles",
                "county",
                "surface",
                "difficulty",
                "highway_type",
                "ref",
                "score_surface",
                "score_difficulty",
                "score_buncombe",
                "score_stilt_grass",
                "score_forest_service",
                "score_named",
                "score_cell",
                "score_elevation",
            ]
        )

        for i, trail in enumerate(top_50, 1):
            writer.writerow(
                [
                    i,
                    trail.name,
                    trail.score,
                    trail.osm_id,
                    f"{trail.latitude:.6f}",
                    f"{trail.longitude:.6f}",
                    f"{trail.elevation_est:.0f}",
                    f"{trail.drive_time_minutes:.0f}",
                    f"{trail.distance_miles:.2f}",
                    trail.county,
                    trail.surface,
                    trail.difficulty,
                    trail.highway_type,
                    trail.ref,
                    trail.score_breakdown.get("surface", 0),
                    trail.score_breakdown.get("difficulty", 0),
                    trail.score_breakdown.get("buncombe", 0),
                    trail.score_breakdown.get("stilt_grass", 0),
                    trail.score_breakdown.get("forest_service", 0),
                    trail.score_breakdown.get("named", 0),
                    trail.score_breakdown.get("cell_coverage", 0),
                    trail.score_breakdown.get("elevation", 0),
                ]
            )

    print("  Saved top 50 to top_50_candidates.csv")

    # Save top 50 GeoJSON
    print("Saving top 50 candidates GeoJSON...")
    top_50_features = []
    for trail_score in top_50:
        for feature in trails_data["features"]:
            if str(feature["properties"].get("osm_id", "")) == trail_score.osm_id:
                feature["properties"]["rank"] = top_50.index(trail_score) + 1
                feature["properties"]["composite_score"] = trail_score.score
                feature["properties"]["drive_time_minutes"] = (
                    trail_score.drive_time_minutes
                )
                feature["properties"]["elevation_est"] = trail_score.elevation_est
                top_50_features.append(feature)
                break

    top_50_geojson = {"type": "FeatureCollection", "features": top_50_features}

    with open("data/top_50_candidates.geojson", "w") as f:
        json.dump(top_50_geojson, f, indent=2)
    print("  Saved top 50 to top_50_candidates.geojson")

    # Save statistics
    print("Saving filter statistics...")

    # Calculate statistics at each stage
    elevation_fails = sum(
        1
        for t in all_scored_trails
        if not (MIN_ELEVATION <= t.elevation_est <= MAX_ELEVATION)
    )
    drive_time_fails = sum(
        1
        for t in all_scored_trails
        if not (MIN_DRIVE_TIME <= t.drive_time_minutes <= MAX_DRIVE_TIME)
    )
    cell_coverage_fails = sum(
        1 for t in all_scored_trails if t.score_breakdown.get("cell_coverage", 0) < 3
    )

    # Surface statistics
    surface_stats = {}
    for trail in filtered_trails:
        surface_stats[trail.surface] = surface_stats.get(trail.surface, 0) + 1

    # Difficulty statistics
    difficulty_stats = {}
    for trail in filtered_trails:
        difficulty_stats[trail.difficulty] = (
            difficulty_stats.get(trail.difficulty, 0) + 1
        )

    stats = {
        "total_trails": total_trails,
        "passed_all_constraints": len(filtered_trails),
        "elimination_rate_percent": round((eliminated_count / total_trails) * 100, 2),
        "constraints_applied": {
            "elevation_range": f"{MIN_ELEVATION}-{MAX_ELEVATION} ft",
            "drive_time_range": f"{MIN_DRIVE_TIME}-{MAX_DRIVE_TIME} minutes",
            "cellular_coverage": "minimum 3/10 score",
        },
        "eliminated_by_constraint": {
            "elevation": elevation_fails,
            "drive_time": drive_time_fails,
            "cellular_coverage": cell_coverage_fails,
        },
        "scoring_weights": {
            "surface_suitable": SCORE_SURFACE_SUITABLE,
            "difficulty_moderate": SCORE_DIFFICULTY_MODERATE,
            "buncombe_county": SCORE_BUNCOMBE_COUNTY,
            "stilt_grass_habitat": SCORE_STILT_GRASS,
            "forest_service_road": SCORE_FOREST_SERVICE,
            "named_trail": SCORE_NAMED_TRAIL,
            "cell_coverage": SCORE_GOOD_CELL_COVERAGE,
            "optimal_elevation": SCORE_OPTIMAL_ELEVATION,
        },
        "filtered_trails_surface_distribution": surface_stats,
        "filtered_trails_difficulty_distribution": difficulty_stats,
        "top_candidate": {
            "name": top_50[0].name,
            "score": top_50[0].score,
            "latitude": top_50[0].latitude,
            "longitude": top_50[0].longitude,
            "elevation_ft": top_50[0].elevation_est,
            "drive_time_minutes": top_50[0].drive_time_minutes,
        }
        if top_50
        else None,
    }

    with open("data/filter_statistics.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("  Saved statistics to filter_statistics.json")
    print()

    print("Processing complete!")
    print()
    print("Files created:")
    print("  - data/filtered_trails.geojson")
    print("  - data/top_50_candidates.csv")
    print("  - data/top_50_candidates.geojson")
    print("  - data/filter_statistics.json")
    print()
    print(f"Top candidate: {top_50[0].name if top_50 else 'None'}")
    print(f"  Score: {top_50[0].score if top_50 else 0}")
    print(
        f"  Location: {top_50[0].latitude:.4f}, {top_50[0].longitude:.4f}"
        if top_50
        else ""
    )
    print(f"  Elevation: {top_50[0].elevation_est:.0f} ft" if top_50 else "")
    print(f"  Drive time: {top_50[0].drive_time_minutes:.0f} min" if top_50 else "")


if __name__ == "__main__":
    main()
