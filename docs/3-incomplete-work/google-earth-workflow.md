# Next Steps: Google Earth Analysis

**Purpose:** Manual data collection from Google Earth to enhance AI analysis and prioritize field searches.

**Time Required:** 2-4 hours total (can be done in phases)

**Prerequisites:**
- Google Earth (web or desktop) with Gemini access
- `trails_priority_only.kml` loaded
- See `GOOGLE_EARTH_DATA_COLLECTION.md` for detailed instructions

---

## Phase 1: Critical Validation (30-45 minutes)

### Cell Tower Proximity Check
**Goal:** Validate cellular coverage requirement (master constraint)

**For each of top 5 trails:**
1. Navigate to trail in Google Earth
2. Search for cell towers within 3 miles
3. Record tower locations and distance
4. Note carrier if visible (Verizon/AT&T preferred)

**Top 5 Trails to Check:**
- #1: Bent Creek Trail (35.4999, -82.6031)
- #2: Old Trestle Road (35.6397, -82.2944)
- #3: Old Trestle Road (35.6390, -82.2950)
- #4: Rainbow Road (35.639, -82.294)
- #5: Old Trestle Road (35.6386, -82.2943)

**Save as:** `data/google_earth/cell_towers.csv`

**Format:**
```csv
trail_name,rank,tower_lat,tower_lon,distance_miles,carrier,notes
Bent Creek Trail,1,35.5123,-82.6234,2.1,Verizon,"On ridge north of trail"
```

**Why Critical:** Can immediately eliminate trails without cellular coverage.

---

## Phase 2: Visual Matching (1-2 hours)

### Satellite Screenshot Collection
**Goal:** Compare satellite imagery to aerial photos for visual matching

**For top 5 trails, capture:**
- 3-4 screenshots per trail at different segments
- Eye altitude: 500-1000 feet
- View: Directly overhead (0° tilt)
- Area: 200-300 yard sections

**Screenshot Naming:**
```
data/google_earth/screenshots/
├── rank01_bent_creek_seg1.jpg
├── rank01_bent_creek_seg2.jpg
├── rank02_old_trestle_seg1.jpg
└── ...
```

**For each screenshot, note:**
- GPS coordinates (center of image)
- Eye altitude
- Trail visibility (1-5 rating)
- Canopy density estimate (%)
- Surface color visible

**Create metadata file:** `data/google_earth/screenshots/metadata.csv`
```csv
filename,trail_name,rank,segment,lat,lon,eye_altitude_ft,trail_visibility,canopy_percent,notes
rank01_bent_creek_seg1.jpg,Bent Creek Trail,1,1,35.5001,-82.6033,500,4,70,"Brown trail visible"
```

**Why Important:** AI can compare to photos/04-06 for visual signature matching.

---

## Phase 3: Terrain Analysis (1 hour)

### Off-Trail Search Zone Identification
**Goal:** Identify specific GPS waypoints for field searches

**For each trail segment:**
1. Tilt view to 45° to see terrain
2. Use ruler tool to measure 20-50 yards from trail
3. Identify areas that are:
   - Flat or gentle slope (not ravine/cliff)
   - Visible ground through canopy (50-80% coverage)
   - Accessible terrain (no water, no dense thicket)
   - Near high ground (better cell coverage)

**Mark waypoints and record:**
```csv
trail_name,segment,zone_lat,zone_lon,distance_from_trail_yards,terrain_type,canopy_density,accessibility,notes
Bent Creek Trail,seg1,35.5003,-82.6031,30,flat,60%,easy,"Visible clearing"
```

**Save as:** `data/google_earth/search_zones.csv`

**Why Important:** Creates specific GPS targets for field searches instead of hiking entire trails.

---

## Phase 4: Historical Changes (30 minutes)

### Ground Disturbance Detection
**Goal:** Find recent changes indicating treasure placement

**For each top 5 trails:**
1. Use Historical Imagery slider (clock icon)
2. Compare October 2024 vs October 2023
3. Look for:
   - New clearings
   - Ground disturbance (light colored soil)
   - Changes in vegetation
   - New paths/offshoots

**Record findings:**
```csv
trail_name,segment,observation,date_old,date_new,lat,lon,notes
Bent Creek Trail,seg2,Ground disturbance,2023-10-15,2024-10-09,35.5012,-82.6034,"Small clearing visible 40 yards west"
Old Trestle Road,seg1,No change,2023-09-20,2024-10-12,35.6398,-82.2945,"No visible disturbances"
```

**Save as:** `data/google_earth/historical_changes.csv`

**Why Important:** Treasure placed Oct 8-9, 2024. Recent disturbances are strong indicators.

---

## Phase 5: Google Earth Gemini Queries (30 minutes)

### Natural Language Analysis
**Goal:** Use Gemini AI to analyze your verified trails

**Recommended Queries:**

### Query 1: Multi-Trail Comparison
```
Analyze these 5 trail locations and rank by:
1. Cellular coverage likelihood (proximity to towers/towns)
2. Trail visibility from satellite
3. Terrain accessibility off-trail

Trails:
1. Bent Creek Trail (FS 480A): 35.4999, -82.6031
2. Old Trestle Road: 35.6397, -82.2944
3. Rainbow Road: 35.639, -82.294
4. Lower Staire (FS 231): 35.XXX, -82.XXX
5. Old Mitchell Toll Road: 35.XXX, -82.XXX

For each, show satellite view and identify specific areas 20-50 yards
off trail that are flat/accessible with moderate canopy coverage.
```

### Query 2: Visual Feature Matching
```
Show satellite imagery for Bent Creek Trail near 35.4999, -82.6031.
Identify sections with:
- Brown/tan bare dirt trail surface visible
- 3-6 feet trail width
- Dense green understory on both sides
- Deciduous forest (50-80% canopy coverage)
- Flat or gentle slope terrain

Compare to these characteristics from aerial photos I have.
```

### Query 3: Historical Analysis
```
For Old Trestle Road at 35.6397, -82.2944, compare satellite
imagery from October 2024 vs October 2023. Show any changes or
ground disturbances within 50 yards of the trail.
```

### Query 4: Cell Coverage Validation
```
Show cell tower locations within 3 miles of:
- Bent Creek Trail: 35.4999, -82.6031
- Old Trestle Road: 35.6397, -82.2944

Which trail has better AT&T/Verizon coverage based on tower proximity?
```

**Save Gemini Outputs:**
- Copy/paste responses to `data/google_earth/gemini_analysis.txt`
- Screenshot any maps Gemini shows
- Note any trails Gemini suggests that aren't in your top 20 (flag for review)

---

## Data Submission for AI Analysis

### Once Data is Collected:

**Minimum Dataset (enables analysis):**
- Cell tower CSV (Priority 1)
- 5-10 satellite screenshots with metadata

**Complete Dataset (optimal analysis):**
- Cell towers CSV
- Screenshots with metadata
- Search zones CSV
- Historical changes CSV
- Gemini outputs

### How to Submit:
1. Save all files to `data/google_earth/` directory
2. Notify Claude: "Google Earth data collected and ready for analysis"
3. I will launch specialized agents:
   - **Agent GE1:** Visual matching (satellite vs aerial photos)
   - **Agent GE2:** Cell tower coverage analysis
   - **Agent GE3:** Terrain prioritization
   - **Agent GE4:** Historical change detection

---

## Expected Outputs from AI Analysis

### After providing data, you'll receive:

1. **Prioritized Trail Rankings**
   - Updated confidence scores based on Google Earth data
   - Trails ranked by cell coverage + visual match + accessibility

2. **Specific GPS Waypoints**
   - List of coordinates for field searches
   - Ranked by probability (high/medium/low)
   - Distance and directions from trailhead

3. **Visual Match Report**
   - Which trail segments best match aerial photos 04-06
   - Similarity scores for each trail
   - Screenshots highlighting matching features

4. **Cell Coverage Assessment**
   - Which trails have verified cellular infrastructure
   - Elimination of trails without coverage
   - Priority ranking based on tower proximity

5. **Field Search Plan**
   - Day-by-day search itinerary
   - Time estimates per trail
   - Equipment/logistics recommendations

---

## Quick Start Option (45 minutes minimum)

### If pressed for time, just do this:

**Phase 1 Only: Cell Tower Validation**
- Check top 5 trails for cell towers within 3 miles
- Save as `data/google_earth/cell_towers.csv`
- This alone can eliminate trails and boost confidence

**Submit to Claude with:** "Cell tower data for top 5 trails collected"

---

## Integration with Existing Analysis

### Google Earth data will enhance:
- `FINAL_COMPREHENSIVE_REPORT.md` - Update confidence scores
- `FIELD_GUIDE.md` - Add specific GPS waypoints
- `treasure_map.html` - Update with new priority rankings
- `data/top_20_verified.csv` - Add cell_coverage_verified column

---

## Timeline Recommendation

### Week 1: Google Earth Reconnaissance
- **Day 1 (evening):** Phase 1 - Cell tower check (45 min)
- **Day 2 (evening):** Phase 2 - Screenshots (1-2 hours)
- **Day 3 (evening):** Phase 3 - Terrain analysis (1 hour)
- **Day 4:** Submit data for AI analysis

### Week 2: Field Verification
- **Day 5:** Receive AI analysis and updated waypoints
- **Day 6:** Prepare field trip (equipment, maps, logistics)
- **Day 7-8:** Field search top 3 trails

---

## Red Flags to Watch For

### While collecting data, if you notice:

❌ **No cell towers within 3 miles** → Deprioritize that trail
❌ **100% canopy coverage** → Not matching aerial photos (50-80%)
❌ **Dense evergreen forest** → Not matching photos (deciduous)
❌ **Trail not visible at all** → Hard to match to aerial imagery
❌ **Steep cliffs/ravines only** → Not matching "moderate terrain" requirement
❌ **Recent development/construction** → May invalidate Oct 2024 placement

✅ **Cell towers within 2 miles** → High priority
✅ **Clear trail visible from satellite** → Matches photos
✅ **Deciduous forest, moderate canopy** → Matches visual signature
✅ **Flat areas visible off trail** → Accessible for hiding treasure
✅ **Ground disturbance visible in Oct 2024** → Strong indicator

---

## Questions to Answer

### Your manual inspection should answer:

1. ✓/✗ **Cell Coverage:** Are there towers within 3 miles?
2. ✓/✗ **Trail Visibility:** Can you see the trail from satellite?
3. ✓/✗ **Visual Match:** Does it look like aerial photos 04-06?
4. ✓/✗ **Terrain Access:** Are there flat/accessible areas off trail?
5. ✓/✗ **Recent Changes:** Any ground disturbances Oct 2024?
6. ✓/✗ **Canopy Type:** Deciduous forest (light green in fall)?
7. ✓/✗ **Parking Access:** Can you see trailhead/parking?

**Goal:** Get 5+ checkmarks for a trail to classify as HIGH PRIORITY.

---

## Files to Create

```
data/google_earth/
├── cell_towers.csv                    ← Priority 1
├── screenshots/
│   ├── rank01_bent_creek_seg1.jpg
│   ├── rank02_old_trestle_seg1.jpg
│   └── metadata.csv
├── search_zones.csv                   ← Priority 2
├── historical_changes.csv             ← Priority 3
├── gemini_analysis.txt               ← If using Gemini
└── observations_notes.txt            ← General notes
```

---

## Ready to Begin?

### Checklist:
- [ ] Load `trails_priority_only.kml` into Google Earth
- [ ] Review `GOOGLE_EARTH_DATA_COLLECTION.md` for detailed instructions
- [ ] Create `data/google_earth/` directory structure
- [ ] Start with Phase 1 (cell towers) - 45 minutes
- [ ] Submit data when ready for AI analysis

### Get Coordinates for Top 5 Trails:
```bash
# Run this to extract coordinates:
cd /Users//workspace/treasure
cat data/top_20_verified.csv | head -6 | awk -F',' '{print $2}' | tail -5
```

Or check: `data/top_20_verified.geojson` for precise coordinates.

---

**Next Action:** Start Phase 1 (Cell Tower Check) for top 5 trails → Save to `data/google_earth/cell_towers.csv` → Submit for analysis
