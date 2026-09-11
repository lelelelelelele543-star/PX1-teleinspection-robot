# PX-1 TRACTION MOTOR GATE — Rev.PQ

Date: 2026-09-01
Last reviewed: 2026-09-11 / Rev.B WB03
Status: ACTIVE MOTOR SELECTION GATE

## Purpose
Freeze the required traction-motor performance envelope before modifying the Proteus-derived crawler housing or buying an underpowered gearmotor simply because it is cheap and available.

## Mechanical architecture retained
PX-1 uses:
- two traction motors total;
- one motor per side;
- longitudinal motor arrangement;
- supported Z16 bevel pinion;
- Z16 -> Z40 bevel reduction = 2.5:1;
- rear long-axle side-drive input;
- five Z50 gears per side with 1:1 speed distribution to the three wheel stations.

The motor gearhead does not carry bevel radial load directly; the bevel input shaft remains separately supported.

## Original/reference performance target
The original observed Proteus motor unit used a FAULHABER gearhead marked 66:1. The replacement does not need to copy the exact motor, but it must reproduce a useful wheel-speed and tractive-force envelope.

Earlier provisional selection target:
- 24 V nominal;
- geared output speed: 45-65 rpm class under light/no load for the slower/stronger first prototype;
- rated output torque: >=1.0 N.m desired;
- geared motor body preferably <=32-35 mm diameter class;
- overall length preferably <=95-100 mm class;
- output shaft geometry compatible with a separately supported bevel input;
- two identical units.

Rev.B WB03 adds an important clarification: **motor rated torque is not the commanded crawler torque**. The existing 40/50 N crawler pull targets require only about 0.48/0.60 N.m motor output per side under the current 2.5:1 bevel and 0.75 path-efficiency screen. A motor with substantially more torque is useful as reserve, but the firmware/current-control strategy must prevent the reserve from destroying the compact bevel pair during stall/skid conditions.

## Leading purchasable candidate — ISL PGM-32P-24-100-60-02

Part:
- manufacturer: ISL Products;
- online ID: `PGM-32P-24-100-60-02`;
- reference ID: `MOT-IG32PGM 100`;
- 24 V brushed planetary gear motor;
- Ø32 mm class;
- ~92 mm overall length;
- reduction ratio 100:1.

Manufacturer-controlled 2023 technical datasheet gives:
- no-load speed: 60 rpm;
- rated speed: 49 rpm;
- rated torque: 18 kg.cm = ~1.765 N.m;
- rated current: 1.06 A;
- theoretical stall torque: 98 kg.cm = ~9.61 N.m;
- stall current: 5.5 A;
- explicit gearbox mechanical limitation: 40 kg.cm = ~3.923 N.m; operation past this limit may cause premature failure.

The manufacturer's online shop was checked on 2026-09-11 and listed 22 units in stock. The shop marketing table shows slightly different torque/speed numbers than the downloadable technical datasheet. Until a newer signed datasheet is obtained, the technical datasheet is the controlled engineering source.

With the active Z16/Z40 2.5:1 bevel and Ø90 wheel:
- at 49 rpm rated motor output -> ~19.6 rpm wheel -> ~0.092 m/s theoretical crawler speed;
- at 60 rpm no-load -> ~24 rpm wheel -> ~0.113 m/s theoretical crawler speed.

Decision: this part is now the **leading Rev.B motor candidate for the slower/stronger first prototype**, subject to physical sample measurement and bench torque/speed/current characterization.

Do not release final motor-holder holes, pilot, coupler length or shaft fit from web/catalogue dimensions alone. Final interface is sample-driven.

## Alternative faster reference — ISL PGM-32P-24-51-118-02

The 51:1 Ø32 mm variant is mechanically attractive because its manufacturer datasheet gives approximately:
- no-load speed 118 rpm;
- rated speed ~96 rpm;
- rated torque ~9.25 kg.cm (~0.907 N.m) in the 2023 technical datasheet.

After the 2.5:1 bevel this corresponds to ~0.181 m/s rated theoretical crawler speed, much closer to the original Proteus speed envelope.

However current shop status checked in Rev.B WB03 does not offer this item as a normal in-stock online purchase. Therefore it remains a performance reference / alternate sourcing target, not the active procurement choice.

## JGB37-520 assessment
The inexpensive JGB37-520 family remains useful for mechanisms and experiments but is NOT the preferred traction motor for the Proteus-derived crawler.

Current family data for 24 V versions give approximately:
- 90:1 -> ~66-67 rpm, rated torque only ~1.8-2.0 kg.cm (~0.18-0.20 N.m);
- 131:1 -> ~45-46 rpm, rated torque only ~2.5-2.7 kg.cm (~0.25-0.26 N.m).

After the 2.5:1 bevel reduction these values remain below the current 40-50 N traction target once cable drag, wet operation and path losses are included.

Decision: do not freeze JGB37-520 as the crawler traction motor.

## Rev.B torque-command rule
Using the current screen:
- 40 N total crawler pull -> ~0.48 N.m motor output per side;
- 50 N -> ~0.60 N.m;
- 60 N -> ~0.72 N.m;
- ~66.7 N -> ~0.80 N.m;
- ~83.3 N -> ~1.00 N.m.

Initial bench tuning target:
- normal traction around the 0.60 N.m class;
- provisional protected ceiling roughly 0.65-0.80 N.m until actual motor torque/current curves, whole-crawler drag and real tether force are measured.

Do not convert that torque target into a fixed current number purely from catalog data. Measure each motor on the bench and calibrate current/torque because brushed-motor and gearbox losses vary and the currently published ISL data revisions are not perfectly identical.

The BTS7960 remains a prototype H-bridge candidate, but a fuse is not a torque regulator. Crawler firmware must monitor current and command PWM reduction/trip; exact current-sense hardware is frozen separately after bench measurements.

## Candidate acceptance rule
A purchasable motor may replace the ISL reference if it meets all of:
1. 24 V nominal;
2. useful geared-output speed preserving crawler speed after the 2.5:1 bevel;
3. verified output torque enough to deliver >=0.60 N.m continuously at the intended duty point with reserve;
4. <=35 mm preferred diameter or proven packaging in the Proteus-derived body;
5. <=100 mm preferred total length;
6. shaft/coupling geometry compatible with a separately supported Z16 input shaft;
7. reversible brushed DC or sensored BLDC with an available serviceable driver;
8. replacement source realistically obtainable for at least two identical motors.

The old requirement `>=1.0 N.m rated, >=1.3 N.m preferred` is retained as a strong procurement preference, not as proof that PX-1 must continuously command that torque.

## Driver consequence
If the selected motor is brushed DC:
- BTS7960-class prototype H-bridge remains acceptable subject to measured current and thermal test;
- current sensing per side is mandatory for protected traction control.

If the selected motor is sensored BLDC:
- replace BTS7960 with two serviceable sensored BLDC driver modules;
- keep the same mechanical drivetrain and 24 V traction bus.

Motor technology must not force a redesign of the side gears or wheel stations.

## Bevel-pair consequence
The in-stock ISL motor can produce much more torque than an unhardened commercial m1 Z16/Z40 bevel pair can safely transmit. Therefore the motor choice and bevel choice are now linked by `REVB_WB03_BEVEL_MOTOR_TORQUE_GATE.md`.

Normal operation will be current/torque limited, while the released bevel pair must itself have a verified minimum continuous and short-overload capacity. Do not install a soft catalog Z16/Z40 pair and rely on software alone to keep it alive.

## Machining gate
Do not release the final motor holder/coupler until:
- the exact purchased motor is physically available or a manufacturer-controlled drawing is obtained;
- the final hardened bevel pair's mounting distance and bore/retention are frozen;
- one motor/bevel side has passed alignment, backlash, current and load tests.

## Decision
- Preserve the Proteus two-motor/Z16-Z40 drive architecture.
- Leading Rev.B motor candidate: `ISL PGM-32P-24-100-60-02`.
- Do not use JGB37-520 as the primary traction motor.
- Do not command the ISL motor's full available torque in normal crawler operation.
- Close the hardened compact bevel-pair gate before manufacturing release.
