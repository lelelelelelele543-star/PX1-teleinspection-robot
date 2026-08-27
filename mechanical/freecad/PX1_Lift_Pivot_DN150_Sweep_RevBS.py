import FreeCAD as App, Part, math
# PX-1 Rev.BS — lift pivot coordinates and DN150 swept-clearance study
# Coordinate convention: X forward from rear body face, Z upward from wheel-contact plane, Y lateral.
doc=App.newDocument('PX1_Lift_Pivot_DN150_Sweep_RevBS')

BODY_L=250.0; BODY_H=76.0; BODY_W=94.0
WHEEL_D=90.0
PIPE_D=150.0; PIPE_R=PIPE_D/2
HEAD_D=52.0; HEAD_R=HEAD_D/2; HEAD_L=78.0
LINK_L=68.0; PIVOT_SPACING=42.0

# With Ø90 wheels touching pipe bottom, wheel-axis height above contact plane = 45 mm.
WHEEL_AXIS_Z=45.0
# Candidate lift base is fixed to front cover; pivot line chosen to clear cover and keep mechanism inside wheel envelope.
BASE_PIVOT_X=250.0
BASE_PIVOT_Z=66.0
UPPER_PIVOT_X=BASE_PIVOT_X
UPPER_PIVOT_Z=BASE_PIVOT_Z+PIVOT_SPACING

# Visual body envelope placed relative to ground/contact plane.
body=doc.addObject('Part::Feature','BodyEnvelope')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H,App.Vector(0,-BODY_W/2,8.0))

# DN150 pipe cross-section as annulus/extruded sleeve around X-axis for visual check.
pipe=doc.addObject('Part::Feature','DN150_InnerBoundary')
pipe.Shape=Part.makeCylinder(PIPE_R,360,App.Vector(-55,0,PIPE_R),App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Meaning').Meaning='Inner clearance boundary only; robot geometry should remain inside this volume with >=3 mm nominal margin'

# Candidate lift positions inherited from earlier kinematics.
positions={'LOW':8.0,'DN150_SAFE':28.0,'HIGH':48.0}
for name,deg in positions.items():
    a=math.radians(deg)
    # Parallelogram top platform translated by link vector.
    dx=LINK_L*math.cos(a)
    dz=LINK_L*math.sin(a)
    tx=BASE_PIVOT_X+dx
    tz=BASE_PIVOT_Z+dz
    p=doc.addObject('Part::Feature',f'Head_{name}_0deg')
    p.Shape=Part.makeCylinder(HEAD_R,HEAD_L,App.Vector(tx,-HEAD_R,tz),App.Vector(0,1,0))
    p.addProperty('App::PropertyString','LiftAngle').LiftAngle=f'{deg} deg'
    p.addProperty('App::PropertyString','HeadAxis').HeadAxis=f'X={tx:.2f}, Z={tz:.2f} mm candidate'

rules=doc.addObject('App::FeaturePython','SweepRules')
rules.addProperty('App::PropertyString','PivotCoordinate').PivotCoordinate=f'base pivot X={BASE_PIVOT_X:.1f}, Z={BASE_PIVOT_Z:.1f} mm from rear-face/contact-plane datum'
rules.addProperty('App::PropertyString','Sweep').Sweep='Check TILT -105..+105 deg in 2 deg increments for LOW and DN150_SAFE'
rules.addProperty('App::PropertyString','Margin').Margin='>=3.0 mm nominal to DN150 inner wall for all moving head solids'
rules.addProperty('App::PropertyString','HighPosition').HighPosition='HIGH is not required to fit DN150'
rules.addProperty('App::PropertyString','Status').Status='PIVOT COORDINATE CANDIDATE — requires full solid sweep, wheel/pipe geometry verification and physical mock-up'

doc.recompute()
doc.saveAs('PX1_Lift_Pivot_DN150_Sweep_RevBS.FCStd')
