# PX-1 Rev.B Work Block 02 — wheel, axle flange and retention

Date: 2026-09-11
Status: ACTIVE REVB CANDIDATE / CAD SCREEN PASS / NOT MACHINING RELEASE

## 1. Purpose

Resolve the wheel-end conflict left by the older PX-1 revisions and make the X250 wheel station serviceable, sealed and compatible with DN150 without relying on a bulky external M8 nut.

This block follows WB01 and does not change the six-wheel / five-Z50-per-side architecture.

## 2. Source recheck

CRP-150 source `ASS-002-103` explicitly lists the wheel-retention assembly as:
- wheel disk `FSS-002-065`;
- M6 x 14 A2 socket-button screw;
- M6 spring washer;
- O-ring 10 x 1.8.

The source screw is an axial retainer. Wheel torque is carried by the positive shaft/key interface, not by screw friction.

## 3. Historical PX-1 conflict

PX-1 accumulated three incompatible wheel-end concepts:
1. source-like internal M6 retention in early source studies;
2. external M8 thread + locknut in Rev.AU/Rev.AV;
3. later recessed internal M8 retention in Rev.GF/Rev.GQ.

For Rev.B the external M8 locknut is rejected at the wheel station. It consumes unnecessary radial/tool envelope and does not improve the torque path because the key already transmits wheel torque.

The later internal M8 concept is also superseded for the DN150 wheel station by the smaller source-like M6 architecture unless first-article testing proves M6 inadequate.

## 4. Rev.B retention decision

Use:
- **M6 x 14 ISO 7380-1 button-head screw, stainless A4** for PX-1;
- M6 DIN 127 / ISO 7980 spring washer, stainless A4;
- separate machined wheel retaining disk, OD 20 mm screening value;
- blind internal M6 x 1 thread in the wheel shaft;
- 10 x 1.8 FKM/FPM 80 Shore O-ring as a local static face seal protecting the blind screw/thread interface from sewage/water.

PX-1 upgrades the source A2 screw to A4 for wet/sewer corrosion resistance.

### Current purchasability check, 2026-09-11

The selected sizes are real catalogue items, not invented geometry:
- M6x14 ISO 7380-1 A4 exists as a full-thread commercial fastener; current Czech marketplace/distributor listings include GTIN `4043377265944` and Killich item `73805906014`;
- M6 A4 DIN 127 spring washers are standard commercial items, nominal 6.1 mm ID / 11.8 mm OD / 1.6 mm section thickness;
- Dichtomatik/FPM 80 `10x1.8` is commercially listed as manufacturer number `57141` / designation `OK.010,00/1,80 F80`.

Final purchase source can be marketplace/local industrial distributor; dimensions are now supplier-verifiable.

## 5. Real fastener envelope used in CAD

For the compact M6 button head the Rev.B screen uses:
- thread: M6 x 1;
- under-head screw length: 14.0 mm;
- head diameter: 10.5 mm;
- head height: 3.3 mm;
- internal hex class: 4 mm for the ISO 7380-1 reference geometry.

Spring washer tightened/solid axial section used for packaging:
- ID 6.1 mm;
- OD 11.8 mm;
- section thickness 1.6 mm.

The washer free height is not used as the tightened running envelope.

## 6. Wheel/shaft axial geometry candidate

Left-side global Y screen:
- flange functional end: Y = 62.20 mm;
- flange-pocket end in wheel core: Y = 62.45 mm;
- Ø17 keyed wheel seat begins: Y = 62.15 mm;
- useful 4x4 key region: Y = 62.15...66.90 mm;
- shaft/wheel-seat end face: Y = 67.00 mm;
- retaining disk: Y = 67.00...68.50 mm;
- compressed M6 spring washer: Y = 68.50...70.10 mm;
- M6 button head: Y = 70.10...73.40 mm.

The screw head intentionally projects beyond the elastomer wheel's nominal Y=71 end plane. This is acceptable because it is small-radius hardware near the wheel axis and remains inside the DN150 cylinder.

M6x14 under-head length passes through 1.5 mm disk + 1.6 mm compressed spring washer. Resulting threaded engagement in the shaft is approximately:

`14.0 - 1.5 - 1.6 = 10.9 mm`

This is about 1.82 x nominal thread diameter and is adequate as a prototype geometry screen; exact tightening torque/thread strip margin remains a material-specific release calculation.

## 7. 10x1.8 O-ring function

Do not treat the small wheel-end O-ring as a pressure-volume shaft seal. The real P1/P2 water barrier remains the X-ring at the axle flange.

Rev.B uses the 10x1.8 FKM ring only to protect the blind M6 screw/thread interface:
- static axial face gland in the Ø17 shaft end around the M6 thread;
- candidate gland depth: 1.35 mm;
- candidate radial gland width: 2.40 mm;
- nominal axial squeeze: 25%;
- nominal gland fill: ~78.5%.

These are prototype values. The final groove is checked against the exact Dichtomatik/supplier tolerance before machining release.

## 8. Revised wheel-core / axle-flange interface

The later three-support wheel station requires more axial flange depth than the old Rev.FH 12 mm envelope.

Rev.B wheel core therefore receives a central dished clearance pocket around the removable axle flange:
- flange clamp envelope: Ø50 mm;
- wheel-core pocket: Ø52 mm;
- radial hard clearance: 1.0 mm;
- flange end Y = 62.20 mm;
- pocket end Y = 62.45 mm;
- axial hard clearance: 0.25 mm.

The pocket removes only metal core material. The external Rev.GF/Rev.GQ tread envelope is unchanged.

## 9. Flange functional stack retained

From inside to outside:
- 61801-2RS-class intermediate bearing;
- 0.20 mm shoulder/gap screen;
- 61903-2RS wheel-load bearing;
- 0.20 mm shoulder/gap screen;
- stationary X-ring gland on the Ø19-class polished shaft land;
- static 32x1.5 flange O-ring;
- positive pilot/register and four M3 clamp screws.

The exact flange body is now a 17-18 mm-class functional part, with part of the bearing pocket overlapping the side-cover thickness. The older 12 mm total-flange statement is historical only.

## 10. DN150 interpretation correction

An important Rev.A interpretation error is corrected here.

The Rev.GF outer wheel tread is an **elastomer rolling/contact surface**. It is supposed to touch the pipe. Therefore its approximately 0.12 mm analytical ideal-pipe margin is not a valid hard-clearance acceptance criterion by itself.

The correct DN150 separation is:
- elastic tread = contact/deformation geometry;
- metal wheel core, axle flange, screw, washer and other rigid hardware = hard-clearance geometry.

With the current 4 mm radial elastomer thickness:
- minimum analytical **metal core** margin to the ideal DN150 cylinder: ~4.12 mm;
- M6 button-head outer-tip hard margin: ~3.11 mm;
- spring-washer hard margin: ~13.72 mm;
- retaining-disk hard margin: ~13.49 mm.

All modeled rigid parts produce zero volume outside the ideal DN150 cylinder.

The tread still requires a physical DN150 sweep because real rubber/PU deformation, pipe ovality, deposits and welds cannot be qualified by the ideal-cylinder CAD model alone.

## 11. Key/load screen

Rev.B keyed wheel-seat useful length is 4.75 mm.

At the protected 4 N.m wheel-torque screening case, 4x4 key on Ø17 gives approximately:
- key shear stress: 24.8 MPa;
- key bearing stress: 49.5 MPa.

The screw is not used as the torque path.

The internal M6 envelope also leaves substantial shaft wall:
- radial wall at Ø17 around an approximate M6 minor diameter: ~6.11 mm;
- minimum local wall between the M6 thread envelope and the screened 2 mm-deep keyway root: ~4.11 mm.

These are geometry screens, not fatigue-release values.

## 12. Executed CAD result

Executable source:
`mechanical/cadquery/PX1_WheelFlange_RevB.py`

Validation record:
`mechanical/cadquery/REV_B_WHEEL_FLANGE_VALIDATION.json`

Current executed result:
- wheel core valid;
- tire valid;
- axle flange valid;
- zero core/flange collision;
- zero tire/flange collision;
- zero bearing/flange material collision for the reserved pockets;
- zero wheel-disk/core collision;
- zero washer/core collision;
- zero real-size M6 head/core collision;
- full M6 engaged-thread envelope remains inside the stepped shaft;
- all rigid wheel-end solids remain within ideal DN150;
- `packaging_status = PASS_SCREEN`;
- `release_status = HOLD`.

## 13. Rev.B release gates still open

1. Freeze actual wheel-disk material/thickness and manufacturing drawing.
2. Freeze exact A4 M6x14 screw article and A4 M6 spring washer article.
3. Freeze exact 10x1.8 FKM ring and redraw gland to its manufacturer tolerance.
4. Calculate M6 tightening torque / screw proof / internal-thread stripping with final shaft material.
5. FEA/deflection check the real axle flange with 61801/61903 pockets and M3 clamp pattern.
6. Verify tool access and wheel removal on a 1:1 printed mock-up.
7. Run pressure-decay and submerged rotating-shaft test.
8. Run a physical DN150 tube sweep with the selected elastic tread.

## Supersession in Rev.B

For the wheel-end retention only:
- `REV_AU_SHAFT_END_FREEZE.md` external M8 nut concept -> historical;
- `REV_AV_M8_FASTENER_FREEZE.md` external M8 locknut concept -> historical;
- Rev.GF/Rev.GQ M8 wheel-retention statement -> superseded by this M6 internal-retention candidate;
- Rev.GF tapered wheel **external tread profile remains active**;
- Rev.GQ elastomer/core manufacturing method remains active where it does not conflict with the new central flange pocket.

## Change log

### 2026-09-11
- reconciled source M6 retention with PX-1 wheel packaging;
- replaced M8 retention for Rev.B wheel station;
- added supplier-real M6x14 A4, M6 A4 spring washer and 10x1.8 FKM references;
- introduced Ø52 dished core pocket around Ø50 axle flange;
- executed real-head/washer/disk CAD collision screen;
- corrected the DN150 criterion to distinguish elastic tread contact from rigid-part clearance.
