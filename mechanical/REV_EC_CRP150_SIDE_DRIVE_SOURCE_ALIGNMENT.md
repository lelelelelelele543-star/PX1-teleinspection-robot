# PX-1 Rev.EC — CRP150 side-drive source alignment correction

Status: architecture correction based directly on uploaded MiniCam drawings DRW-002-374, DRW-002-375 and DRW-002-386. Supersedes the lightweight outer-flange bearing stack in Rev.DZ where it conflicts with this revision.

## What the uploaded drawings actually establish
DRW-002-374 side drive uses, per side:
- 2x idle gear Z50;
- 3x axle gear Z50;
- 1x long axle + 2x short axles;
- 6x 61801-2RS bearings (12x21x5);
- 3x 61903-2RS bearings (17x30x7);
- 3x axle flanges;
- 3x X-ring 18.72x2.62;
- 3x 32x1.5 O-rings at the axle-flange interfaces;
- one large 190x1.5 O-ring for the side cover;
- 4x4 keys.

DRW-002-375 separately shows the crawler body bevel-output system with:
- 2x big bevel gears Z40;
- 2x shaft seals 18x30x7;
- 2x bevel axles;
- 2x 61800-2RS bearings (10x19x5).

DRW-002-386 shows the motor unit as one paired holder containing two motors, two small Z16 bevel gears, two separate bevel/pinion axles and two 61801-2RS bearings.

## PX-1 correction
The previous PX-1 concept with only one small 61801 outer bearing per wheel was too light compared with the proven CRP150 architecture.

New preferred wheel-station architecture:
- inner gear-support journals: Ø12 class, 2x 61801-2RS per wheel axle where packaging permits;
- outer wheel-load bearing: 61903-2RS, 17x30x7, one per wheel;
- shaft steps from Ø12 gear/bearing region to Ø17 outer wheel-load journal;
- replaceable axle flange carries the Ø30 bearing seat and static flange seal;
- dynamic water exclusion uses a quad/X-ring architecture or an equivalent modern rotary seal validated on the Ø17/Ø18 class journal;
- FKM preferred for PX-1 final sealing material unless compatibility testing selects otherwise;
- positive torque transfer remains 4x4 keyed.

This preserves the system-level architecture of CRP150 without copying MiniCam part geometry.

## Why Ø17 outer support is preferable
- wheel radial load is carried by a larger bearing immediately at the wheel/flange;
- inner 61801 bearings primarily locate the gear/axle inside the side bay;
- bending load at the narrow Ø12 gear region is reduced;
- the service flange can be removed with the outer bearing/seal as a replaceable assembly;
- the arrangement matches the proven three-bearing-per-axle philosophy indicated by the source parts count: 6 inner 61801 + 3 outer 61903 for 3 wheel axles.

## Revised per-wheel stack
From inner side-bay structure toward sewer:
1. inner 61801-2RS;
2. Z50 axle gear on keyed Ø12 section;
3. second 61801-2RS;
4. shaft shoulder/transition Ø12 -> Ø17;
5. 61903-2RS in removable axle flange;
6. FKM quad/X-ring or validated rotary seal on uninterrupted outer journal;
7. dirt labyrinth;
8. wheel hub on positive-drive section;
9. retaining disk + M6 screw.

The exact order of the outer 61903 versus dynamic seal is a CAD/service gate; the seal must protect the pressure cavity and the bearing must be protected from sewer grit.

## Flange static seal
Prefer the source-proven class:
- molded O-ring around Ø32 nominal loop, 1.5 mm section class;
- one static seal per axle flange;
- flange pilot locates, screws clamp.

PX-1 will use FKM rather than automatically copying source NBR/X-ring material.

## Side cover
The source confirms one large side-cover O-ring plus multiple screws. PX-1 retains:
- one rectangular rigid side cover;
- one continuous main FKM O-ring;
- three independent wheel-flange seals;
- isolated +0.20…+0.30 bar P1/P2 zones.

## Motor-unit note
DRW-002-386 proves that the two motors are carried together in one compact paired holder and each drives its own bevel pinion through a separately supported pinion axle.

The drawing itself does not provide a crawler XYZ datum on the sheet, so PX-1 must not infer installed 'vertical' versus 'transverse' orientation solely from the page orientation. Rev.DX axes Y=±19 are therefore only a packaging candidate, not source-frozen geometry.

PX-1 will now use a paired removable motor holder as a subsystem. Its final rotation/orientation inside P0 is chosen from actual solid interference with the pressure walls, lift base and bevel outputs.

## Release gates
1. model Ø12->Ø17 stepped wheel shaft;
2. model 2x61801 + 61903 per station;
3. choose modern FKM X/quad-ring or lip-seal equivalent and test rotary drag/leakage;
4. model paired motor holder, not two unrelated motor mounts;
5. align paired holder with the two bevel-output shafts in full body CAD;
6. pressure-test one complete side drive before manufacturing release.
