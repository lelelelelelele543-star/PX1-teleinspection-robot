# PX-1 Rev.DI — traction motor candidate after CRP150 bevel-stage correction

Status: **preferred prototype candidate**, not production freeze.

## Decision
The previous JGB37-520 ~45 rpm / ~107 rpm variants are no longer the preferred traction baseline.

For the six-wheel CRP150-style architecture with a 2.5:1 bevel input stage, use the stronger **JGB37-555, 24 V, gearbox ratio approximately 56:1** class as the prototype target.

Nominal published family data for this class are approximately:
- no-load speed: 107 rpm;
- rated speed: 76 rpm;
- rated torque: about 8–8.4 kgf·cm ≈ 0.78–0.82 N·m;
- rated current: vendor-dependent, around 0.65–0.9 A;
- stall torque: around 32 kgf·cm ≈ 3.14 N·m;
- stall current: vendor data disagree substantially (roughly 3–6.5 A reported), therefore **must be measured on the exact purchased sample**.

## Output after bevel reduction
Reference/adapted bevel ratio: Z16 -> Z40 = 2.5:1.

Assuming 90% bevel efficiency:
- no-load wheel/distribution speed ≈ 107 / 2.5 = 42.8 rpm;
- rated distribution speed ≈ 76 / 2.5 = 30.4 rpm;
- ideal Ø90 no-load linear speed ≈ 12.1 m/min;
- ideal rated linear speed ≈ 8.6 m/min;
- rated side torque after bevel ≈ 0.80 × 2.5 × 0.90 ≈ **1.8 N·m**;
- short theoretical stall torque after bevel ≈ 3.14 × 2.5 × 0.90 ≈ **7.1 N·m**.

This is much closer to the traction requirement than the lighter JGB37-520 107 rpm examples, while still fitting the Ø37 gearbox class.

## Why ratio 56 is the current sweet spot
- faster ratios reduce available torque too much;
- ratio 90 plus the 2.5:1 bevel stage makes the crawler unnecessarily slow;
- ratio 56 gives useful inspection speed while putting approximately 1.8 N·m rated torque into each complete three-wheel side train before side-train losses.

## Purchase requirements
Prototype samples shall be:
- JGB37-555 family;
- 24 V winding;
- 56:1 gearbox, approximately 107 rpm no-load;
- metal gearbox;
- output shaft geometry measured before the pinion bore is released;
- Hall encoder preferred if a reliable vendor version is available, but output-shaft/wheel sensing remains the authoritative odometry channel.

Buy at least 3 samples from the same lot if practical: 2 installed + 1 spare/test motor.

## Incoming bench test
For every sample record:
1. gearbox and body dimensions;
2. shaft diameter/flat/length;
3. no-load current at 24.0 V;
4. no-load rpm;
5. rated-like load current and rpm;
6. controlled short stall current pulse;
7. temperature after 30 min duty cycle;
8. gearbox backlash;
9. acoustic/mechanical abnormality;
10. encoder pulse count if fitted.

## Electrical consequence
Until stall current is measured:
- BTS7960 remains prototype-only;
- per-side fuse value remains HOLD;
- 24 V DC/DC continuous/peak power remains HOLD;
- contactor/current sensor final ratings remain HOLD.

The power system shall be designed so a jam is interrupted electronically before the wiring fuse operates.
