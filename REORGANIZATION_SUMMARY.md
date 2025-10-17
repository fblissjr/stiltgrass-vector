# File Reorganization Summary

**Date:** 2025-10-17
**Reason:** Remove outdated assumptions (south-facing slope) and archive superseded files

---

## Files Archived

### Documentation → archive/
- `FINAL_REPORT.md` - Superseded by FINAL_COMPREHENSIVE_REPORT.md
- `ANALYSIS.md` - Early analysis notes, no longer current
- `IDEAS.md` - Brainstorming document, completed

### Data → archive/data/
- `final_top_20.csv` - Superseded by top_20_verified.csv
- `top_50_candidates.csv` - Intermediate result
- `all_scored_trails.csv` - Raw scores before access verification
- `public_trails_verified.csv` - Intermediate verification

### Scripts → archive/scripts/
- `analyze_buncombe.py` - County-specific analysis (outdated)
- `analyze_photos_optimized.py` - Duplicate photo analysis
- `analyze_photos.py` - Original photo analysis
- `analyze_top_candidates.py` - Intermediate analysis
- `create_summary_map.py` - Superseded by create_treasure_map.py
- `create_supplemental_analysis.py` - One-off analysis
- `extract_trail_angles.py` - **South-facing slope analysis (assumption removed)**

### Elevation Scripts → archive/scripts/elevation/
- `download_closest_tiles.py`
- `download_dem_tiles.py`
- `download_elevation_data.py`
- `download_srtm.py`
- `elevation_processor.py`
- `process_elevation.py`

**Note:** Elevation analysis was started but not completed. Cellular coverage proved more valuable than slope analysis.

### Reports → archive/reports/
- `extended_trail_verification.md` - Superseded by trail_verification.md

---

## Files Updated

### Core Documentation
- `CLAUDE.md` - Updated environment description, removed south-facing slope as constraint
- `FINAL_COMPREHENSIVE_REPORT.md` - Updated gaps section, search checklists, confidence ratings

### Reports
- `reports/google_earth_reconnaissance.md` - Removed trail orientation assumptions, updated slope assessment guidance

---

## New Files Created

### Google Earth Support
- `data/treasure_hunt_priority_trails.kml` - Enhanced KML with 18 top trails, rich HTML descriptions, priority tiers

### Archive Documentation
- `archive/scripts/README.md` - Explains why scripts were archived
- `archive/scripts/elevation/README.md` - Explains incomplete elevation analysis
- `archive/data/README.md` - Documents superseded data files

---

## Current Project Structure

```
treasure/
├── FINAL_COMPREHENSIVE_REPORT.md    ← START HERE (updated)
├── FIELD_GUIDE.md                   ← Field search instructions
├── treasure_map.html                ← Interactive map
├── CLAUDE.md                        ← Project context (updated)
├── README.md                        ← Installation and usage
├── QUICK_START.md                   ← Quick start guide
├── Treasure-doc.md                  ← Contest rules
│
├── data/                            
│   ├── treasure_hunt_priority_trails.kml  ← NEW: For Google Earth
│   ├── top_20_verified.csv          ← FINAL RANKINGS (18 trails)
│   ├── top_20_verified.geojson      
│   ├── trails_summary.csv           ← All 11,954 trails
│   ├── private_trails_flagged.csv   
│   └── photo_features/              ← CV analysis results
│
├── reports/                         
│   ├── agent_a1_findings.md         ← Trail data analysis
│   ├── agent_b2_findings.md         ← Camera analysis
│   ├── agent_c1_findings.md         ← Constraint filtering
│   ├── agent_c2_findings.md         ← Visual analysis
│   ├── trail_verification.md        ← Access verification
│   ├── google_earth_reconnaissance.md  ← Updated: removed slope assumptions
│   └── VERIFICATION_SUMMARY.md      
│
├── scripts/                         
│   ├── automated_satellite_analysis.py  ← Full CV analysis
│   ├── quick_satellite_download.py      ← Fast satellite download
│   ├── create_treasure_map.py           ← Generate HTML map
│   ├── filter_and_score_trails.py       ← Main scoring system
│   └── verify_trail_access.py           ← Access verification
│
├── archive/                         ← Superseded files
│   ├── scripts/                     
│   │   ├── elevation/              ← Incomplete elevation analysis
│   │   └── [7 archived scripts]    
│   ├── data/                        ← Intermediate data files
│   └── [3 archived docs]            
│
└── photos/                          ← Aerial photos 01-08
```

---

## Key Changes to Analysis Approach

### Removed Assumptions
1. **South-Facing Slope** - Cannot confirm from nighttime IR camera or overhead drone photos
2. **Trail Orientation (N-S/NW-SE)** - No reliable evidence for preferred orientation

### What Remains Valid
1. ✅ Cellular coverage (AT&T/Verizon 4G LTE) - **MASTER CONSTRAINT**
2. ✅ Elevation 3,000-4,500 ft (from 55°F temperature reading)
3. ✅ Public land access (verified via OSM access tags)
4. ✅ Trail surface (ground/gravel preferred)
5. ✅ Trail difficulty (hiking/grade2-3)
6. ✅ Japanese stilt grass habitat
7. ✅ 2-hour drive from Charlotte, NC

### Rankings Unaffected
- Top 18 trail rankings remain valid
- Scoring system never used slope orientation as factor
- All constraints applied were verifiable (access, surface, difficulty)

---

## Next Steps for Field Search

1. **Import KML into Google Earth**
   - File: `data/treasure_hunt_priority_trails.kml`
   - Contains all 18 top trails with detailed descriptions

2. **Visual Reconnaissance**
   - Review satellite imagery for each trail
   - Look for flat areas or any slopes (orientation not critical)
   - Identify areas 20-50 yards off trail

3. **Field Verification**
   - Start with Bent Creek Trail (#1)
   - Test cellular coverage at each location
   - Search areas matching aerial photo features

4. **Documentation**
   - Follow checklist in FIELD_GUIDE.md
   - Mark searched areas with GPS waypoints
   - Document findings for each trail

---

## Files Safe to Delete (If Needed)

These archived files can be permanently deleted if storage is a concern:
- `archive/scripts/*.py` (all archived scripts)
- `archive/data/*.csv` (all intermediate data)
- `archive/*.md` (superseded documentation)

However, they are preserved to show the evolution of the analysis.

---

**Summary:** Analysis remains valid. Rankings unchanged. South-facing slope assumption removed. Ready for field verification.
