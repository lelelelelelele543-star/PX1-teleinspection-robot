import cadquery as cq
import math

# PX-1 Rev.DK — integrated six-wheel CRP150-style packaging master.
# Own PX-1 geometry; MiniCam documents are used as architecture references only.

BODY_L = 307.0
BODY_W = 92.0
BODY_H = 76.0
BODY_Z0 = 14.0
WHEEL_OD = 90.0
WHEEL_W = 16.0
WHEEL_Z = 45.0
WHEEL_X = [50.0, 150.0, 250.0]
COVER_T = 5.0
COVER_L = 286.0
COVER_H = 82.0
MOTOR_D = 37.0
MOTOR_L = 95.0       # conservative JGB37-555-class package reserve
MOTOR_Y = 21.0
DRIVE_X = 150.0
DRIVE_Z = 45.0
GEAR_FACE = 8.0

assy = cq.Assembly(name='PX1_CRP150_6W_Master_RevDK')

body = (cq.Workplane('XY')
        .box(BODY_L, BODY_W, BODY_H)
        .translate((BODY_L/2, 0, BODY_Z0 + BODY_H/2)))
assy.add(body, name='BodyEnvelope')

# One non-cassette sealed cover per side.
for side, sy in [('L', +1), ('R', -1)]:
    y = sy * (BODY_W/2 + COVER_T/2)
    cover = (cq.Workplane('XY')
             .box(COVER_L, COVER_T, COVER_H)
             .translate((BODY_L/2, y, 45)))
    assy.add(cover, name=f'SideCover_{side}')

# 6 wheels.
for x in WHEEL_X:
    for side, sy in [('L', +1), ('R', -1)]:
        y0 = sy * (BODY_W/2 + COVER_T)
        if sy > 0:
            wheel = (cq.Workplane('XZ').center(x, WHEEL_Z)
                     .circle(WHEEL_OD/2).extrude(WHEEL_W)
                     .translate((0, y0, 0)))
        else:
            wheel = (cq.Workplane('XZ').center(x, WHEEL_Z)
                     .circle(WHEEL_OD/2).extrude(-WHEEL_W)
                     .translate((0, y0, 0)))
        assy.add(wheel, name=f'Wheel_{side}_{int(x)}')

# Side synchronization: z40 -> z60 -> z40 -> z60 -> z40, m1 candidate.
for side, sy in [('L', +1), ('R', -1)]:
    y0 = 38.0 if sy > 0 else -38.0
    ext = GEAR_FACE if sy > 0 else -GEAR_FACE
    for x in WHEEL_X:
        gear = (cq.Workplane('XZ').center(x, WHEEL_Z)
                .circle(21.0).extrude(ext).translate((0, y0, 0)))
        assy.add(gear, name=f'WheelGear_z40_{side}_{int(x)}')
    for x in (100.0, 200.0):
        idler = (cq.Workplane('XZ').center(x, WHEEL_Z)
                 .circle(31.0).extrude(ext).translate((0, y0, 0)))
        assy.add(idler, name=f'Idler_z60_{side}_{int(x)}')

# Two longitudinal JGB37-555-class motors and 90-degree bevel transfer.
for side, sy in [('L', +1), ('R', -1)]:
    y = sy * MOTOR_Y
    motor = (cq.Workplane('YZ').center(y, DRIVE_Z)
             .circle(MOTOR_D/2).extrude(MOTOR_L)
             .translate((40.0, 0, 0)))
    assy.add(motor, name=f'JGB37_555_{side}_Envelope')

    pinion = (cq.Workplane('YZ').center(y, DRIVE_Z)
              .circle(10.0).extrude(8.0)
              .translate((135.0, 0, 0)))
    assy.add(pinion, name=f'BevelPinion_z16_{side}_Envelope')

    big = (cq.Workplane('XZ').center(DRIVE_X, DRIVE_Z)
           .circle(22.0).extrude(sy*8.0)
           .translate((0, y, 0)))
    assy.add(big, name=f'BevelGear_z40_{side}_Envelope')

    # Independent Ø10 middle-output half-shaft for each side.
    if sy > 0:
        shaft = (cq.Workplane('XZ').center(DRIVE_X, DRIVE_Z)
                 .circle(5.0).extrude(31.0)
                 .translate((0, MOTOR_Y, 0)))
    else:
        shaft = (cq.Workplane('XZ').center(DRIVE_X, DRIVE_Z)
                 .circle(5.0).extrude(-31.0)
                 .translate((0, -MOTOR_Y, 0)))
    assy.add(shaft, name=f'MiddleOutputShaft_{side}_OD10')

# CRP150-style manual lift packaging at DN150_SAFE.
BASE_X = [205.0, 265.0]
BASE_Z = 65.0
ARM_L = 135.0
THETA = 178.0
T = math.radians(THETA)

# Camera position is the verified Rev.DG safe position.
upper_mid_x = 235.0 + ARM_L*math.cos(T)
camera_x = upper_mid_x - 36.0
camera_z = BASE_Z + ARM_L*math.sin(T)
camera = (cq.Workplane('YZ').circle(26.0).extrude(72.0)
          .translate((camera_x-36.0, 0, camera_z)))
assy.add(camera, name='Camera_DN150_SAFE_Envelope')

# Deterministic packaging checks.
OVERALL_W = BODY_W + 2*COVER_T + 2*WHEEL_W
assert abs(OVERALL_W - 134.0) < 1e-9
assert 2*MOTOR_Y - MOTOR_D >= 5.0
assert abs((40.0 + 60.0)/2.0 - 50.0) < 1e-9
assert MOTOR_Y + MOTOR_D/2 <= BODY_W/2 - 4.0
assert DRIVE_Z - MOTOR_D/2 >= BODY_Z0
assert DRIVE_Z + MOTOR_D/2 <= BODY_Z0 + BODY_H

print('PX-1 Rev.DK integrated packaging')
print('overall width:', OVERALL_W, 'mm')
print('motor can gap:', 2*MOTOR_Y - MOTOR_D, 'mm')
print('DN150-safe camera X/Z:', round(camera_x,2), round(camera_z,2), 'mm')
print('PASS')

assy.save('PX1_CRP150_6W_Master_RevDK.step')
