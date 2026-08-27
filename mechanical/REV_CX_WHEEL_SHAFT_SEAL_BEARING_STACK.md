# PX-1 Rev.CX — 6-wheel shaft / seal / bearing stack

Status: detailed prototype architecture. This is the new common wheel-station concept for all six wheels.

## Design intent
The wheel station must survive sewer water, grit and repeated washing while remaining repairable with common tools. The pressurized side gear bay is secondary protection; the rotating shaft seal remains the primary water barrier.

## Common wheel shaft
Baseline shaft diameter: **10 mm**.

Prototype shaft material:
- preferred: AISI 420 / 40X13 stainless, hardened/ground in the seal zone;
- acceptable prototype alternative: AISI 316 with hardened replaceable wear sleeve if field wear is excessive.

Critical journals:
- bearing journals: Ø10 h6;
- seal-running journal: Ø10, smooth continuous surface;
- seal-running finish: Ra <= 0.4 µm target;
- no thread, keyway, flat or cross-hole may pass under the seal lip;
- shoulder runout to journal: <=0.03 mm target.

## Outer-to-inner stack
1. M8 axial retaining screw + locking washer;
2. removable wheel hub, keyed to shaft;
3. stainless thrust/spacer washer;
4. overlapping labyrinth/dirt shield integrated with wheel hub;
5. FKM TC-type double-lip rotary seal, starting size **10x22x7 mm**;
6. outer 6000-2RS bearing, 10x26x8, located in the accurately piloted side cover boss;
7. wheel gear z40, m1.0, keyed to shaft;
8. spacer;
9. inner 6000-2RS bearing, 10x26x8, located in the fixed structural side wall;
10. shaft shoulder / circlip or locknut for axial retention.

The gear sits between the two bearings. This is preferred over a cantilever gear and prevents the JGB37 motor or its gearbox from carrying wheel radial load.

## Keys
Starting key standard: DIN 6885 parallel key, 3x3 mm class for both wheel hub and wheel gear. Keyways are separate and terminate well away from the seal journal.

No adhesive is a primary torque-transmission or axial-retention method.

## Side-cover role
The side cover is removable but structural only at the outer bearing support. It is **not a gearbox cassette**.

The cover is located by:
- machined pilot/land;
- two dowel pins per side cover;
- perimeter screws provide clamp load, not gear alignment.

Removing the cover after removing the wheels releases the outer bearings while the shafts remain supported by their inner bearings.

## Seal orientation
The spring-loaded main lip faces the sewer/water side. The secondary lip acts as dirt exclusion. A small amount of compatible waterproof grease is used at the lip and labyrinth during assembly.

If prototype mud/sand testing shows unacceptable seal wear or air loss, Rev.CX allows an upgrade to a tandem two-seal stack without changing the shaft diameter; final body machining must preserve enough axial reserve for that option.

## Pressure interaction
Normal crawler pressure target remains +0.20…+0.30 bar gauge. Positive pressure is not used to replace the shaft seal. Some outward air leakage at a worn seal is preferable to inward water ingress and becomes detectable as a pressure-decay fault.

## Wheel service sequence
1. depressurize crawler;
2. remove M8 wheel-retaining screw;
3. pull wheel hub from keyed shaft;
4. inspect labyrinth and seal lip area;
5. remove side cover if bearing/gear/seal service is required;
6. replace seal from cover without opening the electronics tray;
7. reassemble with new O-ring/shaft seal as required;
8. pressure leak-test before use.

## Release gates
- measure real purchased seal OD/width and lip geometry;
- runout measurement on prototype shaft;
- 2 h wet rotating test;
- mud/sand + wash-down test;
- 500 forward/reverse cycles;
- pressure decay before/after endurance;
- verify wheel can be removed without opening pressure body.
