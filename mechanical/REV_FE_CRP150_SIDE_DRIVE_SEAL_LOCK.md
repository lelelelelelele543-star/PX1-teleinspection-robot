# PX-1 Rev.FE — CRP150 source-locked side-drive sealing architecture

Status: prototype engineering baseline; exact supplier gland standards remain release gates.

## Why this revision exists
The uploaded MiniCam drawing `DRW-002-374` gives much stronger source evidence for the CRP150 side-drive arrangement than the earlier generic PX-1 assumptions.

The source assembly explicitly contains, per crawler side:
- 5 x Z50 gears total: 3 axle gears + 2 idlers;
- 6 x 61801-2RS bearings (12x21x5);
- 3 x 61903-2RS bearings (17x30x7);
- 3 x axle flanges;
- 3 x X-ring 18.72x2.62;
- 3 x O-ring 32x1.5;
- 1 x O-ring 190x1.5;
- 3 x 4x4x12 keys plus one short 4x4x7 key in the source assembly;
- 12 + 12 M3 Torx fasteners, consistent with one perimeter screw set and one 4-screw-per-flange set.

The uploaded `ASS-002-103` wheel-bolt assembly also shows a separate wheel disk retained by M6x14 with a 10x1.8 O-ring.

PX-1 will preserve this proven service architecture while using its own dimensions/materials.

## Corrections to PX-1
The old generic `Ø12 -> Ø17 + lip seal` wheel shaft description is superseded.

Current PX-1 wheel-station shaft concept from inside to outside:
1. Ø12 bearing journal for first 61801;
2. Ø12 keyed Z50 seat;
3. Ø12 bearing journal for second 61801;
4. Ø17 bearing journal for 61903;
5. dedicated polished dynamic-seal land about Ø19 class;
6. labyrinth/excluder shoulder;
7. Ø17 keyed wheel seat;
8. axial M6 wheel-disk retention.

The ~Ø19 seal land is a PX-1 inference/adaptation, not a dimension copied from MiniCam. It is introduced because the source X-ring nominal ID is 18.72 mm and the keyway must stay completely away from the dynamic sealing track.

## Dynamic wheel seal
Preferred prototype candidate now follows the source architecture:
- X-ring nominal 18.72 x 2.62;
- FKM preferred for PX-1 final wet/sewer service;
- rotating shaft land polished, Ra <=0.4 um target;
- no keyway, circlip groove, thread or shoulder edge under the seal contact band;
- seal gland placed in the removable axle flange so a damaged seal can be serviced without opening P0.

Initial PX-1 geometric candidate:
- seal land: Ø19.0 mm;
- X-ring ID stretch: about 1.50%;
- nominal dynamic radial squeeze target: ~12%;
- calculated candidate gland bottom diameter: ~23.61 mm.

These are prototype geometry values only. Final gland width, corner radii, squeeze and lubrication follow the exact X-ring supplier standard.

## Outer wheel bearing
Retain one 61903-2RS (17x30x7) in each removable axle flange.
This bearing carries wheel radial load close to the wheel and prevents the side cover itself from acting as a flexible wheel support.

## Inner wheel supports
Retain two 61801-2RS (12x21x5) per wheel station around the Z50 gear region.
The gear is therefore supported between/adjacent to two compact bearings as in the CRP150 architecture.

## Axle-flange static seal
Use the source-proven 32x1.5 O-ring class as the starting point.
- FKM preferred for PX-1;
- static face seal only;
- flange positively located by a pilot/register, not by screw clearance;
- 4 x M3 A4 Torx/button screws per flange, matching the source quantity logic;
- no wheel load is carried by the screws alone.

Exact groove is held until the flange register and actual molded O-ring are fixed.

## Side-cover static seal
Use 190x1.5 O-ring class as the preferred source-aligned candidate, not as a path-length value.
The nominal ring circumference is about 596.90 mm.

PX-1 preliminary groove study:
- O-ring section: 1.5 mm;
- face-groove depth: 1.20 mm -> 20% squeeze;
- groove width: 1.90 mm;
- calculated groove fill: ~77.5%;
- a 64 mm-high racetrack with equal centerline length requires about 261.92 mm overall centerline length.

These values show that the source-size ring can be packaged in a CRP150-class cover, but the exact groove must still be checked against the selected O-ring supplier standard and physical seal sample.

## Side-cover size correction
To create a rational screw line outside the 190x1.5 seal path, the PX-1 candidate cover is enlarged from 276x81 to approximately 286x86x5 mm.

This does not change wheel pitch or crawler body length.
Current ideal DN150 cross-section check with the same side-cover outer Y gives approximately:
- lower cover-corner clearance: ~5.6 mm;
- upper cover-corner clearance: ~10.8 mm.

Therefore all lower screws must be flush/countersunk or otherwise remain within the 5 mm cover envelope.
A real DN150 tube/deposit/ovality test remains mandatory.

## Fastener layout
Adopt CRP-like compact M3 hardware for the side-drive service layer:
- 12 x M3 A4 perimeter screws per side cover;
- 4 x M3 A4 screws per axle flange = 12 additional screws per side;
- Torx preferred for wet field service;
- threaded inserts in aluminum if repeated-cycle tests show wear;
- anti-galling paste compatible with FKM and aluminum.

## Pressure architecture
P1 and P2 stay separate dry positive-pressure zones.
Normal fill remains approximately +0.20...+0.30 bar gauge.
Positive pressure is an additional barrier only; it does not replace the X-ring/O-rings.

## Release gates
- actual 18.72x2.62 FKM X-ring supplier drawing;
- actual 32x1.5 and 190x1.5 FKM rings;
- groove coupon test;
- shaft surface finish measurement;
- 20 cover/flange service cycles;
- submerged rotating-shaft test;
- P1/P2 leak-decay logging;
- physical DN150 sweep with all screw heads, wheels and flange faces installed.