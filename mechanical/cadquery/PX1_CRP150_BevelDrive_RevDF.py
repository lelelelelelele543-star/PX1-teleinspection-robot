import cadquery as cq
import math

# PX-1 Rev.DF — CRP150-style traction bevel-drive packaging
# Architecture derived from uploaded Proteus drawings at system level only.
# PX-1 dimensions are independent and parametric.

BODY_L = 307.0
BODY_W = 92.0
BODY_H = 76.0
BODY_Z0 = 14.0

DRIVE_X = 150.0
DRIVE_Z = 45.0
MOTOR_Y = 21.0
MOTOR_D = 37.0
MOTOR_L = 85.0

BEVEL_MODULE = 1.0
PINION_TEETH = 16
GEAR_TEETH = 40
PINION_PD = BEVEL_MODULE * PINION_TEETH
GEAR_PD = BEVEL_MODULE * GEAR_TEETH
FACE = 8.0

# Packaging envelopes include 2 mm radial allowance beyond pitch radius.
PINION_R_ENV = PINION_PD / 2.0 + 2.0
BIG_R_ENV = GEAR_PD / 2.0 + 2.0

assy = cq.Assembly(name='PX1_CRP150_BevelDrive_RevDF')

body = (cq.Workplane('XY')
        .box(BODY_L, BODY_W, BODY_H)
        .translate((BODY_L/2.0, 0, BODY_Z0 + BODY_H/2.0)))
assy.add(body, name='PressureBody_Envelope')

for side, sy in [('L', +1), ('R', -1)]:
    y = sy * MOTOR_Y

    # Motor can, longitudinal axis X. Exact JGB37-520 vendor length remains HOLD.
    motor = (cq.Workplane('YZ')
             .center(y, DRIVE_Z)
             .circle(MOTOR_D/2.0)
             .extrude(MOTOR_L)
             .translate((55.0, 0, 0)))
    assy.add(motor, name=f'JGB37_520_{side}_Envelope')

    # Small bevel pinion envelope on the motor/output axis.
    pinion = (cq.Workplane('YZ')
              .center(y, DRIVE_Z)
              .circle(PINION_R_ENV)
              .extrude(FACE)
              .translate((140.0, 0, 0)))
    assy.add(pinion, name=f'BevelPinion_Z16_{side}_Envelope')

    # Large bevel gear envelope on the transverse half-shaft.
    large = (cq.Workplane('XZ')
             .center(DRIVE_X, DRIVE_Z)
             .circle(BIG_R_ENV)
             .extrude(sy * FACE)
             .translate((0, y, 0)))
    assy.add(large, name=f'BevelGear_Z40_{side}_Envelope')

# Middle-wheel half-shaft envelopes show how each bevel stage feeds one side bay.
for side, sy in [('L', +1), ('R', -1)]:
    shaft = (cq.Workplane('XZ')
             .center(DRIVE_X, DRIVE_Z)
             .circle(5.0)
             .extrude(sy * (BODY_W/2.0 - MOTOR_Y + 12.0))
             .translate((0, sy*MOTOR_Y, 0)))
    assy.add(shaft, name=f'MiddleDriveHalfShaft_{side}_OD10')

# Deterministic packaging checks.
MOTOR_CLEAR = 2.0*MOTOR_Y - MOTOR_D
BIG_Z_MIN = DRIVE_Z - BIG_R_ENV
BIG_Z_MAX = DRIVE_Z + BIG_R_ENV
BIG_X_MIN = DRIVE_X - BIG_R_ENV
BIG_X_MAX = DRIVE_X + BIG_R_ENV
MOTOR_SIDE_EXTENT = MOTOR_Y + MOTOR_D/2.0

assert MOTOR_CLEAR >= 5.0 - 1e-9
assert BIG_Z_MIN >= BODY_Z0
assert BIG_Z_MAX <= BODY_Z0 + BODY_H
assert MOTOR_SIDE_EXTENT <= BODY_W/2.0 - 4.0
assert BIG_X_MIN > 0 and BIG_X_MAX < BODY_L

print('PX-1 Rev.DF bevel packaging')
print('bevel ratio:', GEAR_TEETH/PINION_TEETH)
print('motor can clearance:', MOTOR_CLEAR, 'mm')
print('large bevel envelope Z:', BIG_Z_MIN, '..', BIG_Z_MAX, 'mm')
print('large bevel envelope X:', BIG_X_MIN, '..', BIG_X_MAX, 'mm')
print('motor side extent:', MOTOR_SIDE_EXTENT, 'mm from centerline')
print('PASS')

assy.save('PX1_CRP150_BevelDrive_RevDF.step')
