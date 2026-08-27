# PX-1 Rev.DG — manual lift + DN150 result

Status: verified geometric candidate; detailed joints still HOLD.

## Coordinate correction
For the six-wheel CRP150-style crawler, the DN150 pipe axis is taken approximately through the wheel-axis height rather than treating the crawler as a flat-floor vehicle.

Prototype coordinate basis:
- wheel axis Z = 45 mm;
- nominal DN150 pipe axis Z = 45 mm;
- pipe internal radius = 75 mm.

This is a major correction to earlier flat-floor clearance assumptions.

## Lift candidate
Parallelogram packaging values:
- base midpoint X = 235 mm;
- base pivot height Z = 65 mm;
- arm length = 135 mm;
- camera X offset from top-link midpoint = -36 mm;
- two equal side arms keep the camera carrier parallel.

Positions:
- LOW: arm angle 182°, camera axis ≈ X64.1 / Z60.3 mm;
- DN150_SAFE: 178°, camera axis ≈ X64.1 / Z69.7 mm;
- HIGH: 90°, camera axis ≈ X199 / Z200 mm; HIGH is mechanically blocked in DN150.

The near-identical X in LOW and SAFE is intentional: small height adjustment occurs near the forward folded position without sweeping the head rearward into the body.

## DN150 digital-head sweep
Checked camera envelope:
- Ø52 mm;
- length 72 mm;
- TILT -105…+105°;
- sampled every 2°;
- full cylindrical solid sampled axially and circumferentially;
- required nominal camera-to-pipe clearance >=3 mm.

Calculated results:
- LOW: minimum clearance ≈15.3 mm;
- DN150_SAFE: minimum clearance ≈5.9 mm;
- maximum camera-axis height retaining >=3 mm through full TILT sweep ≈72.6 mm.

Therefore the DN150 mechanical stop shall prevent the camera axis rising above **72 mm nominal** until a physical pipe test validates tolerances, wheel compression and real camera protrusions.

## Important limitation
This result validates the camera-head envelope against the ideal DN150 cylinder. It does NOT yet validate:
- actual tire shoulder geometry/contact point;
- side-cover screw heads;
- lift-arm thickness and pivot fasteners;
- quick-release protrusions;
- lens hood/LED-ring protrusions;
- cable loops.

Those are included in the next complete swept-solid assembly gate.

## Mechanical lift architecture
Retain the uploaded Proteus reference ideas:
- 150 N-class gas spring;
- M8 adjustable clamping lever;
- Belleville/disc spring preload stack;
- Ø8-class replaceable pivot pins/bushings;
- mechanical DN150 stop independent of firmware.

## Release status
PASS for geometry concept only. NO manufacturing release until the full physical lift solids and tire geometry are included.
