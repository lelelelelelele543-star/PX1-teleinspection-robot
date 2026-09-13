# Proteus / CRP source evidence — pressure cover, lift housing and camera harness

Date: 2026-09-14
Purpose: source-register supplement for PX-1 WB23C.

## Evidence hierarchy

1. MiniCam source drawings in the project archive.
2. User repair photographs of real CRP150/Proteus hardware.
3. Manufacturer manuals/product literature.
4. Current catalog data only for replacement component availability.

Dimensions are never scaled from photographs without a known scale.

## DRW-002-752 — LIFT HOUSING

Direct part-list evidence:

- `FSS-002-085 Camera Connector`;
- `FAL-002-071 Housing Cameraconnector`;
- `CAB-002-461 cable fitting M12x1.5 d3.5-5mm`;
- `FAL-002-081 LIFT COVER`;
- O-rings 38 x 1.5, 6 x 1, 21 x 1.5 and 28 x 1.5.

Engineering conclusion: MiniCam deliberately combined a serviceable lift housing, sealed interfaces, compact local cable gland and camera connector instead of requiring a long high-flex industrial cable loop inside the lift.

## DRW-002-745 — Crawler Cover Parts

Direct part-list evidence:

- `CAB-002-461 cable fitting M12x1.5 d3.5-5mm`;
- `FAL-002-086 Holder Cable Fitting`;
- `FSS-001-844 CAMERA VALVE COVER`;
- `SPR-001-847 VALVE SPRING`;
- `FSS-001-843 CAMERA VALVE SHAFT`;
- two 3 x 1 O-rings plus a 6 x 1.5 O-ring;
- `FAL-002-059 Cover Electronic`.

Engineering conclusion: a compact spring-loaded pressure/fill valve and an external local cable fitting are source-backed design features.

## ASS-002-890 — LIFT HOUSING UNIT - CRP300

Direct evidence:

- M12 gland for 3–5 mm cable;
- separate lift housing;
- separate lift-housing cover;
- camera connector;
- protection sheet;
- multiple O-ring seals.

Engineering conclusion: a removable upper/lift cover plus protected local cable is a repeated MiniCam architecture, not a one-off interpretation.

## DRW-003-121 / ASS-003-121 — lift arm

Direct evidence:

- dedicated `FSS-003-127 CAMERA LIFT ARM COVER`;
- side arms;
- lift-housing holding plates;
- multiple bushings, axles and O-rings.

Engineering conclusion: cable/arm protection should be a simple removable guard tied to the lift, not a cassette or bulky energy-chain mechanism.

## Pressure-valve source family

`ASS-002-001` and related CAM026 source assemblies contain the same valve family:

- `FSS-001-843 CAMERA VALVE SHAFT`;
- `FSS-001-844 CAMERA VALVE COVER`;
- 4 mm ball bearing;
- two 3 x 1 O-rings;
- valve spring;
- 6 x 1.5 O-ring.

This reinforces that MiniCam's pressure-service interface was intentionally compact and integrated.

## Repair photographs — 2025-03-14

The repair sequence shows:

- integrated crawler pressure body rather than removable internal pressure cartridges;
- machined top/front service opening in the lift/body region;
- continuous perimeter sealing land/groove around the opening;
- circular camera/lift connector in the same service region;
- dry electronics accessible with upper cover removed;
- simple local wiring in the lift region.

Photographs are used for topology, service access and packaging interpretation only. No unscaled photo dimension is copied into PX-1.

## What is NOT source-confirmed

The archive does not conclusively prove that the exact small CRP150 cover marked `PRESSURE` is retained by exactly two screws. Larger MiniCam cover assemblies use more screws, while field memory points to a smaller pressure-marked sub-cover with about two bolts.

Therefore:

- PX-1 uses **2 x M4** on its small service cover as an independent engineering choice;
- do not describe that screw count as an exact Proteus copy until a source photo/drawing clearly proves it.

## Controlled PX-1 interpretation

WB23C adopts only the source-backed functional logic:

`sealed service opening -> pressure/fill valve -> compact cable gland -> short protected lift harness -> camera connector`.

PX-1 dimensions, connector articles and cover geometry remain independently validated.
