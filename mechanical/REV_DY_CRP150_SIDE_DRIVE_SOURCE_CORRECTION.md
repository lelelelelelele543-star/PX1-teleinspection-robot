# PX-1 Rev.DY — CRP150 side-drive source correction

Status: architecture correction grounded in uploaded MiniCam drawings DRW-002-374, DRW-002-375 and ASS-002-386. This revision supersedes the earlier assumption that the CRP150 external side cover itself has a wavy outer outline.

## What the uploaded CRP150 drawings actually show
DRW-002-374 shows a rectangular removable side cover with three separate circular axle flanges. Inside that cover the transmission uses:
- 2x Idle Gear Z50 B4;
- 3x Gear Axle Z50 B4;
- 1x long wheel axle and 2x short wheel axles;
- 6x 61801-2RS bearings (12x21x5);
- 3x 61903-2RS bearings (17x30x7);
- 3x axle flanges;
- 3x X-rings 18.72x2.62;
- 3x O-rings 32x1.5 at axle-flange interfaces;
- 1x large perimeter O-ring 190x1.5;
- M3 perimeter fasteners.

Therefore the visually important CRP150 feature is:
**rectangular side plate + three round wheel/shaft flanges + internal five-gear train**.
The internal free space around the five Z50 gears is scalloped by the gear envelopes, but the visible outer cover remains substantially rectangular.

ASS-002-386 separately shows two motors driving two small bevel gears Z16, each small bevel gear being supported through a dedicated axle and a 61801-2RS bearing.

DRW-002-375 shows the two large bevel gears Z40 in the main crawler housing, each on its own bevel-output axle with a 61800-2RS bearing and an 18x30x7 shaft seal.

## PX-1 adaptation
PX-1 adopts the same system-level architecture without copying proprietary dimensions:
- 3 wheel shafts per side;
- 2 idler gears between them;
- all five side gears use the same tooth count so all three wheels rotate at 1:1 speed;
- side cover is externally rectangular;
- 3 separate removable axle/seal flanges are visible on each side;
- one continuous side-cover O-ring;
- central bevel stage remains isolated from the side-drive bay by its own shaft seal;
- positive pressure is retained as secondary ingress protection.

## PX-1 gear decision
The side train is corrected to **m1.0, Z50, 20 degrees**:
`wheel Z50 -> idler Z50 -> wheel Z50 -> idler Z50 -> wheel Z50`.

With m=1 and Z50/Z50, each mesh center distance is 50 mm, giving the frozen 100 mm wheel pitch through two meshes per axle interval.

## Cover correction
Do NOT release a wavy external side cover.

New visible cover target:
- rectangular/soft-corner plate similar in overall proportion to DRW-002-374;
- three circular axle-flange bosses;
- countersunk/low-profile perimeter fasteners;
- the internal pressure cavity may follow a racetrack/scalloped shape around the five gears;
- no external drain holes because P1/P2 are dry pressurized zones.

## Bearing philosophy
The source drawing proves that MiniCam separates idler support from driven wheel-axle support. PX-1 keeps that concept but uses its own service stack.

Current PX-1 baseline remains:
- driven wheel shafts: nominal Ø12 where practical;
- idlers: fixed pins with replaceable bearings;
- separate flange at each wheel shaft carrying the outer support/seal;
- no motor radial load transmitted through a wheel axle.

Exact bearing count per idler is our own design and is not copied from MiniCam.

## Pressure/seal philosophy
The MiniCam drawing supports a layered approach: perimeter O-ring + local axle-flange O-rings + local rotating seals. PX-1 keeps the same reliability logic while using FKM where practical and three isolated pressure zones P0/P1/P2.

## Release impact
The following earlier statements are obsolete:
- wavy external side-cover outline as a required CRP150 feature;
- z40/z60 side train;
- exposed side gears;
- single common pressure cavity.

Next work is to integrate exact purchasable Z50 and bevel components into the corrected rectangular-cover geometry.