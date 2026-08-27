# PX-1 Rev.EH — complete side-drive section stack

Status: detailed prototype stack; dimensions around purchased seals and gears remain pre-release.

## Source alignment
The uploaded CRP150 side-drive drawing shows:
- 1 side cover;
- 2 idle gears Z50;
- 3 wheel gears Z50;
- 1 long axle + 2 short axles;
- 6 bearings 61801-2RS (12x21x5);
- 3 bearings 61903-2RS (17x30x7);
- 3 axle flanges;
- 3 X-rings 18.72x2.62;
- 3 O-rings 32x1.5;
- 1 main O-ring 190x1.5;
- 4x4 keys and circlips.

PX-1 keeps this architecture closely, with its own dimensions and FKM sealing materials.

## Per wheel station
From inboard to outboard, prototype stack:
1. structural side-drive wall/bearing land;
2. 61801-2RS inner bearing;
3. Z50 wheel gear, m1, 8 mm face, keyed to Ø12 axle section;
4. second 61801-2RS support bearing;
5. transition shoulder from Ø12 to Ø17;
6. removable axle flange with static FKM O-ring;
7. 61903-2RS outer radial bearing on Ø17 journal;
8. dynamic FKM seal / quad-ring candidate outside the bearing;
9. labyrinth dirt shield integrated with wheel hub/flange nose;
10. removable Ø90 wheel;
11. axial retaining disk + M6 fastener.

The two 61801 bearings locate the gear shaft and keep gear mesh alignment independent of wheel side load. The 61903 nearest the wheel carries the largest wheel bending load.

## Short wheel axles
Front and rear axles are identical wherever possible.

Candidate functional dimensions:
- gear/bearing journal Ø12;
- key 4x4, working length >=12 mm candidate;
- outer bearing journal Ø17;
- dynamic seal journal selected after exact seal article;
- axial retention by shoulder/circlip;
- wheel torque keyed; retaining screw carries only axial load.

## Middle long axle
The middle axle is the driven input of the side train.

It retains the same three-bearing philosophy but extends inboard to the central transfer coupling:
- Ø12 inboard coupling section;
- 61801 support;
- keyed Z50 middle wheel gear;
- second 61801;
- Ø17 outer support / 61903;
- dynamic seal and wheel.

The bevel-transfer shaft from P0 does not have to be removed to service the side cover. The middle axle disengages from the transfer shaft through the positive dog/keyed coupling defined in Rev.EF.

## Idler gears
Two Z50 idlers at X=100 and X=200.

Preferred support:
- fixed hardened stainless or alloy-steel pin;
- replaceable bushing or compact bearing in each idler;
- pin retained from the structural side wall, not by the thin outer cover alone;
- cover may provide secondary location but not carry the full gear radial load.

The source drawing lists 10-12-4 bushings for the idler system; PX-1 keeps a replaceable plain-bush option because it tolerates contamination and is easy to service inside a dry pressurized bay.

## Side cover / local flanges
Main side cover seals the whole P1/P2 gear bay with a continuous static FKM O-ring.
Each of the three axle flanges has its own smaller FKM static seal.

This provides two levels of service:
- wheel seal/bearing service: remove only one axle flange;
- gear-train service: remove main side cover.

## Lubrication
The side bay is dry and pressurized, not oil-filled.
Use a thin controlled coating of compatible synthetic gear grease on the Z50 mesh.
Do not pack the cavity; excessive grease traps wear particles and can migrate to dynamic seals.

## Tolerances / datums
Gear center distances are controlled from one machined datum system in the structural side wall.

Initial manufacturing targets:
- wheel/idler center distance 50.00 mm nominal for equal m1 Z50 gears;
- center-position tolerance +/-0.03 mm prototype target;
- bearing bores H7 class;
- shaft bearing journals h6 class;
- shaft-seal running surface Ra <=0.4 um target;
- shoulder runout to shaft axis <=0.03 mm;
- side-cover screws must not be used as precision locators.

Backlash is verified by real gear contact, not by blindly reducing center distance.

## Service life test
Before machining release:
- 5000 wheel revolutions dry bench;
- 5000 wheel revolutions under representative radial load;
- 1000 reversing cycles;
- submerged powered rotation with P1/P2 pressurized;
- pressure decay measured before and after;
- inspect 61801/61903 temperature, grease condition, key fretting and seal-lip track.

## Release gates
No final axle length, seal groove or flange depth is released until actual 61801, 61903, selected dynamic seal, Z50 gears and wheel hub are physically measured.