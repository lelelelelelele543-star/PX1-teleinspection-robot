import FreeCAD as App, Part
# PX-1 Rev.DP
# Corrected CRP150-style six-wheel packaging master.
# Key correction versus Rev.DA: tapered Ø90 wheels and DN150 pipe position
# solved from wheel contact, not from overall-width-only logic.

doc = App.newDocument('PX1_CRP150_6W_Master_RevDP')

# ---------------- MASTER PARAMETERS ----------------
BODY_L = 307.0
BODY_W = 92.0
BODY_H = 76.0
BODY_Z0 = 14.0
COVER_T = 5.0
WHEEL_AXIS_Z = 45.0
WHEEL_X = [50.0, 150.0, 250.0]
PIPE_R = 75.0
PIPE_AXIS_Z = 52.0480547   # solved from Rev.DL contact at |Y|54, r45
SIDE_BAY_D = 10.0
CENTRAL_HALF_W = BODY_W/2.0 - SIDE_BAY_D
GEAR_FACE = 8.0

# Wheel profile, positive side: crown Y51..54 r45, taper to Y67 r21.
WHEEL_INNER_Y = BODY_W/2.0 + COVER_T  # 51
WHEEL_CROWN_END_Y = 54.0
WHEEL_OUTER_Y = 67.0
WHEEL_R = 45.0
WHEEL_OUTER_R = 21.0

# ---------------- HELPERS ----------------
def cyl_y(radius, length, x, y, z, sign=1):
    return Part.makeCylinder(radius, length, App.Vector(x,y,z), App.Vector(0,sign,0))


def tapered_wheel(x, side):
    """Simplified solid of the new asymmetric/crowned wheel envelope."""
    sign = 1 if side == 'L' else -1
    y0 = sign * WHEEL_INNER_Y
    # 3 mm full-diameter crown.
    crown = cyl_y(WHEEL_R, WHEEL_CROWN_END_Y-WHEEL_INNER_Y,
                  x, y0, WHEEL_AXIS_Z, sign)
    # 13 mm tapered shoulder. makeCone radius1->radius2 along Y.
    taper_start_y = sign * WHEEL_CROWN_END_Y
    taper = Part.makeCone(WHEEL_R, WHEEL_OUTER_R,
                          WHEEL_OUTER_Y-WHEEL_CROWN_END_Y,
                          App.Vector(x,taper_start_y,WHEEL_AXIS_Z),
                          App.Vector(0,sign,0))
    return crown.fuse(taper)

# ---------------- IDEAL DN150 PIPE ----------------
pipe = doc.addObject('Part::Feature', 'DN150_ID_Reference')
pipe.Shape = Part.makeCylinder(PIPE_R, BODY_L+80,
                               App.Vector(-40,0,PIPE_AXIS_Z), App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Reference').Reference = 'IDEAL ID150 envelope; visualization/check reference only'

# ---------------- BODY ----------------
body = doc.addObject('Part::Feature', 'PressureBody_Envelope')
body.Shape = Part.makeBox(BODY_L, BODY_W, BODY_H,
                          App.Vector(0,-BODY_W/2.0,BODY_Z0))
body.addProperty('App::PropertyString','Envelope').Envelope = '307 x 92 x 76 mm packaging candidate'
body.addProperty('App::PropertyString','PressureZones').PressureZones = 'P0 electronics body isolated from P1/P2 side-drive bays'

central = doc.addObject('Part::Feature','CentralDryVolume_Envelope')
central.Shape = Part.makeBox(BODY_L-16, 2*CENTRAL_HALF_W, BODY_H-12,
                             App.Vector(8,-CENTRAL_HALF_W,BODY_Z0+6))
central.addProperty('App::PropertyString','Use').Use = 'electronics + 2 traction motors + compact DC/DC; keep-out'

# ---------------- SIDE COVERS / BAYS ----------------
for side, sign in [('L',1),('R',-1)]:
    y0 = BODY_W/2.0 if sign>0 else -BODY_W/2.0-COVER_T
    cov = doc.addObject('Part::Feature', f'SideCover_{side}')
    cov.Shape = Part.makeBox(276.0,COVER_T,82.0,App.Vector(15.5,y0,4.0))
    cov.addProperty('App::PropertyString','Seal').Seal = 'continuous FKM O-ring; ~200x3 candidate after real groove verification'
    cov.addProperty('App::PropertyString','Locate').Locate = 'machined pilot + 2 dowels; perimeter M4 clamp screws'
    cov.addProperty('App::PropertyString','Pressure').Pressure = 'isolated P1/P2, normal +0.20..+0.30 bar, structure target 1 bar differential'

# ---------------- SIX TAPERED WHEELS ----------------
for x in WHEEL_X:
    for side in ('L','R'):
        w = doc.addObject('Part::Feature',f'Wheel_{side}_{int(x)}')
        w.Shape = tapered_wheel(x,side)
        w.addProperty('App::PropertyString','Profile').Profile = 'Ø90 crown 3mm + tapered shoulder to r21 at |Y|67; prototype profile'
        w.addProperty('App::PropertyString','Mount').Mount = 'keyed Ø10 shaft; M6 axial retaining disk/bolt; serviceable'

# ---------------- SIDE SPUR TRAIN ----------------
for side, sign in [('L',1),('R',-1)]:
    gy = sign*(BODY_W/2.0-SIDE_BAY_D)
    gd = App.Vector(0,sign,0)
    for x in WHEEL_X:
        g = doc.addObject('Part::Feature',f'WheelGear_z40_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(21.0,GEAR_FACE,App.Vector(x,gy,WHEEL_AXIS_Z),gd)
        g.addProperty('App::PropertyString','Gear').Gear = 'm1.0 z40 20deg; OD envelope ~42'
    for x in (100.0,200.0):
        g = doc.addObject('Part::Feature',f'Idler_z60_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(31.0,GEAR_FACE,App.Vector(x,gy,WHEEL_AXIS_Z),gd)
        g.addProperty('App::PropertyString','Gear').Gear = 'm1.0 z60 20deg; 608-2RS idler candidate'

# ---------------- WHEEL STATION BOSSES ----------------
for x in WHEEL_X:
    for side, sign in [('L',1),('R',-1)]:
        y0 = sign*(BODY_W/2.0-1.0)
        d = App.Vector(0,sign,0)
        boss = doc.addObject('Part::Feature',f'WheelSealBearingBoss_{side}_{int(x)}')
        boss.Shape = Part.makeCylinder(15.0,10.0,App.Vector(x,y0,WHEEL_AXIS_Z),d)
        boss.addProperty('App::PropertyString','Stack').Stack = 'labyrinth + FKM TC 10x22x7 + 6000-2RS outer; z40 between bearings; 6000-2RS inner'

# ---------------- CRP150-STYLE BEVEL INPUT ----------------
# Reference architecture only: Z16 small -> Z40 large = 2.5:1.
# Envelopes are cones/cylinders, not involute bevel teeth.
for side, sign, zc in [('L',1,54.0),('R',-1,36.0)]:
    # Longitudinal Ø37 motor envelope (JGB37-555 candidate)
    motor = doc.addObject('Part::Feature',f'JGB37_555_{side}_Envelope')
    motor.Shape = Part.makeCylinder(18.5,100.0,App.Vector(70.0,sign*17.5,zc),App.Vector(1,0,0))
    motor.addProperty('App::PropertyString','Spec').Spec = '24V, ratio~56, ~107rpm no-load candidate; exact sample mandatory'

    small = doc.addObject('Part::Feature',f'BevelPinion_Z16_{side}_Envelope')
    small.Shape = Part.makeCone(9.0,4.0,12.0,App.Vector(170.0,sign*17.5,zc),App.Vector(1,0,0))
    small.addProperty('App::PropertyString','Reference').Reference = 'Z16 reference architecture, exact module/cone geometry HOLD'

    large = doc.addObject('Part::Feature',f'BevelGear_Z40_{side}_Envelope')
    large.Shape = Part.makeCone(21.0,8.0,12.0,App.Vector(182.0,sign*17.5,zc-12.0),App.Vector(0,sign,0))
    large.addProperty('App::PropertyString','Reference').Reference = 'Z40 reference architecture, 2.5:1 target; exact tooth system HOLD'

# ---------------- MANUAL LIFT / CAMERA SAFE ENVELOPE ----------------
liftbase = doc.addObject('Part::Feature','ManualLift_Base_Envelope')
liftbase.Shape = Part.makeBox(110,54,8,App.Vector(178,-27,90))
liftbase.addProperty('App::PropertyString','Mechanism').Mechanism = 'CRP150-style manual lift: 150N gas spring + M8 clamp + disc springs; own linkage geometry'

# Corrected DN150 SAFE target, camera axis Z=76 max provisional.
CAM_CENTER_X = 64.1
CAM_Z_SAFE = 76.0
CAM_LEN = 72.0
CAM_R = 26.0
cam = doc.addObject('Part::Feature','CameraHead_Envelope_DN150_SAFE')
cam.Shape = Part.makeCylinder(CAM_R,CAM_LEN,
                              App.Vector(CAM_CENTER_X-CAM_LEN/2.0,0,CAM_Z_SAFE),
                              App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Safe').Safe = 'Ø52x72 simplified envelope; DN150 SAFE axis <=76mm after corrected pipe-contact model'

# ---------------- MASTER RULES ----------------
rules = doc.addObject('App::FeaturePython','MasterRules')
rules.addProperty('App::PropertyString','Architecture').Architecture = 'CRP150-style 6WD; own geometry/electronics; no proprietary part copying'
rules.addProperty('App::PropertyString','OverallWidth').OverallWidth = 'outer wheel faces ±67 -> 134 mm nominal'
rules.addProperty('App::PropertyString','WheelPitch').WheelPitch = '100 + 100 mm, centers X50/X150/X250'
rules.addProperty('App::PropertyString','DN150PipeAxis').DN150PipeAxis = f'Z={PIPE_AXIS_Z:.2f} mm solved from wheel contact, not wheel-axis assumption'
rules.addProperty('App::PropertyString','Drive').Drive = 'JGB37-555 candidate -> Z16/Z40 bevel reduction -> z40/z60 3-wheel side train'
rules.addProperty('App::PropertyString','Pressure').Pressure = '3 isolated zones P0/P1/P2; normal +0.20..+0.30 bar; individual monitoring'
rules.addProperty('App::PropertyString','Release').Release = 'NO MACHINING RELEASE until full-solid DN150 check + real wheel/motor/connector samples + pressure tests'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevDP.FCStd')
