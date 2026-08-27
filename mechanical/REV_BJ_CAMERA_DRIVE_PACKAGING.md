# PX-1 Rev.BJ — TILT/ROLL drive packaging

Status: packaging verification, not machining release.

## Current real-part envelopes
- camera: RunCam Phoenix 2 class, 19x19x20 mm;
- roll support: 2x 6803-2RS, 17x26x5 mm;
- TILT motor: GM12-N20 class, 12 V, target 30–60 rpm;
- ROLL motor: same GM12-N20 class for spare-parts commonality;
- rotary transfer: Ø12.5 mm prototype keep-out only; final CVBS-capable controlled-impedance transfer remains HOLD.

## Packaging limit
- camera-head outside diameter: <=52 mm;
- cylindrical package length target: <=72 mm;
- nominal shell clearance around purchased envelopes: >=1.0 mm;
- internal non-contact clearance: >=0.5 mm.

## Reduction concept
First mechanical candidate is small external spur gearing, module 0.5, 20° pressure angle.
- TILT: 2:1 to 3:1 additional reduction after N20 gearbox;
- ROLL: approximately 2:1 after N20 gearbox.

These ratios are deliberately not frozen. Actual output torque, backlash, camera-head inertia and motor current must be measured on the selected motors first.

## Important correction
The two 6803 bearings alone do not solve waterproof continuous ROLL. They only support the rotating member. Final design still needs a sealed rotary boundary and a video-compatible rotary electrical path. Do not machine the final head body from this packaging study.

## Next gate
1. select exact N20 SKU and obtain dimensions/current/torque;
2. calculate required TILT holding torque including worst-case eccentric camera mass;
3. decide whether worm reduction or positive brake is needed for TILT;
4. select video rotary transfer;
5. generate actual m=0.5 gear pair and collision-check through full TILT range;
6. re-run DN150 clearance using the resulting solid geometry.
