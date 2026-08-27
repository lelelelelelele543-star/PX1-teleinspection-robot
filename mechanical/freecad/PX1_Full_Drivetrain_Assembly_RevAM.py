import FreeCAD as App, Part

# PX-1 Rev.AM full left/right drivetrain assembly skeleton.
# Uses exact system centers and purchased-part envelopes.

BODY_L=250.0; BODY_W=94.0; BODY_H=76.0
FRONT_X=45.0; REAR_X=205.0; AXLE_Z=37.0
WHEEL_D=90.0; WHEEL_W=18.0
SIDE_CENTERS=[45.0,85.0,125.0,165.0,205.0]


doc=App.newDocument('PX1_Full_Drivetrain_RevAM')

# Pressure-body envelope
body=doc.addObject('Part::Feature','Body_Envelope')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H)
body.addProperty('App::PropertyString','Status').Status='REFERENCE ENVELOPE / Rev.W master governs machining'

# Wheels
for side,y0 in [('L',-WHEEL_W),('R',BODY_W)]:
    for pos,x in [('F',FRONT_X),('R',REAR_X)]:
        w=doc.addObject('Part::Feature',f'Wheel_{side}_{pos}')
        w.Shape=Part.makeCylinder(WHEEL_D/2,WHEEL_W,App.Vector(x,y0,AXLE_Z),App.Vector(0,1,0))
        w.addProperty('App::PropertyString','Spec').Spec='Ø90 x 18 nominal'

# External side gears z40, m1: OD 42, face 8, pitch dia 40.
for side,y0 in [('L',-10.0),('R',BODY_W+2.0)]:
    for idx,x in enumerate(SIDE_CENTERS):
        g=doc.addObject('Part::Feature',f'SideGear_{side}_{idx}_z40')
        outer=Part.makeCylinder(21.0,8.0,App.Vector(x,y0,AXLE_Z),App.Vector(0,1,0))
        bore=Part.makeCylinder(5.0,8.0,App.Vector(x,y0,AXLE_Z),App.Vector(0,1,0))
        g.Shape=outer.cut(bore)
        g.addProperty('App::PropertyString','Spec').Spec='m1 z40, 20deg; envelope only in this assembly'

# Rear shaft bearing/seal stacks, one per side only.
for side,y0,dirv in [('L',0.0,-1),('R',BODY_W,1)]:
    bearing=doc.addObject('Part::Feature',f'Bearing_{side}_6000')
    by=y0 + (-8.0 if side=='L' else 0.0)
    outer=Part.makeCylinder(13.0,8.0,App.Vector(REAR_X,by,AXLE_Z),App.Vector(0,1,0))
    inner=Part.makeCylinder(5.0,8.0,App.Vector(REAR_X,by,AXLE_Z),App.Vector(0,1,0))
    bearing.Shape=outer.cut(inner)
    seal=doc.addObject('Part::Feature',f'Seal_{side}_10x22x7')
    sy=y0 + (-15.0 if side=='L' else 8.0)
    so=Part.makeCylinder(11.0,7.0,App.Vector(REAR_X,sy,AXLE_Z),App.Vector(0,1,0))
    si=Part.makeCylinder(5.0,7.0,App.Vector(REAR_X,sy,AXLE_Z),App.Vector(0,1,0))
    seal.Shape=so.cut(si)

# Front stationary axle envelopes (no pressure penetration)
for side,y0 in [('L',-32.0),('R',BODY_W)]:
    a=doc.addObject('Part::Feature',f'Front_Axle_{side}')
    a.Shape=Part.makeCylinder(5.0,32.0,App.Vector(FRONT_X,y0,AXLE_Z),App.Vector(0,1,0))
    a.addProperty('App::PropertyString','Function').Function='External stationary axle'

# Motor maximum envelopes inside dry volume, deliberately generic.
for side,y0 in [('L',8.0),('R',44.0)]:
    mo=doc.addObject('Part::Feature',f'Motor_{side}_Max_Envelope')
    mo.Shape=Part.makeBox(95.0,42.0,42.0,App.Vector(105.0,y0,16.0))
    mo.addProperty('App::PropertyString','Status').Status='Incoming motor must fit inside this envelope'

# Key geometry checks as document properties.
checks=doc.addObject('App::FeaturePython','Geometry_Checks')
checks.addProperty('App::PropertyLength','Wheelbase').Wheelbase=REAR_X-FRONT_X
checks.addProperty('App::PropertyLength','SideGearCenter').SideGearCenter=40.0
checks.addProperty('App::PropertyLength','MotorGearCenter').MotorGearCenter=24.0
checks.addProperty('App::PropertyString','SealCount').SealCount='2 dynamic shaft seals total'
checks.addProperty('App::PropertyString','Status').Status='PROTOTYPE PACKAGING CHECK'

doc.recompute()
doc.saveAs('PX1_Full_Drivetrain_Assembly_RevAM.FCStd')
