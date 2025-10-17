# Elevation Analysis Scripts (Incomplete)

This directory contains scripts for elevation analysis that were started but not completed during the treasure hunt analysis.

## Why These Scripts Were Not Used

1. **Cellular Coverage Proved More Powerful**: The requirement for dual-SIM cellular coverage (AT&T/Verizon) provided a much stronger constraint than elevation analysis alone.

2. **Temperature Data Sufficient**: The trail camera EXIF temperature reading (55°F at midnight) gave us an elevation range (3,000-4,500 ft) without needing DEM data.

3. **Time Constraints**: Downloading and processing SRTM/USGS 3DEP data for the entire search area would have taken significant time.

4. **South-Facing Slope Assumption Removed**: Originally these scripts were intended to identify south-facing slopes, but this assumption was later removed due to lack of confirmatory evidence.

## Scripts in This Directory

- `download_closest_tiles.py` - Download DEM tiles for search area
- `download_dem_tiles.py` - USGS 3DEP tile downloader
- `download_elevation_data.py` - General elevation data fetcher
- `download_srtm.py` - SRTM data downloader
- `elevation_processor.py` - Process elevation data for trails
- `process_elevation.py` - Calculate slope aspects

## If You Want to Use These

These scripts are functional but incomplete. To use them:

1. Choose elevation data source (SRTM or USGS 3DEP)
2. Download tiles covering search area (35.6-36.4°N, 82.2-83.0°W)
3. Process trails from trails.kml
4. Calculate slope aspects for each trail segment

However, for this treasure hunt, **cellular coverage testing is more valuable** than elevation analysis.

## Related Data

See `data/elevation/` for partial elevation data that was downloaded during early analysis.
