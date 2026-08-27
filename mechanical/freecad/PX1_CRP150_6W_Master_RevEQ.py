import FreeCAD as App, Part, math
# PX-1 Rev.EQ — integrated CRP150-style 6-wheel master
# Adds body nose recess, manual lift, digital camera, rear tail and P0 service-zone envelopes
# to the source-aligned drivetrain architecture. Packaging master only.

doc = App.newDocument('PX1_CRP150_6W_Master_RevEQ')

# ---------------- GLOBAL DATUMS ----------------
BODY_L = 307.0
BODY_W = 92.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
PIPE_R = 75.0
PIPE_AXIS_Z = 52.0480547
WHEEL_Z = 45.0
WHEEL_X = [50.0, 150.0, 250.0]
IDLER_X = [100.0, 200.0]

COVER_T = 5.0
COVER_Y = BODY_W/2.0
COVER_X0 = 15.5
COVER_L = 276.0
COVER_Z0 = 5.0
COVER_H = 81.0

GEAR_OD = 52.0
GEAR_FACE = 8.0
GEAR_Y = 38.0

# Wheel / station
INNER_SHAFT_D = 12.0
OUTER_SHAFT_D = 17.0
B61801_OD = 21.0
B61903_OD = 30.0
FLANGE_OD = 50.0
WHEEL_INNER_Y = COVER_Y + COVER_T
WHEEL_CROWN_END_Y = 54.0
WHEEL_OUTER_Y = 67.0
WHEEL_R = 45.0
WHEEL_OUTER_R = 21.0

# Motor / bevel
MOTOR_D = 37.0
MOTOR_L = 90.0
MOTOR_Y = 19.0
MOTOR_Z = 45.0
BEVEL_SMALL_OD = 30.86
BEVEL_LARGE_OD = 68.18
BEVEL_SMALL_LEN = 21.97
BEVEL_LARGE_LEN = 21.10
BEVEL_X = 150.0

# Lift / camera
LIFT_PIVOT_X = 200.0
LIFT_PIVOT_Z = 94.0
LINK_L = 120.0
LINK_R = 4.0        # envelope only; final arms are plates
CAM_AXIS_OFFSET_Z = 10.0
CAM_R = 26.0
CAM_LEN = 72.0
CAM_Z_LOW = 75.0

# ---------------- HELPERS ----------------
def cyl_y(r, l, x, y, z, sign=1):
    return Part.makeCylinder(r, l, App.Vector(x,y,z), App.Vector(0,sign,0))


def cylinder_between(p1, p2, radius):
    v = App.Vector(p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    return Part.makeCylinder(radius, v.Length, App.Vector(*p1), v)


def lift_pose(camera_axis_z):
    s = (camera_axis_z - (LIFT_PIVOT_Z + CAM_AXIS_OFFSET_Z))/LINK_L
    if abs(s) > 1.0:
        raise ValueError('lift target unreachable')
    th = math.asin(s)
    upper_x = LIFT_PIVOT_X - LINK_L*math.cos(th)
    upper_z = LIFT_PIVOT_Z + LINK_L*math.sin(th)
    return th, upper_x, upper_z


def wheel_envelope(x, side):
    sign = 1 if side == 'L' else -1
    crown = cyl_y(WHEEL_R, WHEEL_CROWN_END_Y-WHEEL_INNER_Y,
                  x, sign*WHEEL_INNER_Y, WHEEL_Z, sign)
    taper = Part.makeCone(WHEEL_R, WHEEL_OUTER_R,
                          WHEEL_OUTER_Y-WHEEL_CROWN_END_Y,
                          App.Vector(x,sign*WHEEL_CROWN_END_Y,WHEEL_Z),
                          App.Vector(0,sign,0))
    return crown.fuse(taper)

# ---------------- DN150 REFERENCE ----------------
pipe = doc.addObject('Part::Feature','DN150_ID_Reference')
pipe.Shape = Part.makeCylinder(PIPE_R, BODY_L+160,
                               App.Vector(-80,0,PIPE_AXIS_Z), App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Note').Note = 'Ideal ID150 reference; wheel traction crown intentional contact'

# ---------------- STRUCTURAL BODY ----------------
# Outer body envelope with the front-upper camera/lift pocket removed.
outer = Part.makeBox(BODY_L, BODY_W, BODY_Z1-BODY_Z0,
                     App.Vector(0,-BODY_W/2.0,BODY_Z0))
# Camera folded envelope requires a sculpted nose instead of a full rectangular roof.
# Keep a lower pressure floor/side structure; recess only the upper central nose.
nose_recess = Part.makeBox(92.0, 62.0, 38.0, App.Vector(38.0,-31.0,54.0))
body_shape = outer.cut(nose_recess)

body = doc.addObject('Part::Feature','PressureBody_P0_StructuralEnvelope')
body.Shape = body_shape
body.addProperty('App::PropertyString','Architecture').Architecture = 'milled Al body/tray with front upper camera recess and removable top service cover'
body.addProperty('App::PropertyString','Pressure').Pressure = 'P0 isolated +0.20..+0.30 bar normal'
body.addProperty('App::PropertyString','Status').Status = 'shape concept; wall thickness/internal pocket machining not production released'

# top service cover behind the nose recess
top = doc.addObject('Part::Feature','TopServiceCover_Envelope')
top.Shape = Part.makeBox(157.0, 74.0, 5.0, App.Vector(138.0,-37.0,BODY_Z1))
top.addProperty('App::PropertyString','Seal').Seal = 'static FKM O-ring; screw line outside seal; exact groove after final body solid'

# ---------------- SIDE DRIVE COVERS ----------------
for side, sign in [('L',1),('R',-1)]:
    y0 = COVER_Y if sign > 0 else -COVER_Y-COVER_T
    cover = doc.addObject('Part::Feature',f'SideCover_{side}')
    cover.Shape = Part.makeBox(COVER_L,COVER_T,COVER_H,App.Vector(COVER_X0,y0,COVER_Z0))
    cover.addProperty('App::PropertyString','Pressure').Pressure = f'P{1 if side=="L" else 2} isolated side-drive zone'
    cover.addProperty('App::PropertyString','Seal').Seal = 'large molded FKM face seal + three local axle-flange seals'

# ---------------- SIX WHEELS / FIVE Z50 GEARS PER SIDE ----------------
for x in WHEEL_X:
    for side, sign in [('L',1),('R',-1)]:
        w = doc.addObject('Part::Feature',f'Wheel_{side}_{int(x)}')
        w.Shape = wheel_envelope(x,side)
        w.addProperty('App::PropertyString','Mount').Mount = 'stepped Ø12/Ø17 shaft; keyed; axial retained wheel'

        # local axle flange envelope
        fl = doc.addObject('Part::Feature',f'AxleFlange_{side}_{int(x)}')
        fl.Shape = Part.makeCylinder(FLANGE_OD/2.0, 7.0,
                                     App.Vector(x,sign*(COVER_Y+COVER_T),WHEEL_Z),
                                     App.Vector(0,sign,0))
        fl.addProperty('App::PropertyString','Bearing').Bearing = '61903 outer wheel-load bearing; internal 61801 support pair philosophy'

for side, sign in [('L',1),('R',-1)]:
    d = App.Vector(0,sign,0)
    gy = sign*GEAR_Y
    for x in WHEEL_X:
        g = doc.addObject('Part::Feature',f'WheelGear_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Spec').Spec = 'm1 Z50 OD52 face8 class, keyed Ø12 station'
    for x in IDLER_X:
        g = doc.addObject('Part::Feature',f'Idler_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Spec').Spec = 'm1 Z50 idler; fixed serviceable pin/bearing'

# ---------------- PAIRED MOTOR HOLDER / BEVEL STAGE ----------------
holder = doc.addObject('Part::Feature','PairedMotorHolder_Envelope')
holder.Shape = Part.makeBox(98.0,80.0,44.0,App.Vector(100.0,-40.0,23.0))
holder.addProperty('App::PropertyString','Architecture').Architecture = 'one removable holder for both motors and supported bevel-pinion shafts'

for side, sign in [('L',1),('R',-1)]:
    m = doc.addObject('Part::Feature',f'JGB37_555_{side}_Envelope')
    m.Shape = Part.makeCylinder(MOTOR_D/2.0,MOTOR_L,
                                App.Vector(104.0,sign*MOTOR_Y,MOTOR_Z),App.Vector(1,0,0))
    m.addProperty('App::PropertyString','Status').Status = '24V ratio~56 / ~107rpm family candidate; exact sample mandatory'

    pin = doc.addObject('Part::Feature',f'KHK_SB1_5_1845H_{side}_Envelope')
    pin.Shape = Part.makeCone(BEVEL_SMALL_OD/2.0,8.0,BEVEL_SMALL_LEN,
                              App.Vector(BEVEL_X-BEVEL_SMALL_LEN,sign*MOTOR_Y,WHEEL_Z),App.Vector(1,0,0))

    large = doc.addObject('Part::Feature',f'KHK_SB1_5_4518H_{side}_Envelope')
    ystart = sign*(36.0-BEVEL_LARGE_LEN)
    large.Shape = Part.makeCone(BEVEL_LARGE_OD/2.0,18.0,BEVEL_LARGE_LEN,
                                App.Vector(BEVEL_X,ystart,WHEEL_Z),App.Vector(0,sign,0))

# ---------------- MANUAL PARALLELOGRAM LIFT ----------------
th, ux, uz = lift_pose(CAM_Z_LOW)
# Two visible side links in LOW position. Final production arms are flat plates, not rods.
for side_y in (-24.0,24.0):
    link = doc.addObject('Part::Feature',f'LiftLink_LOW_{"R" if side_y<0 else "L"}')
    link.Shape = cylinder_between((LIFT_PIVOT_X,side_y,LIFT_PIVOT_Z),(ux,side_y,uz),LINK_R)
    link.addProperty('App::PropertyString','Status').Status = 'kinematic envelope; replace with plate-arm solid'

# Lower pivot bosses
for side_y in (-24.0,24.0):
    p = doc.addObject('Part::Feature',f'LiftPivotBoss_{"R" if side_y<0 else "L"}')
    p.Shape = Part.makeCylinder(8.0,10.0,App.Vector(LIFT_PIVOT_X,side_y-5.0,LIFT_PIVOT_Z),App.Vector(0,1,0))

# Camera at LOW/DN150 position
cam_center_x = ux
cam = doc.addObject('Part::Feature','DigitalCameraHead_LOW_DN150_Envelope')
cam.Shape = Part.makeCylinder(CAM_R,CAM_LEN,
                              App.Vector(cam_center_x-CAM_LEN/2.0,0,CAM_Z_LOW),App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Motion').Motion = 'Ø52x72 envelope; TILT -105..+105; continuous ROLL 360'
cam.addProperty('App::PropertyString','Video').Video = 'fully digital; no coax/CVBS'

# ---------------- P0 INTERNAL PACKAGING ENVELOPES ----------------
control = doc.addObject('Part::Feature','P0_ZoneA_ControlStack_Envelope')
control.Shape = Part.makeBox(85.0,72.0,38.0,App.Vector(10.0,-36.0,14.0))
control.addProperty('App::PropertyString','Contents').Contents = 'NUCLEO-F446RE prototype + isolated comms + low-power conversion + sensor I/O'

# motor holder already occupies Zone B, X~100..198
power = doc.addObject('Part::Feature','P0_ZoneC_PowerStack_Envelope')
power.Shape = Part.makeBox(70.0,65.0,20.0,App.Vector(210.0,-32.5,14.0))
power.addProperty('App::PropertyString','Contents').Contents = '48V protection + ~200W half-brick 48->24 traction converter thermal-mounted to body'

rear_service = doc.addObject('Part::Feature','RearServiceZone_Envelope')
rear_service.Shape = Part.makeBox(22.0,70.0,55.0,App.Vector(282.0,-35.0,18.0))
rear_service.addProperty('App::PropertyString','Contents').Contents = 'tether electrical receptacle service loop + P0/P1/P2 fill manifold + strain-anchor access'

# ---------------- REAR TETHER / RECOVERY ----------------
tail = doc.addObject('Part::Feature','TetherBendSupport_Envelope')
tail.Shape = Part.makeCone(13.0,9.0,100.0,App.Vector(BODY_L,0,45.0),App.Vector(1,0,0))
tail.addProperty('App::PropertyString','Cable').Cable = 'rugged PUR robotic tether Ø8..12 class with separate aramid/UHMWPE strength member'
tail.addProperty('App::PropertyString','LoadPath').LoadPath = 'tensile member -> structural rear anchor; connector carries zero tether pull'

recovery = doc.addObject('Part::Feature','RearRecoveryEye_Envelope')
recovery.Shape = Part.makeTorus(12.0,3.0,App.Vector(295.0,0,82.0),App.Vector(0,1,0),0,360,360)
recovery.addProperty('App::PropertyString','Status').Status = 'structural eye envelope; exact machined/bolted geometry after final rear bulkhead'

# ---------------- MASTER RULES ----------------
rules = doc.addObject('App::FeaturePython','RevEQ_Rules')
rules.addProperty('App::PropertyString','Architecture').Architecture = 'CRP150-style 6WD layout; own PX-1 geometry/electronics'
rules.addProperty('App::PropertyString','Lift').Lift = 'manual parallelogram, L=120, pivot X200/Z94, LOW camera axis Z75; DN150 hard stop'
rules.addProperty('App::PropertyString','Camera').Camera = 'sealed digital Ø52x72 target, continuous internal ROLL, TILT ±105'
rules.addProperty('App::PropertyString','P0').P0 = 'front control stack / center motor holder / rear power stack / rear service zone'
rules.addProperty('App::PropertyString','Tail').Tail = 'rugged PUR tether, strength-member structural anchor, digital pair, no coax'
rules.addProperty('App::PropertyString','Pressure').Pressure = 'P0/P1/P2 isolated positive-pressure zones, common fill with check isolation'
rules.addProperty('App::PropertyString','Release').Release = 'INTEGRATION MASTER ONLY; full solids/physical samples/tests required before machining release'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevEQ.FCStd')
