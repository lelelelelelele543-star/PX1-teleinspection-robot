# PX-1 Rev.CV — CRP150 reference baseline

Status: design reference baseline. This does NOT copy proprietary manufacturing geometry; it freezes the external architecture and service philosophy PX-1 should emulate.

## Primary reference
Mini-Cam Proteus CRP150, especially the six-wheel crawler configuration with manual camera elevator, CAM026-class pan/rotate camera, heavy-duty rear connector, quick-change wheels and pressurised body.

## Verified CRP150 reference facts from official/industry documentation
- six-wheel steerable crawler architecture;
- pipe range: 150–600 mm; up to 1000 mm with crawler cradle;
- standard wheel set: 6 x 90 mm rubber wheels;
- manual elevator; published range approximately 70–257 mm;
- weight approximately 9.25 kg;
- body envelope in Proteus manual: approximately 307 x 133 x 110 mm;
- internal overpressure specification: 1 bar in the Proteus manual;
- heavy-duty rear connector;
- quick-change wheel lock;
- in-built lowering device;
- inclination sensor;
- optional auxiliary light/backeye;
- CAM026-class camera: continuous 360 deg rotation and +/-135 deg pan.

## PX-1 visual/mechanical direction from Rev.CV onward
PX-1 must look and package like a compact professional CRP150-class crawler, not like a generic military UGV or a rectangular hobby robot.

Required external architecture:
1. six wheels total, three per side;
2. long, low, narrow central sealed body;
3. wheels close to the body and partially overlapping the visual body height;
4. manual multi-link/parallelogram camera elevator rising from the top/front-central region;
5. cylindrical pan/rotate camera head mounted at the top of the elevator;
6. rear heavy-duty tether connector aligned with crawler longitudinal axis;
7. compact lowering eye/handle integrated into crawler body;
8. service covers flush or near-flush with the main body;
9. no external antennas, decorative bumpers, exposed hobby modules or vehicle-style bodywork;
10. industrial metal finish with replaceable wheel and seal hardware.

## PX-1 deviations allowed/required
- internal electronics, motors, communication and video system may be modernised;
- PX-1 will use modern digital video rather than legacy CVBS;
- long tether communication may use SPE/10BASE-T1L or another validated modern copper-link solution;
- body and cover geometry must be original and manufacturable with available machines;
- purchased motors, bearings, seals and electronics should be inexpensive, robust and field-replaceable;
- side transmission covers are sealed with O-rings and participate in the pressurised dry volume;
- pressurisation is retained as a core design feature.

## Superseded visual concepts
Any prior PX-1 image/model concept showing:
- four wheels only;
- eight or more wheels;
- military rover styling;
- antennas;
- E-stop button mounted on the crawler;
- large boxy external electronics housings;
- non-CRP150-like camera support
is obsolete for external-layout development.

## Next CAD gate
Create a new six-wheel CRP150-class packaging master using PX-1-owned dimensions and hardware. First pass should target a body envelope near the CRP150 class (roughly 300 x 130 x 110 mm) and six Ø90 wheels, then validate DN150 clearance before dimensions are frozen.
