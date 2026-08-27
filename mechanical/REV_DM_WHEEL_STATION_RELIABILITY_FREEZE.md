# PX-1 Rev.DM — wheel-station reliability freeze

Status: prototype architecture freeze for the six external wheel stations.

## Decision
Keep the wheel station compact. Do **not** install two full 7 mm radial shaft seals in tandem as the baseline because the added axial stack makes the DN150 wheel/cover packaging worse and increases seal drag.

Baseline per wheel:
1. keyed Ø10 wheel shaft;
2. removable wheel + labyrinth dirt shield;
3. one high-quality **FKM TC double-lip 10x22x7** rotary shaft seal;
4. 6000-2RS outer bearing 10x26x8;
5. z40 m1 wheel gear between bearings;
6. 6000-2RS inner bearing;
7. structural inner wall;
8. isolated pressurized side gear bay behind the seal.

The reliability redundancy comes from the complete system, not from stacking seals blindly:
- external labyrinth protects the lip from grit;
- double-lip TC seal provides main water + dust lips;
- side bay is positively pressurized;
- left and right gear bays are isolated from the electronics body;
- pressure is monitored per zone;
- seal is replaceable with common tools.

## Optional severe-service upgrade
Preserve enough local boss depth so a later thin secondary exclusion seal/V-ring or wear sleeve can be added after mud testing without redesigning the whole body.

A second full 10x22x7 radial seal becomes an option only if endurance testing proves the single TC + labyrinth insufficient.

## Shaft
Baseline:
- nominal diameter: 10 mm;
- bearing journals: Ø10 h6;
- seal running surface: Ra <=0.4 µm target;
- preferred shaft: 40X13 / AISI 420-class stainless with finished seal journal;
- no keyway, flat, groove or thread under the seal lip;
- seal lead-in: smooth chamfer, no sharp edge.

## Simple strength sanity check
For a deliberately conservative preliminary wheel radial load of 200 N acting 25 mm outboard of the nearest support:
- bending moment = 5 N·m;
- Ø10 solid-shaft elastic bending stress ≈51 MPa.

This is acceptable as a packaging sanity check for the selected shaft class, but it is **not** a fatigue release calculation. Real obstacle impact, keyway stress concentration and wheel-side bending still require prototype validation.

## Bearing arrangement
The z40 wheel gear remains between two bearings. This is important because:
- gear radial force is reacted locally;
- wheel bending does not load the traction motor gearbox;
- cover removal does not require removing the electronics tray.

Outer bearing seat is in the accurately located side-cover/boss assembly; inner bearing seat is in the fixed structural wall.

## Cover alignment
Because the outer wheel bearing sits in the removable cover, the cover is located by:
- machined pilot/step;
- two dowel pins;
- perimeter bolts used only for clamping.

Target coaxiality after service remains <=0.03 mm between inner/outer bearing axes and seal bore until physical manufacturing capability proves a different practical tolerance.

## Wheel retention
Baseline changes to M6 axial retention to stay closer to the simple CRP150 service philosophy:
- M6 stainless retaining screw;
- locking/Schnorr washer;
- retaining disk/washer;
- small O-ring under the disk where useful for dirt exclusion.

Drive torque passes through the key, not bolt friction.

## Failure behavior
If a wheel seal fails:
- affected side bay pressure decays first;
- electronics body remains isolated by the P0/P1/P2 pressure-zone architecture;
- operator receives LEFT/RIGHT DRIVE pressure alarm;
- crawler should be recovered and seal serviced rather than continuously supplied with air.

## Qualification gates
- shaft runout check;
- 2 h wet rotating test;
- mud/sand slurry test;
- pressure decay during wheel rotation;
- 500 direction reversals;
- obstacle-impact test;
- 20 wheel removal/refit cycles;
- post-test inspection of seal track and bearing play.
