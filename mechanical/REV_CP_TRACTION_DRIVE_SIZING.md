# PX-1 Rev.CP — traction drive sizing

Status: engineering sizing; NOT machining RELEASE.

## Frozen architecture carried forward
- 4WD, gear-only transmission; no belts.
- one drive motor per side, rear gear driven by motor and front wheel mechanically coupled by gears.
- traction bus: 24 V from the 48 V tether DC/DC.
- motor family: JGB37-520, 24 V version.
- current wheel candidate: OD 90 mm.
- drivers: 2x BTS7960, left/right independent.

## Wheel speed target
For D=90 mm, circumference = 0.2827 m.
Wheel rpm / ideal linear speed:
- 30 rpm = 0.141 m/s = 8.48 m/min
- 40 rpm = 0.188 m/s = 11.31 m/min
- 50 rpm = 0.236 m/s = 14.14 m/min
- 60 rpm = 0.283 m/s = 16.96 m/min

PX-1 prototype target is 30–50 wheel rpm. This gives useful inspection control while retaining enough transit speed. Do not choose a 300–600 rpm gearbox output and then rely on PWM alone for low-speed inspection.

## Preferred motor gearbox candidate
Start procurement/testing around JGB37-520 24 V, nominal output about 40–50 rpm. Exact seller/SKU is HOLD because JGB37-520 listings vary greatly in motor winding, gearbox ratio, rated torque and stall current.

If a selected unit is 60 rpm, allow firmware speed limiting for inspection but verify low-speed torque and heating. Mechanical wheel gearing should remain near 1:1 unless measured tests justify a reduction.

## Torque sizing rule
With 45 mm wheel radius:
F_tangent = T_wheel / 0.045.
Examples per driven side before traction losses:
- 1 N*m => 22.2 N
- 2 N*m => 44.4 N
- 3 N*m => 66.7 N

Do NOT freeze required motor torque until complete crawler mass, cable drag and obstacle test load are measured.

## Stall-current gate
Do not infer JGB37-520 stall current from the generic model name. Measure the exact purchased motor at 24.0 V with a current-limited bench supply and suitable current instrumentation.
Record for at least 3 samples:
1. no-load current;
2. no-load output rpm;
3. loaded current at representative crawler load;
4. brief stall current (short controlled pulse only);
5. gearbox/motor temperature after duty-cycle test.

## Protection selection after measurement
Per-side fuse, BTS7960 current limit strategy, 24 V contactor rating and final 48->24 V converter margin are HOLD until measured stall/current data exist.
Design rule: normal acceleration must not nuisance-trip; sustained jam must be interrupted by electronic current/time protection before the fuse. Fuse remains wiring/fire protection, not normal motor control.

## Prototype acceptance tests
- crawl continuously at low inspection speed without cogging/stalling;
- start on dry pipe surface at maximum intended tether drag;
- controlled left/right skid steering;
- obstacle start test;
- 10 repeated forward/reverse cycles while logging 24 V bus and current;
- 30 min thermal run;
- deliberate wheel jam to validate software/hardware shutdown;
- verify gear train remains serviceable with hand tools.

## Release gate
No final motor SKU, fuse value, contactor size, wheel gear ratio or machining drawing is RELEASE until exact motor samples are bench-tested.