# PX-1 Rev.GK — X200 retention, shaft interfaces and bearing-reaction closure

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## Supersedes / continues
Rev.GK continues the supported Rev.GJ X200 drivetrain without changing its global architecture:

`24 V traction motor -> supported Z16 shaft -> Z16/Z40 bevel -> X200 shaft -> 18x30x7 dynamic seal -> side Z50 -> five-Z50 train -> three wheels`

## Pinion shaft detail
- separately supported pinion shaft remains mandatory;
- 6801/61801 12x21x5 placed nearest the overhung bevel;
- second support: 6701 12x18x4;
- support centers X228 and X233;
- pinion force station X221;
- Ø8 pinion seat;
- 2x2x7 parallel-key candidate;
- M4 end-retention thread candidate;
- motor coupling represented as Ø6 D-bore, AF 5.4, 10 mm depth; exact motor sample measurement remains HOLD.

At the provisional 1.0 N.m motor torque ceiling the pinion-force screen gives approximately Ft=100 N, Fr=33.8 N, Fa=13.5 N. With 2x shock screening the bearing reactions are about 507 N on the 6801/61801 and 296 N on the 6701. Static screening safety factors remain above 1.7.

## X200 side-shaft detail
The first attempted compact stack placed a Z50 hub inward into the 18x30x7 seal envelope and was rejected after a non-zero solid-intersection check.

The accepted Rev.GK stack is:
- Z40 bevel seat / Ø10 shaft;
- 6800/61800 10x19x5, Y29.5..34.5;
- 18x30x7 seal on Ø18 land, Y34.5..41.5;
- 0.5 mm rotating slinger/spacer, Y41.5..42.0;
- m1 Z50 face 3.5 mm, Y42.0..45.5, no inward hub;
- 0.3 mm thrust shim, Y45.5..45.8;
- DIN471-12 retaining-groove candidate Ø11.5 x 1.1, beginning Y45.9;
- local X200 side-cover boss Ø26, Y46..54;
- blind 6701 support Y49..53, leaving 1 mm external boss skin.

The local boss is only at the intermediate X200 drive station and does not alter any external wheel station. It keeps the large side-cover O-ring plane untouched.

## Keys / torque interfaces
- pinion Z16: 2x2x7 key candidate;
- large Z40: 3x3x10 key candidate;
- side Z50: 4x4x3.5 key candidate;
- motor-side Ø6 D-bore remains provisional until the purchased motor is measured.

At the current torque ceiling the screening stresses are low:
- pinion key: ~17.9 MPa shear / 35.7 MPa bearing;
- bevel key: ~14.2 / 28.3 MPa;
- Z50 key: ~25.3 / 50.6 MPa;
- shaft torsional shear remains below ~11 MPa on the checked diameters.

## Bearing reaction screen
Conservative side-shaft resultant reactions including bevel and Z50 loads:
- inner 61800: ~185 N nominal, ~370 N at 2x shock;
- outer 6701: ~106 N nominal, ~212 N at 2x shock.

Using the current catalog screening ratings gives 2x-shock static safety factors above 2.2 on both side-shaft supports.

## CadQuery validation
`mechanical/cadquery/PX1_X200_Detail_RevGK.py` executes successfully on CadQuery 2.8.0.

PASS:
- all generated solids valid;
- pinion key clears both pinion supports;
- Z50 clears the seal and blind 6701;
- Z50 key does not cross the seal land;
- slinger, gear and shim do not overlap;
- Z50 does not collide with the local cover boss;
- bevel key clears the 61800 support;
- bearing, shaft and key screening rules pass.

## HOLD / release gates
- exact Ø32 motor SKU and measured output shaft;
- exact bevel manufacturing process, material, heat treatment and rated torque;
- actual purchased bearing fits;
- exact 18x30x7 seal article and pressure-direction test;
- exact DIN471 ring article/groove confirmation;
- physical current-limit calibration;
- integrated full-crawler collision and DN150 rerun.

## Next autonomous block
Rev.GL integrates Rev.GF wheel stations and the Rev.GK X200 drivetrain into the complete two-sided six-wheel crawler, then reruns DN150, seal-land and collision validation before FreeCAD/FEA pressure-body work.
