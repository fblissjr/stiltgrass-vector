# Agent Orchestration Plan

## Overview
This document outlines the parallel agent architecture for AI-assisted treasure hunt analysis. Agents are grouped by dependencies to maximize parallelization.

## Agent Groups & Dependencies

```
PHASE 1 (Parallel): Data Acquisition
├── Agent A1: Trail & Public Land Data
├── Agent A2: Satellite Imagery & Elevation
└── Agent A3: Environmental Data

PHASE 2 (Parallel): Computer Vision
├── Agent B1: Aerial Photo Analysis
└── Agent B2: Satellite Image Matching (depends on A2)

PHASE 3 (Parallel): Geospatial Analysis
├── Agent C1: Constraint Filtering (depends on A1, A3)
└── Agent C2: Multi-Factor Scoring (depends on A1, A2, A3)

PHASE 4 (Sequential): Synthesis
└── Agent D1: Final Recommendations (depends on all)
```

## Agent Specifications

### PHASE 1: Data Acquisition Agents

#### Agent A1: Trail & Public Land Data Collector
**Priority**: Critical
**Dependencies**: None
**Runtime**: 30-60 minutes

**Objectives**:
1. Download OpenStreetMap trail data for Day 8 search area (35.705°N, 82.83°W, 87mi diameter)
2. Identify public land boundaries (National Forest, State Parks)
3. Find popular trails within search zone
4. Export trail GPX data and public land polygons

**Data Sources**:
- OpenStreetMap Overpass API
- USGS Protected Areas Database
- AllTrails (web research for popular trails)
- USFS trail databases for Pisgah/Nantahala

**Deliverables**:
- `data/trails_osm.geojson` - All trails in search area
- `data/public_lands.geojson` - Public land boundaries
- `data/popular_trails.csv` - Named trails with metadata
- `reports/agent_a1_findings.md` - Summary report

---

#### Agent A2: Satellite Imagery & Elevation Data Collector
**Priority**: Critical
**Dependencies**: None
**Runtime**: 45-90 minutes

**Objectives**:
1. Acquire high-resolution satellite imagery for Day 8 area
2. Download Digital Elevation Model (DEM) data
3. Process elevation data to calculate slope and aspect
4. Create basemap for computer vision matching

**Data Sources**:
- Google Earth Engine or Google Earth Pro
- USGS EarthExplorer (Landsat, NAIP)
- SRTM 30m DEM or better resolution if available
- Sentinel-2 satellite data

**Deliverables**:
- `data/satellite_imagery/` - High-res satellite tiles
- `data/elevation/dem.tif` - Digital Elevation Model
- `data/elevation/slope.tif` - Slope raster
- `data/elevation/aspect.tif` - Aspect raster
- `reports/agent_a2_findings.md` - Summary with image quality assessment

---

#### Agent A3: Environmental Data Collector
**Priority**: High
**Dependencies**: None
**Runtime**: 30-60 minutes

**Objectives**:
1. Find cell coverage maps (AT&T, Verizon, T-Mobile)
2. Locate Japanese stilt grass distribution data
3. Calculate drive times from Charlotte, NC
4. Research local ecology and trail conditions

**Data Sources**:
- FCC broadband maps
- OpenSignal or carrier coverage maps
- EDDMapS (invasive species)
- iNaturalist observations
- OpenRouteService for drive time calculations

**Deliverables**:
- `data/cell_coverage.geojson` - Coverage polygons
- `data/invasive_species.geojson` - Stilt grass observations
- `data/drive_times.csv` - Drive time from Charlotte to trailheads
- `reports/agent_a3_findings.md` - Summary with coverage analysis

---

### PHASE 2: Computer Vision Agents

#### Agent B1: Aerial Photo Analyzer
**Priority**: Critical
**Dependencies**: None (uses existing photos)
**Runtime**: 45-90 minutes

**Objectives**:
1. Extract features from photos 1-8
2. Identify visible trails/clearings in photos 4-6
3. Measure scale progression across photos
4. Analyze vegetation patterns and terrain features
5. Perform shadow analysis for slope orientation

**Analysis Tasks**:
- Edge detection for trail identification
- Color segmentation for vegetation types
- Texture analysis for terrain classification
- Scale estimation from photo sequence
- Shadow direction analysis

**Deliverables**:
- `data/photo_features/` - Extracted features per photo
- `data/photo_features/trail_edges.png` - Detected linear features
- `data/photo_features/measurements.json` - Scale, angles, features
- `reports/agent_b1_findings.md` - Detailed photo analysis

---

#### Agent B2: Satellite Image Matcher
**Priority**: Critical
**Dependencies**: Agent A2 (satellite imagery)
**Runtime**: 60-120 minutes

**Objectives**:
1. Match aerial photos 4-6 against satellite imagery
2. Use feature matching (SIFT/ORB) to find similar patterns
3. Generate candidate locations where patterns match
4. Rank matches by similarity score

**Approach**:
- Sliding window search across satellite tiles
- Multi-scale feature matching
- Template matching for trail patterns
- Visual similarity scoring

**Deliverables**:
- `data/visual_matches/` - Top candidate locations
- `data/visual_matches/ranked_locations.geojson` - Top 20 matches with scores
- `data/visual_matches/comparison_images/` - Side-by-side comparisons
- `reports/agent_b2_findings.md` - Match quality and confidence levels

---

### PHASE 3: Geospatial Analysis Agents

#### Agent C1: Constraint Filter
**Priority**: Critical
**Dependencies**: Agent A1 (trails), Agent A3 (coverage, species)
**Runtime**: 30-45 minutes

**Objectives**:
1. Apply hard constraints to eliminate impossible locations
2. Create 50-yard buffers around viable trails
3. Filter by public land, cell coverage, accessibility
4. Calculate search zone area reduction

**Hard Filters**:
- ✅ On public land
- ✅ Within 50 yards of trail
- ✅ Cell coverage present
- ✅ Accessible by hiking

**Deliverables**:
- `data/filtered_trails.geojson` - Trails passing all filters
- `data/search_zones.geojson` - 50-yard buffer polygons
- `data/filter_statistics.json` - Reduction metrics
- `reports/agent_c1_findings.md` - How many miles of trail remain

---

#### Agent C2: Multi-Factor Scorer
**Priority**: High
**Dependencies**: Agent A1, A2, A3 (all data)
**Runtime**: 45-60 minutes

**Objectives**:
1. Score remaining trail segments by soft constraints
2. Weight by: south-facing slope, elevation, drive time, habitat, popularity
3. Rank top 50 locations by probability
4. Create probability heat map

**Scoring Model**:
```
score = (
    40 * south_facing_slope +
    20 * elevation_2000_4000ft +
    15 * drive_time_1_3hrs +
    15 * moderate_trail_use +
    10 * stilt_grass_habitat
)
```

**Deliverables**:
- `data/scored_locations.geojson` - All candidates with scores
- `data/top_50_candidates.geojson` - Highest probability locations
- `data/probability_heatmap.tif` - Visual probability map
- `reports/agent_c2_findings.md` - Scoring methodology and results

---

### PHASE 4: Synthesis Agent

#### Agent D1: Final Recommendations Synthesizer
**Priority**: Critical
**Dependencies**: All agents (A1-A3, B1-B2, C1-C2)
**Runtime**: 30-45 minutes

**Objectives**:
1. Combine visual matches (B2) with constraint-filtered locations (C1, C2)
2. Cross-validate findings across multiple methods
3. Generate final ranked list of top 10-20 locations
4. Create field guide with maps, directions, and photos
5. Assess confidence levels and limitations

**Synthesis Approach**:
- Locations appearing in both visual matches AND high-scored trails: highest priority
- Locations in one method only: medium priority
- Calculate ensemble confidence scores
- Identify any contradictions or gaps

**Deliverables**:
- `FINAL_REPORT.md` - Comprehensive findings and recommendations
- `FIELD_GUIDE.md` - Practical guide for visiting top locations
- `treasure_map.html` - Interactive map with all layers
- `data/final_top_20.geojson` - Final candidate list with full metadata

---

## Execution Timeline

### Wave 1: Launch Phase 1 (Parallel)
- Start agents A1, A2, A3 simultaneously
- Expected completion: 60-90 minutes
- No blocking dependencies

### Wave 2: Launch Phase 2 (Parallel)
- Start agent B1 immediately (no dependencies)
- Start agent B2 when A2 completes
- Expected completion: 60-120 minutes after Wave 1

### Wave 3: Launch Phase 3 (Parallel)
- Start agents C1, C2 when Phase 1 completes
- Expected completion: 45-60 minutes after Wave 1

### Wave 4: Launch Phase 4 (Sequential)
- Start agent D1 when all previous agents complete
- Expected completion: 30-45 minutes after Wave 3

**Total Pipeline Time**: 3-4 hours wall clock (vs 10-15 hours sequential)

---

## Agent Communication Protocol

Each agent will produce:
1. **Structured data files** in `data/` directory
2. **Report markdown** in `reports/` directory
3. **Metadata JSON** with completion status, errors, confidence levels

### Standard Report Format
```markdown
# Agent [ID]: [Name]

## Status
- Started: [timestamp]
- Completed: [timestamp]
- Status: SUCCESS | PARTIAL | FAILED

## Summary
[2-3 sentence summary of findings]

## Key Findings
- Finding 1
- Finding 2
- ...

## Data Produced
- File 1: description
- File 2: description

## Confidence Assessment
- Data quality: HIGH | MEDIUM | LOW
- Coverage completeness: X%
- Limitations: [list]

## Recommendations for Synthesis
[How downstream agents should use this data]

## Blockers/Issues
[Any problems encountered]
```

---

## Success Metrics

### Phase 1 Success
- ✅ 100+ miles of trail data acquired
- ✅ High-resolution satellite imagery covering search area
- ✅ Cell coverage and environmental data obtained

### Phase 2 Success
- ✅ Trail features identified in aerial photos 4-6
- ✅ 10+ visual matches found in satellite imagery
- ✅ Match confidence scores calculated

### Phase 3 Success
- ✅ Search area reduced to <20 miles of trail
- ✅ Top 50 locations scored and ranked
- ✅ Probability map generated

### Phase 4 Success
- ✅ Top 10-20 locations validated across methods
- ✅ Field guide ready for use
- ✅ Confidence levels documented

---

## Fallback Strategies

### If satellite imagery unavailable (A2):
- Agent B2 skips matching, focuses on feature extraction only
- Agent C2 proceeds with other scoring factors
- Final recommendations rely more on constraint filtering

### If trail data incomplete (A1):
- Focus on known/named trails only
- Use satellite imagery to manually identify trails
- Reduce confidence in final recommendations

### If visual matching fails (B2):
- Rely entirely on constraint-based filtering
- Use aerial photos for field validation only
- Increase number of candidate locations to compensate

---

## Next Steps

1. Create `data/` and `reports/` directories
2. Launch Phase 1 agents in parallel
3. Monitor progress and handle any blockers
4. Launch subsequent phases as dependencies complete
5. Generate final synthesis report
