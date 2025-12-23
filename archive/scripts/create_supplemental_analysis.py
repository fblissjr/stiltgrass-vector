#!/usr/bin/env python3
"""
Create supplemental visual analysis showing photo progression and key measurements
"""

import json
from pathlib import Path

import cv2
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PHOTO_DIR = Path("photos")
OUTPUT_DIR = Path("data/photo_features")
MAX_WIDTH = 800  # Small thumbnails


def load_and_resize(photo_num, max_width=MAX_WIDTH):
    """Load and resize photo"""
    path = PHOTO_DIR / f"{photo_num:02d}_aerial.jpg"
    img = cv2.imread(str(path))
    height, width = img.shape[:2]
    if width > max_width:
        scale = max_width / width
        new_width = max_width
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


# Create overview figure
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.2)

# Load all photos
for i in range(8):
    photo_num = i + 1
    row = i // 4
    col = i % 4

    ax = fig.add_subplot(gs[row, col])
    img = load_and_resize(photo_num)
    ax.imshow(img)

    # Add labels
    if photo_num <= 3:
        category = "GROUND"
        color = "brown"
    elif photo_num <= 6:
        category = "MID-ALT"
        color = "red"
    else:
        category = "CANOPY"
        color = "green"

    ax.set_title(
        f"Photo {photo_num}: {category}", fontweight="bold", color=color, fontsize=12
    )
    ax.axis("off")

plt.suptitle(
    "Aerial Photo Progression: Ground Level to Canopy", fontsize=18, fontweight="bold"
)
plt.savefig(OUTPUT_DIR / "photo_progression_overview.png", dpi=150, bbox_inches="tight")
plt.close()

print("Created photo progression overview")

# Create detailed measurement chart
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Load color profile data
with open(OUTPUT_DIR / "color_profiles.json", "r") as f:
    color_data = json.load(f)

# Load scale data
with open(OUTPUT_DIR / "photo_scales.json", "r") as f:
    scale_data = json.load(f)

photos = list(range(1, 9))

# Plot 1: Altitude progression
altitudes = [scale_data[str(i)]["estimated_altitude_feet"] for i in photos]
fovs = [scale_data[str(i)]["estimated_fov_feet"] for i in photos]

axes[0, 0].plot(photos, altitudes, "bo-", linewidth=2, markersize=8, label="Altitude")
axes[0, 0].set_xlabel("Photo Number", fontsize=12)
axes[0, 0].set_ylabel("Altitude (feet)", fontsize=12)
axes[0, 0].set_title("Estimated Altitude by Photo", fontweight="bold", fontsize=14)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xticks(photos)

# Add category shading
axes[0, 0].axvspan(0.5, 3.5, alpha=0.1, color="brown", label="Ground")
axes[0, 0].axvspan(3.5, 6.5, alpha=0.1, color="red", label="Mid-Alt")
axes[0, 0].axvspan(6.5, 8.5, alpha=0.1, color="green", label="Canopy")
axes[0, 0].legend()

# Plot 2: Field of View
axes[0, 1].plot(photos, fovs, "go-", linewidth=2, markersize=8)
axes[0, 1].set_xlabel("Photo Number", fontsize=12)
axes[0, 1].set_ylabel("Field of View (feet)", fontsize=12)
axes[0, 1].set_title("Estimated Field of View by Photo", fontweight="bold", fontsize=14)
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_xticks(photos)

# Plot 3: Vegetation coverage
green_pcts = [color_data[str(i)]["green_percentage"] for i in photos]
brown_pcts = [color_data[str(i)]["brown_bare_percentage"] for i in photos]

x = np.arange(len(photos))
width = 0.35

axes[1, 0].bar(
    x - width / 2, green_pcts, width, label="Green Vegetation", color="green", alpha=0.7
)
axes[1, 0].bar(
    x + width / 2,
    brown_pcts,
    width,
    label="Brown/Bare Ground",
    color="brown",
    alpha=0.7,
)
axes[1, 0].set_xlabel("Photo Number", fontsize=12)
axes[1, 0].set_ylabel("Coverage (%)", fontsize=12)
axes[1, 0].set_title(
    "Vegetation vs Bare Ground Coverage", fontweight="bold", fontsize=14
)
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(photos)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis="y")

# Plot 4: Resolution (inches per pixel)
resolutions = [scale_data[str(i)]["resolution_inches_per_pixel"] for i in photos]

axes[1, 1].plot(photos, resolutions, "ro-", linewidth=2, markersize=8)
axes[1, 1].set_xlabel("Photo Number", fontsize=12)
axes[1, 1].set_ylabel("Resolution (inches per pixel)", fontsize=12)
axes[1, 1].set_title("Spatial Resolution by Photo", fontweight="bold", fontsize=14)
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].set_xticks(photos)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "photo_measurements_analysis.png", dpi=150, bbox_inches="tight"
)
plt.close()

print("Created measurement analysis charts")

# Create trail-specific visualization for photos 4-6
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, photo_num in enumerate([4, 5, 6]):
    img = load_and_resize(photo_num, max_width=1200)

    # Draw annotations
    axes[idx].imshow(img)
    axes[idx].set_title(
        f"Photo {photo_num}: Trail Features", fontweight="bold", fontsize=14
    )
    axes[idx].axis("off")

    # Add text annotations
    alt_ft = scale_data[str(photo_num)]["estimated_altitude_feet"]
    fov_ft = scale_data[str(photo_num)]["estimated_fov_feet"]
    green_pct = color_data[str(photo_num)]["green_percentage"]
    brown_pct = color_data[str(photo_num)]["brown_bare_percentage"]

    text = f"Altitude: {alt_ft:.1f}ft\n"
    text += f"FOV: {fov_ft:.1f}ft\n"
    text += f"Green: {green_pct:.1f}%\n"
    text += f"Bare: {brown_pct:.1f}%"

    axes[idx].text(
        0.02,
        0.98,
        text,
        transform=axes[idx].transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

plt.suptitle(
    "Mid-Altitude Trail Photos: Key for Satellite Matching",
    fontsize=16,
    fontweight="bold",
)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "trail_photos_annotated.png", dpi=150, bbox_inches="tight")
plt.close()

print("Created annotated trail photos")

print("\nAll supplemental visualizations created successfully!")
