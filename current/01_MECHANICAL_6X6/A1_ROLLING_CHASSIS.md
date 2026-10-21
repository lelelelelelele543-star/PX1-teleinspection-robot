# A1 — rolling 6×6 prototype chassis

Status: GENERATED PROTOTYPE FIXTURE / NOT PRODUCTION BODY.

Purpose: move immediately from isolated transmission work to a complete six-wheel rolling article without waiting for pressure-body machining.

## Frozen geometry
- six wheels total;
- wheel stations X50 / X150 / X250 on both sides;
- five Z50 stations per side at X50 / X100 / X150 / X200 / X250;
- rear X250 remains the driven long-axle station;
- left/right differential drive remains mandatory.

The source pack supports the side-drive composition: DRW-002-374 contains three driven Z50 axle gears and two idle Z50 gears on each side assembly; DRW-002-375 contains the Z40 bevel stage in the crawler housing; DRW-002-386 contains two motors, two Z16 gears and two 61801 pinion supports.

## What the A1 fixture deliberately changes
For speed, A1 uses a printable bearing fixture rather than the final sealed axial package:
- 12 mm bench shafts;
- 6001-2RS 12×28×8 bearings in the fixture plates;
- four printable support plates;
- three printable crossbars;
- printable m1/Z50/20° test gears;
- reconstructed 90 mm wheel-screen geometry only.

These substitutions are for rolling and meshing tests only. Production 61801 / 61903 bearings, bushings, X-rings, flange geometry and shaft shoulders remain controlled by H02/H03/H04.

## Generated package
`PX1_A1_Rolling_Chassis.py` creates:
- `PX1_A1_Rolling_6x6_Assembly.step`;
- `PX1_A1_SidePlate.step` and STL;
- three crossbar STEP/STL files;
- `PX1_A1_Z50_m1_PA20_TEST.stl`;
- `PX1_A1_QRW90_SCREEN_ONLY.stl`;
- `PX1_A1_Validation.json`.

The side plate is about 260×74×6 mm and fits the Anycubic Chiron bed. Generated print parts are translated to local coordinates for slicer use.

## Current CAD screen
The generated assembly bounding box is approximately 290×133×90 mm. The reconstructed wheel/profile screen shows a small DN150 envelope violation (about 1.35% maximum outside-volume fraction on the screened components), so the placeholder wheel profile is not released as a DN150 production tire. This is consistent with H01: exact QRW90SR/150 tread/quick-lock geometry is still missing.

## Test order
1. Print one side plate and one Z50 first; verify shaft/bearing and gear print fit.
2. Build one five-gear side train and hand-turn it.
3. Build the mirrored train.
4. Join with the three crossbars.
5. Fit temporary wheel screens/discs and perform flat-floor rolling test.
6. Connect the rear X250 input to the A0 motor/bevel module only after its motor/gearhead interface is locked.

A1 is complete only after the real assembled rig runs forward/reverse and differential-turns without gear binding or shaft migration. CAD generation alone does not close the gate.

## 21.10.2026 — v2 fit-check corrections

The original A0/A1 rectangular cutouts reached into Ø28.16 bearing seats and the M4 retainer positions crossed those cutouts. They are now reduced to 14×32 mm with a nominal 3.92 mm bearing-to-window wall; the two M4 clearance holes per bearing are placed vertically at ±22 mm.

The three A1 crossbars are now aligned to exact panel holes (X,Z) = (30,15), (150,75), (270,15) in the source datums and have real through-bores Ø5.2 mm for long M5 bolts. Prior blind bores and 5 mm hole offsets could not assemble. Four panel STLs and Z50 STL are exported flat on the virtual print bed. The two side plates on each side are spaced 14 mm between plate centres to give ~1 mm nominal axial clearance each side after 6001 bearing protrusions.

CI checks watertight STL, correct print-bed orientation and hole topology. A1 remains a dimensional fixture only: both wheel and gear-to-shaft torque interfaces have NOT been released; motor mounting and Z16/Z40 bevel transmission are missing; printed test gears cannot qualify loaded drivetrain. Do not operate it as a powered crawler or order production machining on this basis.
