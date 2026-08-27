# PX-1 Rev.EO — rear tail / tether / service-body integration

Status: mechanical integration candidate; exact connector remains qualification gate.

## Rear-face functions
The rear of PX-1 now contains only four external service functions:
1. tether mechanical anchor / strain-relief;
2. sealed quick electrical connector;
3. protected pressure fill port;
4. structural lowering/recovery eye.

No antenna and no crawler-mounted operator E-STOP.

## Mechanical load path
Tether tensile load must bypass the connector completely.

Current load path:
`PUR tether jacket -> long flexible bend support -> jacket compression sleeve -> exposed aramid/UHMWPE strength member -> stainless split wedge/anchor -> rear structural bulkhead -> main milled body`.

The copper conductors leave the anchored cable with a relaxed internal service loop and terminate separately at the electrical receptacle.

## Tail housing
Preferred rear tail is not a removable electronics cassette. It is a structural rear boss/guard integral with or bolted directly to the body rear bulkhead.

Baseline envelope:
- rear structural tail boss approximately 55–65 mm wide;
- 80–120 mm external flexible bend-support length depending final tether OD;
- sacrificial replaceable abrasion sleeve over the first bend section;
- no sharp metal edge may contact the PUR jacket.

## Electrical connector
First prototype candidate remains the compact Amphenol LTW X-Lok mixed-current 6-contact family from Rev.DR, but it remains TEST ONLY because the selected variant is not specified by the manufacturer as Ethernet.

Minimum allocation concept:
- +48 V;
- 0 V;
- one balanced 10BASE-T1L pair;
- second spare/service differential pair.

If the X-Lok does not pass 150 m link-margin/EMC testing, move to a connector family with documented high-speed balanced-pair performance rather than forcing the electrical design around the failed connector.

## Pressure fill
Rear service port feeds the previously defined three-branch manifold for P0/P1/P2.

Requirements:
- external capped Schrader/industrial fill fitting;
- secondary internal non-return element;
- fill port located above the lowest mud-contact surface;
- accessible with crawler standing on wheels;
- protected against direct impact by the rear tail geometry.

## Recovery eye
One structural eye is connected to the main body metal, not to a thin rear cover.

Design load gate:
- proof test with complete crawler mass and tether attached;
- target static proof load to be set after final mass is frozen;
- eye must allow controlled lowering into a manhole without loading the camera lift.

## Field retermination
Rear tail is designed so the final damaged tether section can be cut off and reterminated without opening the wheel-drive side bays.

Service order:
1. remove rear bend guard/boot;
2. release mechanical strength-member clamp;
3. disconnect electrical plug/termination;
4. shorten and restrip tether;
5. reinstall strength-member anchor;
6. terminate power/data;
7. continuity/insulation test;
8. pressure test P0 and data-link test before deployment.

## Water barrier philosophy
Do not depend on one gasket only.

Rear barrier sequence:
- external bend boot and abrasion sleeve are dirt protection only;
- electrical receptacle has its own environmental seal;
- strength-member anchor is mechanically independent;
- rear service cover/bulkhead has its own static O-ring;
- P0 positive pressure and pressure sensor provide secondary leak indication.

## Release gates
- exact tether cable OD/construction;
- actual 1 kN-class pull qualification limited by selected cable manufacturer data;
- exact panel connector and panel cutout;
- 150 m data-link test through connector;
- repeated wet/mud mate cycles;
- rear-cover pressure test after 20 open/close cycles;
- field retermination trial timed with ordinary service tools.
