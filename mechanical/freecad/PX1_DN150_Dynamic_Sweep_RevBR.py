import FreeCAD as App, Part, math
# PX-1 Rev.BR dynamic DN150 clearance sweep
# Conservative envelope method for head + lift. This is not final kinematic proof.
doc=App.newDocument('PX1_DN150_Dynamic_Sweep_RevBR')

PIPE_ID=150.0
PIPE_R=PIPE_ID/2
HEAD_OD=52.0
HEAD_L=78.0
HEAD_R=HEAD_OD/2
LIFT_ARM=68.0
BASE_Z=45.0   # provisional head pivot height above pipe invert in LOW reference
ANGLES=[-105,-90,-60,-30,0,30,60,90,105]
LIFT_STATES={'LOW':8.0,'DN150_SAFE':28.0}

# Pipe cross-section ring (visual)
outer=Part.makeCylinder(PIPE_R+1,6)
inner=Part.makeCylinder(PIPE_R,6)
ring=doc.addObject('Part::Feature','DN150_Pipe_Ring')
ring.Shape=outer.cut(inner)

# conservative swept head envelope for each lift state and TILT sample
for state,lift_deg in LIFT_STATES.items():
    lift_z = BASE_Z + LIFT_ARM*math.sin(math.radians(lift_deg))
    for a in ANGLES:
        # Head represented by oriented cylinder about transverse axis.
        # Centerline pivots at one end; conservative radial check is taken from all vertices.
        head=Part.makeCylinder(HEAD_R,HEAD_L,App.Vector(0,0,lift_z),App.Vector(1,0,0))
        head.rotate(App.Vector(0,0,lift_z),App.Vector(0,1,0),a)
        obj=doc.addObject('Part::Feature',f'Head_{state}_{a:+d}')
        obj.Shape=head
        # Compute max radial distance in YZ plane from pipe center at z=75
        max_r=0.0
        for v in head.Vertexes:
            y=v.Point.y
            z=v.Point.z-PIPE_R
            r=(y*y+z*z)**0.5
            if r>max_r: max_r=r
        clearance=PIPE_R-max_r
        obj.addProperty('App::PropertyString','LiftState').LiftState=state
        obj.addProperty('App::PropertyAngle','TiltAngle').TiltAngle=a
        obj.addProperty('App::PropertyLength','EstimatedClearance').EstimatedClearance=clearance
        obj.addProperty('App::PropertyString','Result').Result='PASS' if clearance>=3.0 else 'FAIL/HOLD'

rules=doc.addObject('App::FeaturePython','AcceptanceRules')
rules.addProperty('App::PropertyString','Criterion').Criterion='LOW and DN150_SAFE require >=3.0 mm nominal clearance at all sampled TILT angles'
rules.addProperty('App::PropertyString','Important').Important='Current BASE_Z is provisional; rerun after exact lift pivot location and head mounting geometry are frozen'
rules.addProperty('App::PropertyString','Method').Method='Conservative sampled sweep; final proof requires exact solids and finer angular sweep'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE from this study alone'

doc.recompute()
doc.saveAs('PX1_DN150_Dynamic_Sweep_RevBR.FCStd')
