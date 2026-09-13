# Source register

Revision 0.3, 2026-09-14.

This register identifies evidence without publishing restricted source documents.

| Source ID | Subject | Evidence extracted | State |
|---|---|---|---|
| DRW-002-374 | CRP-150 side drive | Three wheel stations, two idlers, five Z50 B4 gears per side, rear long axle FSS-002-064, 100 mm wheel spacing and module-1 gear geometry by calibrated scale | CONFIRMED-DRAWING + RECONSTRUCTED |
| DRW-002-375 / ASS-002-375 | Crawler housing | Two Z40 bevel gears, two 18x30x7 shaft seals, two 61800-2RS 10x19x5 bearings, lift holding plates/axles and sealing parts | CONFIRMED-DRAWING |
| DRW-002-386 / ASS-002-386 | Crawler motor unit | Two Z16 bevel gears, concentric FSS-002-083 coupling elements, two motor-and-gear units and two 61801-2RS 12x21x5 support bearings | CONFIRMED-DRAWING |
| DRW-002-744 | Manual lift parts | Two levers, 150 N gas spring, M8 clamp and spring-stack architecture | CONFIRMED-DRAWING |
| DRW-002-745 | Crawler cover parts / pressure service | M12x1.5 gland for 3.5–5 mm cable, gland holder, spring-loaded camera/pressure-valve family, electronic cover and O-ring seals | CONFIRMED-DRAWING |
| DRW-002-752 | Lift housing | Camera connector + housing, M12x1.5 3.5–5 mm cable fitting, lift cover and multiple O-ring seals | CONFIRMED-DRAWING |
| ASS-002-890 | Lift housing unit, CRP300 | Lift housing, separate lift-housing cover, M12 gland, camera connector, protection sheet and O-ring seals; supports repeated MiniCam service-topology pattern | CONFIRMED-DRAWING |
| DRW-003-121 / ASS-003-121 | Lift arm, CRP300 | Dedicated CAMERA LIFT ARM COVER, side arms, holding plates, axles, bushings and O-rings | CONFIRMED-DRAWING |
| ASS-002-001 / ASM002 valve family | Compact pressure valve | FSS-001-843 valve shaft, FSS-001-844 valve cover, spring, bearing and O-ring stack; supports compact recessed pressure/fill interface | CONFIRMED-DRAWING |
| ASS-001-801 family | CAM026 camera | Sealed camera-head source architecture | SOURCE-IDENTIFIED |
| ASS-002-004 | CAM026 rotate sealing | Rotate-axis sealing source architecture | SOURCE-IDENTIFIED |
| ASS-004-097 family | RMP300 cable reel | Manual drum, level wind, brake, measuring unit and slip-ring path | SOURCE-IDENTIFIED |
| Repair photographs, 2025-03-14 | CRP-150 crawler/camera/lift service sequence | Integrated pressure body, large dry service cavity, open forward wet bay, perimeter seal land around upper/lift service opening, circular camera/lift interface and simple local wiring. See `PHOTO_EVIDENCE_2025-03-14.md` and `PRESSURE_LIFT_INTERFACE_EVIDENCE.md`. No dimensions are taken from uncalibrated photographs. | CONFIRMED-PHOTO |
| Repair photographs, 2026-08-31 | Open X200 motor compartment | Two longitudinal motor-gear units on one removable holder, separate Z16 bevel inputs and two transverse Z40 paths | CONFIRMED-PHOTO |
| Gearbox marking | FAULHABER 26/1S 66:1, 7060569, Swiss made, 4718 | Gearhead family and nominal ratio; electrical motor type remains unknown | CONFIRMED-PHOTO |

## WB23C interpretation note

The drawings and repair photos confirm the **functional topology** used by WB23C:

`sealed service cover/lift housing -> compact pressure valve -> M12 local cable gland -> protected short lift harness -> camera connector`.

They do **not** yet prove the exact original CRP150 small `PRESSURE` sub-cover screw count. PX-1 therefore treats its 2 x M4 small service-cover retention as an independent prototype design choice, not a copied source fact.

## Interpretation rules

- A product code in a parts list confirms identity and quantity, but not every manufacturing dimension.
- A photograph confirms visible topology, not hidden fits, tolerances or material.
- A reconstructed CAD dimension must not be promoted to `CONFIRMED-DRAWING` unless the dimension is explicitly legible in the source.
- Repeated architecture across CRP150/CRP300/CAM026 can justify topology decisions, but it does not authorize blind copying of dimensions into PX-1.
- `7060569` is retained as an execution/order identifier. It is not treated as a complete public motor model number.
- `4718` is provisionally interpreted as week 47 of 2018; this interpretation is not needed for the mechanical design.
