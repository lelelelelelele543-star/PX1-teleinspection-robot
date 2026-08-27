# PX-1 Rev.EP — internal electronics packaging / power-data segregation

Status: packaging architecture candidate. Uses the current CRP150-style body envelope and supersedes the assumption that all boards can be placed arbitrarily inside P0.

## P0 internal usable envelope
Current body envelope is ~307 x 92 x 82 mm overall. After wall thickness, seals, bosses and service clearances, treat the usable electronics corridor conservatively as roughly:
- length: 285–290 mm;
- width: 76–80 mm;
- height: 62–68 mm depending local ribs/bosses.

The exact machined tray solid will define final numbers.

## Longitudinal zoning
P0 is divided into three service zones.

### Zone A — front control stack, X≈10…95 mm
Reserved for:
- NUCLEO-F446RE prototype controller;
- isolated communications interface;
- pressure-sensor interfaces;
- camera/lift I/O;
- low-power 5 V/12 V conversion;
- service/debug connector.

Mount as a removable two-level electronics tray so the NUCLEO can be removed without disturbing traction gearing.

### Zone B — center traction motor holder, X≈100…200 mm
Reserved for:
- paired JGB37-555 traction motors;
- common motor holder;
- supported bevel-pinion shafts;
- central bevel output shafts/couplings.

No sensitive logic board is mounted directly above a motor unless a grounded metal shield/thermal barrier and service clearance are proven.

### Zone C — rear power stack, X≈210…295 mm
Reserved for:
- 48 V input protection/filter;
- compact isolated 48→24 V half-brick traction DC/DC (~70 x 65 x 18 mm installed envelope);
- traction power disconnect/solid-state or relay element after final selection;
- current sensing;
- branch fusing;
- rear connector and pressure-manifold wiring.

The 48→24 V brick mounts to a machined aluminum thermal pad/boss in the body for conduction cooling.

## Traction drivers
Generic BTS7960 modules remain PROTOTYPE ONLY. Their physical size makes random placement unacceptable.

Prototype tray rule:
- left and right traction drivers mounted on a lower thermal plate, one behind the other longitudinally or on opposite faces of a dedicated metal carrier;
- never sandwich two hot modules with no heat path;
- motor outputs leave the driver area directly toward the central motor holder;
- logic/PWM wiring approaches from the opposite side.

If the final protected driver solution is smaller, keep the same connector/harness interfaces and reduce the carrier footprint rather than redesigning the body.

## Ground / chassis architecture
- rear tether shield/overall braid bonds to chassis at the entry point with a short, wide connection;
- chassis is not used as normal DC return;
- 48 V power return, traction return and logic return are routed conductors;
- star/reference joining follows the selected isolated DC/DC and communication topology;
- video/data pair shield, if the selected cable uses one, is terminated according to measured EMC performance and PHY/application guidance.

## Data path
Modern tether architecture remains:
`digital camera -> internal Ethernet/digital link -> crawler data concentrator/PHY -> 10BASE-T1L pair -> rugged tether -> console`.

No coaxial video path is reserved in the body.

10BASE-T1L physical implementation is still an electronics release gate; connector and cable pair must pass the full 150 m test.

## Separation / EMC
Within P0:
- motor and traction-current conductors twisted and kept close to the chassis/base route;
- digital camera/data pair routed on the opposite side of the body where possible;
- minimum practical separation ~15 mm between long parallel motor-power and data runs;
- crossings near 90°;
- ferrite/common-mode components only after measured EMI results, not decorative placement;
- LED PWM and traction PWM returns never share the camera pair shield as current path.

## Harness serviceability
Use labeled plug-in harnesses between major modules:
- H1 rear 48 V/data;
- H2 input-protection to traction DC/DC;
- H3 left/right traction driver power;
- H4 motor outputs;
- H5 pressure sensors P0/P1/P2;
- H6 camera/lift power-data;
- H7 service/debug.

No permanent soldered wire should prevent removal of the controller tray, power tray or motor holder as independent service assemblies.

## Thermal monitoring
Minimum sensors/measurements:
- traction DC/DC baseplate temperature;
- left/right traction driver temperature or NTC on their heat spreader;
- internal P0 air/body temperature;
- motor current per side.

Firmware derates before converter/driver thermal shutdown.

## Release blockers
1. actual machined-body internal solid;
2. exact final traction-driver module/PCB;
3. exact 48→24 V half-brick purchased sample;
4. NUCLEO tray accessibility with lift installed;
5. connectorized harness bend-radius check;
6. 60 min worst-case thermal run sealed;
7. conducted/radiated noise test with camera streaming and both traction motors reversing.
