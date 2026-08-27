# PX-1 Rev.BQ — combined camera head packaging review

Status: packaging gate, not production release.

## Combined package
The camera, complete Rev.BP TILT drive reservation, ROLL support, ROLL gearing and central rotary-transfer keep-out are now treated as one assembly.

Current hard radial target remains Ø52 mm.

The previous 72 mm cylindrical-length target is no longer credible once realistic service clearances and both drives are combined. Rev.BQ therefore changes the working length target to **78 mm**. This is preferable to hiding interferences or reducing wall/service clearance.

## ROLL
- support: 2x 6803-2RS, 17x26x5;
- gear candidate: m0.5, z17/z51, ratio 3:1;
- z51 pitch diameter 25.5 mm, outside diameter approximately 26.5 mm;
- continuous rotation requires rotary electrical transfer through the axis.

## TILT
- commanded range: -105 to +105 degrees;
- mechanical stops: approximately -108/+108 degrees;
- worm reduction: 20:1 candidate;
- separate Ø3 worm shaft with two 693 bearings retained.

## Engineering result
Diameter Ø52 remains plausible at envelope level, but length grows to 78 mm. This change must be propagated into the DN150 sweep. A static circle check is not enough: the head corners must be swept through TILT positions while the lift is in LOW and DN150_SAFE positions.

## Remaining blockers
1. exact video-rated rotary transfer dimensions;
2. solid collision sweep for TILT -105..+105;
3. lens/window and LED ring real geometry;
4. waterproof rotating boundary for ROLL;
5. cable/service routing around both motors;
6. DN150 swept-clearance result.

No machining drawing for the camera-head shell may be RELEASED until these blockers are closed.
