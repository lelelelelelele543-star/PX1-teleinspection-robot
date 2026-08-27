# PX-1 Rev.DU — supported KHK bevel input

Status: preferred prototype architecture; exact motor/coupler hardware remains incoming-inspection dependent.

## Reference principle
Uploaded MiniCam motor-unit drawing DRW-002-386 does not simply hang the small bevel gears on unsupported motor shafts. It shows:
- 2 motors;
- 2 small bevel gears Z16;
- 2 separate bevel-gear axles;
- 2 bearings 61801-2RS.

PX-1 adopts that proven system principle: the motor transmits torque to a separately supported bevel-pinion shaft. The motor gearbox does not carry bevel-mesh radial/axial reaction loads.

## Selected stock bevel pair
Preferred prototype pair per side:
- KHK `SB1.5-1845H` pinion;
- KHK `SB1.5-4518H` large gear.

Key published dimensions:

### SB1.5-1845H
- module 1.5;
- z18;
- bore Ø8 H7;
- pitch Ø27 mm;
- outside Ø30.86 mm;
- face width 11 mm;
- mounting distance 45 mm;
- total length 21.97 mm;
- hardness 50–60 HRC;
- published Hardened-Plus surface durability about 2.16 N·m.

### SB1.5-4518H
- module 1.5;
- z45;
- bore Ø10 H7;
- pitch Ø67.5 mm;
- outside Ø68.18 mm;
- face width 11 mm;
- mounting distance 30 mm;
- total length 21.1 mm;
- hardness 50–60 HRC;
- published Hardened-Plus surface durability about 5.39 N·m.

Ratio = 45/18 = **2.5:1**.

## Pinion carrier
Each motor channel becomes:

`JGB37-555 Ø6 D-shaft -> clamp/flexible coupling 6-to-8 -> Ø8 supported shaft -> KHK z18 pinion`

Prototype pinion carrier:
- shaft Ø8 h6, 40Cr/17-4PH/appropriate hardened stainless candidate;
- 2x 698-2RS bearings, 8x19x6, as compact starting choice;
- bearing spacing maximized within holder;
- pinion located by shaft shoulder + nut/circlip;
- coupling is not a bearing and must not set pinion position;
- shim provision for bevel backlash/contact-pattern setup.

## Motor packaging correction
To keep the 92 mm CRP150-class body narrow, do not place the two Ø37 motors side-by-side over the same X range.

Preferred packaging:
- one motor approaches the bevel center from the FRONT;
- the other approaches from the REAR;
- motor/pinion axes are parallel to crawler X;
- bevel intersections are laterally separated only about ±5 mm from centerline;
- left and right large gears extend outward on their transverse shafts.

This lets the Ø37 motor bodies occupy different longitudinal zones while the two bevel pairs remain close to the crawler centerline.

Initial bevel intersection station:
- X ≈ 150 mm;
- Z ≈ 45 mm;
- Y ≈ +5 mm left pair;
- Y ≈ -5 mm right pair.

With 30 mm large-gear mounting distance, the large-gear back faces are approximately at |Y| ≈ 35 mm, leaving room for the compact side spur stage before the wheel-cover bosses.

## Output shaft concept
Middle-wheel/output shaft is a stepped shaft:
- Ø10 section for KHK large-bevel bore and central compact bearing;
- transition to Ø12 side-drive/wheel shaft after the large bevel;
- m1 z50 middle spur gear on Ø12 section;
- outer 61801 bearing and rotary seal in side-cover boss;
- wheel keyed on outer Ø12 section.

This avoids a separate dog coupling between the bevel output and middle wheel while retaining serviceable parts.

## Required checks
- exact KHK CAD/contact geometry before machining carrier datums;
- motor body/encoder length from purchased JGB37-555 samples;
- coupling OD and torsional compliance;
- pinion bearing axial reaction capacity;
- contact-pattern marking compound test;
- backlash 0.05–0.15 mm KHK pair range;
- 30 min loaded thermal/noise run.
