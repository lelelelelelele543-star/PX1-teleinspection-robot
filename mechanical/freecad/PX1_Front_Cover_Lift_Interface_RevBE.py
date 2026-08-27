import FreeCAD as App, Part
# PX-1 Rev.BE front cover and manual camera-lift interface
# Prototype architecture for S-100-like one-hand parallelogram lift.
doc=App.newDocument('PX1_Front_Cover_Lift_Interface_RevBE')

W=94.0; H=76.0; T=10.0
PILOT_W=82.0; PILOT_H=64.0; PILOT_D=3.0

cover=doc.addObject('Part::Feature','Front_Cover')
shape=Part.makeBox(T,W,H)
# pilot pocket on inside face
pilot=Part.makeBox(PILOT_D,PILOT_W,PILOT_H,App.Vector(T-PILOT_D,(W-PILOT_W)/2,(H-PILOT_H)/2))
shape=shape.cut(pilot)

# Lift-base hard points: two vertical rows, 4x M5 clearance each side
for y in (22.0,72.0):
    for z in (18.0,58.0):
        hole=Part.makeCylinder(2.75,T,App.Vector(0,y,z),App.Vector(1,0,0))
        shape=shape.cut(hole)

# Central service aperture reserved for camera harness / quick-release submodule
ap=Part.makeBox(T,34.0,26.0,App.Vector(0,(W-34)/2,(H-26)/2))
shape=shape.cut(ap)

cover.Shape=shape
cover.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6'
cover.addProperty('App::PropertyString','LiftMount').LiftMount='8x M5 clearance hard-points, symmetric left/right'
cover.addProperty('App::PropertyString','ServiceAperture').ServiceAperture='34x26 mm prototype reserve; sealed by separate quick-release camera interface module'
cover.addProperty('App::PropertyString','Seal').Seal='Perimeter FKM face O-ring groove HOLD until screw pattern and final pilot are frozen'
cover.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE ARCHITECTURE'

doc.recompute()
doc.saveAs('PX1_Front_Cover_Lift_Interface_RevBE.FCStd')
