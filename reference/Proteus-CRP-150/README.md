# Proteus CRP-150 reference reconstruction

Status: active engineering reference, revision 0.1, 2026-08-31.

This directory collects verified information about the Mini-Cam Proteus CRP-150 crawler system and separates it from the PX1 replacement design. Its purpose is to preserve the proven Proteus architecture while identifying replacements that can be purchased, machined, printed and serviced without proprietary Mini-Cam parts.

## Project rule

Every statement is assigned one of four evidence states:

- `CONFIRMED-DRAWING` - explicitly shown in an available source drawing or parts list;
- `CONFIRMED-PHOTO` - visible in repair photographs or video;
- `RECONSTRUCTED` - derived from several confirmed facts and engineering geometry;
- `PROVISIONAL` - a candidate that still requires measurement or a bench test.

Original Mini-Cam drawings are not stored here. The available drawings contain restrictions on copying and distribution, and this repository is public. This directory stores source identifiers, engineering facts, calculations and original reconstruction work only.

## System map

| Subsystem | Original reference | Replacement goal | Current state |
|---|---|---|---|
| Crawler body and drive | CRP-150 / X200 | Preserve six-wheel, five-gear side drive and two-motor bevel input | Drive architecture confirmed |
| Manual lift | CRP-150 lift | Preserve manual lift, 150 N spring and M8 clamp | Source set identified |
| Camera | CAM026 | Preserve sealed PAN/ROTATE behavior with available camera and motors | Pending detailed reconstruction |
| Cable reel | RMP300 | Preserve manual drum, brake, level wind, measuring wheel and slip ring | Source set identified |
| Control unit | Proteus portable control unit | Rebuild from replaceable 24 V modules | Functional requirements established |
| Tether | Proteus inspection cable | Reinforced, field-repairable six-core copper cable | Architecture fixed; conductor sizing pending |

## Directory map

- [`SOURCE_REGISTER.md`](SOURCE_REGISTER.md) - source identifiers and evidence limits;
- [`VERIFICATION_REGISTER.md`](VERIFICATION_REGISTER.md) - open measurements and proof status;
- [`crawler/DRIVE_ARCHITECTURE.md`](crawler/DRIVE_ARCHITECTURE.md) - confirmed CRP-150/X200 drive reconstruction;
- [`crawler/GEAR_AND_SHAFT_AUDIT.md`](crawler/GEAR_AND_SHAFT_AUDIT.md) - calibrated gear geometry and CAD conflict audit;
- [`replacement-parts/STRATEGY.md`](replacement-parts/STRATEGY.md) - rules and first replacement matrix;
- `cad/reconstruction/` - only original reconstruction CAD, never copied factory drawings;
- `camera/`, `lift/`, `reel/`, `control-unit/` - subsystem work areas.

## Fixed project constraints

- preserve the successful Proteus mechanical architecture unless availability, serviceability, cost, reliability or manufacturability justifies a change;
- use integrated serviceable assemblies, not cartridge or cassette concepts;
- prototype electronics use ready-made modules; no custom main PCB;
- internal robot power is 24 V class;
- main tether is one professional reinforced six-core copper inspection cable;
- no coaxial main cable, no optical fiber and no bundle of loose ordinary twisted pairs;
- keep a universal sealed quick-release tail connection with a separate mechanical strength path;
- do not release machining drawings until one side drive, one camera axis and the reel counter mechanism are physically proven.

## Current priority

1. Complete the original crawler skeleton and shaft stack.
2. Select an available 24 V traction motor that preserves the Z16 to Z40 input.
3. Validate the five-Z50 side drive and wheel speed.
4. Reconstruct the manual lift.
5. Continue with CAM026, RMP300 and the control unit.
