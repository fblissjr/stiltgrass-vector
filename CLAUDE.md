# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status: ARCHIVED (Educational Resource)

**This repository is an educational archive** demonstrating both the capabilities and failure modes of AI-assisted analysis. The treasure hunt ended in October 2025. We did not find the treasure.

**The Key Lesson:** We reduced 5,940 square miles to 18 trails (99.96% reduction), but eliminated the correct answer on Day 2 because our scoring system penalized missing metadata with 0 points.

---

## What Happened

### The Challenge
- $25,350 in gold coins hidden in Blue Ridge Mountains
- 5,940 square mile search area (Day 8)
- 11,954 trail segments to evaluate
- 21-day shrinking search circle

### Our Approach: Multi-Agent AI System
- **Agent A1:** Parsed 11,954 trails from KML
- **Agent B2:** Decoded trail camera EXIF, identified cellular requirement
- **Agent C1:** Applied constraints, created 130-point scoring system
- **Agent C2:** Computer vision on aerial photos
- **Agent V1:** Verified access restrictions, found 470 private trails

### What Worked
- 99.96% search space reduction
- Cellular coverage as master constraint (correctly identified)
- Temperature-to-elevation inference (validated post-hunt)
- Access restriction audit (caught private trail in #1 ranking)

### What Failed: The Scoring System
```python
# THE FATAL ERROR
SCORE_SURFACE = {
    'ground': 40, 'dirt': 35, 'gravel': 25,
    'unknown': 0  # <- Penalized 85% of trails
}
```

**Red Trail (actual treasure location):**
- 17.9 miles from search center
- Score: 15/130 (sparse OSM metadata)
- Rank: ~#500-1000 (eliminated)

**Bent Creek Trail (our top pick):**
- 19.1 miles from search center
- Score: 125/130 (complete OSM metadata)
- Rank: #1 (wrong)

### The Winner's Method
Corey (@Fuzzy) and his daughter Zoe used cloud shadow triangulation:
1. Archived webcam images every 10 minutes for 10+ days
2. Matched cloud shadows to satellite cloud positions
3. Triangulated location using shadow angles + sun position
4. Found treasure in 11 days

**Temporal observation > static database analysis**

---

## Repository Structure

```
treasure/
├── README.md                 <- Main entry point
├── CLAUDE.md                 <- AI assistant guidance (this file)
├── INVENTORY.md              <- Complete file catalog
│
├── docs/                     <- All documentation (organized)
│   ├── 1-post-mortem/              # WHY IT FAILED (start here)
│   │   ├── enterprise-lessons.md       # Business/IT perspective
│   │   ├── technical-analysis.md       # Detailed code analysis
│   │   └── winning-solution.md         # How winner solved it
│   │
│   ├── 2-original-analysis/        # WHAT WE BUILT
│   │   ├── comprehensive-report.md     # Full analysis narrative
│   │   └── field-guide.md              # Field search instructions
│   │
│   ├── 3-incomplete-work/          # THINGS WE STARTED
│   │   └── google-earth-*.md           # Unfinished workflows
│   │
│   └── 4-reference/                # CONTEXT
│       └── contest-rules.md            # Original rules
│
├── scripts/                  <- Python analysis code
│   ├── analyze_trails.py           # Agent A1: KML parsing
│   ├── filter_and_score_trails.py  # Agent C1: Scoring (THE FLAW)
│   ├── verify_trail_access.py      # Agent V1: Access audit
│   ├── extract_exif.py             # Agent B2: EXIF decoding
│   ├── automated_satellite_analysis.py  # Agent C2: Computer vision
│   └── create_treasure_map.py      # Visualization
│
├── data/                     <- 41 MB processed data
│   ├── trails_summary.csv          # All 11,954 trails
│   ├── top_20_verified.csv         # Final rankings (wrong)
│   ├── private_trails_flagged.csv  # 470 private trails
│   ├── filter_statistics.json      # Filtering metrics
│   └── photo_features/             # CV analysis outputs
│
├── reports/                  <- Agent findings (technical)
│   ├── agent_a1_findings.md        # Trail data analysis
│   ├── agent_b2_findings.md        # Camera specs, cellular
│   ├── agent_c1_findings.md        # Constraint filtering
│   ├── agent_c2_findings.md        # Computer vision
│   └── trail_verification.md       # External verification
│
├── photos/                   <- 8 aerial photos (150 MB)
├── trails.kml                <- Original OSM data (13 MB)
├── treasure_map.html         <- Interactive map
└── archive/                  <- Old scripts and early drafts
```

---

## Key Lessons for AI Development

### 1. Data Quality vs Data Completeness
```
Missing data != bad data
Well-documented != high quality
Sparse metadata = less-resourced data collection, not inferior subject
```

### 2. Profile Data BEFORE Building Systems
```python
# Run this FIRST on any dataset:
completeness = df.isnull().sum() / len(df) * 100
for col in df.columns:
    if completeness[col] > 50:
        print(f"WARNING: {col} is {completeness[col]:.1f}% missing")
        print(f"DO NOT use for filtering or heavy scoring")
```

### 3. Geographic Proximity > Metadata Quality
In spatially-constrained problems, distance from target should be PRIMARY factor, not documentation completeness.

### 4. Ensemble Methods Beat Single Models
If we had run 5 ranking methods, Red Trail would have shown HIGH VARIANCE across them, flagging it for investigation.

### 5. Temporal Data > Static Snapshots
For monitored targets (webcam), temporal observation beats static database analysis.

### 6. Domain Experts Are Essential
No local hiking expert who knew:
- Bailey Mountain Preserve exists
- Madison County is adjacent to Buncombe
- Municipal trails near towns have better cell coverage

---

## Running the Code (Educational)

```bash
cd /Users/fredbliss/workspace/treasure

# Setup
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Analysis pipeline
uv run python scripts/analyze_trails.py
uv run python scripts/filter_and_score_trails.py
uv run python scripts/verify_trail_access.py
uv run python scripts/create_treasure_map.py

# Optional: Satellite analysis
uv run python scripts/quick_satellite_download.py
uv run python scripts/automated_satellite_analysis.py
```

---

## Key Data Files

### Input
- `trails.kml` (13 MB) - 11,954 trail segments from OpenStreetMap

### Processed
- `data/trails_summary.csv` (826 KB) - All trails with metadata
- `data/trails.geojson` (28 MB) - Full trail geometries
- `data/top_20_verified.csv` - Final rankings (WRONG ANSWER)
- `data/private_trails_flagged.csv` - 470 private trails found
- `data/filter_statistics.json` - Filtering metrics

### Analysis
- `data/photo_features/` - Computer vision outputs
- `data/satellite_imagery/` - Satellite imagery analysis
- `data/camera_technical_specs.md` - StealthCam analysis
- `data/cellular_requirements.md` - Coverage analysis

---

## The 130-Point Scoring System (Flawed)

| Factor | Points | Issue |
|--------|--------|-------|
| Surface Type | 40 | Unknown scored 0 (should be neutral) |
| Difficulty | 25 | Unknown scored 0 (should be neutral) |
| Trail Type | 20 | OK |
| Length | 15 | OK |
| Named Trail | 10 | OK |
| Forest Service | 10 | Biased toward federal vs municipal |
| Buncombe County | 20 | 93% missing county tag |
| **Geographic Proximity** | **0** | **SHOULD HAVE BEEN 40+** |

---

## What Should Have Been Done

### Defensive Scoring
```python
SCORE_SURFACE = {
    'ground': 40, 'dirt': 35, 'gravel': 25,
    'paved': 0,      # Only penalize known-bad
    'unknown': 20    # Neutral for missing
}
```

### Geographic Prioritization
```python
SCORE_PROXIMITY = {
    '0-15 miles': 40,   # Highest weight
    '15-20 miles': 35,
    '20-25 miles': 30,
    '25-30 miles': 20,
    '30+ miles': 10
}
```

### Data Quality Audit First
```python
# Surface: 14.7% complete -> DON'T SCORE
# Difficulty: 7.5% complete -> DON'T SCORE
# County: 7.0% complete -> DERIVE FROM COORDINATES
# Coordinates: 100% complete -> PRIMARY FACTOR
```

### Ensemble Methods
Run 5 ranking methods, investigate high-variance results:
1. Geographic proximity
2. Metadata quality
3. Cellular coverage likelihood
4. Access certainty
5. Visual similarity

---

## Educational Value

### AI Strengths Demonstrated
- Scale: 11,954 trails in hours vs weeks
- Consistency: 8+ constraints applied without fatigue
- Multi-modal: GPS + EXIF + photos + rules synthesized
- Self-correction: Found private trail, re-ranked

### AI Failure Modes Demonstrated
- Metadata completeness bias
- Optimization target misalignment
- Missing domain expertise
- Single-method ranking
- No validation/holdout

### Enterprise Lessons
- Profile data quality BEFORE building systems
- Missing data != bad data
- Geographic proximity often strongest signal
- Ensemble methods catch what single models miss
- Domain experts provide context AI can't infer
- Always validate against holdout set

---

## Important Notes

### For AI Assistants
- This is an **archived educational repository**
- The analysis is complete but **the answer was wrong**
- Focus on explaining the failure modes, not improving the code
- The post-mortems contain the key lessons

### For Human Users
- Start with `docs/1-post-mortem/enterprise-lessons.md` for enterprise lessons
- Read `docs/1-post-mortem/winning-solution.md` to understand what the winner did
- Open `treasure_map.html` in browser for interactive exploration
- The `scripts/` directory shows the complete implementation

---

## Project Statistics

| Metric | Value |
|--------|-------|
| Trails analyzed | 11,954 |
| Trail miles | 3,198.82 |
| Search space reduction | 99.96% |
| Final candidates | 18 |
| Data processed | 41 MB |
| Time invested | 48 hours |
| Treasure found | No |
| Lessons learned | Invaluable |

---

## The Meta-Lesson

> We built a sophisticated AI system that processed gigabytes of data, ran complex algorithms, produced beautiful visualizations, and reduced an impossible search space by 99.96%. We had the answer in our dataset from the start. We eliminated it because it was poorly documented.

**In your enterprise, what correct answers are you eliminating because they're poorly documented?**

---

**Archive Date:** December 2025
**Project Duration:** October 2025
**Outcome:** Educational failure analysis

- Always run python and install pip packages using uv and uv venv
