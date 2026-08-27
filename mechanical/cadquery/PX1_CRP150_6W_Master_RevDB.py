import cadquery as cq
from cadquery import exporters
import math

# PX-1 Rev.DB — verified packaging master
# CRP150-style six-wheel architecture, own PX-1 geometry.

BODY_L=307.0
BODY_W=92.0
BODY_H=76.0
BODY_Z0=14.0
COVER_T=5.0
WHEEL_OD=90.0
WHEEL_W=16.0
WHEEL_Z=45.0
WHEEL_X=[50.0,150.0,250.0]

assy=cq.Assembly(name='PX1_RevDB')

body=(cq.Workplane('XY')
      .box(BODY_L,BODY_W,BODY_H)
      .translate((BODY_L/2,0,BODY_Z0+BODY_H/2)))
assy.add(body,name='PressureBody')

for side,sy in [('L',1),('R',-1)]:
    y=sy*(BODY_W/2+COVER_T/2)
    cover=(cq.Workplane('XY')
           .box(276,COVER_T,82)
           .translate((153.5,y,45)))
    assy.add(cover,name=f'SideCover_{side}')

for x in WHEEL_X:
    for side,sy in [('L',1),('R',-1)]:
        y0=sy*(BODY_W/2+COVER_T)
        if sy>0:
            wheel=(cq.Workplane('XZ').center(x,WHEEL_Z)
                   .circle(WHEEL_OD/2).extrude(WHEEL_W)
                   .translate((0,y0,0)))
        else:
            wheel=(cq.Workplane('XZ').center(x,WHEEL_Z)
                   .circle(WHEEL_OD/2).extrude(-WHEEL_W)
                   .translate((0,y0,0)))
        assy.add(wheel,name=f'Wheel_{side}_{int(x)}')

# Two Ø37 x 85 mm motor envelopes, longitudinal and vertically staggered.
# The center distance is >37 mm, leaving non-zero clearance between motor cans.
MOTORS=[('L',+17.5,61.0,108.0),('R',-17.5,43.0,108.0)]
for side,y,z,x0 in MOTORS:
    motor=(cq.Workplane('YZ').center(y,z)
           .circle(18.5).extrude(85)
           .translate((x0,0,0)))
    assy.add(motor,name=f'JGB37_520_{side}_Envelope')

# CRP150-style manual lift base packaging envelope
lift_base=(cq.Workplane('XY').box(105,54,8)
           .translate((144.5,0,BODY_Z0+BODY_H+4)))
assy.add(lift_base,name='ManualLift_Base_Envelope')

# Low camera-head envelope only; detailed head is maintained separately.
cam=(cq.Workplane('YZ').circle(26).extrude(72)
     .translate((108,0,103)))
assy.add(cam,name='CameraHead_LOW_Envelope')

# Export when executed locally.
assy.save('PX1_CRP150_6W_Master_RevDB.step')

# Deterministic sanity checks
OVERALL_W=BODY_W+2*COVER_T+2*WHEEL_W
FOOTPRINT=(max(WHEEL_X)+WHEEL_OD/2)-(min(WHEEL_X)-WHEEL_OD/2)
MOTOR_CD=math.hypot(17.5-(-17.5),61.0-43.0)
MOTOR_CLEAR=MOTOR_CD-37.0

assert OVERALL_W < 150.0
assert FOOTPRINT <= BODY_L
assert MOTOR_CLEAR > 2.0
assert BODY_Z0 <= (43.0-18.5)
assert (61.0+18.5) <= (BODY_Z0+BODY_H)

print('PX-1 Rev.DB packaging checks')
print('overall width:',OVERALL_W,'mm')
print('wheel footprint:',FOOTPRINT,'mm')
print('motor center distance:',round(MOTOR_CD,3),'mm')
print('motor can clearance:',round(MOTOR_CLEAR,3),'mm')
print('body top:',BODY_Z0+BODY_H,'mm')
print('PASS')
