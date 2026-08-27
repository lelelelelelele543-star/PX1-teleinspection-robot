# PX-1 Mechanical CAD

Primary CAD: FreeCAD.

## Controlled assembly hierarchy
1. `00_MASTER_PARAMETERS` — global dimensions and interfaces.
2. `10_BODY` — pressure body, covers and seal seats.
3. `20_DRIVETRAIN` — shafts, gears, bearings and wheel interfaces.
4. `30_CAMERA_LIFT` — manual parallelogram lift.
5. `40_CAMERA_HEAD` — TILT/continuous-ROLL head and quick release.
6. `50_TAIL` — tether tail, strain relief and lowering eye.
7. `90_ASSEMBLY` — full crawler assembly and interference checks.

## Current master envelope
- body length: 250 mm
- body width: 94 mm
- body height: 76 mm
- wheelbase: 160 mm
- nominal wheel diameter: 90 mm

No machining file is considered released until copied into `/release` with a controlled drawing revision.
