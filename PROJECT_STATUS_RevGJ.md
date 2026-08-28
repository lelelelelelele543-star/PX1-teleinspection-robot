# PX-1 Rev.GJ — supported X200 drive closure

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## Completed in Rev.GH–GJ
The X200 power path is now geometrically closed from both Ø32 traction-motor envelopes to the side Z50 trains:

`24 V motor -> supported bevel pinion shaft -> compact Z16/Z40 bevel -> 61800 supported X200 shaft -> 18x30x7 dynamic seal -> side Z50 -> five-Z50 side train -> three wheels`

The small bevel remains on a separately supported shaft with a 61801-class bearing, consistent with the source CRP150 architecture rather than hanging the bevel directly on the motor shaft.

## Active X200 geometry
- two Ø32 x 92 mm traction-motor candidate envelopes;
- axes Y +/-16.5, Z45, both pointing rearward to clear the LOW camera envelope;
- custom compact bevel candidate m1.25, Z16/Z40, face 8 mm, ratio 2.5;
- fixed X200 bearing/seal boss, Ø38 envelope;
- inboard 61800 10x19x5 support;
- Ø18 x 7 seal land with 18x30x7 shaft seal;
- outboard Ø12 journal;
- side input Z50 face 3.75 mm at Y42.125..45.875;
- blind 6701-2RS 12x18x4 support in the inside face of the side cover, leaving 1 mm outside skin;
- main side-cover O-ring path untouched.

## Body packaging correction
The full-width Rev.GC body remains 307 mm long. The extra motor-tail length is absorbed in a narrow central rear pressure extension:
- overall pressure envelope length to rear extension: 340 mm;
- rear extension beyond main body: 33 mm;
- rear extension outer section: 76 x 44 mm;
- motor rear ends X329;
- internal rear pressure wall X332;
- motor-to-wall axial clearance 3 mm.

This avoids lengthening both side bays/side covers and gives the rear extension much larger DN150 radial clearance than the side-cover corners.

## CadQuery validation
`mechanical/cadquery/PX1_X200_Drive_RevGJ.py` executes successfully on CadQuery 2.8.0.

Current checks PASS:
- left/right motor intersection: zero;
- motor vs retained LOW camera envelope: zero;
- motor vs pressure shell: zero;
- large bevel vs motor: zero;
- large bevel vs side Z50: zero;
- side Z50 vs body/cover: zero;
- blind 6701 vs remaining side-cover solid: zero;
- side gear 3.75 mm + cover bearing 4 mm = 7.75 mm inside 8 mm bay;
- motor side-wall clearance 1.5 mm;
- motor-to-motor gap 1.0 mm;
- X200 blind-bearing envelope has ~20 mm radial margin to the side-cover O-ring centerline;
- rear extension is well inside ideal DN150 radial envelope.

## Gear decision
A hardened stock KHK m1.25 Z20/Z40 pair was checked. It is not a drop-in: the large gear's catalog mounting distance pushes its back face through the P0/P1/P2 membrane at the existing motor-axis spacing. Rev.GI therefore retains a compact custom Z16/Z40 candidate and records the trade separately.

Current provisional bevel protection rule: design/command ceiling equivalent to 1.0 N.m at motor output until supplier rating and measured motor torque-current data exist. With 2.5:1 and 0.85 screening efficiency this gives ~2.125 N.m into one side train and ~6.1 m/min theoretical speed for the current 54 rpm motor candidate.

## Current HOLD / release gates
1. exact Ø32 motor sample and measured torque-current-speed curve;
2. final bevel supplier, tooth geometry, material, heat treatment and ISO/AGMA allowable torque;
3. exact 18x30x7 seal article and direction/pressure validation;
4. exact 61800/61801/6701 bearing articles and fits;
5. detailed keys/retainers on pinion, large bevel and X200 Z50;
6. physical current-limit calibration;
7. full integrated six-wheel + X200 + lift + tail CAD rerun;
8. pressure test and physical DN150 sweep before machining release.

## Next autonomous block
- detail X200 keys, shoulders, circlips and assembly sequence;
- check bearing reactions from bevel and spur forces;
- define rear pressure-extension/tether transition and service access;
- integrate Rev.GJ into full crawler validation;
- then move to FreeCAD/FEA pressure-body and rear-extension checks.
