# PX-1 Rev.GL — integrated six-wheel drivetrain and DN150 closure

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## Major correction found by full integration
Rev.GK passed as an isolated X200 mechanism, but the full six-wheel sweep exposed a real conflict: the proposed external Ø26 X200 boss / outward 6701 support intersected the rotating Ø90 wheel envelopes at X150 and X250.

That concept is rejected. No external X200 boss or bearing remains between the wheels.

## Rev.GL X200 architecture
The X200 side shaft now uses two 61800-class 10x19x5 bearings completely inside P0, with the Z40 bevel between the supports:
- inner support center Y=11.5 mm;
- Z40 bevel force region around Y=22.5 mm;
- outer/inboard support center Y=32.0 mm;
- 18x30x7 seal immediately outboard of the second support;
- slinger/spacer;
- side-input m1 Z50 in the dry side bay, Y42.0..45.5;
- recessed axial M5 retention inside the Z50 center region;
- side-cover inner face Y46.0 remains solid and smooth at X200.

The Z50 torque path remains keyed; the recessed screw is axial retention only.

This arrangement removes all fixed hardware from the 10 mm geometric gap between adjacent Ø90 wheel sweeps.

## Integrated side trains
Each side is now represented as five equal m1 Z50 positions:
- X50 wheel;
- X100 idler;
- X150 wheel;
- X200 driven input;
- X250 wheel.

Pitch spacing is 50 mm throughout. The X200 gear has 3.3 mm axial face overlap with the neighboring 3.75 mm gears.

With four equal-gear meshes across the train, wheel gears X50, X150 and X250 rotate in the same direction. The X200 input gear rotates opposite to all three wheel gears.

## Rev.GF wheel stations retained
All six external stations retain the Rev.GF packaging:
- Ø90-class tapered/dished wheel;
- 6701 12x18x4 inner support;
- Z50 face 3.75 mm;
- 61801 + 61903 outboard support architecture;
- X-ring 18.72x2.62 on Ø19 land;
- Ø17 keyed wheel seat;
- recessed M8 axial wheel retention;
- no side-cover gear recess.

The exact GF wheel profile stations were rebuilt into the integrated solid. Minimum analytical ideal-DN150 profile margin is about 0.07 mm at the near-contact elastic-tread region. This is wheel contact geometry, not debris allowance; physical DN150 qualification remains mandatory.

## X200 reaction screen after support relocation
At the retained provisional 1.0 N.m motor-output ceiling:
- bevel tangential force: about 100 N;
- bevel axial force: about 33.8 N;
- side Z50 tangential force: about 85 N;
- conservative support resultants: about 98 N and 196 N nominal;
- 2x shock screen: about 196 N and 391 N.

Using the current 61800 static screening rating of 840 N, the 2x static safety factors are about 4.28 and 2.15.

The modest 33.8 N bevel axial component is retained as a release item for final bearing shoulder/endplay and life verification.

## Full-crawler CAD validation
The Rev.GL CadQuery integrated model contains:
- P0 body + narrow rear motor pressure extension;
- P1/P2 dry side bays;
- both side covers and seal-path reservations;
- six Rev.GF wheel profiles, flanges, shafts and retainers;
- five Z50 positions per side;
- detailed two-sided X200 handoff;
- two Ø32 x 92 motor envelopes and supported Z16 shafts;
- LOW manual lift and digital camera envelope;
- rear bulkhead and tether bend-support envelope.

PASS results:
- zero unintended motor/body, motor/camera and bevel/motor intersections;
- zero wheel tire/cover and wheel tire/flange intersections on all six stations;
- zero wheel-gear/body and wheel-gear/cover intersections;
- body, covers, lift/camera fixed hardware, rear bulkhead and tether boot remain inside ideal DN150;
- all six wheel outer profiles remain inside/tangent to ideal DN150;
- side-cover O-ring reservation does not intersect wheel pilots or cover screw holes;
- external X200 cover surface is smooth;
- side-cover lower-corner ideal-DN150 clearance remains ~6.29 mm;
- motor rear-wall clearance 3.0 mm;
- motor-to-motor gap 1.0 mm;
- motor-to-P0 side-wall clearance 1.5 mm.

## Active overall geometry
- main full-width body length: 307 mm;
- rear pressure extension overall length: 340 mm;
- main body width: 92 mm before covers;
- side-cover outer planes: Y +/-51 mm;
- wheel centers: X50 / X150 / X250, Z45;
- nominal wheel pitch: 100 mm;
- pipe-axis solution for current Ø90 profile: Z ~52.048 mm.

## Release gates still HOLD
1. exact Ø32 motor samples and measured current/torque/speed curves;
2. manufacture/rating/contact validation of the compact m1.25 Z16/Z40 bevel pair;
3. exact purchased 61800/61801/61903/6701 bearings and final fits;
4. exact 18x30x7 seal and wheel X-ring articles/glands;
5. final axial endplay/thrust arrangement on the X200 shaft;
6. full FreeCAD/CalculiX pressure-body and rear-extension FEA;
7. physical wheel-station mock-up, pressure/immersion tests and DN150 sweep;
8. real tether-tail pull and bend tests.

## Next autonomous block
- convert the stable Rev.GL pressure body / rear extension into an FEA-ready solid;
- apply P0/P1/P2 pressure cases and rear tether proof-load cases;
- inspect stress around X200 cartridge seats, top opening, side-bay membranes and rear-extension transition;
- thicken/fillet only where FEA requires it, then rerun the complete DN150 validator.
