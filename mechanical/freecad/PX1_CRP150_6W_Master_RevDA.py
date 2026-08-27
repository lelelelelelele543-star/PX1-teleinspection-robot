import FreeCAD as App, Part
# PX-1 Rev.DA
# Parametric packaging master for the CRP150-style 6-wheel architecture.
# Purchased components are envelope models unless explicitly stated.

doc = App.newDocument('PX1_CRP150_6W_Master_RevDA')

# ---------------- MASTER PARAMETERS ----------------
BODY_L = 307.0
BODY_W = 92.0
BODY_H = 76.0
BODY_Z0 = 14.0
COVER_T = 5.0
WHEEL_OD = 90.0
WHEEL_W = 16.0
WHEEL_Z = 45.0
WHEEL_X = [50.0, 150.0, 250.0]
SIDE_BAY_D = 10.0
CENTRAL_HALF_W = BODY_W/2.0 - SIDE_BAY_D
GEAR_FACE = 8.0

# overall width = body + 2 covers + 2 wheels
OVERALL_W = BODY_W + 2*COVER_T + 2*WHEEL_W

# ---------------- BODY ----------------
body = doc.addObject('Part::Feature', 'PressureBody_Envelope')
body.Shape = Part.makeBox(BODY_L, BODY_W, BODY_H,
                          App.Vector(0, -BODY_W/2.0, BODY_Z0))
body.addProperty('App::PropertyString','Status').Status = 'PACKAGING ENVELOPE; detailed machining not released'
body.addProperty('App::PropertyString','Envelope').Envelope = f'{BODY_L:.1f} x {BODY_W:.1f} x {BODY_H:.1f} mm'

# central dry volume visualization
central = doc.addObject('Part::Feature', 'CentralDryVolume_Envelope')
central.Shape = Part.makeBox(BODY_L-16, 2*CENTRAL_HALF_W, BODY_H-12,
                             App.Vector(8, -CENTRAL_HALF_W, BODY_Z0+6))
central.addProperty('App::PropertyString','Note').Note = 'electronics + 2 longitudinal traction motors; keep-out only'

# ---------------- SIDE COVERS ----------------
for side, sy in [('L', +1), ('R', -1)]:
    y0 = BODY_W/2.0 if sy > 0 else -BODY_W/2.0-COVER_T
    cov = doc.addObject('Part::Feature', f'SideCover_{side}')
    cov.Shape = Part.makeBox(276.0, COVER_T, 82.0,
                             App.Vector(15.5, y0, 4.0))
    cov.addProperty('App::PropertyString','Seal').Seal = 'continuous FKM O-ring in rounded-rectangle groove'
    cov.addProperty('App::PropertyString','Location').Location = 'machined pilot + 2 dowels; screws clamp only'

# ---------------- WHEELS ----------------
for x in WHEEL_X:
    for side, sy in [('L', +1), ('R', -1)]:
        if sy > 0:
            y0 = BODY_W/2.0 + COVER_T
            direction = App.Vector(0,1,0)
        else:
            y0 = -BODY_W/2.0 - COVER_T
            direction = App.Vector(0,-1,0)
        wheel = doc.addObject('Part::Feature', f'Wheel_{side}_{int(x)}')
        wheel.Shape = Part.makeCylinder(WHEEL_OD/2.0, WHEEL_W,
                                        App.Vector(x, y0, WHEEL_Z), direction)
        wheel.addProperty('App::PropertyString','Mount').Mount = 'keyed Ø10 shaft + M8 axial retainer; removable without opening body'

# ---------------- GEAR PITCH/OD ENVELOPES ----------------
# Gear cylinders are simplified envelopes; no involute teeth in the packaging master.
# side bay runs inside each structural side wall.
for side, sy in [('L', +1), ('R', -1)]:
    if sy > 0:
        gy = BODY_W/2.0 - SIDE_BAY_D
        gd = App.Vector(0,1,0)
    else:
        gy = -BODY_W/2.0 + SIDE_BAY_D
        gd = App.Vector(0,-1,0)

    for x in WHEEL_X:
        g = doc.addObject('Part::Feature', f'WheelGear_z40_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(21.0, GEAR_FACE, App.Vector(x, gy, WHEEL_Z), gd) # approx OD42
        g.addProperty('App::PropertyString','Gear').Gear = 'm1.0 z40 20deg; envelope OD≈42'

    for x in (100.0, 200.0):
        g = doc.addObject('Part::Feature', f'Idler_z60_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(31.0, GEAR_FACE, App.Vector(x, gy, WHEEL_Z), gd) # approx OD62
        g.addProperty('App::PropertyString','Gear').Gear = 'm1.0 z60 20deg; 608-2RS idler bearing candidate'

# ---------------- SHAFT AXIS / SEAL BOSSES ----------------
for x in WHEEL_X:
    for side, sy in [('L', +1), ('R', -1)]:
        # simplified outer cover boss / seal+outer-bearing reservation
        y0 = BODY_W/2.0-1 if sy > 0 else -BODY_W/2.0+1
        d = App.Vector(0,1,0) if sy > 0 else App.Vector(0,-1,0)
        boss = doc.addObject('Part::Feature', f'SealBearingBoss_{side}_{int(x)}')
        boss.Shape = Part.makeCylinder(15.0, 10.0, App.Vector(x,y0,WHEEL_Z), d)
        boss.addProperty('App::PropertyString','Stack').Stack = '10x22x7 FKM seal + 6000-2RS outer bearing; inner 6000-2RS in fixed wall'

# ---------------- MOTOR ENVELOPES ----------------
# Two Ø37 longitudinal motors are vertically staggered to fit the narrow body.
# Envelope: Ø37 x 85 mm, exact vendor length HOLD.
for side, y, z, x0 in [('L', +17.5, 50.0, 108.0), ('R', -17.5, 38.0, 108.0)]:
    m = doc.addObject('Part::Feature', f'JGB37_520_{side}_Envelope')
    m.Shape = Part.makeCylinder(18.5, 85.0, App.Vector(x0,y,z), App.Vector(1,0,0))
    m.addProperty('App::PropertyString','Spec').Spec = '24V, target ~45rpm; exact purchased motor must be measured'
    m.addProperty('App::PropertyString','Mount').Mount = 'replaceable adapter; motor does not carry wheel radial load'

# ---------------- PRESSURE PASSAGES ----------------
for side, y in [('L', CENTRAL_HALF_W), ('R', -CENTRAL_HALF_W)]:
    p = doc.addObject('Part::Feature', f'PressurePassage_{side}_Envelope')
    p.Shape = Part.makeCylinder(2.5, SIDE_BAY_D+4,
                                App.Vector(145.0,y,30.0),
                                App.Vector(0,1 if side=='L' else -1,0))
    p.addProperty('App::PropertyString','Function').Function = 'central dry volume to sealed side bay; common +0.20..+0.30bar system'

# ---------------- CAMERA LIFT PACKAGING ----------------
liftbase = doc.addObject('Part::Feature','ManualLift_Base_Envelope')
liftbase.Shape = Part.makeBox(105, 54, 8, App.Vector(92, -27, BODY_Z0+BODY_H))
liftbase.addProperty('App::PropertyString','Status').Status = 'CRP150-style manual central lift; detailed parallelogram geometry follows next gate'

cam = doc.addObject('Part::Feature','CameraHead_Envelope_LOW')
cam.Shape = Part.makeCylinder(26, 72, App.Vector(108,0,103), App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Function').Function = 'modern PX-1 digital TILT/ROLL head; low-position packaging envelope'

# ---------------- MASTER RULES ----------------
rules = doc.addObject('App::FeaturePython','MasterRules')
rules.addProperty('App::PropertyString','OverallWidth').OverallWidth = f'{OVERALL_W:.1f} mm nominal with {WHEEL_W:.0f} mm wheels'
rules.addProperty('App::PropertyString','Wheelbase').Wheelbase = '100 mm front-middle + 100 mm middle-rear'
rules.addProperty('App::PropertyString','Pressure').Pressure = '+0.20..+0.30 bar operating; joints mechanically target >=1 bar differential proof'
rules.addProperty('App::PropertyString','Drive').Drive = '6WD, one motor per side, all spur gears, sealed pressurized side bays'
rules.addProperty('App::PropertyString','Service').Service = 'wheels and side covers removable with common tools; no gearbox cassette'
rules.addProperty('App::PropertyString','Release').Release = 'NO MACHINING RELEASE until exact motors, seals, O-ring and DN150 sweep are physically verified'

# dimensional sanity flags
rules.addProperty('App::PropertyString','DN150WidthCheck').DN150WidthCheck = ('PASS packaging width <150 mm' if OVERALL_W < 150 else 'FAIL width >=150 mm')

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevDA.FCStd')
