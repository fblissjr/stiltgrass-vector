# Archived Data Files

This directory contains intermediate and superseded data files from the treasure hunt analysis.

## Why These Files Were Archived

These files represent intermediate analysis steps that have been superseded by more comprehensive or corrected versions in the main `data/` directory.

## Files and Their Replacements

### `final_top_20.csv`
- **Status**: Superseded by `data/top_20_verified.csv`
- **Reason**: Early version before access verification and ranking corrections

### `top_50_candidates.csv`
- **Status**: Intermediate result
- **Reason**: Top 50 before narrowing to verified top 20

### `all_scored_trails.csv`
- **Status**: Raw scores before verification
- **Reason**: Contains all 11,954 trails with initial scores, before access audit
- **Replacement**: `data/trails_summary.csv` (includes access categories)

### `public_trails_verified.csv`
- **Status**: Intermediate verification
- **Reason**: Early access verification, superseded by comprehensive audit
- **Replacement**: `data/top_20_verified.csv` with full verification

## Key Differences from Current Data

1. **Access Verification**: Archived files may include trails later found to be private
2. **Scoring System**: Early files used different scoring before refinement
3. **County Attribution**: Some files have incomplete county data
4. **Ranking Changes**: Quartz Mtn Trail was #1 initially, later removed due to private access

## Current Data Files to Use

For current analysis, use these files in `data/`:
- `top_20_verified.csv` - Final verified rankings (18 trails)
- `trails_summary.csv` - All trails with complete metadata
- `private_trails_flagged.csv` - Trails eliminated due to access restrictions

## Historical Value

These files are preserved to show the evolution of the analysis and document corrections made during the verification process.
