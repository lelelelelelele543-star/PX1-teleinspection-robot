import FreeCAD as App, Part
# PX-1 Rev.BG camera head envelope with TILT and continuous ROLL
# Prototype geometry for clearance checks, not release machining geometry.
doc=App.newDocument('PX1_Camera_Head_TiltRoll_RevBG')

HEAD_OD=52.0
HEAD_L=68.0
ROLL_BODY_OD=42.0
ROLL_BODY_L=44.0
TILT_AXIS_Z=26.0

# Camera pressure capsule / optical head envelope
head=doc.addObject('Part::Feature','CameraHeadEnvelope')
head.Shape=Part.makeCylinder(HEAD_OD/2,HEAD_L,App.Vector(0,0,0),App.Vector(1,0,0))
head.addProperty('App::PropertyString','Seal').Seal='separate pressure-tight camera module'
head.addProperty('App::PropertyString','QuickRelease').QuickRelease='single retained mechanical latch + wet connector target'

# Roll unit envelope
roll=doc.addObject('Part::Feature','RollBodyEnvelope')
roll.Shape=Part.makeCylinder(ROLL_BODY_OD/2,ROLL_BODY_L,App.Vector(-ROLL_BODY_L,0,0),App.Vector(1,0,0))
roll.addProperty('App::PropertyString','Motion').Motion='continuous 360 deg ROLL; no hard software stop'

# Tilt cheeks / yoke envelope
left=doc.addObject('Part::Feature','TiltCheek_L')
left.Shape=Part.makeBox(9,64,54,App.Vector(-10,-32,-27))
right=doc.addObject('Part::Feature','TiltCheek_R')
right.Shape=Part.makeBox(9,64,54,App.Vector(1,-32,-27))

axis=doc.addObject('Part::Feature','TiltAxisEnvelope')
axis.Shape=Part.makeCylinder(4,82,App.Vector(-1,-41,0),App.Vector(0,1,0))

meta=doc.addObject('App::FeaturePython','Limits')
meta.addProperty('App::PropertyString','TiltRange').TiltRange='-105..+105 deg'
meta.addProperty('App::PropertyString','RollRange').RollRange='continuous 360 deg'
meta.addProperty('App::PropertyString','TargetHeadOD').TargetHeadOD='<=52 mm initial DN150 clearance target'
meta.addProperty('App::PropertyString','Status').Status='PROTOTYPE ENVELOPE - motor, bearing, window and connector details pending'

doc.recompute()
doc.saveAs('PX1_Camera_Head_TiltRoll_RevBG.FCStd')
