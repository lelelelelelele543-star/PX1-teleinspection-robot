import FreeCAD as App, Part, math
# PX-1 Rev.BG DN150 section clearance checker.
# Models a 150 mm ID pipe cross-section and conservative crawler/camera envelopes.
doc=App.newDocument('PX1_DN150_Clearance_Check_RevBG')

PIPE_ID=150.0
BODY_W=94.0
BODY_H=76.0
WHEEL_D=90.0
WHEEL_W=18.0
HEAD_OD=52.0

# Pipe section, 300 mm long
pipe_outer=Part.makeCylinder(85,300,App.Vector(0,0,-150),App.Vector(0,0,1))
pipe_inner=Part.makeCylinder(PIPE_ID/2,300,App.Vector(0,0,-150),App.Vector(0,0,1))
pipe=doc.addObject('Part::Feature','DN150_Pipe')
pipe.Shape=pipe_outer.cut(pipe_inner)

# Robot cross-section envelope centered low in pipe.
# Ground/contact line at y=-75; wheel radius 45 => axle center -30.
AXLE_Y=-30.0
body=doc.addObject('Part::Feature','BodySectionEnvelope')
body.Shape=Part.makeBox(BODY_W,BODY_H,30,App.Vector(-BODY_W/2,AXLE_Y-WHEEL_D/2+8,-15))

# Four wheel-side cross-section envelopes simplified as two cylinders
for x in (-BODY_W/2-9,BODY_W/2+9):
    w=doc.addObject('Part::Feature',f'WheelEnvelope_{x:+.0f}')
    w.Shape=Part.makeCylinder(WHEEL_D/2,WHEEL_W,App.Vector(x,AXLE_Y,0),App.Vector(1,0,0))

# Camera-head circles for LOW / SAFE / HIGH preliminary lift states
states={'LOW':12.0,'DN150_SAFE':32.0,'HIGH':50.0}
for name,raise_mm in states.items():
    cy=AXLE_Y+25+raise_mm
    cam=doc.addObject('Part::Feature',f'CameraHead_{name}')
    cam.Shape=Part.makeCylinder(HEAD_OD/2,35,App.Vector(-17.5,cy,0),App.Vector(1,0,0))
    # analytic radial clearance from pipe center to outer camera radius
    radial=PIPE_ID/2-(abs(cy)+HEAD_OD/2)
    cam.addProperty('App::PropertyFloat','TopRadialClearance_mm').TopRadialClearance_mm=radial
    cam.addProperty('App::PropertyString','Interpretation').Interpretation='Positive = clears pipe ID at top/bottom in simplified centered section'

rules=doc.addObject('App::FeaturePython','DN150_Rules')
rules.addProperty('App::PropertyString','Requirement').Requirement='No solid envelope may intersect Ø150 mm pipe ID in LOW or DN150_SAFE'
rules.addProperty('App::PropertyString','HighState').HighState='HIGH may exceed DN150; intended for larger pipes only'
rules.addProperty('App::PropertyString','Tolerance').Tolerance='Require >=3 mm nominal radial clearance after full assembly/tolerance stack'
rules.addProperty('App::PropertyString','Status').Status='PRELIMINARY SECTION CHECK - exact lift geometry and camera-head CAD must replace envelopes before RELEASE'

doc.recompute()
doc.saveAs('PX1_DN150_Clearance_Check_RevBG.FCStd')
