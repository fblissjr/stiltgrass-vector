#!/usr/bin/env python3
"""
Extract dominant trail angles and orientations from photos 4-6
This helps identify trail direction for satellite matching
"""

import json
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

PHOTO_DIR = Path("photos")
OUTPUT_DIR = Path("data/photo_features")


def analyze_trail_orientation(photo_num):
    """Analyze dominant linear feature orientations"""
    path = PHOTO_DIR / f"{photo_num:02d}_aerial.jpg"
    img = cv2.imread(str(path))

    # Downsample
    scale = 2000 / img.shape[1]
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 100)

    # Hough transform for line detection
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=15
    )

    if lines is None:
        return None

    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

        # Normalize to 0-180 (direction, not orientation)
        if angle < 0:
            angle += 180

        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Weight by line length
        angles.extend([angle] * int(length / 10))

    return angles


# Analyze all three mid-altitude photos
results = {}

for photo_num in [4, 5, 6]:
    print(f"Analyzing photo {photo_num}...")
    angles = analyze_trail_orientation(photo_num)

    if angles:
        # Bin angles into 15-degree increments
        angle_bins = np.arange(0, 181, 15)
        hist, bins = np.histogram(angles, bins=angle_bins)

        # Find dominant directions
        dominant_bins = np.argsort(hist)[-3:][::-1]  # Top 3
        dominant_angles = [
            (bins[i], bins[i + 1], hist[i]) for i in dominant_bins if hist[i] > 0
        ]

        # Calculate mean and std
        mean_angle = np.mean(angles)
        std_angle = np.std(angles)
        median_angle = np.median(angles)

        # Convert to compass bearings (0=North, 90=East, 180=South)
        # Note: Image coordinates may need rotation adjustment
        compass_mean = (90 - mean_angle) % 360

        results[photo_num] = {
            "mean_angle_degrees": round(float(mean_angle), 1),
            "median_angle_degrees": round(float(median_angle), 1),
            "std_angle_degrees": round(float(std_angle), 1),
            "compass_bearing_approx": round(float(compass_mean), 1),
            "total_lines_detected": len(angles),
            "dominant_angle_bins": [
                {"range": f"{int(start)}-{int(end)} degrees", "count": int(count)}
                for start, end, count in dominant_angles
            ],
        }

        print(f"  Mean angle: {mean_angle:.1f}°")
        print(f"  Dominant bins: {dominant_angles[0]}")
        print(f"  Total weighted lines: {len(angles)}")

# Save results
with open(OUTPUT_DIR / "trail_orientations.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved trail orientation analysis to trail_orientations.json")

# Create summary
print("\n" + "=" * 60)
print("TRAIL ORIENTATION SUMMARY")
print("=" * 60)

for photo_num, data in results.items():
    print(f"\nPhoto {photo_num}:")
    print(f"  Mean trail angle: {data['mean_angle_degrees']}° (image coords)")
    print(f"  Approx compass bearing: {data['compass_bearing_approx']}°")
    print(f"  Dominant directions: {data['dominant_angle_bins'][0]['range']}")

# Overall trail direction
all_means = [d["mean_angle_degrees"] for d in results.values()]
overall_mean = np.mean(all_means)
print(f"\nOverall average trail angle: {overall_mean:.1f}°")
print(
    f"This suggests the trail runs approximately {'NE-SW' if 30 < overall_mean < 60 else 'NW-SE' if 120 < overall_mean < 150 else 'E-W' if 85 < overall_mean < 95 else 'variable'}"
)
