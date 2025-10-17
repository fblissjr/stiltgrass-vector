# Cellular Requirements Analysis: StealthCam STC-DCPTRX

## Camera Model
**StealthCam Deceptor MAX (STC-DCPTRX)**

## Cellular Technology

### Dual SIM Configuration
- **Pre-installed SIM cards**: AT&T and Verizon (both included)
- **Technology**: 4G LTE cellular
- **Automatic Network Selection**: YES - continuously monitors both networks
- **Switching Behavior**: Automatically connects to strongest available signal

### Network Priority
The camera **does not prefer one carrier over the other**. It uses:
- Real-time signal strength monitoring
- Automatic failover between AT&T and Verizon
- Seamless switching without user intervention

## Signal Requirements

### Minimum Signal Strength
While StealthCam doesn't publish exact specifications, based on typical cellular trail camera requirements:
- **Minimum bars**: 2-3 bars (out of 5) on either AT&T or Verizon
- **Signal threshold**: Approximately -100 dBm to -85 dBm
- **4G LTE required**: Yes - camera uses 4G LTE for data transmission
- **3G support**: No longer supported by major carriers (AT&T/Verizon shut down 3G)

### Data Transmission
- **Upload frequency**: Configurable (in this case: every 10 minutes for webcam)
- **Data per image**: Approximately 100-200 KB for 720p JPEG
- **Daily data usage** (at 10-min intervals): ~14-28 MB per day
- **Monthly estimate**: 420-840 MB per month (moderate usage)

## Coverage Analysis: Blue Ridge Mountains

### Verizon Coverage (BEST)
**Advantages**:
- Superior coverage in Blue Ridge Mountains region
- Better performance in valleys and remote areas
- More reliable in Boone/Blowing Rock area
- Generally stronger signal in mountainous terrain

**Limitations**:
- Still experiences intermittent coverage on Blue Ridge Parkway
- Drop-outs more frequent in mountains than flat areas
- Some valleys and remote locations may have dead spots

### AT&T Coverage (GOOD)
**Advantages**:
- Decent coverage in Asheville and surrounding areas
- Good coverage in populated mountain towns

**Limitations**:
- Coverage weakens significantly north of Asheville and Black Mountain
- Considerably weaker west of Boone
- Absolute dead zones near Tennessee state line
- More "spotty" coverage in mountainous areas compared to Verizon

### Combined Dual-SIM Advantage
The dual-SIM automatic switching provides:
- **Redundancy**: If one network fails, switches to other
- **Optimal signal**: Always uses strongest available network
- **Increased reliability**: Much higher chance of maintaining connection
- **Coverage expansion**: Effectively combines coverage maps of both carriers

## Geographic Implications for Treasure Location

### HIGH PROBABILITY AREAS (Good coverage on both carriers)
- **Asheville vicinity** (but ruled out by other clues)
- **Boone area** - excellent Verizon, good AT&T
- **Blowing Rock area** - strong on both networks
- **Banner Elk region** - reliable dual coverage
- **Populated trailhead areas** - typically have cell coverage

### MODERATE PROBABILITY (Verizon coverage, spotty AT&T)
- **Blue Ridge Parkway access points** - intermittent but functional
- **Grandfather Mountain area** - Verizon works, AT&T weak
- **Linville Gorge rim areas** - depends on specific location
- **Remote but accessible trails** - may have one bar of Verizon

### LOW PROBABILITY (Poor coverage on both carriers)
- **Deep valleys** - signal blocked by terrain
- **Areas near Tennessee state line** - known AT&T dead zones
- **Linville Gorge floor** - canyon effect blocks signal
- **Cherokee area** - hit or miss coverage on Parkway
- **Extreme remote wilderness** - both carriers struggle

### RULED OUT (No coverage)
- **Wilderness areas deep in valleys**
- **Locations requiring significant off-trail hiking**
- **Areas more than 3-4 miles from cell towers**
- **Canyons and deep gorges with no line-of-sight to towers**

## Battery Life & Maintenance

### Expected Battery Life (with 10-minute upload frequency)
- **Standard rating**: 8.4 months (30 photos/day mixed day/night)
- **High-frequency uploads** (10-min intervals = 144 photos/day): Approximately 1.75-2.5 months
- **With solar panel**: Indefinite (recommended for this application)

### Power Configuration
- **Battery capacity**: 16 AA batteries
- **External power port**: 12V DC jack available
- **Solar compatibility**: Yes - StealthCam solar panels supported
- **Recommended setup**: Solar panel for sustained webcam operation

### Maintenance Visit Frequency
Based on power configuration:
- **Batteries only** (no solar): Every 6-8 weeks minimum
- **With solar panel**: Every 3-6 months for SD card and cleaning
- **Optimal setup**: Solar panel + battery backup

**Implication**:
- If treasure was placed October 9 and uses battery-only, camera would need service by late November/early December
- Solar panel setup suggests minimal maintenance visits (harder to detect)
- Location likely chosen for accessibility for battery changes OR has solar power

## Data Plan Requirements

### StealthCam COMMAND Pro App
- **Required**: Yes - cellular data plan required
- **Plan types**: Monthly or annual subscriptions
- **Typical cost**: $8-15/month depending on image volume
- **Plan tiers**:
  - Basic: 1,000 images/month
  - Standard: 2,500 images/month
  - Premium: Unlimited images

### Webcam Application Usage
- **10-minute intervals**: 4,320 images/month
- **Required plan**: Premium/Unlimited tier
- **Data cost**: Significant factor for treasure hunt budget
- **Implication**: Creator invested in premium cellular plan for 24/7 monitoring

## Test Methodology

The camera provides a **Sync button** feature:
- Press to take on-demand test photo
- Camera attempts immediate upload
- Photo appears in app if signal is adequate
- Useful for location scouting and coverage testing

**Implication**: Creator likely tested multiple locations before final placement, looking for spots with adequate dual-carrier coverage.

## Security Considerations

### Camera Detection Risk
- **No-Glo IR**: 940nm LEDs completely invisible to humans and animals
- **Night operation**: No visible flash even when taking photos
- **Physical stealth**: Weatherproof camo housing
- **Cellular advantage**: No need to physically retrieve SD card for images

### Location Advantages
Cellular connectivity provides:
- Remote monitoring without site visits
- Real-time alerts if treasure is disturbed
- No need to approach camera regularly (reduces detection risk)
- Can verify treasure presence without physical check

## Cellular Coverage Maps Research

### Recommended Actions
1. **Overlay coverage maps**: Combine AT&T + Verizon coverage maps for Blue Ridge region
2. **Identify dual-coverage zones**: Focus on areas with 3+ bars on either network
3. **Cross-reference with trails**: Eliminate trails in known dead zones
4. **Test locations**: Visit promising areas and check signal strength on both carriers

### Coverage Testing Tools
- **OpenSignal app**: Real-time coverage testing
- **CellMapper**: Crowdsourced tower locations and coverage
- **Carrier coverage maps**: AT&T and Verizon official maps
- **Field testing**: Physical verification with phones on both networks

## Elevation and Coverage Correlation

### Signal Strength by Elevation
- **Lower valleys**: Blocked by surrounding mountains - POOR coverage
- **Mid-elevation trails**: Often have line-of-sight to towers - GOOD coverage
- **Ridge lines and peaks**: Excellent line-of-sight - BEST coverage
- **North-facing slopes**: May be shielded from southern cell towers

### Optimal Placement Zones
Based on cellular requirements, treasure likely at:
- **Elevation**: 3,000-4,500 feet (good coverage, accessible)
- **Terrain**: Ridge or plateau with line-of-sight to populated valleys
- **Proximity**: Within 2-3 miles of cell towers in valley towns
- **Access**: Near maintained trails where coverage exists

## Conclusion: Coverage Constraint Impact

The dual-SIM cellular requirement **significantly narrows the search area**:

✅ **REQUIRES**:
- AT&T **OR** Verizon coverage (2-3 bars minimum)
- 4G LTE signal strength
- Line-of-sight or near-line-of-sight to cell towers
- Location within reasonable range of civilization

❌ **ELIMINATES**:
- Deep wilderness areas with no coverage
- Gorge floors and deep valleys
- Remote backcountry locations
- Areas near Tennessee border with known dead zones
- Locations requiring extensive off-trail hiking

🎯 **FOCUS AREAS**:
- Popular maintained trails with known cell coverage
- Areas within 1-3 miles of mountain towns (Boone, Blowing Rock, Banner Elk, Linville)
- Ridge-top trails with line-of-sight to valleys
- Blue Ridge Parkway overlooks and access points
- State park areas with visitor infrastructure

**Strategic Impact**: The cellular requirement is one of the most powerful constraints for narrowing the search area. Combined with the 2-hour drive time from Charlotte and trail accessibility, this creates a well-defined search zone in the northern Blue Ridge Mountains of North Carolina.
