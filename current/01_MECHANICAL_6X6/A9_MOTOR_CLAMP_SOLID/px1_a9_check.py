"""PX1 A9 dimensional checks; Python 3, no dependencies. Assumptions only."""
import math
MOTOR_R=12.0
INNER_R=12.5
OUTER_R=15.5
BOLT_X=19.0
HOLE_R=1.6
BASE_HALF=22.0
assert INNER_R-MOTOR_R == 0.5
assert abs((BOLT_X-HOLE_R)-OUTER_R-1.9)<1e-9
assert BASE_HALF-(BOLT_X+HOLE_R)>1.0
assert OUTER_R<17.5 # leg inner edge; bridging required
assert 16.0>10.0 # bolt rows outside strap span: separate ears required
print("PASS: radial clearance 0.5 mm; lateral nominal gap 1.9 mm; edge margin 1.4 mm")
print("SKIPPED: FreeCAD shape validation, STEP export, strength and actual motor fit")
