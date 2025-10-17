# Google Earth Data Collection Guide

This guide explains what data to manually extract from Google Earth for AI analysis.

---

## Priority 1: Visual Matching (HIGHEST VALUE)

### Screenshot Collection - Trail Segments
For each of your top 5 trails, take satellite screenshots of:

**What to Capture:**
- Zoom level: 500-1000 feet eye altitude
- View: Directly overhead (0° tilt)
- Area: 200-300 yard sections of trail

**File Naming:**
```
screenshots/
├── rank01_bent_creek_segment1.jpg
├── rank01_bent_creek_segment2.jpg
├── rank01_bent_creek_segment3.jpg
├── rank02_old_trestle_segment1.jpg
└── ...
```

**Why This Helps:**
- AI can compare satellite imagery to your aerial photos (photos/04-08)
- Computer vision can detect trail visibility, surface color, canopy density
- Can identify sections matching visual signature

### How to Extract:
1. Navigate to trail coordinates
2. Set eye altitude to 500-1000 feet
3. Screenshot each 200-300 yard section
4. Save with descriptive filename

---

## Priority 2: Cellular Infrastructure (CRITICAL)

### Cell Tower Locations
For each top trail, document nearby cell towers:

**Data to Collect:**
```csv
trail_name,tower_lat,tower_lon,distance_miles,carrier,notes
Bent Creek Trail,35.5123,-82.6234,2.1,Verizon,"On ridge north of trail"
Bent Creek Trail,35.4892,-82.5987,2.8,AT&T,"Near highway 191"
Old Trestle Road,35.6401,-82.2756,1.4,Verizon,"Montreat area"
```

**How to Find Towers:**
- Google Earth layers → More → Enable "Cell Towers" (if available)
- Or search "cell tower near [trail name]"
- Or look for tall structures with antennas on ridges
- Note structures with dishes/antennas near trail

**Why This Helps:**
- Validates which trails have AT&T/Verizon coverage (master constraint)
- Can eliminate trails too far from towers (>3 miles suspect)
- Prioritizes trails with multiple nearby towers

### File Format:
Save as: `data/google_earth_cell_towers.csv`

---

## Priority 3: Terrain Features

### Off-Trail Zone Identification
For each trail segment, identify areas 20-50 yards off trail that match:

**Criteria:**
- Flat or gentle slope (not cliff/ravine)
- Visible ground through canopy (50-80% coverage)
- Accessible terrain (no water, no dense thickets visible)
- Within potential cell coverage (near ridge/high ground)

**Data Format:**
```json
{
  "trail_name": "Bent Creek Trail",
  "rank": 1,
  "segments": [
    {
      "segment_id": "seg1",
      "center_lat": 35.5001,
      "center_lon": -82.6033,
      "off_trail_zones": [
        {
          "zone_id": "zone1_north",
          "lat": 35.5003,
          "lon": -82.6031,
          "distance_from_trail_yards": 30,
          "terrain": "flat",
          "canopy_density": "60%",
          "accessibility": "easy",
          "notes": "Visible clearing, brown ground visible"
        }
      ]
    }
  ]
}
```

**Why This Helps:**
- Creates specific GPS waypoints for field search
- Reduces search area from miles to specific zones
- Can be analyzed by AI for probability ranking

### How to Collect:
1. Navigate to trail in Google Earth
2. Tilt view to 45° to see terrain
3. Use ruler tool to measure 20-50 yards from trail
4. Identify flat/accessible areas
5. Record GPS coordinates (right-click → "What's here?")

Save as: `data/google_earth_search_zones.json`

---

## Priority 4: Historical Imagery Timeline

### Ground Disturbance Detection
Check if any trails show recent changes:

**What to Look For:**
- New clearings near trail (Oct 2024 vs Oct 2023)
- Ground disturbance (lighter colored soil)
- New trail offshoots or paths
- Changes in vegetation

**Data Format:**
```csv
trail_name,segment,observation,image_date_old,image_date_new,notes
Bent Creek Trail,seg2,Ground disturbance,2023-10-15,2024-10-09,"Small clearing visible 40 yards west of trail"
Old Trestle Road,seg1,No change,2023-09-20,2024-10-12,"No visible disturbances"
```

**How to Extract:**
1. View → Historical Imagery (clock icon)
2. Compare October 2024 vs October 2023
3. Look for changes in 50-yard buffer around trails
4. Screenshot any suspicious areas

**Why This Helps:**
- Treasure was placed Oct 8-9, 2024
- Recent disturbances are strong indicators
- Can prioritize trails with visible changes

Save as: `data/google_earth_historical_changes.csv`

---

## Priority 5: Trail Visibility Ratings

### Trail Surface Visibility from Satellite
Rate how well each trail is visible:

**Rating Scale:**
- **5 = Excellent**: Clear brown/tan trail visible, distinct edges
- **4 = Good**: Trail mostly visible with some gaps
- **3 = Moderate**: Trail partially visible through canopy
- **2 = Poor**: Trail barely visible, heavy canopy
- **1 = None**: Trail not visible at all

**Data Format:**
```csv
trail_name,rank,segment,visibility_rating,trail_width_pixels,surface_color,canopy_density,notes
Bent Creek Trail,1,seg1,3,2-3,gray/brown,70%,"Gravel surface partially visible"
Old Trestle Road,2,seg1,4,2,brown,60%,"Bare dirt clearly visible"
Rainbow Road,4,seg1,2,1-2,unclear,80%,"Heavy canopy obscures trail"
```

**Why This Helps:**
- Validates aerial photos (photos 04-06 show brown/tan trail)
- Higher visibility = easier to hide nearby (less foot traffic?)
- Can match color signatures to your photo analysis

Save as: `data/google_earth_trail_visibility.csv`

---

## Priority 6: Canopy Density Analysis

### Tree Coverage Percentages
Estimate canopy density along trail segments:

**Method:**
1. Screenshot trail segment from above
2. Visually estimate % of green (trees) vs brown/ground
3. Note if deciduous (light green/yellow in fall) or evergreen (dark green)

**Data Format:**
```csv
trail_name,segment,canopy_percent,canopy_type,understory_visible,matches_photos
Bent Creek Trail,seg1,70,deciduous,yes,high
Old Trestle Road,seg1,60,deciduous,yes,high
Rainbow Road,seg1,85,mixed,no,low
```

**Why This Helps:**
- Photos 7-8 show 50-80% canopy, deciduous dominant
- Can eliminate trails with 100% canopy or dense evergreen
- Validates visual signature match

Save as: `data/google_earth_canopy_analysis.csv`

---

## Priority 7: Access and Parking

### Trailhead Information
Document parking and access for each trail:

**Data to Collect:**
```csv
trail_name,trailhead_lat,trailhead_lon,parking_available,parking_size,road_access,notes
Bent Creek Trail,35.4888,-82.6267,yes,large (50+ cars),paved,"USFS visitor center"
Old Trestle Road,35.6401,-82.2940,yes,small (5-10 cars),gravel,"Roadside parking"
```

**Include:**
- GPS coordinates of parking area
- Parking capacity (important for logistics)
- Road type (paved/gravel/dirt)
- Distance from parking to trail
- Any access restrictions visible

**Why This Helps:**
- Field trip planning
- Validates accessibility for treasure placement
- Creator needed to drive here in early October

Save as: `data/google_earth_trailheads.csv`

---

## Priority 8: 3D Terrain Elevation Profiles

### Elevation Along Trail Segments
Use Google Earth's elevation profile:

**How to Extract:**
1. Draw path along trail with Path tool
2. Right-click path → "Show Elevation Profile"
3. Screenshot elevation graph
4. Note: min elevation, max elevation, average

**Data Format:**
```csv
trail_name,segment,min_elevation_ft,max_elevation_ft,avg_elevation_ft,terrain_type
Bent Creek Trail,seg1,2890,3120,3005,rolling
Old Trestle Road,seg1,3340,3410,3375,gentle slope
```

**Why This Helps:**
- Validates 3,000-4,500 ft elevation requirement (from 55°F temp)
- Identifies flat sections (easier to hide treasure)
- Can eliminate sections outside elevation range

Save as: `data/google_earth_elevations.csv`

---

## Priority 9: Proximity to Towns/Infrastructure

### Nearby Settlements and Roads
Document civilization proximity:

**Data to Collect:**
- Nearest town/settlement and distance
- Major roads within 2 miles
- Power lines visible near trail
- Any buildings/structures within 1 mile

**Format:**
```csv
trail_name,nearest_town,distance_miles,major_road,road_distance_miles,structures_visible
Bent Creek Trail,Asheville,8.2,NC-191,1.5,yes (visitor center)
Old Trestle Road,Montreat,0.8,US-70,2.1,yes (houses)
```

**Why This Helps:**
- Cell coverage correlates with proximity to towns
- Creator lives in Charlotte (urban area familiarity?)
- Validates "accessible but remote" balance

Save as: `data/google_earth_infrastructure.csv`

---

## Priority 10: Comparative Screenshots (Visual Matching)

### Side-by-Side Comparisons
Take satellite screenshots that match your aerial photo angles:

**Goal:** Match photos/04-06 (mid-altitude aerial) to satellite view

**Method:**
1. Study aerial photos 04-06 characteristics:
   - Brown/tan trail visible
   - 3-6 feet wide
   - Dense green on both sides
   - Gentle curves
   - Deciduous canopy

2. Find trail segments in Google Earth that look similar
3. Screenshot at same scale/zoom as aerial photos
4. Save pairs for AI comparison

**File Structure:**
```
screenshots/comparison/
├── aerial_04_reference.jpg (your photo)
├── bent_creek_seg1_satellite.jpg (Google Earth)
├── bent_creek_seg2_satellite.jpg
├── old_trestle_seg1_satellite.jpg
└── ...
```

**Why This Helps:**
- AI can do pixel-by-pixel feature matching
- Can rank trails by visual similarity to aerial photos
- Most direct way to validate location hypotheses

---

## How to Submit Data for Analysis

### Option 1: Structured Data Files
Create these files and I can analyze them:
- `data/google_earth_cell_towers.csv`
- `data/google_earth_search_zones.json`
- `data/google_earth_trail_visibility.csv`
- `data/google_earth_historical_changes.csv`

### Option 2: Screenshots with Metadata
Save screenshots with naming convention:
```
screenshots/
├── rank01_bent_creek_seg1_satellite.jpg
├── rank01_bent_creek_seg1_500ft_altitude.txt (metadata)
└── ...
```

Metadata file content:
```
Trail: Bent Creek Trail
Rank: #1
Segment: 1
Eye Altitude: 500 feet
Center Coordinates: 35.5001, -82.6033
Date of Imagery: 2024-10-15
Canopy Density: ~70%
Trail Visibility: Good (rating 4/5)
Notes: Brown trail surface visible, deciduous forest
```

### Option 3: Gemini Outputs
If you use Google Earth Gemini, you can paste its responses and I'll analyze them for:
- Alignment with your verified trails
- New insights worth investigating
- Contradictions with existing analysis
- Actionable recommendations

---

## Agent Analysis Plan

Once you provide this data, I can launch specialized agents:

### Agent GE1: Visual Matching
- Compare satellite screenshots to aerial photos
- Calculate similarity scores using computer vision
- Rank trail segments by visual match

### Agent GE2: Cell Tower Analysis
- Map all towers relative to trails
- Calculate signal probability for each trail
- Eliminate trails with poor coverage

### Agent GE3: Terrain Prioritization
- Analyze off-trail zones for accessibility
- Create prioritized waypoint list for field search
- Rank by: accessibility + canopy match + cell coverage

### Agent GE4: Historical Change Detection
- Analyze before/after imagery
- Flag suspicious disturbances
- Prioritize trails with recent changes

---

## Quick Start: Minimum Viable Data

If you only have time for ONE task, do this:

### Collect Cell Tower Data for Top 5 Trails
1. Navigate to each top trail in Google Earth
2. Look for cell towers within 3 miles
3. Record tower locations and estimated distance
4. Save as simple CSV

**This single dataset can eliminate trails and boost confidence in others.**

---

## Example Workflow

**Day 1: Reconnaissance (2 hours)**
- Load `trails_priority_only.kml` into Google Earth
- For top 5 trails:
  - Take 3-4 satellite screenshots per trail
  - Note any cell towers visible
  - Mark any areas 20-50 yards off trail that look accessible
- Save screenshots with trail name labels

**Day 2: Data Entry (1 hour)**
- Create `google_earth_observations.csv` with findings
- Note trail visibility ratings
- Record cell tower proximity

**Day 3: AI Analysis**
- Provide data to Claude Code
- Launch specialized agents
- Get prioritized waypoint list for field search

**Day 4: Field Verification**
- Use waypoints from analysis
- Search top-ranked zones
- Document results

---

## Data Storage Locations

Save all Google Earth data in:
```
data/google_earth/
├── screenshots/
├── cell_towers.csv
├── search_zones.json
├── trail_visibility.csv
├── historical_changes.csv
├── canopy_analysis.csv
├── trailheads.csv
└── elevations.csv
```

I can create this directory structure and template files if helpful.

---

## Questions to Answer Through Manual Inspection

While collecting data, look for answers to these:

1. **Cell Coverage Validation**: Can you see cell towers near your top trails?
2. **Trail Visibility**: Are trails clearly visible in satellite view?
3. **Recent Changes**: Any ground disturbances visible Oct 2024 vs 2023?
4. **Terrain Accessibility**: Can you identify specific zones 20-50 yards off trail?
5. **Visual Match**: Do any satellite views match your aerial photos 04-06?
6. **Canopy Type**: Deciduous (light green) or evergreen (dark green)?
7. **Elevation Confirmation**: Are trail sections at 3,000-4,500 feet?
8. **Parking Access**: Can you see parking areas and trailheads?

---

## Most Valuable Single Dataset

If you can only provide ONE thing:

**High-resolution satellite screenshots of top 5 trails with GPS coordinates labeled**

This allows AI visual matching against your aerial photos, which is the most direct validation method.

---

Ready to analyze any data you collect! Just save files to `data/google_earth/` directory or share screenshots with metadata.
