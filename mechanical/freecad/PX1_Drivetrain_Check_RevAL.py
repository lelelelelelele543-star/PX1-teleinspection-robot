import FreeCAD as App, Part
from PX1_Master_Parameters import *

# Geometry-only interference and center-distance assembly check.
# Uses pitch/OD cylinders so the center chain can be verified independently of tooth details.

doc=App.newDocument('PX1_Drivetrain_Check_RevAL')

# body envelope
body=doc.addObject('Part::Feature','Body')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H)
body.ViewObject.Transparency=80

# wheel envelopes
for side,y0 in [('L',-WHEEL_W),('R',BODY_W)]:
    for pos,x in [('F',FRONT_AXLE_X),('R',REAR_AXLE_X)]:
        w=doc.addObject('Part::Feature',f'Wheel_{side}_{pos}')
        w.Shape=Part.makeCylinder(WHEEL_D/2,WHEEL_W,App.Vector(x,y0,AXLE_Z),App.Vector(0,1,0))

# side gear train: five z40 centers, 40mm pitch spacing
for side,y0 in [('L',-12),('R',BODY_W+12)]:
    xs=[FRONT_AXLE_X+i*SIDE_CENTER for i in range(5)]
    for i,x in enumerate(xs):
        g=doc.addObject('Part::Feature',f'SideGear_{side}_{i}')
        od=(SIDE_Z+2)*GEAR_MODULE
        g.Shape=Part.makeCylinder(od/2,8,App.Vector(x,y0,AXLE_Z),App.Vector(0,1,0))
        g.addProperty('App::PropertyLength','CenterX','Check').CenterX=x

# rear reduction center and motor pinion center in XY reference plane
# z18/z30 center distance = m*(18+30)/2 = 24mm
center = GEAR_MODULE*(PINION_Z+REDUCTION_Z)/2.0
for side,y0 in [('L',8),('R',BODY_W-8)]:
    red=doc.addObject('Part::Feature',f'Reduction_{side}')
    red.Shape=Part.makeCylinder((REDUCTION_Z+2)*GEAR_MODULE/2,8,App.Vector(REAR_AXLE_X,y0,AXLE_Z),App.Vector(0,1,0))
    pin=doc.addObject('Part::Feature',f'Pinion_{side}')
    pin.Shape=Part.makeCylinder((PINION_Z+2)*GEAR_MODULE/2,8,App.Vector(REAR_AXLE_X-center,y0,AXLE_Z),App.Vector(0,1,0))

# engineering checks
checks=doc.addObject('App::FeaturePython','Checks')
checks.addProperty('App::PropertyLength','ComputedWheelbase','Geometry').ComputedWheelbase=REAR_AXLE_X-FRONT_AXLE_X
checks.addProperty('App::PropertyLength','SideGearChainLength','Geometry').SideGearChainLength=4*SIDE_CENTER
checks.addProperty('App::PropertyLength','MotorMeshCenter','Geometry').MotorMeshCenter=center
checks.addProperty('App::PropertyString','WheelbaseStatus','Status').WheelbaseStatus='PASS' if abs((REAR_AXLE_X-FRONT_AXLE_X)-WHEELBASE)<1e-6 else 'FAIL'
checks.addProperty('App::PropertyString','SideChainStatus','Status').SideChainStatus='PASS' if abs(4*SIDE_CENTER-WHEELBASE)<1e-6 else 'FAIL'
checks.addProperty('App::PropertyString','MotorMeshStatus','Status').MotorMeshStatus='PASS' if abs(center-MOTOR_REDUCTION_CENTER)<1e-6 else 'FAIL'

doc.recompute()
doc.saveAs('PX1_Drivetrain_Check_RevAL.FCStd')
