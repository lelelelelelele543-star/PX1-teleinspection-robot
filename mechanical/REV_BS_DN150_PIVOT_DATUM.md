# PX-1 Rev.BS — lift pivot datum for DN150 verification

Status: candidate geometry for the next full sweep, not machining release.

## Coordinate convention
- X: longitudinal, rear body face = 0, front body face = 250 mm;
- Z: vertical from wheel-contact plane;
- Y: lateral from crawler centerline.

With nominal Ø90 wheels, wheel-axis height above the contact plane is 45 mm.

## Candidate lift pivot
To close the previously unresolved DN150 geometry, the front lift base pivot is now placed at:
- X = 250.0 mm;
- Z = 66.0 mm;
- second parallelogram pivot = 42.0 mm above it;
- link length = 68.0 mm.

This is a CAD candidate chosen to keep the lift base on the front-cover plane while leaving room below for the body and above for the head. It is not yet a released drilling coordinate.

## Sweep requirement
The combined Rev.BQ head Ø52 x 78 mm must be checked in LOW and DN150_SAFE positions through TILT -105..+105 degrees at 2-degree increments.

PASS criterion: minimum nominal clearance to the DN150 inner wall >=3.0 mm at every sampled angle, including the head ends/corners and all fixed lift links.

HIGH position is intentionally excluded from DN150 compliance.

## Release gate
Before the pivot holes are released to machining:
1. perform full solid sweep using actual head/lift solids, not cylinder envelopes only;
2. confirm nominal Ø90 wheel contact geometry inside a true Ø150 pipe section;
3. check cover, link and fastener interference;
4. print 1:1 front/lift mock-up and physically place it in a Ø150 ring/pipe gauge;
5. freeze pivot drilling coordinates only after CAD and physical checks agree.
