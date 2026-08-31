# CRP-150 gear and shaft audit

Revision 0.2, 2026-08-31.

## Purpose

This audit checks the current PX1/X200 reconstruction against DRW-002-374, DRW-002-375 and DRW-002-386. The assembly sheets do not print every gear dimension, so scale-derived values are kept as `RECONSTRUCTED` until an individual part drawing or physical measurement confirms them.

## Calibrated drawing method

The source sheets are vector A3 PDFs. Geometry was measured from 300/400 dpi renders and converted using the PDF page size and the printed view scale.

DRW-002-374 uses a 1:1.5 drive view. The measured front-to-middle and middle-to-rear axle spacing is approximately 1,050 pixels at 400 dpi:

```text
actual spacing = 1050 px / (400 px/in / 25.4 mm/in) x 1.5
               = 100.0 mm
```

There is one equal idler between adjacent wheel gears, therefore the adjacent Z50 gear-center distance is 50.0 mm.

For two equal external gears:

```text
a = m x (z1 + z2) / 2
50 = m x (50 + 50) / 2
m = 1.0 mm
```

This result also matches the rendered gear outside diameter of approximately 52 mm for a standard Z50 spur gear.

## Confirmed and reconstructed gear data

| Gear | Quantity per crawler | Function | Teeth | Module | Pitch diameter | Face width | Evidence state |
|---|---:|---|---:|---:|---:|---:|---|
| GEA-002-528 | 4 | Side-drive idler | 50 | 1.0 mm | 50 mm | 4 mm (`B4`) | RECONSTRUCTED from calibrated drawing and designation |
| GEA-002-529 | 6 | Wheel/axle gear | 50 | 1.0 mm | 50 mm | 4 mm (`B4`) | RECONSTRUCTED from calibrated drawing and designation |
| GEA-002-531 | 2 | Motor bevel pinion | 16 | 1.0 mm | 16 mm | Not yet frozen | RECONSTRUCTED from calibrated drawing |
| GEA-002-530 | 2 | Transverse bevel gear | 40 | 1.0 mm | 40 mm | Not yet frozen | RECONSTRUCTED from calibrated drawing |

Quantities above are for the complete two-sided crawler. One side contains three Z50 axle gears and two Z50 idlers.

## Bevel-pair geometry

The Z16/Z40 pair is a 90-degree straight-bevel reduction.

```text
i = 40 / 16 = 2.5
delta_pinion = atan(16/40) = 21.801 degrees
delta_gear   = 90 - delta_pinion = 68.199 degrees
cone distance R = 0.5 x m x sqrt(16^2 + 40^2) = 21.541 mm
```

Approximate standard outside diameters at the large end:

```text
de_pinion = m x (16 + 2 cos(delta_pinion)) = 17.86 mm
de_gear   = m x (40 + 2 cos(delta_gear))   = 40.74 mm
```

The approximately 40.6 mm outside span measured on DRW-002-375 agrees with the module-1 calculation within raster and line-width uncertainty. A module-1.25 gear would be substantially too large for the shown housing and 18x30x7 sealing stack.

Face width, pressure angle, tooth system, backlash and mounting-distance tolerances remain unresolved. Do not order or machine the bevel pair only from tooth count and module.

## Side-drive layout

Per side, from front to rear:

1. wheel gear Z50;
2. idler Z50;
3. wheel gear Z50;
4. idler Z50;
5. rear wheel/input gear Z50.

Adjacent centers are 50 mm. Wheel centers are 100 mm apart. Front-to-rear wheelbase is 200 mm. Four external spur meshes make all three wheels on one side rotate in the same direction.

DRW-002-374 places FSS-002-064, the long input axle, at the rear wheel station. It is not a center-wheel input and there is no separate fourth input shaft.

## Shaft, bearing and key load paths

### Motor bevel input

DRW-002-386 shows the Z16/FSS-002-083 assembly supported in the motor holder by one 61801-2RS bearing per motor. FSS-002-083 is concentric with the FAULHABER gearhead output and acts as the transition/coupling element inside the supported Z16 assembly. The exact bore, flat/key, interference and axial retention remain unresolved.

The important functional rule is confirmed: bevel-mesh radial load is reacted through the 61801 bearing into FAL-002-082, rather than relying only on the small gearhead output bearing.

### Rear long axle

The rear input station uses:

- one 61903-2RS bearing on the wheel/outer shaft path;
- the one-per-side 61801-2RS bearing on the inboard long-axle path;
- one 4x4x12 key for the Z50 axle gear;
- one additional 4x4x7 key on the long input path;
- one X-ring 18.72x2.62 in the axle flange;
- one static O-ring 32x1.5 under the axle flange.

The front and middle wheel stations use short axles and do not receive the extra long-axle 61801 support.

### Transverse Z40 path

DRW-002-375 shows each Z40 on FSS-002-066. The inner end is supported by a 61800-2RS bearing (10x19x5); the outer path passes through an 18x30x7 dynamic shaft seal and connects to the side-drive long axle. The side-drive bearing completes the support system when the side cover is installed.

## Current CAD conflicts

The published RevGK/RevGN checkpoints are not valid architecture masters. Their STEP product names and geometry record the following conflicts:

| Current CAD item | Current value | Source-correct direction |
|---|---|---|
| Spur gears | Z50, module 1.25 | Z50, module 1.0, B4 |
| Bevel gears | Z16/Z40, module 1.25 | Z16/Z40, module 1.0 |
| Driven wheel station | Center axle | Rear long axle FSS-002-064 |
| Side-cover O-ring | 170x1.5 reference | SEA-002-102, 190x1.5 |

The files are retained only as historical reconstruction checkpoints. A corrected CAD revision must rebuild the drive skeleton before any manufacturing drawing is produced.

