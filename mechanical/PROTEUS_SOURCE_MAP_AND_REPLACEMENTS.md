# Proteus source map -> PX-1 serviceable replacements

Status: active working map.

## 1. Crawler body / bevel handoff
Source: `DRW-002-375 / ASS-002-375 Housing - CRAWLER`

Verified source architecture:
- FAL-002-058 Crawler Housing
- 2x GEA-002-530 large bevel Z40
- 2x SEA-002-702 shaft seal 18-30-7
- 2x FSS-002-066 bevel axles
- 2x BEA-002-703 61800 2RS (10-19-5)
- lift pivots/holding plates integrated with main housing
- weight plate integrated low in body

PX-1 action:
- preserve the two-sided Z40 bevel handoff and low central weight concept;
- keep standard 61800-class bearings if fit/load tests pass;
- use common stainless or hardened steel axles;
- use catalog FKM/NBR seals from a currently available manufacturer;
- machine own housing from aluminum; no proprietary PCB-dependent geometry.

## 2. Side drive
Source: `DRW-002-374`

Verified source architecture per side:
- 1x FAL-002-062 side cover
- 2x GEA-002-528 idle Z50 B4
- 3x GEA-002-529 axle Z50 B4
- 1x long axle + 2x short axles
- 1x 61801 2RS (12-21-5)
- 3x 61903 2RS (17-30-7)
- 3x axle sealing flanges
- 3x X-ring 18.72x2.62
- 3x static O-ring 32x1.5
- 1x side-cover O-ring 190x1.5
- keys 4x4

Functional topology:
`wheel Z50 - idle Z50 - wheel Z50 - idle/input Z50 - wheel Z50`

All three wheel gears rotate in the same direction.

PX-1 action:
- preserve five equal Z50 positions and three wheel positions;
- preserve removable side cover and three serviceable axle-flange seals;
- do not introduce extra gear stages unless motor fit forces it;
- use current catalog 61801/61903 equivalents and current catalog X-ring/O-rings;
- wheel, shaft and flange dimensions may change only as much as required for available bearings/seals and machining.

## 3. Motor unit
Source: `DRW-002-386 / ASS-002-386 Motor Unit - Crawler`

Verified source architecture:
- one common motor holder
- 2x motor+gear units
- 2x small bevel Z16
- 2x bevel pinion axles
- 2x 61801 2RS (12-21-5)
- narrow stacked/parallel two-motor arrangement

PX-1 action:
- preserve two motors total and Z16 -> Z40 architecture;
- find currently purchasable 24 V brushed planetary/gearmotor with equivalent envelope/output performance;
- use a simple mechanical adapter if motor bolt pattern differs;
- do not redesign the crawler around a large proprietary motor.

## 4. Manual lift
Source: `DRW-002-744 Crawler Lift Parts`

Verified source architecture:
- 2x side levers
- lever arm assembly
- 150 N gas spring
- M8 clamping lever
- Belleville spring stack DIN2093 20x10.2x1.1
- simple pins/circlips/washers
- O-rings only where shafts cross sealed boundaries

PX-1 action:
- preserve this manual lift principle almost directly;
- no powered lift in baseline;
- retain one-hand adjustment target;
- maintain open forward area around folded camera for vision and drainage;
- substitute standard gas spring/clamping lever/pins where source parts are unavailable.

## 5. CAM026-like camera
Sources:
- `ASS-001-801 CAMERA HOUSING ASSY`
- `ASS-001-802 SIDE FRAME HOUSING ASSY`
- `ASS-001-803 BEARING HOUSING ASSY - CAM026`
- `ASS-001-917 PAN MOTOR ASSY`
- `ASS-001-919 ROTATE AXLE ASSY`
- `ASS-001-998 ROTATE SPUR GEAR ASSY`

Verified source architecture:
- camera barrel carried on two side axles;
- PAN axis uses worm/worm-gear style drive and bearings;
- separate rotate axis around the camera/yoke assembly;
- front light ring around lens;
- multiple static O-rings separating service covers;
- small DC gearmotors and small control PCBs.

PX-1 action:
- preserve mechanical arrangement and visual form;
- replace PAL DSP proprietary module with accessible compact CVBS/AHD camera module selected for lens/FOV and dimensions;
- replace proprietary focus system with fixed-focus lens for baseline unless focus is demonstrably required;
- replace proprietary pan/rotate control PCBs with simple H-bridge modules and limit/home sensing;
- keep continuous rotation only if the selected slip-ring solution proves clean video operation; otherwise first prototype may use bounded rotation while retaining the same external camera shape.

## 6. RMP300 reel
Source: `ASS-004-097 CABLE REEL ASSY (RMP300)` and subassemblies.

Verified source architecture:
- open two-side-plate frame
- manual central drum
- hand crank
- main shaft with slip ring
- chain-driven mechanism on one side
- mechanical brake
- level-wind spindle
- measure unit with rollers and measuring wheel

Specific verified source items:
- reel chain Z30/Z16 (`ASS-004-096`)
- 12-pole slip ring A6023-12 on source reel left side (`ASS-004-094`)
- 61804 and 6203/16006/61904-class bearings used in reel side assemblies
- 272 mm layering spindle in RMP300 (`ASS-002-710`)
- 160 mm crank handle (`ASS-002-712`)
- meter counter with 618/8 bearings (`ASS-004-092`)

PX-1 action:
- preserve manual reel, brake, level wind, meter wheel and open frame;
- substitute a commonly available 12+ circuit slip ring rated for selected tether voltage/current;
- replace proprietary PCB counter with encoder/Hall sensor + console distance calculation;
- use standard chain/sprockets and bearings;
- retain easy one-person transport as a primary requirement.

## 7. Tether connector
Sources:
- `ASS-002-090 Connector crawler`
- `ASS-003-215 PROTEUS CABLE END SOCKET`
- `ASS-002-364 Connector Cable`

Verified source architecture:
- six electrical contacts;
- multiple O-ring sealed connector pieces;
- spring / nut / cable housing and mechanical cable-gland pieces;
- separate cable-side and crawler-side serviceable assemblies.

PX-1 action:
- preserve 6-contact functional architecture and field-retermination principle;
- use a modern obtainable waterproof connector only if its contact current, sealing and field service are adequate;
- keep cable tensile load off the contacts.

## Baseline replacement philosophy
Part categories ranked by preference:
1. standard metric fasteners, circlips, keys, bearings and O-rings;
2. catalog industrial seals and shafts;
3. common 24 V gearmotors;
4. ready-made H-bridge / RS-485 / DC-DC modules;
5. machined aluminum/stainless parts from our own drawings;
6. custom PCB only if a later production revision proves it is genuinely simpler/cheaper.

The closer a source Proteus mechanism is to standard mechanical parts, the less PX-1 should change it.