# PX-1 Rev.GN — traction / tether / ballast screen

Status: ENGINEERING SCREEN; not release data.

## Why this revision exists
Rev.GL closed the full six-wheel drivetrain geometry and Rev.GM showed that the current body wall architecture is not obviously strength-limited. The next dominant system risk is therefore traction, especially when pulling a long tether in DN150.

The current Ø90 wheel contact point from Rev.DL/GF is approximately Y=54 mm in an R=75 mm pipe. The wall-normal vertical support factor is:

`kz = sqrt(75^2 - 54^2) / 75 = 0.69397`

Therefore, on a level pipe, the sum of wheel normal forces required to support the crawler is approximately:

`N_total = W / kz ≈ 1.441 x W`

This geometric amplification is why crawler mass can improve available longitudinal traction in a round pipe.

## Current protected drive ceiling
Until the exact Ø32 motor is bench-characterised, retain the Rev.GJ protected motor-output limit of 1.0 N.m per motor.

For screening:
- two motors;
- bevel ratio 2.5:1;
- Ø90 wheels, r=45 mm;
- deliberately conservative whole-path efficiency = 0.75.

This gives a motor-limited theoretical longitudinal force ceiling of approximately **83.3 N total** at the six wheels.

For the present 6.3–7.7 kg expected crawler mass, normal soft/high-grip tires are expected to reach the adhesion limit before this motor ceiling in most ordinary conditions. More motor torque is therefore not the current priority.

## Self-climb friction threshold
Using a placeholder rolling-resistance screen Crr=0.02, the minimum effective tire/pipe friction coefficient before any positive tether-pull reserve remains is:

- 0 deg: μ > 0.014
- 5 deg: μ > 0.075
- 10 deg: μ > 0.136
- 20 deg: μ > 0.266
- 30 deg: μ > 0.415

Important consequence: **at 30 degrees, adding ballast cannot rescue a tire/pipe pair that only achieves μ≈0.40**. The tire compound/surface must first exceed the friction threshold.

## Nominal 7 kg crawler, no ballast
Available pull after crawler grade force and a Crr=0.02 screening allowance:

### Effective tire μ = 0.40
- 0 deg: ~38.2 N
- 5 deg: ~32.1 N
- 10 deg: ~25.7 N
- 20 deg: ~12.4 N
- 30 deg: negative reserve (~-1.2 N)

### Effective tire μ = 0.50
- 0 deg: ~48.1 N
- 5 deg: ~41.9 N
- 10 deg: ~35.4 N
- 20 deg: ~21.7 N
- 30 deg: ~7.3 N

These are screening values, not guaranteed field pull.

## Tether model
The full deployed tether is conservatively modelled as sliding on the pipe floor on the same uphill grade:

`F_per_m = m' g (sin(theta) + μ_cable cos(theta))`

Two mass values are retained:
- 54 g/m: published reference for Minicam Proteus Lite 1/4-inch Kevlar reinforced cable; this is **not** declared to be the final PX-1 6-core cable mass;
- 80 g/m: internal conservative sensitivity point until the actual PX-1 tether sample is weighed.

Cable sliding coefficient is swept 0.15 / 0.20 / 0.30. Exact PUR-jacket drag in PVC, clay, concrete, water, slime and bends must be measured.

For μ_cable=0.20, nominal 7 kg crawler:

### Tire μ=0.40 — maximum ideal straight deployed length
| Uphill grade | 54 g/m tether | 80 g/m tether |
|---:|---:|---:|
| 0 deg | ~361 m | ~243 m |
| 5 deg | ~211 m | ~143 m |
| 10 deg | ~131 m | ~88 m |
| 20 deg | ~44 m | ~30 m |
| 30 deg | 0 | 0 |

### Tire μ=0.50 — maximum ideal straight deployed length
| Uphill grade | 54 g/m tether | 80 g/m tether |
|---:|---:|---:|
| 0 deg | ~454 m | ~306 m |
| 5 deg | ~276 m | ~187 m |
| 10 deg | ~181 m | ~122 m |
| 20 deg | ~77 m | ~52 m |
| 30 deg | ~21 m | ~14 m |

Real bends can increase drag sharply; a powered/synchronised reel can reduce crawler-side tension. These tables must not be used as guaranteed range.

## Wheel family decision
Current Minicam Proteus documentation is useful as an architecture sanity check:
- 90 mm soft black rubber wheels are specified for the 150 mm crawler class and described as providing improved traction in regular pipes;
- separate high-grip wheels use a hard-wearing carborundum/deep-bevel concept for wet/greasy pipes;
- carbide wheels are a separate severe-condition option;
- Minicam also offers a 2.5 kg extra weight plate specifically to increase crawler down-force/traction.

PX-1 will not copy proprietary wheel geometry, but the same system philosophy is valid.

PX-1 therefore keeps one common keyed metal wheel core with interchangeable traction variants:
1. **SR prototype tire** — compliant elastomer, normal pipe use;
2. **HG prototype tire** — more aggressive grooved/high-friction surface for wet/greasy/plastic pipe;
3. carbide/grit concept remains OPTIONAL severe-service only, because it can wear pipe surfaces and is not the default DN150 wheel.

Exact Shore hardness is deliberately NOT frozen from internet data. It will be selected from measured pull tests.

## Ballast policy
Ballast is useful only after adequate tire friction is established.

Do not permanently increase body wall thickness to gain mass. Preserve a removable low-mounted ballast provision so the same crawler can be tested in at least these states:
- 0 kg;
- +0.5 kg;
- +1.0 kg;
- +1.5 kg nominal options.

The ballast should sit low and near the longitudinal CG, be mechanically captured, have no through-hole into P0, and present a smooth snag-resistant exterior if mounted below the body.

Final ballast geometry is Rev.GO work and must pass DN150 clearance and tether/lift interference checks.

## Physical traction qualification
Build the traction test before freezing the wheel compound.

Minimum test matrix:
- pipe coupons/sections: PVC, clay/concrete if available;
- dry, wet, detergent/slime surrogate;
- SR and HG tread variants;
- ballast 0 / +0.5 / +1.0 / +1.5 kg;
- straight horizontal pull;
- 5, 10, 20, 30 degree incline where safe;
- record left/right motor current, wheel slip onset, pull force, speed and temperature.

Acceptance targets for the first prototype:
- no-load rolling test has no abnormal seal/gear drag;
- measured effective μ on normal wet pipe should target >=0.50 if practical;
- minimum static straight pull target: 40 N with normal wheel set;
- preferred high-grip straight pull target: >=50 N without exceeding protected motor/current limits;
- demonstrate 40 m actual tether before any 150 m range claim;
- 150 m deployment remains a later system qualification with real cable and reel.

## External reference used for architecture only
Minicam Proteus 2026 brochure: https://www.minicam.co.uk/wp-content/uploads/2026/02/Proteus-Brochure_UK-EN_V1.1.0_27022026.pdf

Proteus Lite cable reference: https://minicaminc.com/proteus-lite-systems/

## Next autonomous block
Rev.GO:
- model snag-resistant removable ballast provision;
- create two interchangeable Ø90 tread candidates on the current keyed core;
- preserve DN150 profile and side-cover clearance;
- generate a physical pull-test fixture concept with load-cell/spring-scale interface;
- rerun full crawler mass/CG and DN150 clearance with +1.5 kg maximum ballast.
