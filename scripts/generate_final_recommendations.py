#!/usr/bin/env python3
"""
Agent D1: Master Synthesizer and Recommendation Generator
Combines all agent findings to generate top 20 candidate locations
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict

def load_trail_data():
    """Load trail data from CSV"""
    print("Loading trail data...")
    df = pd.read_csv('data/trails_summary.csv')
    print(f"Loaded {len(df):,} trails")
    return df

def load_geojson_data():
    """Load trail GeoJSON data"""
    print("Loading GeoJSON trail data...")
    with open('data/trails.geojson') as f:
        geojson = json.load(f)
    print(f"Loaded {len(geojson['features']):,} trail features")
    return geojson

def apply_constraint_filters(df):
    """Apply hard constraint filters based on agent findings"""
    print("\n=== APPLYING CONSTRAINT FILTERS ===")

    initial_count = len(df)
    print(f"Starting trails: {initial_count:,}")

    # Filter 1: Suitable surface types (ground, dirt, gravel, unpaved)
    # These surfaces allow for burying items
    suitable_surfaces = ['ground', 'dirt', 'gravel', 'unpaved']
    df_filtered = df[df['surface'].isin(suitable_surfaces)].copy()
    print(f"After surface filter (ground/dirt/gravel/unpaved): {len(df_filtered):,} ({len(df_filtered)/initial_count*100:.1f}%)")

    # Filter 2: Trail types (prefer path, track, footway - not cycleway)
    suitable_types = ['path', 'track', 'footway']
    df_filtered = df_filtered[df_filtered['highway_type'].isin(suitable_types)]
    print(f"After trail type filter: {len(df_filtered):,} ({len(df_filtered)/initial_count*100:.1f}%)")

    # Filter 3: Minimum length (at least 0.1 miles - too short might be urban connectors)
    df_filtered = df_filtered[df_filtered['distance_miles'] >= 0.1]
    print(f"After minimum length filter: {len(df_filtered):,} ({len(df_filtered)/initial_count*100:.1f}%)")

    # Filter 4: Exclude extremely long trails (>10 miles - likely wilderness backcountry)
    # Camera needs to be accessible for setup
    df_filtered = df_filtered[df_filtered['distance_miles'] <= 10.0]
    print(f"After maximum length filter (<10 miles): {len(df_filtered):,} ({len(df_filtered)/initial_count*100:.1f}%)")

    return df_filtered

def calculate_scores(df):
    """Calculate probability scores for each trail segment"""
    print("\n=== CALCULATING PROBABILITY SCORES ===")

    scores = []

    for idx, row in df.iterrows():
        score = 0
        score_breakdown = {}

        # Factor 1: Surface type (40 points max)
        # Ground and dirt are best for burying
        if row['surface'] == 'ground':
            surface_score = 40
        elif row['surface'] == 'dirt':
            surface_score = 35
        elif row['surface'] == 'gravel':
            surface_score = 25
        elif row['surface'] == 'unpaved':
            surface_score = 20
        else:
            surface_score = 0
        score += surface_score
        score_breakdown['surface'] = surface_score

        # Factor 2: Difficulty level (25 points max)
        # Moderate difficulty is ideal - accessible but not too popular
        difficulty = str(row['difficulty']).lower()
        if difficulty in ['grade2', 'grade3', 'hiking']:
            difficulty_score = 25
        elif difficulty in ['mountain_hiking', 'grade4']:
            difficulty_score = 15
        elif difficulty == 'grade1':
            difficulty_score = 10
        else:
            difficulty_score = 5  # Unknown difficulty
        score += difficulty_score
        score_breakdown['difficulty'] = difficulty_score

        # Factor 3: Trail type (20 points max)
        # Tracks (old roads) are ideal - moderate traffic, easy access
        if row['highway_type'] == 'track':
            type_score = 20
        elif row['highway_type'] == 'path':
            type_score = 15
        elif row['highway_type'] == 'footway':
            type_score = 10
        else:
            type_score = 5
        score += type_score
        score_breakdown['trail_type'] = type_score

        # Factor 4: Trail length (15 points max)
        # Prefer moderate length trails (0.5-3 miles) - not too short, not wilderness
        length = row['distance_miles']
        if 0.5 <= length <= 3.0:
            length_score = 15
        elif 0.25 <= length <= 0.5 or 3.0 <= length <= 5.0:
            length_score = 10
        elif 0.1 <= length <= 0.25 or 5.0 <= length <= 7.0:
            length_score = 5
        else:
            length_score = 2
        score += length_score
        score_breakdown['length'] = length_score

        # Bonus points for named trails (not generic "Trail XXXX")
        name = str(row['name'])
        if name != 'nan' and not name.startswith('Trail '):
            score += 10
            score_breakdown['named'] = 10
        else:
            score_breakdown['named'] = 0

        # Bonus points for Forest Service roads (reliable access)
        ref = str(row['ref'])
        if 'FS' in ref or 'Forest Service' in name:
            score += 10
            score_breakdown['forest_service'] = 10
        else:
            score_breakdown['forest_service'] = 0

        scores.append({
            'trail_name': name,
            'osm_id': row['osm_id'],
            'total_score': score,
            'breakdown': score_breakdown,
            'distance_miles': row['distance_miles'],
            'surface': row['surface'],
            'difficulty': row['difficulty'],
            'highway_type': row['highway_type'],
            'county': row['county'],
            'ref': ref
        })

    return pd.DataFrame(scores)

def integrate_camera_constraints(scored_df):
    """Apply camera-specific constraints from Agent B2 findings"""
    print("\n=== APPLYING CAMERA CONSTRAINTS ===")
    print("From Agent B2 findings:")
    print("- Dual-SIM cellular (AT&T + Verizon) required")
    print("- Temperature reading: 55F suggests 3,000-4,500 ft elevation")
    print("- Must be accessible for camera setup")
    print("- Within detection range (80-120 feet) of trail")

    # We don't have actual cellular coverage or elevation data loaded
    # But we can prioritize certain trail characteristics

    # Boost scores for trails likely to have good cell coverage
    # (named trails, forest service roads, near Asheville)
    for idx, row in scored_df.iterrows():
        # Buncombe County (Asheville area) has best coverage
        if row['county'] == 'Buncombe':
            scored_df.at[idx, 'total_score'] += 20
            print(f"Boosting Buncombe County trail: {row['trail_name']}")

    return scored_df

def generate_top_candidates(scored_df, top_n=20):
    """Generate final ranked list of top candidates"""
    print(f"\n=== GENERATING TOP {top_n} CANDIDATES ===")

    # Sort by total score
    top_candidates = scored_df.nlargest(top_n, 'total_score')

    print(f"\nTop {top_n} Trail Segments by Probability Score:")
    print("="*100)

    for i, (idx, row) in enumerate(top_candidates.iterrows(), 1):
        print(f"\n{i}. {row['trail_name']}")
        print(f"   Score: {row['total_score']:.0f}/130 points")
        print(f"   Length: {row['distance_miles']:.2f} miles")
        print(f"   Surface: {row['surface']}, Difficulty: {row['difficulty']}")
        print(f"   Type: {row['highway_type']}, County: {row['county']}")
        print(f"   Breakdown: Surface={row['breakdown']['surface']}, "
              f"Difficulty={row['breakdown']['difficulty']}, "
              f"Type={row['breakdown']['trail_type']}, "
              f"Length={row['breakdown']['length']}")

    return top_candidates

def main():
    """Main analysis pipeline"""
    print("="*80)
    print("AGENT D1: MASTER SYNTHESIZER AND RECOMMENDATION GENERATOR")
    print("="*80)

    # Load data
    df = load_trail_data()

    # Apply constraint filters
    df_filtered = apply_constraint_filters(df)

    # Calculate scores
    scored_df = calculate_scores(df_filtered)

    # Apply camera constraints
    scored_df = integrate_camera_constraints(scored_df)

    # Generate top candidates
    top_candidates = generate_top_candidates(scored_df, top_n=20)

    # Save results
    print("\n=== SAVING RESULTS ===")
    output_path = 'data/final_top_20.csv'
    top_candidates.to_csv(output_path, index=False)
    print(f"Saved top 20 candidates to: {output_path}")

    # Save full scored dataset for reference
    scored_df.to_csv('data/all_scored_trails.csv', index=False)
    print(f"Saved all scored trails to: data/all_scored_trails.csv")

    print("\n=== ANALYSIS COMPLETE ===")
    print(f"From {len(df):,} total trails:")
    print(f"  -> {len(df_filtered):,} passed constraint filters")
    print(f"  -> Top 20 identified with scores ranging from "
          f"{top_candidates['total_score'].min():.0f} to {top_candidates['total_score'].max():.0f}")

if __name__ == '__main__':
    main()
