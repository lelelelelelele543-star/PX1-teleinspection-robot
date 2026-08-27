# PX-1 Rev.DV — traction torque/current protection

Status: prototype control limits derived from published motor family data and selected KHK bevel pair. Final limits require measurement of the exact motors.

## Motor reference data
Current preferred traction sample: JGB37-555, 24 V, ratio ~56.

Published family data used only for prototype sizing:
- no-load current ~0.10 A;
- no-load speed ~107 rpm;
- rated current ~0.90 A;
- rated speed ~76 rpm;
- rated torque ~8.4 kgf·cm = 0.824 N·m;
- stall current ~6.5 A;
- stall torque ~32 kgf·cm = 3.14 N·m.

The exact purchased motors must be bench-measured before production release.

## Why current limiting is mandatory
The selected KHK SB1.5-1845H pinion has published Hardened-Plus surface durability around 2.16 N·m. The motor-family theoretical stall torque of ~3.14 N·m is above that value.

Therefore PX-1 must never treat full motor stall as a permissible operating state.

## First prototype electronic ceiling
Using a simple linear torque-current interpolation between ~0.1 A no-load and ~6.5 A stall:

- 3.0 A -> ~1.42 N·m motor torque;
- 3.2 A -> ~1.52 N·m;
- 3.5 A -> ~1.67 N·m;
- 4.0 A -> ~1.91 N·m.

Preferred initial hard software/current-control ceiling: **3.2 A per side**.
Temporary laboratory upper ceiling for obstacle testing: **3.5 A per side**, only after the current sensor is calibrated.

At 3.5 A, calculated pinion torque remains about 1.67 N·m, below the 2.16 N·m published surface-durability value. This is still a prototype engineering margin, not a certified safety factor.

## After 2.5:1 bevel stage
Assuming ~90% bevel efficiency:
- 3.2 A ceiling -> ~3.42 N·m into one complete side distribution train;
- 3.5 A ceiling -> ~3.75 N·m.

At 45 mm wheel radius, this corresponds to ideal side tangential force before spur-train/tire losses of roughly:
- 3.2 A -> 76 N;
- 3.5 A -> 83 N.

Actual sewer traction will be lower and must be measured.

## Jam algorithm
Initial firmware behavior:
- normal acceleration current may briefly exceed rated current;
- if current >3.2 A, PWM is reduced immediately;
- if current remains near ceiling while measured wheel speed is near zero, declare JAM;
- target jam decision window: 100–250 ms after startup/inrush allowance;
- after JAM: disable that H-bridge, report side/fault, require operator release/retry;
- repeated automatic hammering/reversing is prohibited.

## Hardware hierarchy
1. electronic PWM/current control = normal torque protection;
2. driver overcurrent/thermal protection = secondary protection;
3. per-side fuse = wiring/fire protection only;
4. traction contactor/E-STOP = independent hardware isolation.

Do not size the fuse to act as the normal motor current limiter.

## Validation
Bench procedure for each motor sample:
- measure I0 and rpm at 24.0 V;
- torque/current sweep on a brake or lever-arm fixture;
- brief controlled stall pulse;
- confirm current sensor accuracy;
- set real 3.2 A-equivalent torque point from measurement rather than interpolation;
- inspect bevel contact pattern after jam tests;
- verify no tooth pitting or gearbox damage after repeated obstacle starts.
