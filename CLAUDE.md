# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-assisted analysis project for the **Countdown Treasure** hunt - a real-world treasure hunt in the Blue Ridge Mountains with $25,350 in gold coins. The treasure is monitored by live webcam and the search area shrinks daily from 420 miles (Day 1) to 1 foot (Day 21).

**Key Objective**: Demonstrate how AI can provide significant value in solving complex geospatial puzzles, even if it cannot provide a 100% solution. This is a proof-of-concept showing AI's capability to narrow search areas, analyze visual data, and synthesize multi-modal information.

## Contest Rules & Constraints

### Critical Facts
- **Location**: Blue Ridge Mountains, on public land only
- **Placement**: No more than 50 yards off a hiking trail (not on trail itself)
- **Accessibility**: Requires moderate off-trail hiking, regular forest floor
- **Visibility**: If taller, could be seen from trail
- **Monitoring**: Live webcam with 10-minute updates (requires cell coverage)
- **Creator**: Lives in Charlotte, NC
- **Environment**: South-facing slope (most likely), Japanese stilt grass present, deer and raccoons confirmed

### Daily Progression
The hunt started October 9th, 2024. All aerial photos were taken by drone on October 8th.

| Day | Center Point [lat, lng] | Search Diameter |
|-----|------------------------|-----------------|
| 1   | [37.5, -82.0]         | 420 miles      |
| 2   | [37.0, -82.0]         | 340 miles      |
| 3   | [36.7, -82.1]         | 270 miles      |
| 4   | [36.3, -82.4]         | 210 miles      |
| 5   | [36.15, -82.67]       | 160 miles      |
| 6   | [35.925, -82.85]      | 120 miles      |
| 7   | [35.79, -82.8]        | 100 miles      |
| 8   | [35.705, -82.83]      | 87 miles       |
| 9-21| (continues shrinking) | 75mi → 1ft     |

**Important**: Each day's circle is fully contained within the previous day's circle. The treasure never moves outside previous boundaries.

## Data Assets

### Aerial Photography Sequence
Located in `photos/` directory:
- `01_aerial.jpg` - Ground level: Shows treasure (small cylindrical object) on forest floor with Japanese stilt grass
- `02_aerial.jpg` - Low altitude: ~3-5 feet up, shows immediate surrounding area
- `03_aerial.jpg` - Mid altitude: ~10-15 feet, beginning to see terrain patterns
- `04_aerial.jpg` - Medium altitude: ~25-40 feet, clearing/trail edges visible
- `05_aerial.jpg` - Higher altitude: ~60-100 feet, shows forest canopy structure
- `06_aerial.jpg` - High altitude: ~150-200 feet, broader terrain context
- `07_aerial.jpg` - Very high: Dense canopy view from above
- `08_aerial.jpg` - Highest: Shows large area of forest canopy

### Visual Pattern Analysis
The progression shows:
1. **Ground features**: Mixed deciduous forest, leaf litter, invasive grass species
2. **Canopy structure**: Deciduous trees (visible in photos 7-8), some evergreen presence
3. **Terrain hints**: Possible trail/clearing edges in mid-altitude photos
4. **Scale reference**: The treasure container is approximately 3-4 inches in diameter

## AI Analysis Approaches

### Computer Vision
- **Feature extraction**: Identify trails, clearings, terrain features from aerial photos
- **Pattern matching**: Compare aerial photos against satellite imagery to geolocate
- **Vegetation analysis**: Use flora identification (Japanese stilt grass, tree species) to narrow biome
- **Shadow analysis**: Determine sun angle and slope orientation from photo 1-6

### Geospatial Analysis
- **Trail mapping**: Overlay public trail databases (AllTrails, USGS, OpenStreetMap) with search circles
- **Elevation models**: Filter for south-facing slopes using DEM data
- **Cell coverage**: Cross-reference with carrier coverage maps (webcam requirement)
- **Public land**: Filter using USGS, NPS, USFS boundary data

### Multi-Modal Reasoning
- **Constraint satisfaction**: Combine all rules (50 yards from trail, public land, cell coverage, south slope)
- **Probability mapping**: Weight areas by likelihood based on multiple factors
- **Human logistics**: Consider placement from Charlotte, NC (drive time, familiarity)

## Development Environment

### Python Environment
- Use `uv` for all Python package management
- Activate virtual environment: `source .venv/bin/activate` (or `uv venv` if needed)
- Install packages: `uv pip install <package>`

### Typical Workflow
1. Geospatial analysis: Consider `geopandas`, `shapely`, `folium`, `rasterio`
2. Computer vision: Consider `opencv-python`, `pillow`, `scikit-image`
3. Mapping: Consider `folium`, `contextily`, `matplotlib`
4. Data analysis: Consider `pandas`, `numpy`, `scipy`

## Project Structure

### Documentation Files
- `Treasure-doc.md` - Source material with all contest details
- `CLAUDE.md` - This file: project context for AI assistants
- `ANALYSIS.md` - Detailed findings from data analysis
- `IDEAS.md` - Strategic approaches and methodologies for using AI

### Data Files
- `photos/` - Aerial photo sequence from Day 1-8
- Additional satellite/map data can be added as needed

## Analysis Philosophy

This project demonstrates **AI-augmented decision making** rather than fully autonomous solving:

1. **Data synthesis**: Combine disparate data types (imagery, GPS, terrain, rules)
2. **Hypothesis generation**: Propose likely locations based on multi-factor analysis
3. **Constraint filtering**: Systematically eliminate impossible areas
4. **Probability ranking**: Order remaining candidates by likelihood
5. **Actionable output**: Provide human-readable recommendations for field verification

The goal is to reduce a 43+ mile diameter search area (Day 12) to perhaps 10-20 high-probability locations that a human could investigate.

## Key Insight

The treasure location is deterministic and unchanging - all the clues already exist in the data. AI's value is in processing scale (analyzing thousands of trail segments) and pattern recognition (matching aerial photos to satellite imagery) that would take humans weeks to do manually.
