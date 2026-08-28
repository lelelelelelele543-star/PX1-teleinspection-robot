# PX1-TP-020 — traction / wheel / ballast / tether qualification

Status: prototype test procedure.

## Purpose
Calibrate the Rev.GN analytical model with real PX-1 hardware before wheel compound, ballast quantity or 150 m tether capability is frozen.

## Test article
Use the complete six-wheel drivetrain with:
- all six Ø90 wheels installed;
- pressure/seal stack assembled as intended for the prototype;
- current protected motor-current/torque limit active;
- real tether tail mechanical load path installed;
- representative crawler mass and camera/lift mass.

## Pipe fixtures
Minimum:
1. actual or representative DN150 PVC section;
2. clay/concrete section if available later.

Recommended useful length: >=1.5 m for static pull/slip tests and longer for rolling-current tests.

The test section should be mountable at 0, 5, 10, 20 and 30 degrees. Do not conduct high-angle pull tests with unsecured hanging masses or an unsecured crawler.

## Force measurement
Preferred:
- inline force gauge/load cell, 0–100 N minimum useful range, mounted on the structural rear tether anchor/load path.

Acceptable low-cost cross-check:
- low-friction pulley and known hanging masses, where 1 kg hanging mass ≈9.81 N.

Do not attach the test load to the electrical connector or camera lift.

## Test surfaces
For every candidate wheel set:
- clean/dry;
- clean/wet;
- wet + mild detergent film as repeatable low-grip surrogate;
- real slime/mud only as a later field test because repeatability is poor.

## Wheel variants
A. Rev.GO SR compliant/smooth prototype.
B. Rev.GO HG 18-slot prototype with the same external DN150 envelope.
C. Later abrasive/high-grip insert only if A/B are insufficient.

Exact Shore hardness/material is intentionally a test variable, not a frozen drawing value.

## Ballast states
- 0 plates;
- 1 plate, approximately +0.49 kg;
- 2 plates, approximately +0.98 kg;
- 3 plates, approximately +1.47 kg.

Record actual measured crawler mass for each state.

## Test 1 — free rolling resistance
Traction motors disabled/unpowered.
Pull the complete crawler axially at slow approximately constant speed and record force.

Run in both directions at least 3 times.

This replaces the Rev.GN placeholder Crr=0.02 with measured whole-crawler drag including:
- wheel seals;
- bearings;
- gear train;
- wheel deformation.

Equivalent level-pipe rolling coefficient for the model:

`Crr_eff = F_roll / (m g)`

Keep raw force as the primary result; Crr_eff is only a convenient model parameter.

## Test 2 — static/slow traction limit
Anchor the structural rear load point to the force gauge.
Command both drive sides forward with a slow speed ramp.
Increase commanded force/current until one of these occurs:
- stable wheel slip;
- protected current/torque ceiling;
- mechanical/thermal limit.

Record the maximum stable pull for at least 3 runs.

For a level pipe, approximate effective tire coefficient:

`mu_eff = (F_pull + F_roll) * kz / (m g)`

where Rev.GN contact geometry gives `kz = 0.69397`.

## Test 3 — incline traction
Repeat with the pipe at 5, 10, 20 and 30 degrees where safe.

Approximate effective tire coefficient:

`mu_eff = (F_pull + m g sin(theta) + F_roll(theta)) * kz / (m g cos(theta))`

A 30-degree test is meaningful only if the crawler can safely be caught mechanically after loss of grip.

## Test 4 — steering/skid current
On horizontal DN150:
- command left/right equal forward;
- gentle differential turn;
- zero-radius counter-rotation only for a short controlled test.

Record motor current per side and pressure/temperature. The skid-turn load can exceed straight-line rolling load and must be represented in current-limit tuning.

## Test 5 — real 40 m tether
Only after tests 1–4 pass:
- connect actual 40 m PX-1 tether;
- deploy it through the intended guide/reel arrangement;
- measure rear-anchor tension at 10, 20, 30 and 40 m;
- record crawler speed and left/right current;
- repeat at minimum on level wet pipe and one modest incline.

Do not extrapolate 40 m results linearly through bends without a separate bend-drag test.

## Test 6 — tether sliding coefficient
With crawler removed, pull a known straight length of actual tether through the same pipe at constant low speed.
Measure drag force and cable mass per metre.

For level pipe, first-order:

`mu_cable_eff = F_drag / (m_tether g)`

Repeat dry and wet. This directly replaces the Rev.GN assumed 0.15/0.20/0.30 sweep with measured values.

## Initial acceptance targets
These are prototype engineering targets, not customer specification:
- normal wet wheel set: target >=40 N stable level pull;
- preferred normal/high-grip result: >=50 N stable level pull without exceeding protected current limit;
- no abnormal seal/bearing temperature after repeated pulls;
- left/right pull/current asymmetry investigated if >15%;
- 40 m tether deployment must complete without connector load, unstable wheel slip or uncontrolled current rise.

## Data to save
For every run record:
- wheel material/version;
- surface state;
- crawler mass/ballast;
- incline;
- pull force;
- left/right current;
- speed;
- wheel slip yes/no;
- motor/driver temperature;
- P0/P1/P2 pressure before/after;
- tether deployed length where applicable.

## Release rule
No claim of 100–150 m operational capability until the actual tether mass and drag are measured and a representative long deployment is completed with the real reel/guide arrangement.
