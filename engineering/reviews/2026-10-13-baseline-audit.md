# PX1 independent baseline audit — 2026-10-13

Status: **RELEASE BLOCKED**. This review is based on repository data and analytical models; **no physical robot was tested**.

## Evidence examined
- current/PX1_Current_Validation.json: Rev.C 2026-09-14, status HOLD_NOT_MANUFACTURING_RELEASE, metal_release=false.
- CAD model count: 6 wheels, 10 Z50, 2 Z16/Z40 inputs, 2 traction motors; shape validity list empty.
- Current CAD boolean report: **55 recorded interference/contact entries**, of which **29 are RIGID_INTERFERENCE**. Other entries: 12 seals, 6 thread engagements, 6 wheel profiles, 2 tooth contacts requiring check.
- current/HOLD_REGISTER.json: 10 open blockers H01-H10.
- current/01_MECHANICAL_6X6/A0_DRIVETRAIN_BENCH.md: active A0 engine is FAULHABER 2250S024BX4 + 26/1S ratio 66:1, older Pololu5707 retired to fallback.
- current/PX1_Current_BOM.csv P01: Pololu5707 remains selected; the current CAD validation also lists Pololu5707 geometry. **The nominal speed simulation uses FAULHABER while current BOM/CAD does not. This mismatch must be resolved before fabrication.**

## Largest CAD blockers (absolute boolean volume only; geometry may still be conceptual)
1. Pressure body vs SP13 connector envelope: 4050.67 mm³.
2. Camera carrier vs gas spring rod: 422.65 mm³.
3. Pressure body vs six-wire camera harness: 289.27 mm³.
4. Left middle wheel axle vs Pololu motor: 262.27 mm³.
5. Right middle wheel axle vs Pololu motor: 254.88 mm³.

## Immediate next executable task
For mechanics agent: choose the actual motor/gearhead, get source STEP with manufacturer envelope, update active BOM and current CAD consistently, then regenerate boolean intersections; do NOT hide an intersection by renaming it or excluding the pair. Do not modify six-wheel axle stations. Quantify updated motor-to-axle clearance and gearhead mounting stress.

For electric agent: test 40 m cable with representative load on actual cable before accepting an elevated-voltage architecture. A stable steady-state constant-power quadratic root is **not** permission to connect 110 V to an unrated tether.

## Evidence grades
- STATIC CHECK: counts and existing reported collisions.
- ANALYTICAL SCREEN: gear reduction/wheel speed, assumed copper feed and reference watchdog timing.
- LIVE CAD REBUILD: requires independent CI geometry solver job and its logged artifact for the exact commit.
- HARDWARE BENCH / SEAL / CAMERA / CABLE / E-STOP: NOT PERFORMED.
- MANUFACTURING RELEASE: NOT APPROVED.

Use python tools/px1_gate.py and inspect engineering/out/gates.md after each design change.
