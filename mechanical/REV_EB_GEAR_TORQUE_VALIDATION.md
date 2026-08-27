# PX-1 Rev.EB — catalog torque validation for selected gears

Status: catalog-level validation, not endurance qualification.

## Bevel pair
Current candidate:
- KHK SB1.5-1845H pinion, m1.5, z18;
- KHK SB1.5-4518H gear, m1.5, z45;
- ratio 2.5:1.

KHK 2025 bevel-gear catalog publishes for the H surface-durability condition approximately:
- z18 pinion: 2.16 N·m surface-durability-H allowable torque;
- z45 gear: 5.39 N·m surface-durability-H allowable torque.

PX-1 provisional electronic/mechanical input ceiling remains 1.50 N·m at the pinion.

With 0.90 mechanical efficiency, output estimate:
`1.50 x 2.5 x 0.90 = 3.375 N·m`

Catalog-level margins:
- pinion surface-H margin ~2.16 / 1.50 = 1.44;
- large gear surface-H margin ~5.39 / 3.375 = 1.60.

This is acceptable for prototype sizing but is NOT generous enough to ignore shock loads. Therefore the 1.50 N·m pinion ceiling remains a hard prototype limit until real current/torque tests.

Do not use the non-H surface-durability column for this candidate: the non-hardened values are much lower and would not support our present torque target.

Source used for catalog verification:
https://khkgears.net/pdf/2025/bevel-gears.pdf

## Side Z50 spur gears
Candidate KHK SSG1-50 published data:
- module 1;
- 50 teeth;
- bore 12 mm;
- pitch diameter 50 mm;
- outside diameter 52 mm;
- face width 8 mm;
- surface-durability allowable torque ~10.8 N·m;
- bending-strength allowable torque ~13 N·m;
- published backlash range about 0.08–0.16 mm.

At ~3.375 N·m side input, simple catalog torque margin is >3x. The spur train is therefore not the first catalog-strength bottleneck; the bevel pinion, shock loading, alignment, bearing supports and traction current are more critical.

Source used for catalog verification:
https://catalog.khkgears.us/item/spur-gears/ground-spur-gears-ssg/ssg1-50

## Engineering decision
- KEEP SB1.5-1845H / 4518H as prototype pair.
- KEEP electronic torque ceiling at 1.50 N·m pinion equivalent.
- KEEP SSG1-50-class side gears.
- add jam detection fast enough that a blocked wheel does not dwell at peak motor torque.
- if actual JGB37-555 stall torque/current can exceed this ceiling faster than control can react, use a stronger/larger bevel pair or a mechanical torque limiter rather than relying on firmware alone.

## Qualification gates
1. verify H-suffix on purchased bevel gears;
2. inspect tooth hardness/marking and supplier traceability;
3. record actual motor current vs shaft torque on bench;
4. set driver current limit from measured torque curve;
5. 5000 wheel-revolution loaded endurance;
6. repeated jam/reverse shock test;
7. inspect contact pattern/pitting before production release.
