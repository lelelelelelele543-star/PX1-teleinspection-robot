# PX-1 Rev.CW — CRP150-style six-wheel master architecture

Status: new master architecture candidate; supersedes 4-wheel external-layout concepts.

## Design target
PX-1 now follows the successful Mini-Cam Proteus CRP150 architecture at system level:
- 6 wheels, 3 per side;
- low, narrow, elongated pressure body;
- manual central camera lift;
- rear tether connection;
- side drivetrain covers;
- all side drivetrain cavities sealed and pressurized;
- service with common hand tools;
- modern PX-1 electronics/video inside; no copying of proprietary part geometry.

## Reference envelope
CRP150 reference class is approximately 307 x 133 x 110 mm with Ø90 wheels. PX-1 should remain close to this external class unless real component packaging forces a change.

Current CAD target envelope for packaging:
- overall length: 305–320 mm;
- overall width: 130–140 mm;
- chassis height without lift: 105–115 mm;
- wheel OD: 90 mm baseline;
- three wheel centers per side, nominal longitudinal pitch about 105–110 mm.

These are packaging targets, not machining dimensions.

## Six-wheel arrangement
Provisional wheel-center X coordinates in a 307 mm reference envelope:
- front: X = 45 mm;
- middle: X = 153.5 mm;
- rear: X = 262 mm.

Wheel-center height: Z = 45 mm for Ø90 wheels.

Exact centers will be adjusted after body, lift and rear connector packaging.

## Pressure-body + side gear bays
The previous idea of exposed wet gears is cancelled.

Each side becomes a sealed pressurized gear bay:
- structural side wall is part of the crawler body;
- a rigid removable aluminum side cover closes the full gear bay;
- continuous O-ring in a machined groove around the cover perimeter;
- cover retained by perimeter screws into metal threads/inserts;
- no drain holes;
- gear bay communicates with the central dry body through a dedicated internal pressure passage;
- whole crawler is filled from one pressure port and monitored by one pressure sensor.

The side cover is NOT a removable cassette. Gears, shafts and bearings remain mounted to the crawler structure.

## Wheel shaft modules
Three shaft exits per side. Each wheel shaft has:
- replaceable outer rotary seal;
- protected seal running surface;
- two-bearing support where packaging allows, otherwise one bearing plus inboard support;
- axial retention by shoulder + nut/circlip, not adhesive;
- wheel removable independently of the side cover where practical.

The pressurized gear bay sits behind the shaft seals, so positive internal pressure assists leak detection but does not replace the shaft seals.

## Drive topology
One 24 V traction motor per side remains preferred.

Preferred architecture:
- motor inside the central dry body or inner part of the pressurized side bay;
- motor pinion drives one supported gear stage;
- three wheel shafts are synchronized by spur gears;
- all six wheels powered;
- no belt;
- no chain;
- no separate gearbox cassette.

Initial gear family remains module 1.0 / 20° with 8–10 mm face width, but tooth counts will be redesigned around the new 3-wheel pitch.

## Pressure
Prototype operating overpressure target:
- normal: +0.20…+0.30 bar gauge;
- pre-work leak test required;
- alarm on pressure loss;
- final working pressure and proof pressure only after cover/shaft qualification.

Do not rely on pressure alone as waterproofing. Every cover, connector and rotating shaft retains a physical seal.

## Camera/lift
CRP150-style central manual lift becomes the external-layout reference.
PX-1 camera remains our own modern two-axis head:
- TILT: approximately -105…+105° current target;
- ROLL: continuous 360°;
- digital video architecture;
- quick-removable camera head;
- lift manually indexed for pipe diameter.

The lift must fold low enough to preserve DN150 operation.

## Tail
Rear tether connection remains centered/near-centered and mechanically strain-relieved.
The tether tensile member must terminate mechanically in the tail structure; electrical contacts do not carry crawler pull load.

## Service rules
- side cover removed with ordinary hex/torx tools;
- O-ring reusable for inspection only if undamaged; normal service kit carries spares;
- gears individually replaceable;
- wheel shaft seal cartridge serviceable without disturbing electronics where practical;
- no glued structural covers;
- no proprietary one-use retaining hardware.

## Superseded concepts
Rev.CT four-wheel architecture and Rev.CU four-wheel side-cover layout are obsolete as complete-vehicle layouts. Their sealing philosophy (O-ring covers + positive pressure) is retained and adapted to six wheels.

## Next gates
1. build 6-wheel master CAD envelope;
2. solve exact three-wheel gear train geometry;
3. define side-cover O-ring land and fastener pitch;
4. define 3x wheel shaft seal stack per side;
5. place two motors and verify dry-volume packaging;
6. place CRP150-style manual lift and run DN150 clearance;
7. only then update manufacturing drawings.