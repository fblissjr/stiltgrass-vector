# Quick Start Guide - Automated Satellite Analysis

## 30-Second Summary

Run automated satellite analysis to boost confidence in top trail candidates **before** field visits:

```bash
cd /Users//workspace/treasure
uv pip install -r requirements.txt
uv run python scripts/quick_satellite_download.py
```

Then review images in `data/satellite_imagery/` - look for brown/tan trails through green forest.

---

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd /Users//workspace/treasure

# Install Python dependencies
uv pip install -r requirements.txt
```

**Dependencies installed:**
- pandas, numpy (data processing)
- geopandas, shapely (geospatial)
- opencv-python, pillow (computer vision)
- requests (satellite download)

### Step 2: Download Satellite Imagery (2 minutes)

```bash
uv run python scripts/quick_satellite_download.py
```

**What this does:**
- Downloads satellite imagery for top 5 trail candidates
- Uses free ESRI World Imagery (no API key needed)
- Saves to `data/satellite_imagery/`

**Output:**
```
Rank 1: Bent_Creek_Trail
  ✓ Saved: rank1_Bent_Creek_Trail_single.jpg
  ✓ Saved: rank1_Bent_Creek_Trail_3x3.jpg
...
```

### Step 3: Review Downloaded Images (5 minutes)

```bash
open data/satellite_imagery/
```

**Look for:**
- Brown/tan linear trails (3-6 feet wide)
- Through green deciduous forest
- Orientation: N-S (0-15°) or NW-SE (165-180°)
- Compare to `photos/04_aerial.jpg`, `photos/05_aerial.jpg`, `photos/06_aerial.jpg`

**Rate each trail:**
- ✅ **HIGH**: Trail clearly visible, matches photos
- 🟡 **MEDIUM**: Some features visible
- ❌ **LOW**: Trail not visible or doesn't match

---

## 15-Minute Full Analysis (Optional)

### Run Automated Computer Vision Analysis

```bash
uv run python scripts/automated_satellite_analysis.py
```

**What this does:**
- Edge detection to find linear trail features
- Hough transform to detect trail angles
- Color analysis (brown trail vs green forest)
- Feature matching against aerial photos 4-6
- Generates confidence scores (0-100)

**Output:**
```json
{
  "name": "Old_Trestle_Road",
  "lat": 35.6397,
  "lon": -82.2944,
  "confidence": 75,
  "visible": true,
  "num_lines": 45,
  "orientation_match": true,
  "color_match": true,
  "match_score": 18.5,
  "match_quality": "MEDIUM"
}
```

**Results saved to:** `data/satellite_imagery/automated_analysis_results.json`

### Interpret Confidence Scores

- **70-100**: HIGH confidence - Priority field visit
- **50-70**: MEDIUM confidence - Secondary priority
- **0-50**: LOW confidence - Lower priority or needs manual check

---

## What to Do With Results

### High Confidence Trails (70+)
1. Print satellite image
2. Load GPS coordinates on phone
3. Visit with cellular coverage tester
4. Search 20-50 yards off trail
5. Compare terrain to aerial photo #1

### Medium Confidence Trails (50-70)
1. Manual Google Earth check first
2. If confirmed, visit after high-priority trails

### Low Confidence Trails (<50)
1. Manual verification needed
2. May have tree canopy obscuring trail
3. Consider visiting if top trails unsuccessful

---

## File Locations

**Scripts:**
- `scripts/quick_satellite_download.py` - Fast download (2 min)
- `scripts/automated_satellite_analysis.py` - Full analysis (10-15 min)

**Outputs:**
- `data/satellite_imagery/rank*.jpg` - Downloaded images
- `data/satellite_imagery/automated_analysis_results.json` - Confidence scores

**Reference:**
- `photos/04_aerial.jpg` - Trail visible at mid-altitude
- `photos/05_aerial.jpg` - Mid-altitude context
- `photos/06_aerial.jpg` - Higher altitude view
- `data/top_20_verified.csv` - Trail rankings

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
uv pip install -r requirements.txt
```

### "Cannot download satellite imagery"
- Check internet connection
- ESRI servers may be temporarily down
- Try manual Google Earth check instead

### "No trails.geojson file found"
- Script will use hardcoded coordinates for top 5 trails
- Manual coordinates are provided as fallback

### Images downloaded but can't see trails
- Trails may be obscured by tree canopy
- Try zooming in on images
- Compare multiple images (single vs 3x3)
- Run full automated analysis for computer vision detection

---

## Expected Time Investment

| Task | Time | Value |
|------|------|-------|
| Install dependencies | 2 min | Required once |
| Download satellite images | 2 min | Quick visual check |
| Review images manually | 5-10 min | Human validation |
| Run automated analysis | 10-15 min | Quantified scores |
| **Total** | **20-30 min** | **Boost confidence 10-20%** |

---

## Success Criteria

**Before automated analysis:**
- Top 18 trails identified
- 75-85% overall confidence
- 60-70% confidence for top 10

**After automated analysis:**
- Visual confirmation of 3-5 trails
- 80-90% confidence for visually confirmed trails
- Prioritized field visit list
- Reduced field time by 50% (visit only high-confidence trails)

---

## Next Steps After Analysis

1. **High confidence trails found:**
   - Use `FIELD_GUIDE.md` for field visit instructions
   - Print satellite images for reference
   - Visit in ranked order (highest confidence first)

2. **No high confidence matches:**
   - Expand analysis to ranks 6-10
   - Consider manual Google Earth inspection
   - Review analysis methodology in `FINAL_COMPREHENSIVE_REPORT.md`

3. **Mixed results:**
   - Visit high-confidence trails first
   - Keep medium-confidence trails as backup
   - Document findings to refine analysis

---

## Quick Commands Reference

```bash
# Install dependencies
uv pip install -r requirements.txt

# Download satellite imagery (fast)
uv run python scripts/quick_satellite_download.py

# Run automated analysis (comprehensive)
uv run python scripts/automated_satellite_analysis.py

# View images
open data/satellite_imagery/

# Check results
cat data/satellite_imagery/automated_analysis_results.json
```

---

**For detailed analysis methodology, see:**
- `FINAL_COMPREHENSIVE_REPORT.md` - Complete analysis
- `FIELD_GUIDE.md` - Field search instructions
- `CLAUDE.md` - Project technical documentation
