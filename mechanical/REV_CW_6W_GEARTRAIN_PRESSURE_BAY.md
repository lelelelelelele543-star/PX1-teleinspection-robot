# PX-1 Rev.CW — 6WD gear train inside pressurized side bays

Status: geometry candidate for master packaging.

## Why this layout
A CRP150-style six-wheel crawler needs all three wheels on each side synchronized while keeping the robot narrow and mechanically simple.

The selected starting layout uses one large idler between each adjacent pair of wheel gears:

front z40 — idler z60 — middle z40 — idler z60 — rear z40

All gears: module 1.0, 20° pressure angle, initial face width 8 mm.

## Geometry
For m=1:
- z40 pitch diameter = 40 mm;
- z60 pitch diameter = 60 mm;
- z40↔z60 center distance = (40+60)/2 = 50 mm.

Therefore wheel-to-wheel pitch through one idler is exactly 100 mm.

This allows provisional wheel centers:
- X50 front;
- X150 middle;
- X250 rear.

With Ø90 wheels the wheel footprint becomes about 290 mm long, leaving room inside a roughly 307 mm CRP150-class overall envelope for front structure and rear tether interface.

## Rotation direction
Each wheel pair is connected through one idler = two gear meshes from wheel to wheel, so front/middle/rear wheel gears rotate in the same direction.

## Motor drive
One longitudinal JGB37-520-class motor per side remains the preferred inexpensive prototype architecture.

The motor does NOT support a wheel shaft. It drives the middle-wheel shaft through a separate supported reduction/input stage. The middle shaft then distributes torque forward and rearward through the z60 idlers.

Input stage ratio is HOLD. Do not automatically retain old z18/z30 until motor speed and torque are bench-tested.

## Pressurized side bay
All z40/z60 gears sit behind a rigid aluminum side cover.

Boundary stack:
outside sewer environment -> wheel -> rotary shaft seal -> pressurized side gear bay -> structural inner side wall / central pressure body.

The gear bay:
- shares crawler internal pressure through an internal passage;
- is sealed by continuous O-ring under the side cover;
- has no drain hole;
- has no separate removable gearbox cassette;
- is accessible by removing only the side cover and wheel hardware.

## Cover starting rules
Before FEA/pressure test:
- aluminum cover candidate thickness 4–5 mm;
- continuous O-ring groove around gear perimeter;
- metal-thread fasteners around perimeter, provisional spacing 35–45 mm;
- local bosses around wheel-shaft seal cartridges;
- at least 2 mm static clearance from gear OD to cover;
- cover should locate on a machined pilot/step so screws do not define gear-bay alignment.

## Contamination control
Unlike the previous exposed-gear concept, sewer water and grit should not enter this bay during normal use.
Positive pressure is secondary protection only. The shaft seals and cover O-ring remain the primary water boundary.

## Failure/service philosophy
A leaking shaft seal should be replaceable as a cartridge/service stack without replacing the body.
A damaged gear should be removable individually.
The complete side bay must be inspectable without disturbing camera, main electronics or rear tether connector.

## Required next checks
- exact shaft diameter and seal size;
- gear tooth root strength at measured motor stall/current limit;
- idler bearing size;
- motor-input gear location;
- cover screw pattern around three wheel hubs;
- cover deflection at test pressure;
- DN150 external clearance with 133–140 mm overall crawler width.