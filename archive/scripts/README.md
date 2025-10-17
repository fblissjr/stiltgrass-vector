# Archived Scripts

This directory contains scripts from earlier analysis phases that have been superseded or are no longer relevant to the final treasure hunt strategy.

## Archived Scripts and Reasons

### Photo Analysis (Superseded)
- `analyze_photos.py` - Original photo analysis script
- `analyze_photos_optimized.py` - Optimized version
- **Reason**: Early attempts at computer vision analysis. Photo feature analysis was later consolidated into reports in `data/photo_features/`

### Geographic Analysis (Superseded)
- `analyze_buncombe.py` - Buncombe County-specific analysis
- **Reason**: Early focus on Buncombe County. Later analysis showed county tags were 93% missing, so we switched to coordinate-based filtering

### Trail Analysis (Intermediate)
- `analyze_top_candidates.py` - Early candidate analysis
- **Reason**: Intermediate script before comprehensive scoring system in `filter_and_score_trails.py`

### Mapping (Superseded)
- `create_summary_map.py` - Early map generation
- **Reason**: Replaced by `create_treasure_map.py` which generates the interactive HTML map

### Supplemental Analysis (One-off)
- `create_supplemental_analysis.py` - One-time analysis
- **Reason**: Generated specific report, no longer needed for ongoing analysis

### South-Facing Slope Analysis (Removed Assumption)
- `extract_trail_angles.py` - Calculate trail orientations and slope aspects
- **Reason**: Attempted to identify south-facing slopes, but this assumption was later removed due to lack of confirmatory evidence from photos. Cannot determine slope orientation from nighttime IR camera or overhead drone imagery.

## Current Active Scripts

For current analysis, use these scripts in `scripts/`:

### Satellite Analysis
- `automated_satellite_analysis.py` - Full CV analysis of satellite imagery
- `quick_satellite_download.py` - Fast satellite image download

### Trail Processing
- `filter_and_score_trails.py` - Main scoring and filtering system
- `verify_trail_access.py` - Access verification
- `create_verified_geojson.py` - Generate verified GeoJSON

### Mapping and Visualization
- `create_treasure_map.py` - Generate interactive HTML map
- `generate_final_recommendations.py` - Create final report

### Data Extraction
- `extract_exif.py` - Extract EXIF from webcam images

## Elevation Analysis

See `elevation/README.md` for scripts related to DEM/elevation analysis that were started but not completed.
