# Google Earth Gemini Queries for Treasure Hunt

Since you have access to Google Earth with Gemini, here are strategic queries to narrow your search.

---

## Top Priority Queries

### 1. Bent Creek Trail (Rank #1) - Score 125
**Coordinates:** 35.4999, -82.6031

```
Show me Bent Creek Trail (FS 480A) in Pisgah National Forest near 35.4999, -82.6031.
Identify areas 20-50 yards off the trail with:
- Bare ground or leaf litter visible through tree canopy
- Mixed deciduous forest (not dense evergreen)
- Gentle slopes or flat terrain
- Within sight of the trail if standing tall
```

**Follow-up:**
```
Compare satellite imagery of this trail from October 2024, 2023, and 2022.
Show any new disturbances or changes near the trail.
```

---

### 2. Old Trestle Road (Ranks #2, #3, #5) - Score 125
**Coordinates:** 35.6397, -82.2944

```
Show me Old Trestle Road historic railroad grade near 35.6397, -82.2944 in Buncombe County.
This is a ground surface trail. Identify sections where:
- The trail is clearly visible from satellite (brown/tan bare dirt)
- Dense understory vegetation grows on both sides
- Terrain is accessible for hiking 50 yards off trail
- Cell towers or towns are visible within 2-3 miles
```

**Follow-up:**
```
Measure the distance from Old Trestle Road trailhead to the nearest cell tower.
Show AT&T and Verizon coverage in this area if available.
```

---

### 3. Rainbow Road (Rank #4) - Score 125
**Coordinates:** 35.639, -82.294 (Montreat area)

```
Find Rainbow Road near Montreat, NC (35.639, -82.294).
Show areas where:
- Trail is visible as doubletrack
- Orange trail markers might be visible
- Terrain allows easy off-trail access
- Deciduous forest dominates (not evergreen)
```

---

### 4. Lower Staire (Rank #8) - Score 120
**Coordinates:** 35.XXX, -82.XXX (check data/top_20_verified.geojson)

```
Show me Lower Staire (FS 231) trail. Identify areas:
- Within 0.45 miles of trail length
- With gravel surface visible from above
- Within 2 miles of valley towns (for cell coverage)
- At elevation 3,000-4,500 feet
```

---

### 5. Old Mitchell Toll Road (Rank #9) - Score 120
**Coordinates:** Check top_20_verified.geojson

```
Show Old Mitchell Toll Road near [coordinates].
Compare this trail to the aerial photos I'm analyzing:
- Brown/tan bare dirt trail surface
- 3-6 feet wide
- Dense green understory vegetation
- Mixed deciduous canopy (50-80% coverage)
```

---

## Analytical Queries

### Multi-Trail Comparison
```
Compare these 5 trail locations and rank by likelihood of cellular coverage:
1. Bent Creek Trail: 35.4999, -82.6031
2. Old Trestle Road: 35.6397, -82.2944
3. Rainbow Road: 35.639, -82.294
4. Lower Staire: [coordinates]
5. Old Mitchell Toll Road: [coordinates]

Show proximity to cell towers, towns, and main roads.
```

### Terrain Analysis
```
For each of these trails, identify flat areas or gentle slopes
(not steep cliffs) within 50 yards where a small cylindrical object
could be hidden on the forest floor.
```

### Vegetation Pattern Matching
```
Show areas in western North Carolina (35.6-36.4°N, 82.2-83.0°W) with:
- Mixed deciduous forest (visible yellow-green in fall)
- NOT dense evergreen forest
- Moderate canopy density (50-80%, not solid coverage)
- Visible understory vegetation
Match this to trails within 2 hours drive from Charlotte, NC.
```

### Historical Imagery Analysis
```
For trails at [coordinates], show satellite imagery from:
- October 2024 (when treasure was placed)
- October 2023 (pre-placement)
Compare and highlight any ground disturbances, new trails, or changes.
```

---

## Visual Feature Matching

### Trail Surface Detection
```
Analyze satellite imagery for trails near these coordinates: [list top 5].
Identify trails with:
- Brown/tan bare dirt surface (RGB approximately 140, 120, 90)
- Trail width 3-6 feet visible from above
- Linear path with gentle curves
- Clear trail edges distinct from surrounding forest
```

### Canopy Analysis
```
Show forest canopy density along these trails: [coordinates].
Identify sections with 50-80% canopy coverage where:
- Ground is partially visible through leaves
- Deciduous trees dominate (not conifers)
- Understory vegetation is dense
```

---

## Access and Logistics

### Drive Time Analysis
```
Calculate drive time from Charlotte, NC (35.2271, -80.8431) to:
1. Bent Creek Trail trailhead
2. Old Trestle Road trailhead
3. Rainbow Road trailhead
Which are within 2 hours drive?
```

### Parking and Access
```
Show parking areas and trail access points for:
- Bent Creek Experimental Forest
- Old Trestle Road (Montreat area)
- Rainbow Road
- Lower Staire (FS 231)
Which have established trailheads with public parking?
```

### Cellular Infrastructure
```
Show cell tower locations within 5 miles of these trails: [coordinates].
Identify which trails are within 2-3 miles of AT&T or Verizon towers.
```

---

## Advanced Queries

### Pattern Recognition Across All Trails
```
I'm searching for a treasure hidden off a hiking trail in western NC.
The location has these characteristics:
- 3,000-4,500 feet elevation
- Mixed deciduous forest
- Ground surface or gravel trail
- Within 50 yards of trail
- Cell phone coverage (AT&T or Verizon)
- 2 hours drive from Charlotte, NC
- NOT on private land

Analyze satellite imagery and suggest the 10 most likely trail locations
matching these criteria.
```

### Photo Matching
```
I have aerial photos showing:
- Dense leaf litter and understory vegetation
- Mixed deciduous forest canopy (50-80% coverage)
- Brown/tan trail surface visible in some photos
- Japanese stilt grass (invasive species) present

Find trails in Buncombe County, NC that match this visual signature
in satellite imagery.
```

---

## Iteration Strategy

### Phase 1: Broad Reconnaissance (First Session)
1. Run multi-trail comparison query
2. Verify cellular coverage for top 5 trails
3. Check historical imagery for changes
4. Identify parking and access points

### Phase 2: Detailed Analysis (Second Session)
1. Trail-by-trail detailed terrain analysis
2. Identify specific 50-yard zones off each trail
3. Compare satellite vs aerial photo features
4. Rank zones by probability

### Phase 3: Field Planning (Third Session)
1. Create waypoints for high-probability zones
2. Plan driving routes and logistics
3. Estimate search time for each trail
4. Prioritize based on Gemini insights

---

## Output Format Requests

When querying, you can request specific formats:

```
"Show me [query] and provide:
- GPS coordinates for identified areas
- Distance measurements from trail
- Elevation data if available
- Historical imagery comparison
- Export as KML for offline use"
```

---

## Integration with Existing Analysis

### Cross-Reference with AI Analysis
After Gemini provides insights, compare with:
- `data/top_20_verified.csv` - Your scored rankings
- `reports/agent_b2_findings.md` - Cellular coverage requirements
- `data/photo_features/visual_signature.md` - Visual matching criteria
- `FIELD_GUIDE.md` - Field search protocols

### Update Rankings
If Gemini reveals new insights (e.g., one trail has no cell coverage, another has recent disturbances), update your field search priority order.

---

## Example Conversation Flow

**You:** "Show me Bent Creek Trail near 35.4999, -82.6031 in satellite view.
Identify areas 20-50 yards off trail with visible ground and moderate canopy."

**Gemini:** [Shows satellite imagery with highlighted areas]

**You:** "Of those areas, which are within 2 miles of cell towers for AT&T or Verizon coverage?"

**Gemini:** [Filters to show areas with likely coverage]

**You:** "Compare the terrain in those areas to this description:
mixed deciduous forest, leaf litter on ground, dense understory vegetation,
gentle slope or flat terrain. Which zones match best?"

**Gemini:** [Ranks zones by match quality]

**You:** "Create waypoints for the top 3 zones and measure walking distance from trailhead."

**Gemini:** [Provides coordinates and distances]

---

## Notes

- Gemini can analyze patterns humans might miss in satellite imagery
- Can correlate multiple data sources (terrain, coverage, access)
- May identify trails you haven't considered that match criteria
- Can validate or refute assumptions (like cellular coverage at specific locations)

## Important

If Gemini suggests trails NOT in your top 20, cross-check against:
- Access restrictions (must be public land)
- Drive time from Charlotte (<2 hours)
- Trail surface type (ground/gravel preferred)
- Temperature/elevation correlation (55°F = 3,000-4,500 ft)

Do not explore Gemini suggestions that violate hard constraints.

---

**Remember:** Gemini in Google Earth is a powerful tool, but the cellular coverage requirement and public access constraints remain your master filters. Use Gemini to optimize within those constraints, not replace them.
