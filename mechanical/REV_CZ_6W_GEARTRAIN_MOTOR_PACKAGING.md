# PX-1 Rev.CZ — six-wheel geartrain + motor packaging

Status: packaging freeze candidate, pending exact motor and gear samples.

## Wheel centers
Prototype master coordinates per side:
- front wheel X = 50 mm;
- middle wheel X = 150 mm;
- rear wheel X = 250 mm;
- wheel center Z = 45 mm baseline;
- wheel OD = 90 mm.

This gives 100 mm adjacent wheel pitch and approximately 290 mm wheel footprint.

## Wheel synchronization gears
Selected starting family:
- wheel gears: z40, module 1.0, 20°, face 8 mm;
- two idlers: z60, module 1.0, 20°, face 8 mm;
- topology: z40(front) -> z60 -> z40(middle) -> z60 -> z40(rear).

Center distances:
- z40/z60 = 50.0 mm;
- two meshes per adjacent wheel = 100.0 mm wheel pitch.

Front, middle and rear wheels therefore rotate in the same direction.

## Gear material strategy
Prototype:
- wheel gears: C45/40Cr steel, black oxide or suitable corrosion protection;
- idlers: same steel family preferred for first durability tests;
- polymer idlers are not the baseline because sewer grit, temperature and long service life are priorities.

Final tooth hardening is HOLD until real torque/current tests define root load.

## Idler support
Each z60 idler uses:
- fixed Ø8 mm stainless pin;
- 608-2RS bearing, 8x22x7, in the idler hub;
- thrust washers both sides;
- pin supported by inner structural wall and accurately located side cover where practical.

The gear cover pilot/dowels keep the outer support repeatable after service.

## Motor placement
One 24 V JGB37-520-class motor per side.

Preferred position:
- inside the central dry body;
- longitudinal motor axis;
- motor output near the middle-wheel station to keep the torque path symmetric;
- motor mounted on replaceable adapter plate so exact vendor gearbox length/hole pattern does not change the body.

The wheel gear train carries wheel loads. The motor shaft carries only motor-input gear load.

## Motor input stage
Do not hard-freeze ratio before exact motor bench data.

Packaging reserve is created for:
- motor pinion z18–z24, m1.0;
- driven input gear z30–z40, m1.0;
- expected reduction range approximately 1.25:1 to 2.0:1.

For a 24 V / ~45 rpm motor, a 1.5–1.7:1 reduction would produce approximately 26–30 wheel rpm, or roughly 7.4–8.5 m/min at Ø90. This is a sensible inspection baseline but remains test-dependent.

## Backlash
Prototype target backlash:
- wheel train: 0.10–0.20 mm circumferential equivalent at pitch line;
- motor input: adjustable by slotted motor adapter before lock-down.

Do not preload the external gear train tightly. Thermal expansion and minor housing distortion must not create tight spots.

## Lubrication
Because the side bay is sealed and dry:
- use a light, water-resistant synthetic gear grease sparingly on teeth;
- avoid completely packing the cavity with grease;
- grease must be compatible with FKM O-rings/seals and bearing seals;
- after endurance test inspect whether grease migrates toward shaft lips.

## Six-wheel steering note
Six fixed wheels increase skid-steer scrub relative to the previous 4-wheel concept. Do not compensate by removing drive from the middle axle. All six wheels remain driven.

Prototype handling tests must check:
- dry concrete turn-in-place;
- wet PVC/PE pipe;
- DN150 pipe;
- cable drag;
- current difference straight vs turning.

If turning current is excessive, permissible tuning sequence is:
1. tire compound/tread;
2. middle-wheel vertical offset <=1 mm candidate;
3. firmware current/speed shaping;
4. only then revisit wheel geometry.

## Release gates
- exact motor dimensions and shaft measured;
- exact gear vendor/tool geometry verified;
- full 360° hand rotation with side cover torqued;
- gear contact pattern check;
- loaded current and temperature test;
- 5000 wheel-revolution endurance before manufacturing RELEASE.
