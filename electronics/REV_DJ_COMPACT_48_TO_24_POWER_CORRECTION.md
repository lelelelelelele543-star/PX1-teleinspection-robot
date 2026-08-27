# PX-1 Rev.DJ — compact 48V -> 24V traction converter correction

Status: preferred prototype architecture; exact supplier/thermal plate still HOLD.

## Problem found
The previously discussed Mean Well RSD-200/RSD-300 railway converters are electrically robust but physically too large for the CRP150-size PX-1 body. A 300 W RSD unit is roughly 216 x 97 x 40 mm, which is not realistic inside a ~92 mm-wide crawler body.

## New architecture
Use an industry-standard **half-brick isolated DC/DC module** mounted to the crawler aluminum chassis/baseplate.

Preferred prototype class:
- Cincon **CHB200W-48S24** or equivalent;
- input: 18–75 VDC class;
- output: 24 VDC;
- power: 200 W;
- half-brick package approximately 58 x 61 x 13 mm class;
- isolated and protected industrial module;
- conduction/baseplate cooling into the crawler housing.

Equivalent half-brick modules with the same electrical/thermal envelope are allowed if procurement is easier.

## Power split
The 200 W module powers **traction only**:
48 V tether -> protection/filter -> 48/24 V half-brick -> traction contactor -> left/right motor drivers.

Camera, lighting and logic remain on separate lower-power isolated converters. This prevents video/control disturbances and ensures the full 200 W traction module is available to the motors.

## Motor-current assumption
Current traction candidate: 2x JGB37-555 24 V ratio 56.

Published family data vary, so final limits follow measured motors. Prototype control target before measurement:
- normal rated current expected <1 A per side;
- firmware soft current limiting around 2.5–3.0 A per side as an initial ceiling;
- short jam detection measured in tens/hundreds of milliseconds, not seconds;
- wiring fuse remains backup fire protection, not normal current control.

With a 3 A/side control ceiling the worst commanded motor input is about 144 W, leaving useful margin below a 200 W traction converter rating.

## Thermal mounting
- converter baseplate thermally coupled to aluminum crawler base;
- thin electrically appropriate thermal interface pad;
- mounting fasteners with defined torque;
- no reliance on an internal fan;
- temperature sensor on or adjacent to the DC/DC baseplate;
- firmware derating before converter thermal shutdown.

## Packaging gate
Reserve approximately 70 x 65 x 18 mm including connector/lead and mounting clearances rather than only the bare brick footprint.

This envelope fits the CRP150-style central body far better than the earlier RSD module.

## Release gates
1. source exact CHB200W-48S24/equivalent datasheet and 3D dimensions;
2. confirm availability/cost from the selected supplier;
3. build input/output filter per manufacturer application note;
4. 200 W heat-run on an aluminum mock chassis;
5. motor reversal/jam transient test;
6. verify 24 V bus remains inside BTS7960/next-driver limits;
7. repeat with 150 m tether-equivalent supply impedance.
