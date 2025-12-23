# Project Inventory - Complete Catalog

This document catalogs every artifact in the Countdown Treasure Hunt AI Analysis project.

---

## Documentation (`docs/`)

### 1-post-mortem/ - Why It Failed
| File | Purpose |
|------|---------|
| `README.md` | Reading guide for post-mortem docs |
| `enterprise-lessons.md` | Business/IT lessons (656 lines) |
| `technical-analysis.md` | Detailed code analysis (2,050 lines) |
| `winning-solution.md` | How winner solved it (143 lines) |

### 2-original-analysis/ - What We Built
| File | Purpose |
|------|---------|
| `README.md` | Context for original analysis |
| `comprehensive-report.md` | Full analysis narrative |
| `field-guide.md` | Field search instructions |

### 3-incomplete-work/ - Things We Started
| File | Purpose |
|------|---------|
| `README.md` | Context for incomplete work |
| `google-earth-workflow.md` | Manual GE analysis workflow |
| `google-earth-data.md` | Data collection procedures |
| `gemini-queries.md` | Multimodal AI prompts |

### 4-reference/ - Context
| File | Purpose |
|------|---------|
| `README.md` | Reference materials overview |
| `contest-rules.md` | Original contest rules |
| `quick-start.md` | Historical quick-start |
| `reorganization-notes.md` | Project reorg notes |

---

## Scripts (`scripts/`)

### Core Analysis Pipeline

| Script | Agent | Purpose | Key Output |
|--------|-------|---------|------------|
| `analyze_trails.py` | A1 | Parse 11,954 trails from KML | `trails_summary.csv`, `trails.geojson` |
| `filter_and_score_trails.py` | C1 | Apply constraints, 130-point scoring | `filtered_trails.geojson`, `filter_statistics.json` |
| `verify_trail_access.py` | V1 | Audit access restrictions | `private_trails_flagged.csv`, `top_20_verified.csv` |
| `extract_exif.py` | B2 | Decode trail camera EXIF | `exifdata.txt`, camera specs |
| `automated_satellite_analysis.py` | C2 | Computer vision on satellite imagery | `satellite_imagery/` |
| `quick_satellite_download.py` | - | Download ESRI satellite tiles | `satellite_imagery/*.jpg` |
| `create_treasure_map.py` | - | Generate interactive Folium map | `treasure_map.html` |
| `create_verified_geojson.py` | - | Convert CSV to GeoJSON | `top_20_verified.geojson` |
| `calculate_drive_times.py` | - | Calculate distances from Charlotte | Drive time estimates |
| `generate_final_recommendations.py` | - | Compile final report | Recommendations |

### Key Functions

**`analyze_trails.py`:**
- `parse_description()` - Extract OSM tags from CDATA
- `parse_coordinates()` - Convert KML coords to tuples
- `calculate_distance()` - Haversine formula for trail length

**`filter_and_score_trails.py`:**
- `haversine_distance()` - Great circle distance
- `estimate_drive_time()` - Mountain road adjustment (1.4x)
- `calculate_trail_score()` - 130-point scoring (THE FLAW)
- `apply_constraints()` - Hard filtering logic

**`automated_satellite_analysis.py`:**
- `download_satellite_tile()` - ESRI World Imagery API
- `detect_trail_edges()` - Canny edge detection
- `analyze_trail_colors()` - HSV color histogram

---

## Data Files (`data/`)

### Geospatial Data

| File | Size | Contents |
|------|------|----------|
| `trails.geojson` | 28 MB | 11,954 trail geometries |
| `filtered_trails.geojson` | 677 KB | 235 trails passing constraints |
| `top_50_candidates.geojson` | 154 KB | Top 50 by score |
| `top_20_verified.geojson` | 153 KB | Final 20 verified |

### Tabular Data

| File | Size | Rows | Contents |
|------|------|------|----------|
| `trails_summary.csv` | 807 KB | 11,954 | All trails with metadata |
| `top_20_verified.csv` | 4 KB | 20 | Final rankings (WRONG) |
| `private_trails_flagged.csv` | 45 KB | 533 | Trails with restrictions |

### Metadata

| File | Contents |
|------|----------|
| `filter_statistics.json` | Constraint elimination metrics |
| `trails_statistics.json` | Distribution summaries |
| `exif_analysis.json` | Camera EXIF decoded |
| `webcam_metadata.json` | Webcam specs |

### Technical Analysis

| File | Contents |
|------|----------|
| `camera_technical_specs.md` | StealthCam Deceptor MAX specs |
| `cellular_requirements.md` | AT&T/Verizon 4G LTE analysis |
| `exif_codes_decoded.md` | [MP:05], [TP:055F] meanings |

### Photo Analysis (`data/photo_features/`)

| File | Contents |
|------|----------|
| `visual_signature.md` | Trail matching criteria |
| `vegetation_analysis.md` | Forest characteristics |
| `aerial_photos_detailed_analysis.md` | Photo-by-photo analysis |
| `photo_scales.json` | Altitude to pixel conversion |
| `color_profiles.json` | RGB/HSV analysis |
| `trail_orientations.json` | Trail direction vectors |

### Satellite Imagery (`data/satellite_imagery/`)

| Contents |
|----------|
| Individual tiles for top 5 trails |
| 3x3 grid composites |
| `coordinates.txt` - GPS reference |
| Analysis results JSON |

### Elevation Data (`data/elevation/`)

| File | Size | Contents |
|------|------|----------|
| `dem.tif` | 3.0 MB | Digital Elevation Model |
| `slope.tif` | 5.9 MB | Slope steepness |
| `aspect.tif` | 5.5 MB | Slope direction |
| `south_facing_mask.tif` | 194 KB | South-facing detection |

---

## Reports (`reports/`)

### Agent Reports

| Report | Agent | Contents |
|--------|-------|----------|
| `agent_a1_findings.md` | A1 | Trail data analysis (11,954 trails) |
| `agent_b2_findings.md` | B2 | Camera specs, cellular requirement |
| `agent_c1_findings.md` | C1 | Constraint filtering, 130-point scoring |
| `agent_c2_findings.md` | C2 | Computer vision photo analysis |

### Verification Reports

| Report | Contents |
|--------|----------|
| `trail_verification.md` | AllTrails/USFS cross-reference |
| `access_analysis.md` | 470 private trails audit |
| `VERIFICATION_SUMMARY.md` | Quick reference |
| `FINAL_STATISTICS.md` | Comprehensive metrics |
| `google_earth_reconnaissance.md` | Satellite analysis notes |

---

## Photos (`photos/`)

| Photo | Size | Altitude | Purpose |
|-------|------|----------|---------|
| `01_aerial.jpg` | 6.4 MB | ~1.5 ft | Ground level, treasure visible |
| `02_aerial.jpg` | 6.6 MB | ~3 ft | Leaf litter, stilt grass |
| `03_aerial.jpg` | 7.6 MB | ~4.5 ft | Vegetation detail |
| `04_aerial.jpg` | 30 MB | ~13 ft | Trail edges (key for matching) |
| `05_aerial.jpg` | 19 MB | ~21 ft | Trail visibility |
| `06_aerial.jpg` | 18 MB | ~29 ft | Trail context |
| `07_aerial.jpg` | 22 MB | ~40 ft | Canopy structure |
| `08_aerial.jpg` | 26 MB | ~65 ft | Large area context |
| `output.gif` | 14 MB | - | Animated progression |

---

## Archive (`archive/`)

### Historical Reports

| File | Contents |
|------|----------|
| `AGENT_A1_COMPLETE.md` | Early A1 findings |
| `AGENT_B2_COMPLETE.md` | Early B2 findings |
| `AGENT_D1_COMPLETE.md` | Alternative approach |
| `ANALYSIS.md` | Original framework |
| `IDEAS.md` | Strategy brainstorming |
| `FINAL_REPORT.md` | Intermediate report |
| `ORCHESTRATION_PLAN.md` | Multi-agent strategy |

### Archive Scripts (`archive/scripts/`)

| Script | Status |
|--------|--------|
| `download_srtm.py` | Elevation download |
| `download_dem_tiles.py` | DEM tiles |
| `elevation_processor.py` | DEM processing |
| `analyze_photos.py` | Photo analysis |
| `analyze_buncombe.py` | County-specific |
| Various others | Exploratory |

---

## KML/GIS Files

| File | Size | Contents |
|------|------|----------|
| `trails.kml` | 13 MB | Original OSM data (11,954 trails) |
| `trails_priority_only.kml` | 177 KB | Top priority trails |
| `treasure_hunt_priority_trails.kml` | 65 KB | Final priority set |

---

## Interactive Output

| File | Size | Description |
|------|------|-------------|
| `treasure_map.html` | 16 KB | Folium interactive map |

Open in browser to:
- View all 18 verified candidates
- Click markers for popup details
- See Day 8 search circle
- Zoom/pan across region

---

## Project Statistics

| Category | Count/Size |
|----------|------------|
| Python scripts | 10 active |
| Data files | 41 MB total |
| Documentation | 2.3 MB |
| Aerial photos | 150 MB |
| Total trails | 11,954 |
| Trail miles | 3,198.82 |
| Final candidates | 18 |
| Verification rate | 77.8% |

---

## The 5-Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     trails.kml (13 MB)                      │
│                    11,954 trail segments                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Agent A1: Data Analysis                   │
│    analyze_trails.py → trails_summary.csv, trails.geojson   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│ Agent B2: Camera EXIF   │     │  Agent C2: Computer     │
│ extract_exif.py         │     │  Vision                 │
│ → cellular requirement  │     │  → photo_features/      │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent C1: Constraint Filtering                 │
│   filter_and_score_trails.py → filtered_trails.geojson      │
│            130-point scoring system (FLAWED)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent V1: Access Verification                  │
│      verify_trail_access.py → top_20_verified.csv           │
│           Found 470 private trails                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Final Outputs                            │
│   treasure_map.html, docs/2-original-analysis/report.md     │
│                   18 verified trails                        │
│                      (WRONG ANSWER)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## File Dependencies

```
trails.kml
    │
    ├─→ analyze_trails.py
    │       ├─→ trails_summary.csv
    │       ├─→ trails.geojson
    │       └─→ trails_statistics.json
    │
    ├─→ filter_and_score_trails.py
    │       ├─→ filtered_trails.geojson
    │       ├─→ top_50_candidates.geojson
    │       └─→ filter_statistics.json
    │
    └─→ verify_trail_access.py
            ├─→ private_trails_flagged.csv
            └─→ top_20_verified.csv
                    │
                    └─→ create_treasure_map.py
                            └─→ treasure_map.html

photos/01-08_aerial.jpg
    │
    └─→ [Agent C2 analysis]
            └─→ data/photo_features/

top_20_verified.csv
    │
    └─→ automated_satellite_analysis.py
            └─→ data/satellite_imagery/
```

---

**Last Updated:** December 2025
