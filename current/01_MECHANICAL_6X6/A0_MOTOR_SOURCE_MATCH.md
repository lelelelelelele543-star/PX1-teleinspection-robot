# A0 motor-source match — ASS-002-386

Status: MECHANICAL BASELINE SELECTED FOR A0 / OEM IDENTITY NOT CLAIMED.

## Source evidence
MiniCam ASS-002-386 lists:
- 2 x MOT-001-760 MOTOR and GEAR;
- 2 x GEA-002-531 Bevel Gear small Z16;
- 2 x FSS-002-083 Axle Bevel Gear;
- 2 x BEA-002-701 61801-2RS (12x21x5);
- common FAL-002-082 motor holder.

The 1:1 drawing shows a three-stage Ø26-class reduction gearhead followed by an Ø22-class motor. The Z16 is on a separate supported shaft, not simply cantilevered directly from the motor shaft.

## FAULHABER envelope match
Candidate used for PX1 A0:
- motor: FAULHABER 2250S024BX4;
- gearhead: FAULHABER 26/1 S, 66:1 three-stage candidate.

Published geometry:
- motor Ø22 mm, L=51.8 mm;
- 26/1 S Ø26 mm;
- three-stage 26/1 S L2=44.4 mm;
- gearhead output shaft Ø5 mm x 12 mm;
- gearhead mounting pilot Ø13 mm;
- 4 x M3 mounting holes on Ø20 mm circle;
- 26/1 S continuous recommended input speed <=4000 rpm;
- three-stage ratios include 43:1, 66:1 and 86:1.

Two Ø26 gearheads placed on the recovered 27 mm motor-centre spacing occupy 53 mm total width. This equals the current reconstructed 53 mm dry-cavity width. Combined motor + three-stage gearhead body length is 96.2 mm and matches the proportions of ASS-002-386 closely.

This is sufficient to use the pair as the PX1 A0 source-match mechanical baseline. It is not sufficient to state that MOT-001-760 was manufactured by FAULHABER or that the original ratio was exactly 66:1.

## Motor electrical data relevant to A0
2250S024BX4:
- nominal voltage 24 V;
- no-load speed about 6200 rpm;
- rated speed about 4870 rpm;
- rated torque 26.2 mNm;
- rated current 0.85 A;
- digital Hall sensors, +5 V supply, Hall A/B/C;
- standard Hall outputs are open collector and require pull-ups unless the chosen controller provides them.

Because 6200 rpm exceeds the 26/1 S recommended continuous input limit, the motor controller must impose the gearhead speed limit rather than allowing full no-load motor speed.

## Estimated crawler output with 66:1
Using the exact published nominal ratio 66.220408, 70% gearhead efficiency, Z16/Z40 = 2.5 and a planning-only 85% bevel efficiency:
- rated motor torque 26.2 mNm -> about 1.21 Nm at the gearhead output;
- after bevel reduction -> about 2.58 Nm at the rear X250 axle before losses in the side Z50 distribution;
- at 3500 motor rpm -> about 21.1 wheel rpm / 6.0 m/min for Ø90 wheels.

These are design estimates, not acceptance values. Actual current, speed and traction are measured in A0.

## Pinion support
Keep the source logic:
`gearhead Ø5 output -> short coupling/socket -> Ø12 supported pinion axle -> 61801 -> Z16`.

A0 uses a split/pinch socket adapter so no permanent geometry is released before actual gear/shaft parts are tested. The final axle must be a single serviceable machined part after A0 determines socket depth, axial retention and Z16 hub dimensions.

## References
- MiniCam source: DRW-002-386 / ASS-002-386.
- FAULHABER 2250 ... BX4 current datasheet/product page.
- FAULHABER 26/1 S planetary gearhead datasheet.
