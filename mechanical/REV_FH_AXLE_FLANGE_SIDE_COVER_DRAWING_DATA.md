# PX-1 Rev.FH — axle flange and side-cover manufacturing drawing data

Status: prototype drawing candidate.

## Source basis
The uploaded `DRW-002-374` shows the CRP150 side-drive service layer as:
- one side cover;
- three removable axle flanges;
- 3 x 61903-2RS bearings;
- 3 x X-ring 18.72x2.62;
- 3 x O-ring 32x1.5;
- 1 x O-ring 190x1.5;
- two M3 screw groups of quantity 12 each.

PX-1 now deliberately follows this service architecture rather than using a generic lip-seal plate.

# A. PX1-432 AXLE FLANGE

Quantity: 6.

Material:
- EN AW-6082 T6, hard anodized only if the selected seal chemistry and dimensional tolerances remain acceptable after coating;
- alternatively 1.4404 stainless for a heavier but very corrosion-resistant prototype.

## External geometry candidate
- external flange disk OD: Ø50 mm;
- visible/external disk thickness: 3.0 mm;
- inboard locating/bearing spigot: Ø34 g6 candidate;
- inboard spigot length: 9.0 mm;
- total axial part envelope: 12 mm;
- external projection beyond side-cover plane: only ~3 mm to preserve DN150 clearance.

## Cover register
Side-cover pilot bore:
- Ø34 H7 candidate.

The pilot locates the wheel axis. M3 screws provide clamp load only.

## Outer bearing pocket
For 61903-2RS (17x30x7):
- bore Ø30 H7 candidate;
- depth 7.0 +0.05/0 mm candidate;
- square bearing shoulder;
- bearing shoulder runout to pilot axis <=0.02 mm target;
- entry chamfer 0.3x30 deg maximum.

The exact bearing outer-ring fit is confirmed against purchased bearing tolerances and thermal/service requirements.

## Dynamic X-ring gland
Source ring: 18.72x2.62.

PX-1 candidate:
- shaft seal land Ø19 h8;
- stationary gland in axle flange;
- nominal radial squeeze target ~12%;
- preliminary gland bottom diameter ~23.61 mm;
- axial gland width candidate ~3.4 mm.

Important: this is a packaging calculation, not a final seal drawing. The exact gland is redrawn to the selected FKM X-ring supplier handbook before machining.

## Static axle-flange O-ring
Source ring: 32x1.5.

Preferred PX-1 concept:
- O-ring retained on the flange/register interface, not loose on the wheel shaft;
- current CAD reserves a radial-groove region on the Ø34 pilot near the cover face;
- prototype modeled reservation ~1.9 mm axial x ~0.9 mm radial.

Exact gland is HOLD until a real 32x1.5 FKM ring is selected. Radial stretch/squeeze must be checked from that supplier's tolerances.

## Flange fasteners
- 4 x M3 A4 Torx/button screws per flange;
- PCD 40 mm candidate;
- clearance Ø3.4 mm in flange;
- threaded holes or inserts in parent side structure;
- screw heads must not become the primary wheel-load location feature.

## Surface requirements
- static seal faces Ra <=1.6 um;
- dynamic gland surfaces Ra <=0.8 um preferred;
- no radial scratches through O-ring sealing faces;
- all wet external edges deburred 0.2...0.5 mm.

# B. PX1-433 SIDE COVER

Quantity: 2.

Material:
- EN AW-6082 T6.

Current candidate envelope:
- 286 x 86 x 5 mm;
- visible shape remains a low rectangular CRP150-like plate;
- exact edge chamfers/rounded corners follow the finished body contour.

This supersedes the earlier 276x81 envelope because the larger plate gives a realistic screw/seal margin while still fitting the current DN150 cross-section.

## Wheel-station centers
Relative to cover local lower-left datum:
- X = 50 / 150 / 250 mm;
- Z/local vertical center = 45 mm;
- three Ø34 H7-class flange-register openings.

Wheel pitch remains exactly 100 mm nominal.

## Main side-cover O-ring
Source candidate: 190x1.5.

Nominal circumference:
- pi x 190 = 596.90 mm.

Current equal-length racetrack study:
- groove centerline overall length: ~261.92 mm;
- groove centerline overall height: 64.0 mm;
- centered on 286x86 plate;
- centerline edge margins: ~12.04 mm longitudinal and 11.0 mm vertical.

Prototype groove candidate:
- width 1.90 mm;
- depth 1.20 mm;
- nominal squeeze 20%;
- calculated groove fill ~77.5%.

These groove dimensions are NOT production-frozen until the actual FKM 190x1.5 ring supplier is selected.

## Side-cover fasteners
12 x M3 A4 screws per cover.
Current local coordinate candidate, measured from cover lower-left corner:
- lower line: (8,5), (62,5), (116,5), (170,5), (224,5), (278,5);
- upper line: (8,81), (62,81), (116,81), (170,81), (224,81), (278,81).

These coordinates keep the screw line outside the current racetrack seal study.

Use:
- Torx countersunk or truly low-profile flush hardware along DN150-critical lower edge;
- button heads only where the complete DN150 solid check proves enough clearance;
- thread inserts after service-cycle testing if bare aluminum threads show damage.

## Datum/tolerance proposal
- Datum A: body-mating sealing face;
- Datum B: center axis of middle wheel-station pilot;
- Datum C: longitudinal center plane through all three pilots.

Requirements:
- three pilot centers positional tolerance <=0.03 mm relative to B/C target for prototype;
- sealing-face flatness <=0.08 mm;
- cover thickness 5.00 +/-0.05 mm candidate;
- three pilot axes mutually parallel and perpendicular to sealing face within 0.03 mm/100 mm target;
- surface finish on main seal land Ra <=1.6 um.

## DN150 consequence
With current crawler transverse geometry, enlarging the cover to 86 mm height does not worsen the lower corner, which remains the critical point.
Ideal-pipe nominal clearances remain approximately:
- lower corner: 5.6 mm;
- upper corner: 10.8 mm.

This is not enough to tolerate protruding lower screw heads, so the lower fastener line must stay flush.

## First article inspection
For each side cover/flange set:
- CMM or jig-check all 3 wheel center locations;
- verify cover flatness;
- blue-check flange seating face;
- pressure-test bare P1/P2 cavity before gears are installed;
- fit actual X-rings/O-rings and repeat pressure test;
- rotate dummy Ø19 seal mandrels and log friction/leakage;
- then assemble real shafts/gears and repeat submerged rotation test.