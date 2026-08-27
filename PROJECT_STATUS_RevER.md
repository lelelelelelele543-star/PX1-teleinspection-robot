# PX-1 Rev.ER — integrated project status

Status: PROTOTYPE ENGINEERING BASELINE, not machining/serial release.

## Frozen architecture
- CRP150-inspired compact six-wheel crawler layout, own PX-1 geometry;
- 6 x Ø90-class profiled wheels, three per side;
- one traction motor per side;
- bevel input reduction 2.5:1 candidate using KHK SB1.5 18/45 H-class pair;
- five equal m1 Z50 gears per side, 100 mm wheel pitch;
- sealed side-drive bays under rigid covers;
- P0 central body + P1 left drive + P2 right drive as isolated positive-pressure zones;
- common fill point with check-valve isolation;
- manual CRP-style parallelogram camera lift;
- digital camera only, no CVBS/NTSC/PAL/coax;
- TILT -105…+105°, continuous ROLL 360°;
- rugged PUR/TPU tether with separate tensile member, 48 V power and balanced digital pair(s);
- tether mechanical anchor independent from electrical connector.

## Current main geometry
- main body length class: 307 mm;
- body width class: 92 mm before side covers/wheels;
- body Z envelope: ~8…90 mm in current CAD master;
- wheel centers X = 50 / 150 / 250 mm;
- wheel axis Z = 45 mm;
- ideal DN150 pipe axis in current wheel-contact model ≈52.05 mm;
- camera head envelope target Ø52 x 72 mm;
- DN150 LOW camera axis target Z = 75 mm;
- manual lift pivot candidate X=200 / Z=94, link length 120 mm.

## Current traction stack
Per wheel station:
- stepped shaft Ø12 gear/support journal -> Ø17 outer wheel-support journal;
- inner 61801-class supports;
- outer 61903-class wheel-load bearing in service flange;
- dynamic FKM/X-ring/lip-seal candidate;
- labyrinth/exclusion geometry;
- keyed wheel torque transfer with independent axial retention.

Central bevel output:
- dedicated cross shaft;
- 61800-class support philosophy;
- 18x30x7-class dynamic seal boundary candidate;
- serviceable coupling to side-drive center shaft.

## Manual lift positions
Current kinematic model:
- LOW/DN150: camera Z75, arm angle about -14.0°;
- MID: camera Z130, arm angle about +12.5°;
- HIGH: camera Z205, arm angle about +57.3°.

Only LOW/DN150 is allowed in DN150 until full-solid physical verification.

## P0 packaging
Current service zoning:
- Zone A front: controller/comms/low-power electronics;
- Zone B center: paired traction motor holder + bevel input;
- Zone C rear: 48 V protection + compact isolated 48->24 V traction DC/DC;
- rear service zone: tether connector/service loop + three-zone pressure manifold.

Prototype controller remains NUCLEO-F446RE. Generic BTS7960 modules remain prototype-only and must not be treated as final production traction drivers.

## Biggest remaining engineering blockers
1. exact purchased JGB37-555 samples and measured current/torque/RPM;
2. exact final traction driver rather than generic module assumption;
3. exact camera PCB mechanical drawing and power/thermal measurement;
4. exact Ethernet-capable rotary-transfer sample/drawing;
5. exact tether cable and connector passing 150 m digital-link/EMC tests;
6. full-solid body, side cover, wheel flanges, lift plates/yoke and camera latch;
7. real DN150 tube sweep including screw heads, cable loop and pipe imperfections;
8. pressure qualification of P0/P1/P2 and wheel seals under rotation;
9. final gas-spring mounting geometry and article;
10. manufacturing drawings with tolerances only after the above physical gates close.

## Current CAD master
`mechanical/freecad/PX1_CRP150_6W_Master_RevEQ.py`

This master integrates:
- six-wheel drive architecture;
- side covers;
- bevel/motor envelopes;
- sculpted front body recess for folded camera;
- manual lift LOW geometry;
- digital head envelope;
- internal control/motor/power/service packaging zones;
- rear tether bend support and recovery-eye envelope.

## Next production-oriented work sequence
1. replace packaging wheel stations with machinable shaft/flange solids;
2. replace box body with actual hollow milled pressure-body solid and seal lands;
3. replace lift rod envelopes with plate arms, clamp and stop hardware;
4. replace camera cylinder with shell/yoke/latch/LED/window solids;
5. close rear bulkhead/connector/fill-port machining geometry;
6. run full interference/DN150 checks;
7. generate drawing candidates and machining BOM;
8. build first mechanical prototype and close dimensional/pressure gates before serial-release drawings.
