# PX-1 Rev.BB — main pressure-body architecture

Status: DRAWING-CANDIDATE envelope, not production release.

## Envelope
- external: 250 x 94 x 76 mm
- material target: EN AW-6082 T6 aluminium; 6061-T6 acceptable alternate subject to stock/machining availability
- side walls: 6 mm prototype
- top wall: 6 mm prototype
- bottom wall: 8 mm prototype for impact/fastener margin
- front/rear end lands: 12 mm

## Architecture
The crawler electronics and motors live in one dry central pressure body. Routine external drivetrain service must not require opening this volume.

Rear dynamic shaft sealing remains modular: two PX1-DR-002 carrier modules with PX1-DR-001 shafts. The pressure body itself therefore does not contain a directly machined rotary-seal lip seat.

## End covers
Both end covers will be removable, piloted and O-ring sealed. Fasteners remain outside the O-ring sealing line wherever practical. Cover geometry is intentionally not frozen in Rev.BB because camera/lift front interfaces and tether-tail rear interfaces must be integrated first.

## Manufacturing intent
Preferred route for first article: machine from aluminium billet/block or thick-wall custom blank. Welded pressure-body seams are not preferred for the first prototype because they add distortion and leak paths.

## Pressure rule
0.5 bar gauge is a prototype proof-test ceiling currently used for the sealing development fixture, not a certified operating pressure. Final allowable pressure requires completed body geometry, fastener pattern, material certificate/stock condition, engineering check and proof test.

## Next CAD gates
1. rear cover with tether quick-release interface;
2. front cover with camera/lift service interface;
3. two rear carrier bores and PCD54 mounting patterns at rear axle station;
4. internal motor/NUCLEO/driver/DC-DC keep-out volumes;
5. wall/fastener interference check;
6. mass and center-of-gravity estimate.
