# PX-1 Rev.CQ — JGB37-520 24 V ratio selection

Status: component selection candidate, not purchase freeze.

## Source-backed motor family data
Manufacturer-family data for JGB37-520 24 V lists these relevant reductions:
- 1:90 -> 66 rpm no-load, about 46 rpm under listed load;
- 1:131 -> 45 rpm no-load, about 32 rpm under listed load;
- 1:168 -> 35 rpm no-load, about 25 rpm under listed load.

The same catalog family shows gearbox lengths increasing with reduction, so exact purchased SKU dimensions must be checked before machining mounts.

## PX-1 preferred candidate
Primary prototype target: **24 V, 1:131 gearbox, nominal ~45 rpm no-load**.

Reason:
- directly matches the desired 30–50 wheel-rpm range with approximately 1:1 external wheel gearing;
- avoids relying on deep PWM reduction from a much faster motor;
- gives better low-speed controllability and torque reserve than the 1:90 option;
- remains faster and less reduction-heavy than 1:168.

With 90 mm wheels and direct 1:1 external gearing:
- 45 rpm ideal no-load vehicle speed ~12.72 m/min;
- 32 rpm representative loaded speed ~9.05 m/min.

These are acceptable transit speeds; inspection speed will be reduced electronically.

## Important catalog inconsistency
Generic JGB37-520 data available online are inconsistent in listed current and torque, including suspicious repeated stall-current values. Therefore **do not use catalog stall current as a protection design input**. The exact purchased samples must be measured.

## Purchase requirements
Search for JGB37-520 with ALL of:
- 24 V winding;
- ~45 rpm output / ratio near 1:131;
- 6 mm D-shaft or documented shaft geometry compatible with replaceable pinion hub;
- metal gearbox;
- exact dimension drawing supplied by seller/manufacturer;
- preferably encoder version if the price/length penalty is modest, but wheel odometry remains independent.

## Alternate choices
- 1:90 / 66 rpm: acceptable fallback if 1:131 is unavailable; external reduction around 1.3–1.5:1 may then be considered.
- 1:168 / 35 rpm: acceptable if tests show cable drag/obstacle torque is more important than transit speed.

## Release gate
Motor mount hole pattern, pinion bore, fuse rating, current limit, contactor and final wheel gear ratio remain HOLD until at least two purchased motors are measured for rpm, running current, stall pulse current and output-shaft dimensions.
