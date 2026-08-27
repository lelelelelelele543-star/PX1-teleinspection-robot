import FreeCAD as App, Part

# PX-1 Rev.AP — full left/right service assembly
BODY_L=250.0; BODY_W=94.0; BODY_H=76.0
FRONT_X=45.0; REAR_X=205.0; AXLE_Z=37.0
WHEEL_D=90.0; WHEEL_W=18.0
SIDE_Z=40; M=1.0; GEAR_FACE=8.0
SIDE_OD=(SIDE_Z+2)*M
SHAFT_D=10.0
BEARING_OD=26.0; BEARING_W=8.0
SEAL_OD=22.0; SEAL_W=7.0
COVER_T=3.0

DOC='PX1_Full_Service_Assembly_RevAP'
doc=App.newDocument(DOC)

# Main sealed body envelope
body=doc.addObject('Part::Feature','Body_Envelope')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H)
body.addProperty('App::PropertyString','Status').Status='REFERENCE ENVELOPE / body release remains Rev.W-derived'

# Helper functions

def cyl_y(r,l,x,y,z):
    return Part.makeCylinder(r,l,App.Vector(x,y,z),App.Vector(0,1,0))

def add_wheel(name,x,y,side_dir):
    obj=doc.addObject('Part::Feature',name)
    obj.Shape=cyl_y(WHEEL_D/2,WHEEL_W,x,y,AXLE_Z)
    obj.addProperty('App::PropertyString','Service').Service='removable externally'
    return obj

def add_gear(name,x,y):
    obj=doc.addObject('Part::Feature',name)
    outer=cyl_y(SIDE_OD/2,GEAR_FACE,x,y,AXLE_Z)
    bore=cyl_y(SHAFT_D/2,GEAR_FACE,x,y,AXLE_Z)
    obj.Shape=outer.cut(bore)
    obj.addProperty('App::PropertyInteger','Teeth').Teeth=SIDE_Z
    obj.addProperty('App::PropertyFloat','Module').Module=M
    obj.addProperty('App::PropertyString','Status').Status='service envelope; use exact involute part for manufacture'
    return obj

def add_rear_stack(prefix,y0,dir_sign):
    # Bearing and seal are purchased-part envelopes placed around the rear shaft axis.
    bearing=doc.addObject('Part::Feature',prefix+'_Bearing_6000_2RS')
    bearing.Shape=cyl_y(BEARING_OD/2,BEARING_W,REAR_X,y0,AXLE_Z).cut(cyl_y(5.0,BEARING_W,REAR_X,y0,AXLE_Z))
    bearing.addProperty('App::PropertyString','PurchasedPart').PurchasedPart='6000-2RS 10x26x8'

    seal_y=y0 + dir_sign*(BEARING_W+3.0)
    seal=doc.addObject('Part::Feature',prefix+'_Seal_10x22x7')
    seal.Shape=cyl_y(SEAL_OD/2,SEAL_W,REAR_X,seal_y,AXLE_Z).cut(cyl_y(5.0,SEAL_W,REAR_X,seal_y,AXLE_Z))
    seal.addProperty('App::PropertyString','PurchasedPart').PurchasedPart='FKM radial seal 10x22x7'

    shaft=doc.addObject('Part::Feature',prefix+'_Rear_Shaft')
    shaft_y=y0-5 if dir_sign>0 else y0-57
    shaft.Shape=cyl_y(SHAFT_D/2,62.0,REAR_X,shaft_y,AXLE_Z)
    shaft.addProperty('App::PropertyString','Journal').Journal='Ø10 h6; seal track Ra<=0.4'
    shaft.addProperty('App::PropertyString','ServiceRule').ServiceRule='no thread/key/D-flat under seal lip'

# Left/right external geometry
left_y=-WHEEL_W
right_y=BODY_W
left_gear_y=-10.0
right_gear_y=BODY_W+2.0

for side,wy,gy,sgn in [('L',left_y,left_gear_y,-1),('R',right_y,right_gear_y,1)]:
    add_wheel(f'Wheel_{side}_Front',FRONT_X,wy,sgn)
    add_wheel(f'Wheel_{side}_Rear',REAR_X,wy,sgn)

    centers=[FRONT_X,FRONT_X+40,FRONT_X+80,FRONT_X+120,REAR_X]
    for i,x in enumerate(centers):
        add_gear(f'Gear_{side}_{i}_z40',x,gy)

    rear_stack_y = -8.0 if side=='L' else BODY_W
    add_rear_stack(side,rear_stack_y,sgn)

# Side covers as removable service guards
for side,y in [('L',-15.0),('R',BODY_W+12.0)]:
    cov=doc.addObject('Part::Feature',f'Side_Cover_{side}')
    cov.Shape=Part.makeBox(214,COVER_T,70,App.Vector(18,y,2))
    cov.addProperty('App::PropertyString','Service').Service='remove first; no pressure seal function'

# Tool-access cylinders around wheel-retention region
for side,y,sgn in [('L',-32,-1),('R',BODY_W+18,1)]:
    for pos,x in [('F',FRONT_X),('R',REAR_X)]:
        acc=doc.addObject('Part::Feature',f'Tool_Access_{side}_{pos}')
        acc.Shape=cyl_y(9.5,28.0,x,y,AXLE_Z)
        acc.addProperty('App::PropertyString','Meaning').Meaning='minimum socket/spanner clearance envelope'

# Service rules
rules=doc.addObject('App::FeaturePython','Service_Rules')
for name,val in [
    ('Rule1','Both side covers removable without opening sealed body'),
    ('Rule2','Wheel retention accessible with ordinary hand tools'),
    ('Rule3','z40 idlers removable from outside'),
    ('Rule4','Rear wheel/gear removal must not disturb bearing/seal stack'),
    ('Rule5','Bearing/seal replacement is a second-level service operation'),
    ('Rule6','No special puller required for first-level field service'),
]:
    rules.addProperty('App::PropertyString',name,'Service')
    setattr(rules,name,val)

doc.recompute()
doc.saveAs('PX1_Full_Service_Assembly_RevAP.FCStd')
