# PX-1 TRACTION MOTOR GATE — Rev.PQ

Date: 2026-09-01
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

The motor gearhead does not carry wheel radial load directly.

## Original/reference performance target
The original observed Proteus motor unit used a FAULHABER gearhead marked 66:1. The replacement does not need to copy the exact motor, but it must reproduce the useful wheel-speed and tractive-force envelope.

For the current DN150-class crawler geometry, the replacement motor target is approximately:
- 24 V nominal;
- geared output speed: 45-65 rpm class under light/no load;
- rated output torque: >=1.0 N.m desired, >=1.3 N.m preferred;
- short peak torque above rated with current limiting;
- geared motor body preferably <=32-35 mm diameter class;
- overall length preferably <=95 mm class;
- output shaft around 6 mm or another geometry that can accept a supported coupling to the Z16 shaft;
- two identical units.

## Strong documented reference
ISL Products `PGM-32P-24-100-60-02 / MOT-IG32PGM 100` remains the dimensional/performance reference:
- Ø32 mm class;
- ~92 mm total length class;
- 24 V;
- 60 rpm no-load;
- roughly 49-54 rpm rated depending data revision;
- roughly 1.37-1.77 N.m published rated torque range depending revision;
- 6 mm output shaft class;
- planetary gearbox.

This part proves that the required motor envelope is physically realistic. It is not yet the compulsory purchased part.

## JGB37-520 assessment
The inexpensive JGB37-520 family remains useful for mechanisms and experiments but is NOT the preferred traction motor for the Proteus-derived crawler.

Current family data for 24 V versions give approximately:
- 90:1 -> ~66-67 rpm, rated torque only ~1.8-2.0 kg.cm (~0.18-0.20 N.m);
- 131:1 -> ~45-46 rpm, rated torque only ~2.5-2.7 kg.cm (~0.25-0.26 N.m).

After the 2.5:1 bevel reduction these values are still far below the preferred PX-1 traction torque target. The low price and correct rpm therefore do not compensate for inadequate torque reserve for cable drag, wet pipe operation and turning.

Decision: do not freeze JGB37-520 as the crawler traction motor.

## Candidate acceptance rule
A purchasable motor may replace the ISL reference if it meets all of:
1. 24 V nominal;
2. 45-65 rpm class geared output or a nearby speed that preserves useful crawler speed;
3. >=1.0 N.m documented/verified rated output torque, >=1.3 N.m preferred;
4. <=35 mm preferred diameter or proven packaging in the Proteus-derived body;
5. <=100 mm preferred total length;
6. shaft/coupling geometry compatible with a separately supported Z16 input shaft;
7. reversible brushed DC or sensored BLDC with an available serviceable driver;
8. replacement source must be realistically obtainable for at least two identical motors.

## Driver consequence
If the selected motor is brushed DC:
- BTS7960-class prototype H-bridge remains acceptable subject to measured current and thermal test.

If the selected motor is sensored BLDC:
- replace BTS7960 with two serviceable sensored BLDC driver modules;
- keep the same mechanical drivetrain and 24 V traction bus.

Motor technology must not force a redesign of the side gears or wheel stations.

## Machining gate
Do not release the final motor holder/coupler until the exact purchased motor is physically available or a manufacturer-controlled drawing is obtained.

The housing may continue using the provisional Ø32-35 x <=100 mm packaging envelope, but final hole PCD, pilot, shaft bore, axial position and coupling are sample-driven.

## Decision
- Preserve the Proteus two-motor/Z16-Z40 drive architecture.
- Do not use the cheap JGB37-520 as the primary traction motor merely because a 24 V / 66 rpm variant is available.
- Continue procurement search against the >=1.0 N.m, 45-65 rpm, <=35 mm-class envelope.
