import FreeCAD as App, Part, math

# PX-1 Rev.EW — integrated machining-oriented master.
# Integrates Rev.ES motor relocation, Rev.ET three-zone body, Rev.EU wheel stations,
# and Rev.EV plate-arm LOW lift. Prototype engineering baseline only.

doc = App.newDocument('PX1_CRP150_6W_Master_RevEW')

# ---------------- datums ----------------
L=307.0; W=92.0; Z0=8.0; Z1=90.0
PIPE_R=75.0; PIPE_Z=52.0480547
WHEEL_X=[50.0,150.0,250.0]
IDLER_X=[100.0,200.0]
WHEEL_Z=45.0
SIDE_COVER_T=5.0
GEAR_OD=52.0; GEAR_W=8.0
INPUT_X=200.0

# ---------------- helpers ----------------
def cyl_y(r,l,x,y,z,sign=1):
    return Part.makeCylinder(r,l,App.Vector(x,y,z),App.Vector(0,sign,0))


def tapered_wheel(x,side):
    s=1 if side=='L' else -1
    inner_y=51.0
    crown_end=55.0
    outer_y=68.0
    crown=cyl_y(45.0,crown_end-inner_y,x,s*inner_y,WHEEL_Z,s)
    taper=Part.makeCone(45.0,22.0,outer_y-crown_end,
                        App.Vector(x,s*crown_end,WHEEL_Z),App.Vector(0,s,0))
    return crown.fuse(taper)

# ---------------- DN150 reference ----------------
pipe=doc.addObject('Part::Feature','DN150_ID_Reference')
pipe.Shape=Part.makeCylinder(PIPE_R,L+160,App.Vector(-80,0,PIPE_Z),App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Note').Note='ideal ID150 reference; wheel crown contact intentional'

# ---------------- actual three-zone body candidate ----------------
outer=Part.makeBox(L,W,Z1-Z0,App.Vector(0,-W/2.0,Z0))
# front P0 cavity under lowered roof
front=Part.makeBox(120.0,62.0,39.0,App.Vector(8.0,-31.0,14.0))
# rear P0 cavity open/service region
rear=Part.makeBox(171.0,62.0,78.0,App.Vector(128.0,-31.0,14.0))
body_shape=outer.cut(front.fuse(rear))
# side P1/P2 bays
for s in (1,-1):
    y0=35.0 if s>0 else -46.0
    bay=Part.makeBox(275.0,11.0,66.0,App.Vector(16.0,y0,12.0))
    body_shape=body_shape.cut(bay)
# rear/top service opening already represented by rear cavity; external LOW-camera nose recess
nose=Part.makeBox(85.0,58.0,34.0,App.Vector(40.0,-29.0,58.0))
body_shape=body_shape.cut(nose)

body=doc.addObject('Part::Feature','PressureBody_RevET')
body.Shape=body_shape
body.addProperty('App::PropertyString','Zones').Zones='P0 central; P1/P2 side bays; 4 mm nominal P0-to-side bulkhead web'
body.addProperty('App::PropertyString','Material').Material='EN AW-6082-T6 candidate'

# side covers
for side,s in [('L',1),('R',-1)]:
    y0=46.0 if s>0 else -51.0
    c=doc.addObject('Part::Feature',f'SideCover_{side}')
    c.Shape=Part.makeBox(281.0,5.0,76.0,App.Vector(13.0,y0,7.0))
    c.addProperty('App::PropertyString','Seal').Seal='closed-loop FKM face seal; screw line outside seal'

# top cover reference
cover=doc.addObject('Part::Feature','TopServiceCover')
cover.Shape=Part.makeBox(174.0,70.0,5.0,App.Vector(124.0,-35.0,90.0))
cover.addProperty('App::PropertyString','Seal').Seal='FKM static seal; removable motor/electronics access'

# ---------------- side gears and wheel station solids ----------------
for side,s in [('L',1),('R',-1)]:
    gy=s*38.0
    d=App.Vector(0,s,0)
    for x in WHEEL_X:
        g=doc.addObject('Part::Feature',f'WheelGear_Z50_{side}_{int(x)}')
        g.Shape=Part.makeCylinder(GEAR_OD/2.0,GEAR_W,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Spec').Spec='m1 Z50, 8 mm face, Ø12 keyed journal'
    for x in IDLER_X:
        g=doc.addObject('Part::Feature',f'Idler_Z50_{side}_{int(x)}')
        g.Shape=Part.makeCylinder(GEAR_OD/2.0,GEAR_W,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Input').Input='traction input station' if x==INPUT_X else 'idler'

    for x in WHEEL_X:
        w=doc.addObject('Part::Feature',f'Wheel_{side}_{int(x)}')
        w.Shape=tapered_wheel(x,side)

        # stepped shaft envelope
        shaft=doc.addObject('Part::Feature',f'WheelShaft_{side}_{int(x)}')
        inner=cyl_y(6.0,18.0,x,s*31.0,WHEEL_Z,s)
        outer=cyl_y(8.5,29.0,x,s*49.0,WHEEL_Z,s)
        shaft.Shape=inner.fuse(outer)
        shaft.addProperty('App::PropertyString','Spec').Spec='Ø12 inner -> Ø17 outer, keyed gear/wheel; polished seal journal'

        fl=doc.addObject('Part::Feature',f'AxleFlange_{side}_{int(x)}')
        fl.Shape=Part.makeCylinder(25.0,9.0,App.Vector(x,s*46.0,WHEEL_Z),d)
        fl.addProperty('App::PropertyString','Bearing').Bearing='61903 17x30x7 + compact FKM dynamic seal'

# ---------------- Rev.ES rearward paired motors / bevel input X200 ----------------
# motor bodies extend rearward from the X200 bevel plane.
holder=doc.addObject('Part::Feature','PairedMotorHolder_Rearward')
holder.Shape=Part.makeBox(104.0,80.0,46.0,App.Vector(196.0,-40.0,22.0))
holder.addProperty('App::PropertyString','Architecture').Architecture='both motor output shafts face forward toward X200; holder removable through top'

MOTOR_D=37.0; MOTOR_L=90.0; MOTOR_Y=19.0; MOTOR_Z=45.0
for side,s in [('L',1),('R',-1)]:
    m=doc.addObject('Part::Feature',f'JGB37_555_{side}_RearwardEnvelope')
    m.Shape=Part.makeCylinder(MOTOR_D/2.0,MOTOR_L,
                              App.Vector(205.0,s*MOTOR_Y,MOTOR_Z),App.Vector(1,0,0))
    m.addProperty('App::PropertyString','Orientation').Orientation='body extends X205..295; output/pinion toward X200'

    pin=doc.addObject('Part::Feature',f'BevelPinion_Z18_{side}_Envelope')
    pin.Shape=Part.makeCone(15.43,8.0,21.97,
                            App.Vector(INPUT_X-21.97,s*MOTOR_Y,WHEEL_Z),App.Vector(1,0,0))
    pin.addProperty('App::PropertyString','Spec').Spec='KHK SB1.5-1845H class, m1.5 Z18'

    large=doc.addObject('Part::Feature',f'BevelLarge_Z45_{side}_Envelope')
    ystart=s*(35.0-21.10)
    large.Shape=Part.makeCone(34.09,18.0,21.10,
                              App.Vector(INPUT_X,ystart,WHEEL_Z),App.Vector(0,s,0))
    large.addProperty('App::PropertyString','Spec').Spec='KHK SB1.5-4518H class, m1.5 Z45; output to X200 side idler'

# ---------------- front low-profile electronics packaging ----------------
pwr=doc.addObject('Part::Feature','FrontPowerHalfBrick_Envelope')
pwr.Shape=Part.makeBox(70.0,58.0,18.0,App.Vector(15.0,-29.0,16.0))
pwr.addProperty('App::PropertyString','Contents').Contents='48V input protection + ~200W half-brick traction converter thermal coupled to floor'

ctrl=doc.addObject('Part::Feature','FrontControlStack_Envelope')
ctrl.Shape=Part.makeBox(92.0,58.0,15.0,App.Vector(15.0,-29.0,36.0))
ctrl.addProperty('App::PropertyString','Contents').Contents='controller/comms/sensor I/O on low-profile removable tray'

# ---------------- plate-arm lift LOW ----------------
PIVOT_X=200.0; PIVOT_Z=94.0; LINK_L=120.0; CAM_Z=75.0; CAM_OFF=10.0
sval=(CAM_Z-(PIVOT_Z+CAM_OFF))/LINK_L
th=math.asin(sval)
ux=PIVOT_X-LINK_L*math.cos(th)
uz=PIVOT_Z+LINK_L*math.sin(th)

def plate_between(x1,z1,x2,z2,y0,t,w):
    dx=x2-x1; dz=z2-z1; ll=math.hypot(dx,dz)
    a=math.degrees(math.atan2(dz,dx))
    sh=Part.makeBox(ll,t,w,App.Vector(x1,y0,z1-w/2.0))
    sh.rotate(App.Vector(x1,y0,z1),App.Vector(0,1,0),-a)
    return sh

for side,y0 in [('L',24.0),('R',-28.0)]:
    a=doc.addObject('Part::Feature',f'LiftArm_{side}_LOW')
    a.Shape=plate_between(PIVOT_X,PIVOT_Z,ux,uz,y0,4.0,22.0)

cam=doc.addObject('Part::Feature','DigitalCameraHead_LOW')
cam.Shape=Part.makeCylinder(26.0,72.0,App.Vector(ux-36.0,0,CAM_Z),App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Video').Video='digital only; continuous internal ROLL, TILT +/-105'

# ---------------- rear interface references ----------------
tail=doc.addObject('Part::Feature','RearTetherBoot_Envelope')
tail.Shape=Part.makeCone(13.0,9.0,100.0,App.Vector(L,0,45.0),App.Vector(1,0,0))
tail.addProperty('App::PropertyString','LoadPath').LoadPath='tether tensile member anchors to body independently of electrical connector'

rules=doc.addObject('App::FeaturePython','RevEW_Rules')
rules.addProperty('App::PropertyString','Input').Input='traction input moved to X200 idler; motor bodies extend rearward'
rules.addProperty('App::PropertyString','Body').Body='milled three-pressure-zone body, side bays behind sealed covers'
rules.addProperty('App::PropertyString','Wheel').Wheel='machining-oriented Ø12/Ø17 station, 61801/61903 philosophy'
rules.addProperty('App::PropertyString','Lift').Lift='4 mm plate arms in LOW; DN150 hard stop mandatory'
rules.addProperty('App::PropertyString','Release').Release='ENGINEERING MASTER; physical parts/pressure tests still required before machining release'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevEW.FCStd')
