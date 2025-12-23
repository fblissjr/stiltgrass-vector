#!/usr/bin/env python3
"""
Extract EXIF data from aerial photos and webcam images.
Focused on trail camera metadata analysis.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import exifread
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def extract_exif_exifread(image_path):
    """Extract EXIF data using exifread library (more comprehensive)"""
    exif_data = {}

    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=True)

        for tag, value in tags.items():
            # Convert to string for JSON serialization
            exif_data[tag] = str(value)

    return exif_data


def extract_exif_pil(image_path):
    """Extract EXIF data using PIL (alternative method)"""
    exif_data = {}

    try:
        image = Image.open(image_path)
        exif_raw = image._getexif()

        if exif_raw:
            for tag_id, value in exif_raw.items():
                tag = TAGS.get(tag_id, tag_id)

                # Handle GPS data specially
                if tag == "GPSInfo":
                    gps_data = {}
                    for gps_tag_id, gps_value in value.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_data[gps_tag] = str(gps_value)
                    exif_data[tag] = gps_data
                else:
                    # Convert to string for JSON
                    exif_data[tag] = str(value)
    except Exception as e:
        exif_data["error"] = str(e)

    return exif_data


def analyze_trail_camera_metadata(exif_data):
    """Analyze trail camera specific metadata"""
    analysis = {
        "camera_make": None,
        "camera_model": None,
        "image_description": None,
        "datetime": None,
        "gps_coordinates": None,
        "special_codes": [],
        "camera_type": "unknown",
    }

    # Check for camera make/model
    for key in exif_data:
        key_lower = key.lower()

        if "make" in key_lower:
            analysis["camera_make"] = exif_data[key]

        if "model" in key_lower or "camera model" in key_lower:
            analysis["camera_model"] = exif_data[key]

        if "description" in key_lower:
            analysis["image_description"] = exif_data[key]

            # Look for special codes like [MP:05][TP:055F]
            desc = exif_data[key]
            if "[" in desc and "]" in desc:
                import re

                codes = re.findall(r"\[([^\]]+)\]", desc)
                analysis["special_codes"] = codes

        if "datetime" in key_lower or "date" in key_lower:
            if analysis["datetime"] is None:  # Take first datetime found
                analysis["datetime"] = exif_data[key]

        if "gps" in key_lower:
            analysis["gps_coordinates"] = exif_data[key]

    # Determine camera type
    if analysis["camera_make"]:
        make_lower = analysis["camera_make"].lower()
        if "stealth" in make_lower:
            analysis["camera_type"] = "trail_camera"
        elif "canon" in make_lower or "nikon" in make_lower or "sony" in make_lower:
            analysis["camera_type"] = "professional_camera"
        elif "dji" in make_lower or "drone" in make_lower:
            analysis["camera_type"] = "drone"

    return analysis


def main():
    # Setup paths
    photos_dir = Path("photos")
    data_dir = Path("data")
    webcam_dir = data_dir / "webcam_images"

    # Create output directories
    data_dir.mkdir(exist_ok=True)
    webcam_dir.mkdir(exist_ok=True)

    all_results = {}

    # Process all aerial photos
    print("Extracting EXIF data from aerial photos...")
    for photo_file in sorted(photos_dir.glob("*.jpg")):
        print(f"\nProcessing: {photo_file.name}")

        # Extract using both methods
        exif_exifread = extract_exif_exifread(photo_file)
        exif_pil = extract_exif_pil(photo_file)

        # Analyze trail camera metadata
        analysis = analyze_trail_camera_metadata(exif_exifread)

        all_results[photo_file.name] = {
            "path": str(photo_file),
            "exif_exifread": exif_exifread,
            "exif_pil": exif_pil,
            "trail_camera_analysis": analysis,
        }

        # Print key findings
        print(f"  Camera Make: {analysis['camera_make']}")
        print(f"  Camera Model: {analysis['camera_model']}")
        print(f"  Description: {analysis['image_description']}")
        print(f"  Special Codes: {analysis['special_codes']}")
        print(f"  Camera Type: {analysis['camera_type']}")
        print(f"  DateTime: {analysis['datetime']}")
        print(f"  GPS: {analysis['gps_coordinates']}")

    # Save comprehensive results
    output_file = data_dir / "exif_analysis.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n\nComplete EXIF data saved to: {output_file}")

    # Create summary report
    print("\n" + "=" * 80)
    print("SUMMARY OF TRAIL CAMERA FINDINGS")
    print("=" * 80)

    trail_cam_photos = []
    for photo_name, data in all_results.items():
        analysis = data["trail_camera_analysis"]
        if analysis["camera_type"] == "trail_camera" or analysis["special_codes"]:
            trail_cam_photos.append(
                {
                    "photo": photo_name,
                    "make": analysis["camera_make"],
                    "model": analysis["camera_model"],
                    "codes": analysis["special_codes"],
                    "description": analysis["image_description"],
                }
            )

    if trail_cam_photos:
        print("\nTRAIL CAMERA IMAGES DETECTED:")
        for item in trail_cam_photos:
            print(f"\n{item['photo']}:")
            print(f"  Make: {item['make']}")
            print(f"  Model: {item['model']}")
            print(f"  Description: {item['description']}")
            print(f"  Special Codes: {item['codes']}")
    else:
        print("\nNo trail camera metadata detected in aerial photos.")
        print(
            "This suggests the aerial photos are from a drone or professional camera."
        )
        print("The trail camera webcam is likely separate from these aerial photos.")

    return all_results


if __name__ == "__main__":
    results = main()
