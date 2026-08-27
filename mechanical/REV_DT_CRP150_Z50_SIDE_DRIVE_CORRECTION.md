# PX-1 Rev.DT — CRP150 side-drive correction: five equal Z50 gears

Status: architecture correction based directly on uploaded MiniCam drawing DRW-002-374. Supersedes the earlier PX-1 z40/z60/z40/z60/z40 side-train assumption.

## Reference finding
DRW-002-374 lists:
- 2x `Idle Gear Z50 B4`;
- 3x `Gear Axle Z50 B4`.

The assembly view shows the five equal gears in one row. Therefore the proven CRP150-style topology is:

`wheel Z50 -> idler Z50 -> wheel Z50 -> idler Z50 -> wheel Z50`

All three wheel gears rotate in the same direction because there are two meshes between adjacent wheel shafts.

## PX-1 geometry
Adopt for the prototype:
- module m = 1.0;
- pressure angle = 20 deg;
- all five gears z = 50;
- pitch diameter = 50 mm;
- outside diameter = 52 mm;
- adjacent gear center distance = 50.0 mm;
- wheel-to-wheel pitch = 100.0 mm.

Master wheel centers remain X = 50 / 150 / 250 mm and idlers X = 100 / 200 mm.

## Procurement/manufacturing candidate
Preferred starting blank: KHK `SSG1-50` ground, induction-hardened S45C gear:
- z50, m1;
- pitch Ø50;
- OD Ø52;
- face width 8 mm;
- stock bore Ø12 H7;
- stock total length 18 mm including hub;
- published surface durability around 10.8 N·m.

PX-1 does not need the full stock hub. The hub may be turned down/removed outside the hardened tooth zone and a shaft keyway broached, subject to KHK secondary-operation rules. Final compact target is essentially the 8 mm tooth-face disk plus only the hub/retention material actually required.

## Shaft correction
Because SSG1-50 is already Ø12 H7 and the uploaded CRP side-drive also uses 61801-2RS bearings (12x21x5), the preferred PX-1 wheel/idler shaft family changes from Ø10 to **Ø12 mm** for the side drive.

Benefits:
- stronger wheel shaft;
- compact 61801 bearing OD only 21 mm;
- direct stock-gear bore match;
- closer to the proven CRP150 packaging philosophy.

Wheel-retaining M6 fastener remains axial retention only; wheel torque is carried by a key/spline, not bolt friction.

## Side-bay axial target
Target gear tooth face position per side: approximately 8 mm axial width. The removable side cover remains a cover, not a cassette. Bearings/seals are carried by structural bosses and the cover.

## Backlash
Initial assembly target for equal m1 gears: 0.08–0.18 mm normal backlash class. Do not design zero-backlash meshing for the dirty/thermally cycling crawler environment.

## Release gates
1. verify exact purchased SSG1-50 blank dimensions;
2. confirm hub removal/broach process without damaging hardened teeth;
3. change six wheel shafts to Ø12 and reselect seals/bearings;
4. hand-rotate complete 5-gear train with cover torqued;
5. contact-pattern and noise check;
6. 5000-revolution loaded endurance;
7. wet DN150 skid-steer current test.
