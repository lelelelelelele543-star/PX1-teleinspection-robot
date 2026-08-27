# PX-1 Rev.BF — manual camera lift kinematics

Status: KINEMATIC CANDIDATE, not machining release.

## Candidate geometry
- four-bar/parallelogram architecture;
- link length: 68 mm;
- base pivot spacing: 42 mm;
- link section target: 12 x 5 mm;
- pivot diameter target: 6 mm;
- symmetric left/right links;
- three positive manual positions: LOW / DN150_SAFE / HIGH.

## Candidate detent angles
Referenced from the body-top plane:
- LOW: 8 deg
- DN150_SAFE: 28 deg
- HIGH: 48 deg

These angles are only kinematic starting points. Final lock-hole positions must come from the complete assembly with the real camera-head envelope.

## Pivot hardware direction
Preferred field-serviceable arrangement:
- M6 shoulder screws where purchasable, or Ø6 stainless pins;
- replaceable polymer (POM/iglidur type) or oil-impregnated bronze bushings;
- no plain aluminium-on-stainless pivot surface;
- all pivot fasteners accessible from outside with normal hex tools;
- retainers must not rely only on threadlocker.

## Manual locking
Every operating height requires positive mechanical locking. Friction alone is prohibited. Target is one-hand operation: lift with one hand, automatic or thumb-operated detent engagement, then confirm lock before driving.

## DN150 validation rule
The name `DN150_SAFE` is provisional until the complete robot is checked inside an actual Ø150 mm circular envelope including:
- Ø90 wheels;
- body;
- lift arms;
- camera carrier;
- final TILT/ROLL head;
- lighting;
- fastener heads and guards;
- manufacturing tolerances.

Minimum design clearance to pipe wall at the validated DN150 position should be 3 mm nominal where practical, excluding intentional wheel contact. The final value will be frozen only after the camera dimensions are fixed.

## Next gates
1. define final camera-head outer envelope;
2. add Ø150 pipe-section clearance checker in FreeCAD;
3. select exact M6 pivot hardware/bushings;
4. calculate link bending with camera mass and impact factor;
5. design locking plate/detent pin;
6. check one-hand motion and finger clearance with printed prototype.
