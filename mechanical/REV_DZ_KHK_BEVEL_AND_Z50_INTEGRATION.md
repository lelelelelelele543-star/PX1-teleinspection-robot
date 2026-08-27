# PX-1 Rev.DZ — exact bevel + Z50 integration

Status: preferred prototype drivetrain hardware; manufacturing release still requires purchased-part measurement.

## Bevel pair
Preferred exact pair:
- KHK SB1.5-1845H — m1.5, Z18, bore 8 mm, OD 30.86 mm, face width 11 mm, total length 21.97 mm;
- KHK SB1.5-4518H — m1.5, Z45, bore 10 mm, OD 68.18 mm, face width 11 mm, total length 21.10 mm;
- ratio 45/18 = 2.5:1;
- pressure angle 20 deg;
- hardened tooth version H preferred.

This replaces the earlier abstract Z16/Z40 envelope while preserving the same 2.5:1 ratio seen in the uploaded MiniCam architecture.

## Torque gate for the bevel pair
KHK catalog data for the m1.5 45/18 pair show the small gear as the limiting member. For the hardened surface-durability column the small gear is approximately 2.16 N*m, while bending strength is higher.

PX-1 therefore sets a provisional maximum motor-output torque target of **1.50 N*m** before the bevel stage.

At eta_bevel = 0.90:
`T_side = 1.50 * 2.5 * 0.90 = 3.375 N*m`.

The motor must never be allowed to deliver its theoretical stall torque continuously into this pair. Current limiting/jam shutdown is mandatory and is calibrated against the exact purchased motors.

## Motor-side shaft
The small KHK gear has an 8 mm bore while the JGB37-555 candidate normally uses a smaller motor-output shaft.

Use a separate short bevel-pinion shaft:
- Ø8 h6 gear seat;
- 3x3 key or clamp arrangement after real gear inspection;
- one compact radial bearing immediately behind the bevel pinion;
- short rigid/clamping coupling from motor shaft to the bevel-pinion shaft;
- motor gearbox bearing provides the second widely-spaced support.

Do not hang the bevel pinion directly on an unsupported motor shaft extension.

## Large-bevel / side-drive shaft
The KHK large gear has a 10 mm bore. The side wheel gears are standardized around 12 mm bores.

Use a stepped middle output shaft:
- Ø10 h6 seat in P0 for the KHK Z45 bevel gear;
- Ø10 bearing/seal journal at the P0/P1 or P0/P2 boundary;
- step to Ø12 h6 in the side bay;
- Z50 side gear on Ø12 keyed seat;
- outer Ø12 bearing/seal flange;
- wheel hub on Ø12 outer seat.

This keeps the exact bought bevel gear unmodified at the bore while allowing stronger/common Ø12 side-drive hardware.

## Large bevel packaging
With OD 68.18 mm centered at X=150, Z=45:
- X envelope ≈ 115.91…184.09 mm;
- Z envelope ≈ 10.91…79.09 mm.

Therefore the crawler body lower surface is moved from the older Z=14 packaging datum to approximately **Z=8 mm**, while keeping the body top near Z=90 mm. This leaves ~2.9 mm nominal radial packaging margin below the large bevel envelope and more above it.

The body still clears ideal DN150 because the limiting transverse corner is the side cover, not the lower central body.

## Twin-motor packaging
Preferred JGB37-555 motor center positions:
- left motor axis Y=+19 mm;
- right motor axis Y=-19 mm;
- both approximately Z=45 mm;
- axes longitudinal in X.

For Ø37 mm motor envelopes:
- motor-to-motor gap ≈1 mm;
- nearest body-wall radial gap ≈8.5 mm inside a 92 mm body width.

This is tighter than earlier staggered concepts but closer to the two-parallel-motor layout shown in the uploaded MiniCam motor-unit drawing.

## Side Z50 gears
Preferred purchased wheel gear candidate:
- KHK SSG1-50;
- m1, Z50, 20 deg;
- bore 12 H7;
- pitch Ø50;
- OD Ø52;
- face width 8 mm;
- hardened/ground teeth.

Published allowable torque is comfortably above the 3.375 N*m maximum side-input target.

For packaging, the stock hub may be shortened on the non-tooth side after the purchased gear is inspected. No machining is allowed into the tooth/root hardened zone.

## Idler adaptation
Idlers remain Z50 m1 so the train is 1:1.

Preferred prototype route:
- start from the same KHK tooth geometry where practical;
- rework only the hub/bore to accept compact bearings or use a separately machined idler hub;
- fixed idler pin remains non-rotating;
- gear rotates on replaceable bearings;
- thrust washers control axial float.

Do not make the idler pin itself rotate in the aluminum side plate.

## Side output and traction
At 3.375 N*m per side and wheel effective radius 45 mm, theoretical tangential force before side-train losses is about 75 N per side. Actual pipe traction will be tire/grip limited well before the drivetrain shaft reaches its stress limit.

## Release gates
1. buy/measure one KHK bevel pair;
2. verify mounting distance/contact pattern with marking compound;
3. measure JGB37 output shaft and coupling fit;
4. verify large gear does not contact body at full tolerance stack;
5. buy one SSG1-50 and confirm hub can be shortened without entering hardened tooth/root region;
6. run low-speed loaded contact-pattern and temperature test;
7. calibrate current-to-torque limit before stall testing.