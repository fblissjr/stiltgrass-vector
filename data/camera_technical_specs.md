# StealthCam STC-DCPTRX Complete Technical Specifications

## Model Identification
- **Model Number**: STC-DCPTRX
- **Product Name**: Stealth Cam Deceptor MAX
- **Manufacturer**: StealthCam (GSM Outdoors)
- **Category**: Cellular Trail Camera
- **Release**: 2023-2024 model year
- **Firmware Version** (treasure camera): 11.024.125

---

## IMAGE & VIDEO SPECIFICATIONS

### Photo Resolution Options
- **Maximum**: 40 MP (interpolated from 16MP sensor)
- **Native Sensor**: 16 MP (actual sensor resolution)
- **Available Settings**:
  - 40 MP (interpolated)
  - 16 MP (native)
  - 8 MP
  - 5 MP ⭐ **(Used by treasure camera - see EXIF [MP:05])**
  - 4 MP
  - 2 MP
- **Image Format**: JPEG
- **Compression**: Adjustable quality settings

### Video Specifications
- **Resolution**: 1440P QHD (2560x1440)
- **Frame Rate**: 30 FPS
- **Format**: MP4 with H.264 codec
- **Audio**: Yes - video with sound recording
- **Length**: Configurable (5-60 seconds typical)

### Captured Image Details
- **Actual resolution in use**: 1280x720 (720p) for web transmission
- **EXIF indicates**: 5MP capture setting
- **Downscaling**: Images likely captured at 5MP then compressed to 720p for cellular upload
- **SD card storage**: Likely stores full 5MP originals locally

---

## DETECTION & TRIGGER PERFORMANCE

### Trigger System
- **Sensor Type**: Passive Infrared (PIR) with wide-angle coverage
- **Trigger Speed**:
  - Photos: 0.4 seconds (exceptionally fast)
  - Videos: 0.76 seconds
- **Detection Range**: 80-120 feet (adjustable sensitivity)
- **Detection Width**: Wide-angle PIR sensor (approximately 50-60 degree arc)
- **Recovery Time**: Near-instant for burst mode

### Multi-Shot Capabilities
- **Burst Mode**: 1-9 photos per trigger event
- **Time-Lapse**: Programmable intervals (1 minute to 24 hours)
- **Rapid-Fire**: Fast recovery between shots in burst mode

---

## FLASH & NIGHT ILLUMINATION

### LED Array
- **Type**: No-Glo (940nm infrared)
- **LED Count**: 36-piece array
- **Visibility**: Completely invisible to human and animal eyes
- **Range**: 80 feet effective IR illumination
- **Power**: Automatic intensity adjustment

### Night Performance
- **Image Quality**: Good monochrome IR images at night
- **Flash Fired**: Confirmed in EXIF data (treasure photo taken at 23:37:26)
- **Detection**: No red glow, no visible light emission
- **Stealth**: Ideal for security applications and wildlife monitoring

---

## CELLULAR CONNECTIVITY (CRITICAL FOR TREASURE HUNT)

### Network Technology
- **Type**: Dual SIM 4G LTE cellular
- **Carriers**: AT&T + Verizon (both pre-installed)
- **SIM Management**: Automatic network selection
- **Switching**: Real-time monitoring and automatic carrier switching
- **Technology**: 4G LTE only (3G no longer supported)

### Automatic Network Coverage Feature
- **Monitors**: Both AT&T and Verizon signal strength continuously
- **Selects**: Strongest available network automatically
- **Failover**: Seamless switching if primary network fails
- **Redundancy**: Maximizes uptime in remote locations

### Data Transmission
- **App**: StealthCam COMMAND Pro (iOS and Android)
- **Features**:
  - Live image streaming
  - On-demand remote capture (Sync button)
  - Settings management
  - Multi-camera management
  - GPS location mapping
  - Firmware over-the-air updates

### Upload Performance
- **Speed**: Depends on cellular signal strength
- **Typical**: 10-30 seconds for image upload
- **Frequency**: Configurable (treasure camera: 10-minute intervals)
- **Reliability**: High with dual-carrier redundancy

### Data Plan
- **Required**: Yes - separate cellular subscription
- **Provider**: StealthCam COMMAND service
- **Tiers**:
  - Basic: 1,000 images/month (~$8-10/month)
  - Standard: 2,500 images/month (~$12/month)
  - Premium: Unlimited images (~$15-20/month)
- **Treasure camera usage**: Premium tier (4,320+ images/month for 10-min updates)

---

## POWER SYSTEM

### Battery Configuration
- **Type**: 16 AA batteries (not included)
- **Arrangement**: 4 columns of 4 batteries each
- **Voltage**: Approximately 24V nominal (16x 1.5V)
- **Chemistry**: Works with alkaline, lithium, or rechargeable NiMH

### Battery Life Estimates
**Standard usage (30 photos/day, mixed day/night)**:
- Photo mode: ~8.4 months
- Video mode: ~3.8 months

**High-frequency usage (treasure webcam scenario)**:
- 144 photos/day (10-minute intervals)
- Estimated life: 1.75-2.5 months (6-10 weeks)
- Recommendation: Solar panel or frequent battery changes

### External Power Options
- **DC Input**: 12V DC jack
- **Solar Panel**: Compatible with StealthCam solar panels
- **External Battery**: 12V rechargeable battery packs supported
- **Power Management**: Intelligent power switching between sources

### Treasure Camera Power Analysis
Given 10-minute update frequency since October 9, 2025:
- **Battery-only scenario**: Would need service by mid-late December
- **Solar panel scenario**: Can run indefinitely with minimal maintenance
- **Likely configuration**: Solar panel + battery backup for reliability
- **Accessibility implication**: Location must be accessible for maintenance OR has solar power

---

## PHYSICAL SPECIFICATIONS

### Housing & Construction
- **Material**: High-impact plastic, weatherproof
- **Weather Rating**: IP66 or equivalent (rain, snow, dust proof)
- **Operating Temperature**: -20°F to 120°F (-29°C to 49°C)
- **Storage Temperature**: -40°F to 140°F
- **Humidity**: Up to 90% non-condensing

### Security Features
- **Lock Latch**: Integrated security latch
- **Cable Lock**: Python cable lock compatible
- **Strap Mount**: Standard tree mounting strap included
- **Security Box**: Compatible with third-party security boxes

### Dimensions & Weight
- **Size**: Compact trail camera form factor (~5"H x 3.5"W x 2.5"D typical)
- **Weight**: Approximately 1.5 lbs without batteries
- **With batteries**: Approximately 2.5 lbs total

### Storage
- **Card Type**: SD/SDHC card
- **Maximum Capacity**: 32GB recommended (supports larger with formatting)
- **Format**: FAT32 file system
- **Storage Management**: Circular recording when full (overwrites oldest)

---

## OPERATING MODES & SETTINGS

### Capture Modes
- **Photo**: Single or burst photos on motion detection
- **Video**: Video recording on trigger
- **Time-Lapse**: Scheduled photos at set intervals
- **Hybrid**: Photo + video on same trigger

### Configuration Options
- **Sensitivity**: Adjustable PIR sensor sensitivity (Low/Medium/High)
- **Detection Range**: Adjustable via sensitivity settings
- **Delay**: Programmable delay between triggers (prevent false triggers)
- **Time Restrictions**: Operate only during certain hours
- **Date/Time Stamp**: Customizable on-image information

### EXIF Metadata Embedded
Based on treasure camera analysis:
- **Image Description**: `Trail Camera[MP:05][TP:055F]`
  - [MP:XX] = MegaPixel setting (05 = 5MP mode)
  - [TP:XXXF] = Temperature in Fahrenheit (055F = 55°F)
- **GPS Coordinates**: Can be embedded if enabled
- **Date/Time**: Standard EXIF timestamp
- **Camera Settings**: Various EXIF fields for exposure, ISO, aperture

---

## ADVANCED FEATURES

### AI & Image Processing
- **Animal Recognition**: AI-powered animal detection and classification
- **AI Night Colorization**: Enhanced night image processing
- **False Trigger Reduction**: Smart detection algorithms
- **Image Enhancement**: Automatic brightness and contrast adjustment

### GPS & Mapping
- **GPS Module**: Built-in GPS receiver
- **Location Tagging**: Automatic GPS coordinates in EXIF
- **Mapping in App**: Camera locations displayed on map
- **Multi-Camera Management**: Track multiple camera locations

### Firmware Updates
- **Method**: Over-the-air (OTA) via cellular connection
- **Automatic**: Can be set to auto-update
- **Current Version** (treasure camera): 11.024.125
- **Release Notes**: Typically include bug fixes and feature improvements

### Remote Control
- **On-Demand Photos**: Take photo remotely via app (Sync button)
- **Settings Changes**: Adjust camera settings remotely
- **Live Status**: Battery level, signal strength, SD card capacity
- **Alerts**: Notifications for low battery, SD card full, etc.

---

## PERFORMANCE RATINGS

### Independent Testing Scores
Based on TrailCamPro.com testing:
- **Overall Score**: 90/100 (Excellent)
- **Picture Quality**: 90/100
  - Day: Excellent color and sharpness
  - Night: Good IR illumination and detail
- **Detection Performance**: Excellent
  - Fast 0.4s trigger speed
  - Wide detection zone
  - Minimal false triggers
- **Battery Life**: Excellent
  - 8+ months for standard photo use
  - Above-average power efficiency
- **Cellular Reliability**: Excellent
  - Dual-SIM provides superior connectivity
  - Auto-switching works seamlessly

### User Reviews Summary
- **Pros**: Fast trigger, dual cellular, no-glo flash, reliable app
- **Cons**: Price, requires cellular plan, 16-battery requirement
- **Common Uses**: Wildlife monitoring, property security, research

---

## TYPICAL USE CASES

### Primary Applications
1. **Wildlife Monitoring**: Game scouting for hunters
2. **Property Security**: Remote surveillance of cabins, equipment
3. **Research**: Wildlife studies and conservation
4. **Remote Monitoring**: Construction sites, farms, vacation properties
5. **Treasure Hunt Webcam**: 24/7 live feed of hidden treasure (novel use!)

### Ideal Conditions
- Locations with AT&T or Verizon 4G LTE coverage
- Outdoor environments within operating temperature range
- Areas needing remote monitoring without physical access
- Long-term deployment with solar panel or regular maintenance

---

## PURCHASE & AVAILABILITY

### Retail Information
- **MSRP**: $249-299 (camera only)
- **Cellular Plan**: $8-20/month additional
- **Retailers**:
  - Tractor Supply Co.
  - Rural King
  - Amazon
  - Bass Pro Shops
  - Cabela's
  - Sporting goods stores
- **Charlotte, NC availability**: Widely available locally

### Package Options
- **Single camera**: Standard package with mounting strap
- **2-pack bundle**: Discounted dual-camera package (STC-DCPTRX-2PK)
- **Solar bundle**: Camera + solar panel + mounting hardware
- **Complete kit**: Camera + solar panel + SD card + batteries

---

## TREASURE HUNT SPECIFIC ANALYSIS

### Why This Camera for Treasure Hunt?

**Advantages**:
1. **Dual cellular coverage**: Maximizes reliability in mountains
2. **No-Glo flash**: Undetectable at night (stealth operation)
3. **Long battery life**: Minimal maintenance visits
4. **Remote access**: Monitor without visiting site
5. **Solar compatible**: Can run indefinitely with solar panel
6. **Fast trigger**: Captures anyone approaching treasure
7. **Wide detection**: 80-120 ft range covers large area
8. **4G LTE**: Fast image upload for 10-minute intervals
9. **Weatherproof**: Survives mountain weather conditions
10. **GPS tagging**: Creator knows exact coordinates

**Setup Implications**:
- Creator likely tested multiple locations for cellular coverage
- Camera probably has solar panel for long-term operation
- 10-minute updates require premium cellular plan ($15-20/month)
- Location must have 2-3 bars on AT&T or Verizon
- SD card stores full-resolution backup images

### Location Constraints from Camera Choice

**REQUIRES**:
✅ AT&T or Verizon 4G LTE coverage (2-3 bars minimum)
✅ Accessible for camera placement (within reach height)
✅ Mounting point (tree, post, rock face)
✅ Reasonably accessible for battery changes (unless solar)
✅ Location within 80-120 feet of treasure for detection

**ELIMINATES**:
❌ Deep wilderness with no cellular coverage
❌ Areas below cell tower line-of-sight (deep valleys)
❌ Extreme remote backcountry locations
❌ Locations requiring significant off-trail hiking to maintain
❌ Areas with dense overhead canopy (solar panel efficiency)

**OPTIMAL CONDITIONS**:
🎯 Ridge or elevated terrain with good cell signal
🎯 Near maintained trail (within 200-500 feet)
🎯 Clear view to sky for solar panel (if used)
🎯 Tree or structure for mounting 4-6 feet high
🎯 Location within 2-hour drive from Charlotte for setup/maintenance

---

## TECHNICAL SPECIFICATIONS SUMMARY TABLE

| Category | Specification |
|----------|---------------|
| **Model** | STC-DCPTRX (Deceptor MAX) |
| **Sensor** | 16MP native, 40MP interpolated |
| **Video** | 1440P QHD @ 30fps |
| **Trigger Speed** | 0.4 seconds (photos) |
| **Detection Range** | 80-120 feet |
| **IR Flash** | 36-piece 940nm No-Glo, 80 ft range |
| **Cellular** | Dual SIM 4G LTE (AT&T + Verizon) |
| **Battery** | 16 AA batteries |
| **Battery Life** | 8.4 months (standard), ~2 months (webcam use) |
| **Solar** | Compatible, recommended for webcam |
| **SD Card** | Up to 32GB, FAT32 |
| **Operating Temp** | -20°F to 120°F |
| **Weather Rating** | IP66 weatherproof |
| **Price** | $249-299 + cellular plan |
| **Firmware** (treasure) | 11.024.125 |
| **EXIF Codes** | [MP:05] = 5MP mode, [TP:055F] = 55°F |

---

## CONCLUSION

The StealthCam STC-DCPTRX is a high-quality cellular trail camera ideally suited for remote monitoring applications. Its dual-SIM automatic network coverage makes it particularly effective in mountainous terrain where single-carrier cameras might struggle.

For the Countdown Treasure application, this camera choice provides:
- Reliable 24/7 monitoring with minimal maintenance
- Undetectable nighttime operation
- Real-time upload capability for 10-minute webcam updates
- Weather resistance for outdoor deployment

The cellular requirement creates a significant constraint on possible treasure locations, effectively eliminating vast areas of wilderness and focusing the search on accessible locations with adequate AT&T or Verizon coverage.

**Key Takeaway**: The treasure MUST be located within reliable cellular coverage range, which narrows the search area considerably when combined with other clues (2-hour drive, trail accessibility, elevation indicators).
