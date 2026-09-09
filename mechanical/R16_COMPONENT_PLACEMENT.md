# PX-1 Rev.R16 — dry-bay component placement

The R16 packaging gate uses a nominal dry reserve envelope of
**X=10…297, Y=-36…36, Z=16…82 mm** (287 × 72 × 66 mm).  These are envelopes
for purchased modules, not machining pockets or final standoff drawings.

| Module | Nominal envelope (mm) | R16 reserve placement (mm) | Service reason |
|---|---:|---|---|
| Mean Well RSD-60H-24 | 128 × 60 × 25 | X=10…138, Y=-30…30, Z=16…41 | Replaces the too-large RSD-100D-24; front/lower power bay |
| Pololu 4695, front-side reserve | Ø36.8 × 72.6 | X=25…97.6, centre Y=17, Z=60 | Staggered away from second motor and RSD |
| Pololu 4695, rear-side reserve | Ø36.8 × 72.6 | X=210…282.6, centre Y=-17, Z=60 | Rear drive zone, encoder plug serviceable |
| NUCLEO-F446RE | 82.5 × 70 × 18 | X=150…232.5, Y=-35…35, Z=20…38 | One millimetre side clearance in dry bay |
| 4× DRV8871 reserve (2 traction + 2 camera) | 100 × 24 × 10 | X=105…205, Y=-12…12, Z=71…81 | One high service rail; camera drivers stay out of the moving pod |
| СУ-1П video transmitter | 50 × 42 × 18 | X=140…190, Y=-21…21, Z=41…59 | Short CVBS run to tether interface |
| TTL→RS485 isolator | 42.8 × 15.2 × 4.75 | X=140…182.8, Y=-7.6…7.6, Z=59.5…64.25 | Isolated command interface |
| D24V22F12 12 V converter | 17.8 × 17.8 × 8 | X=115…132.8, Y=-8.9…8.9, Z=43…51 | Camera/miscellaneous 12 V rail |
| 2× INA260 reserve | 46 × 23 × 5 | X=115…161, Y=-35…-12, Z=65…70 | Current monitoring on the service side |
| TMP117/pressure reserve | 26 × 18 × 5 | X=110…136, Y=-35.5…-17.5, Z=47…52 | Wall-coupled temperature/pressure sensing |

The RunCam Phoenix 2 SE V2 board is not in this table: it is held in the
separate camera pod at the lift, with its own shock isolator and window guard.

The CAD regression checks all ten body reserves for pairwise nominal overlap and
for escape from the dry reserve envelope.  The checks do not prove connector
bend radius, creepage/clearance, heat flow, vibration, pressure, or wiring
service loops.  Those are the next drawing and bench gates.

## Power choice

The selected onboard candidate is **RSD-60H-24**, not RSD-100D-24.  Mean Well's
current RSD-60 datasheet lists a 128 × 60 × 25 mm enclosure and the H-24 model
as a 40…160 VDC input, 24 V/2.5 A, 60 W converter.  The first demo is bounded
by the DRV8871 current limit and must log bus current and converter temperature;
the 60 W rating is not a license to use the motor's theoretical 3 A stall
current continuously.

Pololu's 4695 data gives a 24 V, 100 RPM motor, 100 mA no-load and 3 A
extrapolated stall current.  R16 therefore retains the 100 kΩ DRV8871 current
limit candidate and treats motor thermal/current testing as a release gate.

References: [Mean Well RSD-60 datasheet](https://www.meanwell.com/Upload/PDF/RSD-60/RSD-60-SPEC.PDF),
[Pololu 4695](https://www.pololu.com/product/4695).
