# PX-1 Rev.GT — drivetrain bearing / dynamic-seal prototype baseline

Status: PROTOTYPE COMPONENT BASELINE; exact purchased samples/fits remain measurement gates.

## Why Rev.GT is required
Rev.GL closed the complete six-wheel geometry, but two seal assumptions were still weak:
- X200 still used a directional 18x30x7 radial lip seal even though P0/P1-P2 pressure differential can reverse;
- wheel shafts used the source-inspired 18.72x2.62 X-ring on an Ø19 land without an exact modern rotary gland table for that shaft diameter.

Rev.GT standardizes the drivetrain dynamic sealing around one current catalog geometry and removes those two uncertainties without changing the crawler external envelope.

## Common drivetrain dynamic seal — prototype baseline
Preferred part family:
- Trelleborg Quad-Ring® / X-Ring;
- part size: **QRAR04116 = 18.72 x 2.62 mm**;
- preferred material baseline: **V7002, FKM 70 Shore A**;
- prototype article nomenclature: **QRAR04116-V7002** where available.

Current Trelleborg rotary/internal installation table for an Ø18 rotating rod/shaft gives:
- shaft d5: **18.0 f7**;
- Quad-Ring: QRAR04116, 18.72x2.62;
- fixed-part groove root diameter d6: **22.8 H8**;
- groove width b1 without backup ring: **2.8 +0.2 mm**;
- groove corner radius r1: **0.30 mm**;
- maximum radial clearance S: **0.08 mm** in the listed table.

The natural ring ID is 4.0% larger than the Ø18 shaft, consistent with the rotary/internal installation geometry rather than stretching an undersize ring onto the shaft.

Trelleborg describes Quad-Ring as a double-acting four-lip seal usable in rotary applications. This is better aligned with the PX-1 possibility of pressure differential acting in either direction than a single directional lip seal.

FKM V7002 is the initial chemical-resistance baseline, not an unconditional production freeze. NBR N7004 remains a legitimate comparison sample for low-temperature/water/friction testing. Final compound is selected after wet drag, chemical exposure and endurance tests.

## Standardization decision
Use the same nominal dynamic-seal geometry at **eight drivetrain locations**:
- 6 wheel shafts;
- 2 X200 side-input shafts.

Benefits:
- one field spare seal size instead of separate wheel/X200 dynamic seals;
- one shaft finishing process for the dynamic land;
- one groove inspection gauge concept;
- double-acting pressure capability at both wheel and X200 interfaces;
- lower risk of service parts being mixed up.

## X200 correction
The Rev.GL 18x30x7 lip seal is superseded in the active PX-1 design by the fixed-groove Quad-Ring concept.

The original CRP150 drawing remains a valid architecture reference and does show an 18x30x7 shaft seal with the Z40/61800 housing, but PX-1 is not required to retain that exact seal when a current double-acting rotary gland packages more cleanly.

Rev.GT local CAD result:
- old X200 seal axial zone retained: Y34.5...41.5, length 7.0 mm;
- new 2.8 mm groove: Y36.6...39.4;
- solid axial shoulder each side: ~2.1 mm;
- groove-to-X200-Z50 axial gap: ~2.6 mm;
- fixed seal housing remains within the previous Ø30 seal-pocket envelope;
- zero local housing/Z50 collision;
- external side-cover surface remains unchanged/smooth.

## Wheel-station correction
Change only the internal dynamic seal land from **Ø19 to Ø18**.

Active left-side axial stack becomes:
- 61903 ends at Y58.35;
- Ø18 dynamic seal land: Y58.35...62.15, length 3.80 mm;
- Quad-Ring groove: Y58.85...61.65;
- axial shoulder to adjacent features: 0.50 mm each side;
- keyed Ø17 wheel seat begins at Y62.15 exactly.

The Ø17 -> Ø18 shoulder still provides a clear wheel-side shaft transition; the Ø18 land is well outside the wheel keyway.

Packaging screen:
- groove-root Ø22.8 to nominal static flange O-ring ID Ø32 leaves **4.6 mm radial ligament**;
- no external wheel/flange/cover envelope changes;
- no change to DN150 tire geometry;
- no keyway or thread enters the dynamic seal track.

## Rotary speed severity
With the current 54 rpm reference traction motor and 2.5:1 bevel stage:
- wheel/X200 side shaft speed ≈21.6 rpm;
- Ø18 dynamic surface speed ≈0.020 m/s.

This is an extremely low-speed rotary application. Seal friction, contamination and shaft finish are more relevant to service life than centrifugal/speed limits.

## Prototype bearing candidates
The dimensions below remain those required by the active Rev.GF/GL geometry.

### Inner wheel support
Preferred first sample:
- **JTEKT/Koyo 6701 2RS**;
- 12x18x4 mm;
- Cr 1.15 kN;
- C0r 0.530 kN.

Reason: this thin bearing is what makes the Z50 + support package fit inside the 8 mm dry side bay without cutting the side-cover seal plane.

### Wheel axle-flange intermediate support
Preferred corrosion-resistant sample where practical:
- **SKF W 61801-2RS1** stainless;
- 12x21x5 mm;
- C about 1.51 kN;
- C0 about 0.90 kN.

Standard steel 61801-2RS1 remains an acceptable prototype fallback inside the dry/pressurized housing if the stainless article is unavailable.

### Wheel main outboard support
Preferred corrosion-resistant sample:
- **SKF W 61903-2RS1** stainless;
- 17x30x7 mm;
- C about 3.97 kN;
- C0 about 2.55 kN.

This bearing carries the highest external wheel bending contribution and has a very large static margin relative to the current prototype load screens.

### X200 supports
Preferred corrosion-resistant sample where practical:
- **SKF W 61800-2RS1** stainless;
- 10x19x5 mm;
- C about 1.48 kN;
- C0 about 0.83 kN.

Two are used per X200 side shaft in Rev.GL. Standard steel 61800-2RS1 remains a dry-P0 fallback.

## Bearing-fit rule — do not blanket-freeze h6/H7
No single shaft fit is frozen across all four bearing positions.

Reason:
- inner rings rotate relative to the applied radial load and may require transition/interference fits;
- JTEKT and SKF published fit-selection tables differ slightly in the light-load boundary recommendations;
- thin-section bearings are sensitive to ring expansion and lost internal clearance;
- exact selected brand/internal-clearance class and actual measured loads must drive the final journal fit.

Therefore the Rev.GR WS-01 inspection rule remains active:
1. purchase one exact sample of each bearing;
2. measure actual dimensions and identify internal-clearance designation;
3. use that manufacturer's fit table for the actual load case;
4. machine one first-article shaft/flange;
5. measure installed running torque/endplay/temperature;
6. only then freeze the drawing tolerance and duplicate five more wheel stations.

## Shaft / groove finish gates
Before release:
- Ø18 dynamic seal surface must be polished and free of keyways, flats, grooves or threads under the lips;
- target surface finish starts at Ra <=0.4 µm class, then is checked against the final Trelleborg rotary recommendation and physical drag/leak test;
- shaft lead-in must not cut the seal during assembly;
- groove root Ø22.8 H8 and b1 2.8+0.2 are inspection-controlled dimensions;
- groove edges must be burr-free; r1 target 0.30 mm;
- actual radial extrusion gap is measured, not inferred only from nominal CAD.

## Test gates for the common seal
Before all eight locations are released:
- compare V7002 FKM and N7004 NBR samples if both are available;
- measure dry and lubricated breakaway torque;
- 2 h rotating wet test;
- pressure decay with shaft stopped and rotating;
- pressure differential in both directions;
- mud/silt contamination test with external exclusion/labyrinth geometry;
- 500 direction reversals;
- inspect the Ø18 shaft track and Quad-Ring lips;
- repeat after at least 20 service removal/refit cycles on WS-01.

## Static seals not yet frozen by Rev.GT
Rev.GT does not automatically change:
- axle-flange static O-ring: nominal 32x1.5 architecture from source/current CAD;
- main side-cover perimeter seal: nominal 190x1.5 / later PX-1 groove studies.

Those two static seals are the next sealing block. Their cross-section/material/gland must be frozen by their own CAD and compression/fill checks; do not infer static gland dimensions from this rotary Quad-Ring selection.

## Decision
- active dynamic drivetrain shaft diameter at seal lands: **Ø18 mm**;
- common prototype dynamic seal: **QRAR04116 18.72x2.62**, V7002 FKM 70 preferred for first chemical-resistant sample;
- X200 18x30x7 lip seal is no longer the active PX-1 baseline;
- all eight dynamic locations use the same Quad-Ring geometry unless testing disproves it;
- external crawler dimensions and Rev.GL DN150 geometry are unchanged;
- final bearing fits, exact seal compound and production release remain HOLD until physical first-article tests.
