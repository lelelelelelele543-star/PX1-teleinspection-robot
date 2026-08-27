import FreeCAD as App, Part, math
# PX-1 Rev.BP complete TILT module packaging/kinematic model
# Purchased parts are envelopes; worm geometry remains matched-set reference.
doc=App.newDocument('PX1_Tilt_Module_RevBP')

# Design constants
TILT_MIN=-105.0
TILT_MAX=105.0
WORM_RATIO=20.0
WORM_SHAFT_D=3.0
BEARING_ID=3.0; BEARING_OD=8.0; BEARING_W=4.0
WORM_OD=10.0; WORM_L=18.0
WHEEL_OD=11.3; WHEEL_W=4.0
CENTER_DIST=9.5
COUPLER_OD=6.0; COUPLER_L=10.0
HEAD_OD=52.0

# Motor envelope: GM12-N20 class
motor=doc.addObject('Part::Feature','Tilt_Motor_N20')
motor.Shape=Part.makeBox(12,10,26,App.Vector(-6,-24,-13))
motor.addProperty('App::PropertyString','Part').Part='DCGM-N20-12V-EN-200RPM class'

# Coupler
coupler=doc.addObject('Part::Feature','Coupler_3mm')
coupler.Shape=Part.makeCylinder(COUPLER_OD/2,COUPLER_L,App.Vector(0,-14,0),App.Vector(0,1,0))
coupler.addProperty('App::PropertyString','Spec').Spec='Turned Ø6x10, bore Ø3 H7, 2x M2 clamp/set screws'

# Independent worm shaft
shaft=doc.addObject('Part::Feature','Worm_Shaft')
shaft.Shape=Part.makeCylinder(WORM_SHAFT_D/2,34,App.Vector(0,-4,0),App.Vector(0,1,0))
shaft.addProperty('App::PropertyString','Material').Material='Stainless or hardened steel prototype'

# Two 693-ZZ supports
for i,y in enumerate((-3.5,22.5),1):
    b=doc.addObject('Part::Feature',f'Bearing_693ZZ_{i}')
    b.Shape=Part.makeCylinder(BEARING_OD/2,BEARING_W,App.Vector(0,y,0),App.Vector(0,1,0)).cut(
        Part.makeCylinder(BEARING_ID/2,BEARING_W,App.Vector(0,y,0),App.Vector(0,1,0)))
    b.addProperty('App::PropertyString','Envelope').Envelope='693-ZZ 3x8x4'

# Worm matched-set envelope
worm=doc.addObject('Part::Feature','Worm_1start_m05')
worm.Shape=Part.makeCylinder(WORM_OD/2,WORM_L,App.Vector(0,4,0),App.Vector(0,1,0))
worm.addProperty('App::PropertyString','Status').Status='MATCHED-SET ENVELOPE ONLY; supplier tooth form governs'

# Worm wheel and tilt output axis
wheel=doc.addObject('Part::Feature','Worm_Wheel_20T')
wheel.Shape=Part.makeCylinder(WHEEL_OD/2,WHEEL_W,App.Vector(CENTER_DIST,-2,0),App.Vector(0,1,0))
wheel.addProperty('App::PropertyString','Ratio').Ratio='20:1 with 1-start worm'

axis=doc.addObject('Part::Feature','Tilt_Output_Axis')
axis.Shape=Part.makeCylinder(3.0,28,App.Vector(CENTER_DIST,-14,0),App.Vector(0,1,0))

# Mechanical stop arc representation and Hall home marker
stop=doc.addObject('Part::Feature','Mechanical_Stop_Sector')
stop.Shape=Part.makeCylinder(9,3,App.Vector(CENTER_DIST,7,0),App.Vector(0,1,0))
stop.addProperty('App::PropertyString','Range').Range='Physical hard stops at approximately -108° and +108°; software limit ±105°'

hall=doc.addObject('Part::Feature','Hall_HOME')
hall.Shape=Part.makeBox(4,3,3,App.Vector(CENTER_DIST+7,3,4))
hall.addProperty('App::PropertyString','Function').Function='Non-contact HOME near 0° using Hall sensor + magnet'

# Head diameter keep-out for packaging check
head=doc.addObject('Part::Feature','Head_Diameter_Keepout')
head.Shape=Part.makeCylinder(HEAD_OD/2,4,App.Vector(0,-2,0),App.Vector(0,1,0))
head.addProperty('App::PropertyString','Requirement').Requirement='All TILT drive geometry must fit inside Ø52 mm head package'

rules=doc.addObject('App::FeaturePython','EngineeringRules')
rules.addProperty('App::PropertyString','SoftwareRange').SoftwareRange='-105°..+105°'
rules.addProperty('App::PropertyString','HardStops').HardStops='Nominal -108°/+108°; adjust after real collision test'
rules.addProperty('App::PropertyString','HoldingTorque').HoldingTorque='Target >=0.22 N·m at output with margin'
rules.addProperty('App::PropertyString','Backdrive').Backdrive='Do NOT assume self-locking until physical test passes'
rules.addProperty('App::PropertyString','Status').Status='ASSEMBLY-CANDIDATE; final bearing pockets/stop geometry after exact parts measured'

doc.recompute()
doc.saveAs('PX1_Tilt_Module_RevBP.FCStd')
