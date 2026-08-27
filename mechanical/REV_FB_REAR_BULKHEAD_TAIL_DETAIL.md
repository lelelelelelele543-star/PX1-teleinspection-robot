# PX-1 Rev.FB — rear bulkhead, tether anchor and service interfaces

Status: prototype mechanical baseline.

## Rear bulkhead functions
The rear bulkhead carries four independent functions:
1. structural tether tensile anchor;
2. sealed electrical receptacle;
3. pressure fill/service port;
4. recovery/lowering eye.

These functions must not share a weak decorative cover.

## Structural tether anchor
The tether strength member terminates mechanically before electrical conductors reach the connector.

Load path:
`tether jacket -> long flexible boot -> jacket compression support -> exposed aramid/UHMWPE strength member -> metal wedge/clamp -> rear structural boss -> main body`.

Target working pull class remains >=1 kN pending actual tether manufacturer specification.
Electrical contacts carry no towing load.

## Bend support
Target external flexible support length: 80–120 mm depending actual cable OD.
- smooth radius;
- replaceable sacrificial abrasion sleeve;
- no sharp clamp edge against PUR/TPU jacket;
- cable can leave rear body without contacting recovery eye or wheel at full steering/slip conditions.

## Electrical connector
The current low-cost candidate family remains Amphenol LTW X-Lok 6-contact mixed-current class for prototype evaluation only.
Minimum allocation:
- +48 V;
- 0 V;
- digital differential pair;
- spare/service pair.

Final machining does not freeze the connector hole until a real receptacle passes dimensional and 150 m link testing.
Use a replaceable adapter ring/plate so changing connector family does not require replacing the complete main body.

## Pressure fill
Single external capped fill point feeds the internal three-branch check-valve manifold for P0/P1/P2.
- external service valve is not the only non-return barrier;
- valve remains accessible with crawler standing on wheels;
- cap protects against grit;
- fill fitting located away from electrical contacts.

## Recovery eye
Recovery eye attaches directly to the structural bulkhead/main body.
It must withstand crawler weight plus tether drag with safety factor determined at prototype load test.
No recovery load goes into the electrical connector plate.

## Rear service cover
Provide a small dry-service access region behind/around the connector adapter and pressure manifold where practical.
The service cover gets its own static O-ring and captive fasteners.

## Isolation
Any feedthrough from P0 into P1/P2 remains sealed independently. The common pressure fill manifold uses check valves so a damaged side seal does not dump P0.

## Machining candidate
Rear wall base thickness: 8–10 mm class locally, with thicker bosses around:
- tether anchor;
- recovery eye;
- connector adapter;
- fill port.

Final boss dimensions follow FEA/load test and actual connector geometry.

## Qualification
- 1 kN static tether pull with electrical connector unloaded;
- repeated 500 N pull/bend cycles;
- recovery-eye proof lift;
- mated connector submersion;
- 150 m data test during tether pull and motor PWM;
- tail retermination then pressure test;
- mud/wash cycle followed by connector mating test.