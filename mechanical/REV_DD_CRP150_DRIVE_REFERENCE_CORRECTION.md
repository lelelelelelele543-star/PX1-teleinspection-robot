# PX-1 Rev.DD — CRP150 drive-reference correction

Status: architecture correction based on the uploaded original MiniCam crawler drawings. Supersedes the Rev.CZ assumption that a ~45 rpm JGB37 motor should directly feed the middle wheel gear through a spur reduction.

## What the uploaded CRP150/Proteus drawings actually show
The original crawler motor unit uses two motors and **two small bevel gears Z16**. The crawler housing carries **two large bevel gears Z40**, two bevel-output axles and two shaft seals 18x30x7. The motor unit drawing also shows 61801-2RS bearings (12x21x5), while the crawler housing drawing shows 61800-2RS bearings (10x19x5).

This is a key architectural clue: the successful CRP150 layout turns the motor drive through 90° using a compact bevel stage rather than placing a long motor directly on a wheel shaft.

## PX-1 adaptation
We do NOT copy MiniCam part geometry, but we adopt the same useful architecture:

motor -> small bevel pinion -> large transverse bevel gear -> one side-drive input -> three-wheel side gear train.

Per crawler:
- 2 traction motors total, one per side;
- 2 bevel input stages;
- 6 driven wheels;
- side covers remain our own sealed/O-ring/pressurized design.

## Ratio
Reference tooth count: Z16 : Z40 = **2.5:1 reduction**.

For PX-1 this changes the preferred motor speed class.

With Ø90 wheels:
- 100 rpm motor -> 40 wheel rpm after 2.5:1 -> about 11.3 m/min ideal;
- 107 rpm motor -> 42.8 wheel rpm -> about 12.1 m/min ideal;
- 120 rpm motor -> 48 wheel rpm -> about 13.6 m/min ideal.

Therefore the new prototype purchase target becomes approximately **24 V / 100–120 rpm / Hall encoder**, not 45 rpm, if the 2.5:1 bevel stage is retained.

## Why this is better for the CRP150-style body
- motors can sit inside the narrow central housing;
- wheel radial loads never reach motor gearboxes;
- the two side drivetrains receive torque at a compact central station;
- the 2.5:1 stage adds torque before the 6-wheel distribution train;
- the external form stays much closer to CRP150 proportions.

## Bearing/seal philosophy
Original MiniCam dimensions are reference evidence only and are not copied blindly.

PX-1 prototype decision:
- motor-side bevel shaft bearing class: compact 12 mm ID bearing equivalent to 61801-2RS where geometry supports it;
- side-output shaft bearing class: compact 10 mm ID bearing equivalent to 61800-2RS or stronger 6000-2RS after load calculation;
- physical water boundary remains our sealed side-cover system with FKM seals;
- common positive pressure remains +0.20…+0.30 bar initially.

## Side wheel train
The existing PX-1 side synchronization concept remains valid after the bevel input:
front z40 -> idler z60 -> middle z40 -> idler z60 -> rear z40.

The bevel stage drives the middle-wheel distribution gear or a coaxial input gear at that station. Exact compound-gear arrangement is the next CAD gate.

## Motor procurement correction
Do not order the previous 45 rpm motor specification as the final traction motor.

New purchase target for bench samples:
- JGB37-520 family;
- 24 V;
- approximately 100–120 rpm;
- metal gearbox;
- Hall A/B encoder preferred;
- nominal Ø6 mm D-shaft candidate;
- exact stall current and gearbox torque measured before release.

## Evidence-based design rule
Where uploaded MiniCam drawings provide a proven architecture (bevel transfer, compact bearings, O-ring service covers, manual lift with gas spring), PX-1 should use that architecture as a reference while retaining its own dimensions, electronics and purchasable parts.

## Next release gates
1. model Z16/Z40 bevel stage inside the 92 mm body;
2. place both 100–120 rpm JGB37 motor envelopes without collision;
3. build compound middle-wheel input gear;
4. recalculate torque and motor current;
5. update the traction BOM and obsolete the 45 rpm purchase note;
6. integrate the CRP150-style manual lift using the uploaded lift drawings as structural reference.
