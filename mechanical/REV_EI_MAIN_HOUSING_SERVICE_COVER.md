# PX-1 Rev.EI — main pressure housing / electronic service cover

Status: prototype body architecture; replaces the earlier simple box envelope with a manufacturable one-piece housing concept.

## Source-derived architecture
The CRP150 housing drawing uses a dedicated crawler housing containing the big bevel gears, bevel axles, 61800 bearings, 18x30x7 shaft seals, lift holding plates and a weight plate.

The uploaded crawler-cover drawing separately identifies:
- an electronic cover;
- a 110x1.5 O-ring;
- multiple M3 cover screws;
- a thermal sheet;
- a camera/service valve and cable-fitting hardware.

PX-1 follows the same service philosophy: one structural housing carries drivetrain/lift datums, while electronics are accessed through a separate sealed cover.

## Main body
Preferred manufacturing concept:
- one-piece CNC-machined Al 6082-T6 main housing;
- overall current packaging envelope remains approximately 307 x 92 x 82 mm before local bosses;
- no split body seam along the bottom or wheel-shaft datum plane;
- side-drive datum faces machined in the same setup where practical;
- central bevel-transfer bearing/seal bores machined coaxially across the body.

The body is not a thin folded sheet box.

## Structural zones
The body contains:
- central P0 electronics/motor cavity;
- left and right bevel-output bores at the middle wheel station;
- two lift pivot/holding bosses integrated into the upper structure;
- rear tail/strain-relief structural land;
- top electronic service opening;
- internal thermal mounting pads for traction DC/DC and motor-holder heat transfer.

## Top electronic service opening
The service opening must be large enough to remove:
- NUCLEO/controller tray;
- traction driver modules;
- DC/DC modules;
- pressure manifold/sensors;
- paired motor holder if its final withdrawal path is upward.

Current packaging target for the opening is approximately 205–225 mm long x 58–64 mm wide, shifted rearward enough to leave a solid bridge under the camera-lift pivot region.

Exact opening shape follows the final electronics layout.

## Top cover
Prototype target:
- Al 6082-T6, 4–5 mm thick;
- continuous FKM O-ring in a machined face groove;
- 10–14 M4 stainless screws around the perimeter;
- two locating dowels or a machined pilot so repeated service does not rely on screw clearance;
- no fastener hole crosses the P0 pressure boundary unless independently sealed.

The cover can double as a heat spreader for low-power electronics, but heavy traction heat should preferably go directly into the main body/base.

## Lift load path
The manual camera lift must not be mounted only to the removable electronic cover.

Use two permanent structural ears/holding plates tied directly into the main housing, analogous in function to the dedicated lift holding plates shown in the source crawler housing.

The lift pivot and gas-spring loads therefore bypass the electronic cover O-ring and do not distort its sealing land.

## Bevel-output bore
At X=150 / Z=45 each side has a coaxial stepped bore for:
- 61800 bearing seat;
- Ø18 transfer-shaft seal running interface / 18x30x7 seal housing;
- local static O-ring/retainer as required by the removable bearing/seal carrier.

Preferred service direction: bearing/seal carrier removable from the outside side-drive bay after removing the side cover, without opening the electronics cavity.

## Side-drive interface
P1/P2 side-drive cavities remain separate from P0.
The side-cover main O-ring and three axle-flange O-rings belong to P1/P2, not P0.

The structural side wall must remain thick enough around all five Z50 axes to hold their bearing/pin datums after repeated cover service.

## Bottom / ballast
The source crawler housing includes a dedicated weight plate. PX-1 retains a replaceable ballast/thermal plate concept instead of permanently making the body excessively thick.

Candidate:
- external or internal stainless ballast plate under the center of gravity;
- mechanically bolted, not glued;
- can be changed to tune traction after tether-drag tests;
- doubles as a local thermal spreader only if galvanic isolation/corrosion is controlled.

## Rear structure
The rear tether tensile member anchors into the main body or a bolted structural tail block. The electrical connector does not carry crawler pull load.

Provide a recovery eye tied into the same structural region, not into the electronic cover.

## Pressure qualification
P0 normal operating pressure remains +0.20..+0.30 bar gauge.
Prototype body structural qualification target remains at least 1 bar differential using a safe low-energy/hydrostatic method where practical.

Leak test sequence:
1. empty body with dummy shaft plugs;
2. top cover installed;
3. tail and service ports installed;
4. complete motor/bevel system installed;
5. P1/P2 intentionally vented while verifying P0 retention.

## Machining rules
Initial targets:
- common bearing/seal axes coaxiality <=0.03 mm;
- sealing-face flatness <=0.08 mm around top cover;
- O-ring-land Ra <=1.6 um;
- bearing bores H7;
- all internal sharp corners relieved for machining and stress reduction;
- avoid blind deep pockets that cannot be cleaned after sewer-service contamination.

## Release gates
- full-solid body mass and wall-thickness review;
- final electronics packing confirms service opening;
- lift load calculation and static proof;
- motor-holder withdrawal path verified;
- full DN150 collision check with actual screw heads/tail/lift;
- pressure proof on first machined body;
- only then issue manufacturing drawing.