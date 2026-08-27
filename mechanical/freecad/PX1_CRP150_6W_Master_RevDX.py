import FreeCAD as App, Part
# PX-1 Rev.DX — corrected CRP150-style six-wheel packaging master.
# Source-driven corrections: rectangular side cover + three axle flanges,
# five Z50 side gears, exact KHK m1.5 18/45 bevel envelopes, twin JGB37 motors.

doc = App.newDocument('PX1_CRP150_6W_Master_RevDX')

BODY_L = 307.0
BODY_W = 92.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
COVER_T = 5.0
COVER_X0 = 15.5
COVER_L = 276.0
COVER_Z0 = 5.0
COVER_H = 81.0
WHEEL_X = [50.0, 150.0, 250.0]
IDLER_X = [100.0, 200.0]
WHEEL_Z = 45.0
PIPE_R = 75.0
PIPE_AXIS_Z = 52.0480547
SIDE_WALL_Y = 36.0
COVER_OUT_Y = BODY_W/2.0 + COVER_T
GEAR_M = 1.0
GEAR_Z = 50
GEAR_OD = 52.0
GEAR_FACE = 8.0
WHEEL_INNER_Y = COVER_OUT_Y
WHEEL_CROWN_END_Y = 54.0
WHEEL_OUTER_Y = 67.0
WHEEL_R = 45.0
WHEEL_OUTER_R = 21.0
FLANGE_OD = 48.0
FLANGE_EXT = 6.0
MOTOR_D = 37.0
MOTOR_L = 90.0
MOTOR_Y = 19.0
BEVEL_SMALL_OD = 30.86
BEVEL_LARGE_OD = 68.18
BEVEL_SMALL_LEN = 21.97
BEVEL_LARGE_LEN = 21.10
BEVEL_CENTER_X = 150.0
BEVEL_CENTER_Z = 45.0
CAM_R = 26.0
CAM_LEN = 72.0
CAM_X = 64.1
CAM_Z_SAFE = 75.0


def cyl_y(radius, length, x, y, z, sign=1):
    return Part.makeCylinder(radius, length, App.Vector(x, y, z), App.Vector(0, sign, 0))


def tapered_wheel(x, side):
    sign = 1 if side == 'L' else -1
    y0 = sign * WHEEL_INNER_Y
    crown = cyl_y(WHEEL_R, WHEEL_CROWN_END_Y-WHEEL_INNER_Y,
                  x, y0, WHEEL_Z, sign)
    taper = Part.makeCone(WHEEL_R, WHEEL_OUTER_R,
                          WHEEL_OUTER_Y-WHEEL_CROWN_END_Y,
                          App.Vector(x, sign*WHEEL_CROWN_END_Y, WHEEL_Z),
                          App.Vector(0, sign, 0))
    # The production wheel will have a recessed center around the axle flange;
    # this master keeps the conservative external traction envelope.
    return crown.fuse(taper)


# Ideal DN150 reference
pipe = doc.addObject('Part::Feature', 'DN150_ID_Reference')
pipe.Shape = Part.makeCylinder(PIPE_R, BODY_L+100,
                               App.Vector(-50, 0, PIPE_AXIS_Z), App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Status').Status = 'IDEAL PIPE ID reference; not a manufactured component'

# Central pressure body P0
body = doc.addObject('Part::Feature', 'PressureBody_P0_Envelope')
body.Shape = Part.makeBox(BODY_L, BODY_W, BODY_Z1-BODY_Z0,
                          App.Vector(0, -BODY_W/2.0, BODY_Z0))
body.addProperty('App::PropertyString','Pressure').Pressure = 'P0 isolated body; +0.20..+0.30 bar normal'

# Rectangular side covers P1/P2
for side, sign in [('L',1),('R',-1)]:
    y0 = BODY_W/2.0 if sign > 0 else -BODY_W/2.0-COVER_T
    cov = doc.addObject('Part::Feature', f'SideCover_{side}')
    cov.Shape = Part.makeBox(COVER_L, COVER_T, COVER_H,
                             App.Vector(COVER_X0, y0, COVER_Z0))
    cov.addProperty('App::PropertyString','Architecture').Architecture = 'rectangular visible plate; internal 5-lobed gear cavity'
    cov.addProperty('App::PropertyString','Seal').Seal = 'FKM 190x2.5 candidate, racetrack groove; exact supplier gate'
    cov.addProperty('App::PropertyString','Pressure').Pressure = f'P{1 if side=="L" else 2} isolated side-drive zone'

# Six tapered wheel envelopes + three axle flanges per side
for x in WHEEL_X:
    for side, sign in [('L',1),('R',-1)]:
        w = doc.addObject('Part::Feature', f'Wheel_{side}_{int(x)}')
        w.Shape = tapered_wheel(x, side)
        w.addProperty('App::PropertyString','Mount').Mount = 'Ø12 keyed shaft + M6 axial retaining disk; recessed hub around flange'

        fy = sign*COVER_OUT_Y
        f = doc.addObject('Part::Feature', f'AxleFlange_{side}_{int(x)}')
        f.Shape = Part.makeCylinder(FLANGE_OD/2.0, FLANGE_EXT,
                                    App.Vector(x, fy, WHEEL_Z), App.Vector(0,sign,0))
        f.addProperty('App::PropertyString','Stack').Stack = '3xM3 PCD40; FKM 30x1.5 static O-ring; 61801 + 12x22x7 shaft seal'

# Five equal Z50 gears per side: wheel-idler-wheel-idler-wheel
for side, sign in [('L',1),('R',-1)]:
    gy = sign*41.0
    gd = App.Vector(0,sign,0)
    for x in WHEEL_X:
        g = doc.addObject('Part::Feature', f'WheelGear_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0, GEAR_FACE,
                                    App.Vector(x, gy, WHEEL_Z), gd)
        g.addProperty('App::PropertyString','Gear').Gear = 'KHK SSG1-50 class: m1 Z50 OD52 face8 bore12; hub shortening gate'
    for x in IDLER_X:
        g = doc.addObject('Part::Feature', f'IdlerGear_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0, GEAR_FACE,
                                    App.Vector(x, gy, WHEEL_Z), gd)
        g.addProperty('App::PropertyString','Gear').Gear = 'm1 Z50 OD52; fixed pin + replaceable bearing hub'

# Twin JGB37-555 longitudinal motor envelopes
for side, sign in [('L',1),('R',-1)]:
    m = doc.addObject('Part::Feature', f'JGB37_555_{side}_Envelope')
    m.Shape = Part.makeCylinder(MOTOR_D/2.0, MOTOR_L,
                                App.Vector(55.0, sign*MOTOR_Y, WHEEL_Z), App.Vector(1,0,0))
    m.addProperty('App::PropertyString','Spec').Spec = '24V ratio~56 ~107rpm candidate; exact purchased sample mandatory'

# Exact KHK bevel envelopes; tooth detail intentionally not modeled here.
# Small gear/pinion axes are longitudinal X, large bevel axes transverse Y.
for side, sign in [('L',1),('R',-1)]:
    small = doc.addObject('Part::Feature', f'KHK_SB1_5_1845H_{side}_Envelope')
    small.Shape = Part.makeCone(BEVEL_SMALL_OD/2.0, 8.0,
                                BEVEL_SMALL_LEN,
                                App.Vector(BEVEL_CENTER_X-BEVEL_SMALL_LEN, sign*MOTOR_Y, BEVEL_CENTER_Z),
                                App.Vector(1,0,0))
    small.addProperty('App::PropertyString','Catalog').Catalog = 'SB1.5-1845H m1.5 Z18 bore8 OD30.86 face11'

    # Place one large gear near each side of P0; hub points toward body center.
    y_start = sign*(SIDE_WALL_Y-BEVEL_LARGE_LEN)
    large = doc.addObject('Part::Feature', f'KHK_SB1_5_4518H_{side}_Envelope')
    large.Shape = Part.makeCone(BEVEL_LARGE_OD/2.0, 18.0,
                                BEVEL_LARGE_LEN,
                                App.Vector(BEVEL_CENTER_X, y_start, BEVEL_CENTER_Z),
                                App.Vector(0,sign,0))
    large.addProperty('App::PropertyString','Catalog').Catalog = 'SB1.5-4518H m1.5 Z45 bore10 OD68.18 face11; 2.5:1 pair'

# Camera DN150-safe envelope
cam = doc.addObject('Part::Feature','CameraHead_DN150_SAFE_Envelope')
cam.Shape = Part.makeCylinder(CAM_R, CAM_LEN,
                              App.Vector(CAM_X-CAM_LEN/2.0, 0, CAM_Z_SAFE), App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Motion').Motion = 'TILT -105..+105 deg; ROLL continuous 360; full sweep checker separate'

rules = doc.addObject('App::FeaturePython','MasterRules')
rules.addProperty('App::PropertyString','SourceCorrection').SourceCorrection = 'visible side cover rectangular + 3 axle flanges; five equal Z50 internal train'
rules.addProperty('App::PropertyString','WheelPitch').WheelPitch = '100 mm: X50/X150/X250, idlers X100/X200'
rules.addProperty('App::PropertyString','Bevel').Bevel = 'KHK SB1.5-1845H / SB1.5-4518H exact envelopes, ratio 2.5'
rules.addProperty('App::PropertyString','MotorSpacing').MotorSpacing = 'axes Y±19, Ø37 envelopes -> 1 mm nominal inter-motor gap'
rules.addProperty('App::PropertyString','Pressure').Pressure = 'P0/P1/P2 isolated, separately sensed, common fill manifold with check valves'
rules.addProperty('App::PropertyString','Release').Release = 'PACKAGING MASTER ONLY; no machining release until purchased-part and full-solid qualification'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevDX.FCStd')
