# A0 — 6×6 DRIVETRAIN BENCH

Purpose: prove the mandatory Rev.A transmission before final crawler body release.

## Frozen geometry/topology
- 3 wheel stations per side: X50 / X150 / X250.
- 5 × m1 Z50 per side: X50 / X100 / X150 / X200 / X250.
- Rear X250 long axle is the driven wheel station.
- One traction motor per side, two total.
- Motor input: Z16 -> Z40 bevel pair -> rear long axle -> Z50 train.

## Current blockers to resolve first
1. Exact motor installation envelope and mount. The current BOM motor candidate is not automatically released merely because a manufacturer STEP exists.
2. Exact matched Z16/Z40 bevel pair geometry and mounting distance.
3. Exact shaft shoulders/spacers so bearings cannot preload incorrectly or walk axially.
4. Gear width/backlash/cover clearance.

The final 90 mm tire profile is NOT required to prove A0. A0 may use shaft outputs or simple temporary wheel discs as long as the real shaft/bearing/gear positions are unchanged.

## Bench article
Build two mirrored side-drive test chains or one reusable fixture that can prove both sides with production-intent shaft centers.

Required hardware for test:
- 2 traction motors only after mount compatibility is locked;
- 2 × Z16;
- 2 × Z40;
- 10 × Z50;
- rear long axles and wheel/idler shafts;
- all bearings/bushings used by the side-drive chain;
- temporary rigid side plates preserving exact shaft centres;
- traction drivers and current measurement.

## Test sequence
1. Hand-turn with motor disconnected: full train must rotate without tight spots.
2. Low-voltage powered rotation: left and right separately.
3. Nominal-voltage no-load run.
4. Forward/reverse cycling.
5. Add representative output resistance/load.
6. Run both sides simultaneously.
7. Inspect tooth contact, bearing temperature, shaft movement and fastener loosening.

## Record
For every run record:
- supply voltage;
- idle and loaded current per motor;
- direction;
- run duration;
- noise/vibration observations;
- gear/bearing temperature observation;
- any visible tooth/shaft movement;
- exact hardware revision used.

## PASS
A0 passes only when both sides run forward/reverse without binding, tooth collision, shaft walk or bearing displacement and the selected motor mounting is physically reproducible.

A CAD export alone cannot close A0.
