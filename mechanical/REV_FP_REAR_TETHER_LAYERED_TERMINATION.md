# PX-1 Rev.FP — layered rear tether termination

Status: prototype mechanical baseline.

## Source basis
Uploaded Proteus cable-end drawings show a deliberately layered tail rather than a single gland. The source assembly includes:
- connector spring / strain element;
- separate cable housing and connector housing;
- cable nut;
- multiple O-rings;
- cable gland;
- PU tubing;
- hose crimp;
- adhesive-lined heat shrink;
- a separate cable cup/retainer.

PX-1 keeps that rugged multi-layer philosophy but uses a modern digital tether and a completely independent tensile-member load path.

## PX-1 tail layers
From crawler outward:
1. structural rear boss in main body;
2. metal tensile-member anchor/wedge;
3. replaceable connector adapter plate, mechanically independent from towing load;
4. sealed electrical receptacle;
5. primary jacket compression/gland region;
6. flexible spring/boot transition;
7. PU/TPU anti-abrasion sleeve;
8. outer sacrificial heat-shrink/boot layer where useful;
9. main rugged tether.

## Tether target
Not an Ethernet patch cable.

Target construction:
- hydrolysis-resistant PUR/TPU outer jacket;
- aramid/Kevlar or UHMWPE strength member;
- 2 x 1.5 mm² power conductors baseline for 48 V;
- at least one shielded balanced data pair, preferably two;
- overall OD target 8–12 mm after supplier freeze;
- repetitive flex, sewage/water/oil/abrasion resistance;
- target temperature class at least -30…+70 °C.

## Mechanical load path
Copper and connector contacts do not pull the robot.

Required load path:
`tether strength member -> metal clamp/wedge -> structural rear boss -> main crawler body`.

Electrical conductors receive a relaxed internal service loop after the strength member is anchored.

Prototype proof target remains 1 kN static pull until the selected tether manufacturer provides an allowable working load.

## Bend control
External flexible support length target: 80–120 mm.

Rules:
- no sharp clamp edge against PUR jacket;
- progressive bend stiffness, not a hard hinge at the body;
- cable cannot touch rear wheel at maximum lateral deflection;
- sacrificial sleeve replaceable without opening P0;
- tail can be reterminated in the field.

## Pressure boundary
The electrical receptacle is a sealed feedthrough into P0.
The mechanical tensile anchor should preferably remain outside the primary P0 sealing path so servicing the cable grip does not automatically expose electronics.

If an internal conductor passage crosses a removable rear plate:
- static FKM O-ring around that plate;
- captive fasteners;
- connector adapter seal independent from tether anchor hardware.

## Field retermination
Required field procedure:
1. cut damaged end square;
2. fit new outer boot/sleeve parts first;
3. strip jacket to gauge length;
4. expose strength member without nicking power/data cores;
5. mechanically clamp strength member;
6. terminate crimp contacts;
7. assemble connector and jacket gland;
8. continuity/insulation test;
9. digital link test;
10. pressure leak test before deployment.

Potting may be used locally for environmental support but must not be the only tensile retention method.

## Connector interface
Current project shortlist remains a compact wet-mate/harsh-environment multi-contact connector, with final model HOLD until it passes:
- 48 V current-rise test;
- 150 m digital link test;
- motor PWM/reversal EMC test;
- repeated wet/muddy mate cycles;
- submerged pressure test.

The rear body uses a replaceable adapter plate so a connector-family change does not scrap the machined main housing.

## Qualification
- 1 kN static pull with electrical contacts unloaded;
- 500 N repeated pull/bend cycles;
- 100 connector mate cycles minimum prototype gate;
- tail retermination followed by leak test;
- motor PWM + digital link while pulling/bending cable;
- mud wash and thermal-cycle inspection.