import FreeCAD as App, Part

# PX-1 Rev.CW
# Six-wheel CRP150-style packaging master.
# Reference/envelope model only — NOT machining RELEASE.

doc = App.newDocument('PX1_CRP150_6W_Master_RevCW')

# ----------------------
# Packaging parameters
# ----------------------
WHEEL_OD = 90.0
WHEEL_W = 18.0
WHEEL_R = WHEEL_OD / 2.0
WHEEL_X = [50.0, 150.0, 250.0]   # provisional 100 mm pitch
WHEEL_Z = 45.0
WHEEL_Y = 57.5                    # gives ~133 mm overall width with 18 mm wheels

BODY_X0 = 20.0
BODY_L = 260.0
BODY_W = 82.0
BODY_Z0 = 14.0
BODY_H = 72.0

COVER_L = 230.0
COVER_H = 66.0
COVER_T = 4.0
COVER_X0 = 35.0
COVER_Z0 = 12.0

# ----------------------
# Main pressure body
# ----------------------
body = doc.addObject('Part::Feature', 'MainPressureBody_Envelope')
body.Shape = Part.makeBox(BODY_L, BODY_W, BODY_H, App.Vector(BODY_X0, -BODY_W/2, BODY_Z0))
body.addProperty('App::PropertyString', 'Status').Status = 'PACKAGING ENVELOPE — final cast/machined shape TBD'
body.addProperty('App::PropertyString', 'Reference').Reference = 'CRP150-style low narrow chassis; own PX-1 geometry'

# top lid/service seam envelope
lid = doc.addObject('Part::Feature', 'TopServiceLid_Envelope')
lid.Shape = Part.makeBox(210, 66, 4, App.Vector(45, -33, BODY_Z0 + BODY_H))
lid.addProperty('App::PropertyString', 'Seal').Seal = 'continuous O-ring; pressurized dry volume'

# ----------------------
# Six wheels
# ----------------------
for side_name, y, direction in [('L', -WHEEL_Y, App.Vector(0,1,0)), ('R', WHEEL_Y, App.Vector(0,-1,0))]:
    for i, x in enumerate(WHEEL_X, 1):
        w = doc.addObject('Part::Feature', f'Wheel_{side_name}{i}')
        # cylinder axis along Y
        start_y = y - (WHEEL_W/2 if side_name == 'R' else -WHEEL_W/2)
        if side_name == 'R':
            p = App.Vector(x, y - WHEEL_W/2, WHEEL_Z)
            axis = App.Vector(0,1,0)
        else:
            p = App.Vector(x, y + WHEEL_W/2, WHEEL_Z)
            axis = App.Vector(0,-1,0)
        w.Shape = Part.makeCylinder(WHEEL_R, WHEEL_W, p, axis)
        w.addProperty('App::PropertyString', 'Size').Size = 'Ø90 x 18 baseline'

# ----------------------
# Pressurized side gear-bay covers
# ----------------------
for side_name, y in [('L', -(BODY_W/2 + COVER_T)), ('R', BODY_W/2)]:
    cover = doc.addObject('Part::Feature', f'PressurizedGearCover_{side_name}')
    cover.Shape = Part.makeBox(COVER_L, COVER_T, COVER_H, App.Vector(COVER_X0, y, COVER_Z0))
    cover.addProperty('App::PropertyString', 'Seal').Seal = 'continuous perimeter O-ring'
    cover.addProperty('App::PropertyString', 'Pressure').Pressure = 'common dry volume, target +0.20..+0.30 bar gauge'
    cover.addProperty('App::PropertyString', 'Service').Service = 'cover only; NOT cassette'

# ----------------------
# Side gear pitch envelopes
# z40 wheel gears + z60 single idler between wheel pairs
# m=1 gives exact 100 mm wheel pitch: 50 + 50 mm center distances.
# ----------------------
GEAR_WHEEL_PD = 40.0
GEAR_IDLER_PD = 60.0
GEAR_T = 8.0
IDLER_X = [100.0, 200.0]

for side_name, y0, axis in [('L', -(BODY_W/2 + 1.0), App.Vector(0,-1,0)), ('R', BODY_W/2 + 1.0, App.Vector(0,1,0))]:
    # wheel gears
    for i, x in enumerate(WHEEL_X, 1):
        g = doc.addObject('Part::Feature', f'WheelGear_z40_{side_name}{i}')
        p = App.Vector(x, y0, WHEEL_Z)
        g.Shape = Part.makeCylinder((GEAR_WHEEL_PD+2)/2, GEAR_T, p, axis)
        g.addProperty('App::PropertyString', 'Candidate').Candidate = 'm1, 20deg, z40, face 8 mm'
    # idlers
    for i, x in enumerate(IDLER_X, 1):
        g = doc.addObject('Part::Feature', f'IdlerGear_z60_{side_name}{i}')
        p = App.Vector(x, y0, WHEEL_Z)
        g.Shape = Part.makeCylinder((GEAR_IDLER_PD+2)/2, GEAR_T, p, axis)
        g.addProperty('App::PropertyString', 'Candidate').Candidate = 'm1, 20deg, z60, face 8 mm'

# ----------------------
# Motor packaging envelopes: longitudinal, one per side
# drive middle shaft through supported spur stage, not wheel radial load
# ----------------------
for side_name, y in [('L', -22.0), ('R', 22.0)]:
    motor = doc.addObject('Part::Feature', f'JGB37_520_Envelope_{side_name}')
    motor.Shape = Part.makeCylinder(19.0, 82.0, App.Vector(106.0, y, 58.0), App.Vector(1,0,0))
    motor.addProperty('App::PropertyString', 'Spec').Spec = '24 V, ~40-50 rpm class; exact purchased SKU HOLD'

# ----------------------
# CRP150-style central manual camera lift packaging base
# ----------------------
lift_base = doc.addObject('Part::Feature', 'ManualLift_Base_Envelope')
lift_base.Shape = Part.makeBox(92, 58, 7, App.Vector(104, -29, BODY_Z0 + BODY_H + 4))
lift_base.addProperty('App::PropertyString', 'Architecture').Architecture = 'central manual indexed lift, CRP150-style system layout'

# folded lift clearance envelope
folded = doc.addObject('Part::Feature', 'Lift_Folded_Keepout')
folded.Shape = Part.makeBox(112, 64, 28, App.Vector(94, -32, BODY_Z0 + BODY_H + 11))
folded.addProperty('App::PropertyString', 'Status').Status = 'KEEP-OUT only; linkage geometry to be redesigned'

# camera head envelope at LOW position — intentionally compact placeholder
cam = doc.addObject('Part::Feature', 'DigitalCameraHead_Envelope')
cam.Shape = Part.makeCylinder(26.0, 72.0, App.Vector(114, 0, 112), App.Vector(1,0,0))
cam.addProperty('App::PropertyString', 'Motion').Motion = 'TILT approx -105..+105; ROLL continuous 360'

# ----------------------
# Rear tether / strain relief envelope
# ----------------------
tail = doc.addObject('Part::Feature', 'RearTether_Interface_Envelope')
tail.Shape = Part.makeCylinder(22, 38, App.Vector(280, 0, 50), App.Vector(1,0,0))
tail.addProperty('App::PropertyString', 'Rule').Rule = 'tensile member terminates mechanically; connector contacts carry no pull load'

# lifting eye envelope
for x in (55.0, 245.0):
    eye = doc.addObject('Part::Feature', f'LoweringEye_{int(x)}')
    eye.Shape = Part.makeTorus(8, 2.5, App.Vector(x, 0, 94), App.Vector(0,1,0), 0, 360, 360)

# ----------------------
# Rules object
# ----------------------
rules = doc.addObject('App::FeaturePython', 'RevCW_Rules')
rules.addProperty('App::PropertyString', 'OverallTarget').OverallTarget = '305-320 L x 130-140 W x 105-115 H chassis class'
rules.addProperty('App::PropertyString', 'Drive').Drive = '6WD, one motor per side, spur gears only'
rules.addProperty('App::PropertyString', 'WheelPitch').WheelPitch = '100 mm provisional; z40/z60/z40 geometry gives same rotation direction'
rules.addProperty('App::PropertyString', 'Pressure').Pressure = '+0.20..+0.30 bar gauge prototype target; seals remain mandatory'
rules.addProperty('App::PropertyString', 'Release').Release = 'NO RELEASE until exact CRP150-reference packaging, DN150 sweep, shaft seals and motor fit are verified'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevCW.FCStd')
