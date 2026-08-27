import FreeCAD as App, Part
# PX-1 Rev.EJ — integrated CRP150-style drivetrain/housing master.
# Architecture basis: uploaded DRW-002-374 / 375 / 386.
# Own PX-1 geometry: 6 wheels, five equal Z50 side gears, paired JGB37 holder,
# separate P0/P1/P2 pressure zones, transfer shafts and removable side drives.
# Envelope/detail master only — NOT machining RELEASE.

doc = App.newDocument('PX1_CRP150_6W_Master_RevEJ')

# ---------------- MASTER DATUMS ----------------
BODY_L = 307.0
BODY_W = 92.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
BODY_H = BODY_Z1-BODY_Z0
WHEEL_X = [50.0, 150.0, 250.0]
IDLER_X = [100.0, 200.0]
WHEEL_Z = 45.0
PIPE_R = 75.0
PIPE_AXIS_Z = 52.0480547

SIDE_COVER_T = 5.0
SIDE_COVER_X0 = 15.5
SIDE_COVER_L = 276.0
SIDE_COVER_Z0 = 5.0
SIDE_COVER_H = 81.0
SIDE_COVER_Y = BODY_W/2.0

TOP_COVER_X0 = 16.0
TOP_COVER_L = 275.0
TOP_COVER_W = 74.0
TOP_COVER_T = 5.0

GEAR_M = 1.0
GEAR_Z = 50
GEAR_OD = 52.0
GEAR_FACE = 8.0
GEAR_Y = 38.0

B61801_ID = 12.0
B61801_OD = 21.0
B61801_W = 5.0
B61903_ID = 17.0
B61903_OD = 30.0
B61903_W = 7.0
B61800_ID = 10.0
B61800_OD = 19.0
B61800_W = 5.0

MOTOR_D = 37.0
MOTOR_L = 90.0
MOTOR_AXIS_Y = 19.0
MOTOR_AXIS_Z = 45.0
MOTOR_X0 = 52.0

BEVEL_X = 150.0
BEVEL_Z = 45.0
BEVEL_SMALL_OD = 30.86
BEVEL_SMALL_LEN = 21.97
BEVEL_LARGE_OD = 68.18
BEVEL_LARGE_LEN = 21.10

FLANGE_OD = 50.0
FLANGE_EXT = 7.0

# Wheel envelope retained from DN150 correction.
WHEEL_INNER_Y = BODY_W/2.0 + SIDE_COVER_T
WHEEL_CROWN_END_Y = 54.0
WHEEL_OUTER_Y = 67.0
WHEEL_R = 45.0
WHEEL_OUTER_R = 21.0

CAM_R = 26.0
CAM_LEN = 72.0
CAM_X = 64.1
CAM_Z_SAFE = 75.0

# ---------------- HELPERS ----------------
def cyl_y(r, length, x, y, z, sign=1):
    return Part.makeCylinder(r, length, App.Vector(x, y, z), App.Vector(0, sign, 0))


def cyl_x(r, length, x, y, z):
    return Part.makeCylinder(r, length, App.Vector(x, y, z), App.Vector(1, 0, 0))


def wheel_shape(x, side):
    s = 1 if side == 'L' else -1
    crown = cyl_y(WHEEL_R, WHEEL_CROWN_END_Y-WHEEL_INNER_Y,
                  x, s*WHEEL_INNER_Y, WHEEL_Z, s)
    shoulder = Part.makeCone(WHEEL_R, WHEEL_OUTER_R,
                             WHEEL_OUTER_Y-WHEEL_CROWN_END_Y,
                             App.Vector(x, s*WHEEL_CROWN_END_Y, WHEEL_Z),
                             App.Vector(0, s, 0))
    return crown.fuse(shoulder)


def ring_y(od, id_, width, x, y, z, sign=1):
    outer = cyl_y(od/2.0, width, x, y, z, sign)
    inner = cyl_y(id_/2.0, width+0.2, x, y-0.1*sign, z, sign)
    return outer.cut(inner)

# ---------------- DN150 REFERENCE ----------------
pipe = doc.addObject('Part::Feature', 'DN150_ID_Reference')
pipe.Shape = Part.makeCylinder(PIPE_R, BODY_L+100,
                               App.Vector(-50,0,PIPE_AXIS_Z), App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Status').Status = 'Ideal pipe ID reference; wheel crown intentional contact'

# ---------------- MAIN P0 TROUGH BODY ----------------
outer = Part.makeBox(BODY_L, BODY_W, BODY_H, App.Vector(0,-BODY_W/2.0,BODY_Z0))
# Open-top cavity leaves ~10 mm side walls, 6 mm bottom, 12 mm front/rear walls.
inner = Part.makeBox(BODY_L-24.0, BODY_W-20.0, BODY_H-6.0,
                     App.Vector(12.0, -(BODY_W-20.0)/2.0, BODY_Z0+6.0))
body_shape = outer.cut(inner)
body = doc.addObject('Part::Feature','MainPressureHousing_P0')
body.Shape = body_shape
body.addProperty('App::PropertyString','Material').Material = 'Al 6082-T6 candidate, CNC one-piece trough'
body.addProperty('App::PropertyString','Pressure').Pressure = 'P0 isolated; normal +0.20..+0.30 bar'
body.addProperty('App::PropertyString','Datum').Datum = 'side drivetrain and bevel-output bores referenced to one machined body datum system'

# Top electronic service cover.
top = doc.addObject('Part::Feature','ElectronicServiceCover_P0')
top.Shape = Part.makeBox(TOP_COVER_L, TOP_COVER_W, TOP_COVER_T,
                         App.Vector(TOP_COVER_X0,-TOP_COVER_W/2.0,BODY_Z1))
top.addProperty('App::PropertyString','Seal').Seal = 'continuous FKM face O-ring; exact section/path after final opening design'
top.addProperty('App::PropertyString','Fasteners').Fasteners = 'M4 perimeter, cover located by pilot/dowels, not screw clearance'

# Lift holding ears: permanent structural mounts outside service-cover load path.
for y in (-40.0, 32.0):
    ear = doc.addObject('Part::Feature',f'LiftStructuralEar_{"R" if y<0 else "L"}')
    ear.Shape = Part.makeBox(38.0,8.0,28.0,App.Vector(176.0,y,88.0))
    ear.addProperty('App::PropertyString','Function').Function='manual lift loads bypass electronic cover seal'

# ---------------- SIDE COVERS P1/P2 ----------------
for side,s in [('L',1),('R',-1)]:
    y0 = SIDE_COVER_Y if s>0 else -SIDE_COVER_Y-SIDE_COVER_T
    cov = doc.addObject('Part::Feature',f'SideCover_{side}_P{1 if s>0 else 2}')
    cov.Shape = Part.makeBox(SIDE_COVER_L,SIDE_COVER_T,SIDE_COVER_H,
                             App.Vector(SIDE_COVER_X0,y0,SIDE_COVER_Z0))
    cov.addProperty('App::PropertyString','Seal').Seal='main continuous FKM O-ring; source architecture uses one large side-cover O-ring'
    cov.addProperty('App::PropertyString','Service').Service='remove for Z50/idler access; three axle flanges can be serviced locally'

# ---------------- FIVE-Z50 SIDE TRAIN + WHEEL STATIONS ----------------
for side,s in [('L',1),('R',-1)]:
    gd = App.Vector(0,s,0)
    gy = s*GEAR_Y

    # Wheel gears.
    for x in WHEEL_X:
        g = doc.addObject('Part::Feature',f'WheelGear_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),gd)
        g.addProperty('App::PropertyString','Spec').Spec='m1 Z50 face8, keyed Ø12 shaft candidate'

    # Idlers.
    for x in IDLER_X:
        g = doc.addObject('Part::Feature',f'IdlerGear_Z50_{side}_{int(x)}')
        g.Shape = Part.makeCylinder(GEAR_OD/2.0,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),gd)
        g.addProperty('App::PropertyString','Support').Support='fixed structural pin + replaceable 10-12-4-class bushing/bearing candidate'

    # Wheels, stepped axles, bearings and flanges.
    for x in WHEEL_X:
        w = doc.addObject('Part::Feature',f'Wheel_{side}_{int(x)}')
        w.Shape = wheel_shape(x,side)
        w.addProperty('App::PropertyString','Mount').Mount='keyed wheel hub, axial M6 retainer, replaceable traction ring'

        # Ø12 inboard shaft from side-drive wall toward flange.
        shaft12 = doc.addObject('Part::Feature',f'Axle12_{side}_{int(x)}')
        shaft12.Shape = cyl_y(6.0,22.0,x,s*29.0,WHEEL_Z,s)
        shaft12.addProperty('App::PropertyString','Journal').Journal='Ø12 h6 gear/bearing journal; 4x4 key candidate'

        # Ø17 outer support section.
        shaft17 = doc.addObject('Part::Feature',f'Axle17_{side}_{int(x)}')
        shaft17.Shape = cyl_y(8.5,28.0,x,s*51.0,WHEEL_Z,s)
        shaft17.addProperty('App::PropertyString','Journal').Journal='Ø17 h6 outer wheel-load journal; seal surface final after selected FKM element'

        # Two 61801 envelopes.
        for j,yabs in enumerate((31.0,44.0),start=1):
            b = doc.addObject('Part::Feature',f'B61801_{side}_{int(x)}_{j}')
            b.Shape = ring_y(B61801_OD,B61801_ID,B61801_W,x,s*yabs,WHEEL_Z,s)

        # Axle flange + 61903.
        fy = s*(SIDE_COVER_Y+SIDE_COVER_T)
        fl = doc.addObject('Part::Feature',f'AxleFlange_{side}_{int(x)}')
        fl.Shape = Part.makeCylinder(FLANGE_OD/2.0,FLANGE_EXT,
                                     App.Vector(x,fy,WHEEL_Z),App.Vector(0,s,0))
        fl.addProperty('App::PropertyString','StaticSeal').StaticSeal='FKM 32x1.5 class; 3-bolt removable flange concept'

        b3 = doc.addObject('Part::Feature',f'B61903_{side}_{int(x)}')
        b3.Shape = ring_y(B61903_OD,B61903_ID,B61903_W,x,s*52.0,WHEEL_Z,s)

        seal = doc.addObject('Part::Feature',f'WheelDynamicSeal_{side}_{int(x)}_Envelope')
        seal.Shape = ring_y(31.0,17.0,6.0,x,s*59.0,WHEEL_Z,s)
        seal.addProperty('App::PropertyString','Status').Status='FKM dynamic seal/quad-ring candidate; exact article HOLD'

# ---------------- CENTRAL TRANSFER SHAFTS P0 -> P1/P2 ----------------
for side,s in [('L',1),('R',-1)]:
    # Main transfer shaft envelope: Ø10 bearing/gear area, Ø18 seal land, Ø12 side stub.
    tr10 = doc.addObject('Part::Feature',f'TransferShaft10_{side}')
    tr10.Shape = cyl_y(5.0,28.0,BEVEL_X,s*10.0,BEVEL_Z,s)
    tr10.addProperty('App::PropertyString','Function').Function='KHK large bevel gear + 61800 bearing journal'

    tr18 = doc.addObject('Part::Feature',f'TransferSealJournal18_{side}')
    tr18.Shape = cyl_y(9.0,9.0,BEVEL_X,s*38.0,BEVEL_Z,s)
    tr18.addProperty('App::PropertyString','Finish').Finish='Ø18 dynamic seal journal, Ra<=0.4 um target, no key/thread under lip'

    stub = doc.addObject('Part::Feature',f'TransferStub12_{side}')
    stub.Shape = cyl_y(6.0,10.0,BEVEL_X,s*47.0,BEVEL_Z,s)
    stub.addProperty('App::PropertyString','Coupling').Coupling='positive removable dog/keyed coupling to middle long axle'

    b0 = doc.addObject('Part::Feature',f'B61800_Transfer_{side}')
    b0.Shape = ring_y(B61800_OD,B61800_ID,B61800_W,BEVEL_X,s*32.0,BEVEL_Z,s)

    seal0 = doc.addObject('Part::Feature',f'ShaftSeal18x30x7_{side}_Envelope')
    seal0.Shape = ring_y(30.0,18.0,7.0,BEVEL_X,s*39.0,BEVEL_Z,s)
    seal0.addProperty('App::PropertyString','Boundary').Boundary='secondary dynamic boundary P0 <-> side drive'

    dog = doc.addObject('Part::Feature',f'ServiceDogCoupling_{side}_Envelope')
    dog.Shape = cyl_y(11.0,9.0,BEVEL_X,s*51.0,BEVEL_Z,s)
    dog.addProperty('App::PropertyString','Service').Service='metal positive drive, OD<=22 target; side unit removable without disturbing bevel gear'

    # Large KHK bevel envelope on transverse shaft.
    large = doc.addObject('Part::Feature',f'KHK_SB1_5_4518H_{side}_Envelope')
    ystart = s*(19.0-BEVEL_LARGE_LEN/2.0)
    large.Shape = Part.makeCone(BEVEL_LARGE_OD/2.0,18.0,BEVEL_LARGE_LEN,
                                App.Vector(BEVEL_X,ystart,BEVEL_Z),App.Vector(0,s,0))
    large.addProperty('App::PropertyString','Spec').Spec='m1.5 Z45 bore10; ratio 2.5 with Z18 pinion'

# ---------------- PAIRED MOTOR HOLDER / PINION SHAFTS ----------------
holder = doc.addObject('Part::Feature','PairedMotorHolder')
# Nose plate plus two side rails, leaving motor bodies visible/serviceable.
nose = Part.makeBox(16.0,80.0,44.0,App.Vector(138.0,-40.0,23.0))
rail1 = Part.makeBox(90.0,5.0,44.0,App.Vector(48.0,-40.0,23.0))
rail2 = Part.makeBox(90.0,5.0,44.0,App.Vector(48.0,35.0,23.0))
holder.Shape = nose.fuse(rail1).fuse(rail2)
holder.addProperty('App::PropertyString','Architecture').Architecture='one removable holder for 2 motors + 2 supported pinion axles; source-aligned concept'
holder.addProperty('App::PropertyString','Location').Location='2 dowels + 4 clamp screws; bevel mesh by defined shim pack'

for side,s in [('L',1),('R',-1)]:
    mot = doc.addObject('Part::Feature',f'JGB37_555_{side}_Envelope')
    mot.Shape = cyl_x(MOTOR_D/2.0,MOTOR_L,MOTOR_X0,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z)
    mot.addProperty('App::PropertyString','Status').Status='24V ~107rpm class candidate; exact vendor sample required'

    # Stepped pinion shaft: Ø8 gear seat, Ø12 bearing journal.
    p8 = doc.addObject('Part::Feature',f'PinionShaft8_{side}')
    p8.Shape = cyl_x(4.0,24.0,142.0,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z)
    p8.addProperty('App::PropertyString','Journal').Journal='Ø8 KHK pinion seat / coupling section'

    p12 = doc.addObject('Part::Feature',f'PinionBearingJournal12_{side}')
    p12.Shape = cyl_x(6.0,7.0,147.0,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z)
    p12.addProperty('App::PropertyString','Journal').Journal='Ø12 h6 for 61801 support'

    pb = doc.addObject('Part::Feature',f'B61801_Pinion_{side}')
    # bearing axis X: create ring by X cylinders
    outerb = cyl_x(B61801_OD/2.0,B61801_W,148.0,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z)
    innerb = cyl_x(B61801_ID/2.0,B61801_W+0.2,147.9,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z)
    pb.Shape = outerb.cut(innerb)

    small = doc.addObject('Part::Feature',f'KHK_SB1_5_1845H_{side}_Envelope')
    small.Shape = Part.makeCone(BEVEL_SMALL_OD/2.0,8.0,BEVEL_SMALL_LEN,
                                App.Vector(BEVEL_X-BEVEL_SMALL_LEN,s*MOTOR_AXIS_Y,MOTOR_AXIS_Z),
                                App.Vector(1,0,0))
    small.addProperty('App::PropertyString','Spec').Spec='m1.5 Z18 bore8 H version; torque limited until bench test'

# ---------------- CAMERA / LIFT SAFE ENVELOPE ----------------
cam = doc.addObject('Part::Feature','CameraHead_DN150_SAFE_Envelope')
cam.Shape = Part.makeCylinder(CAM_R,CAM_LEN,
                              App.Vector(CAM_X-CAM_LEN/2.0,0,CAM_Z_SAFE),App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Motion').Motion='Ø52x72 envelope, tilt -105..+105, roll continuous 360'

# ---------------- MASTER RULES ----------------
rules = doc.addObject('App::FeaturePython','RevEJ_Rules')
rules.addProperty('App::PropertyString','SourceBasis').SourceBasis='uploaded DRW-002-374 / 375 / 386 architecture; PX-1 dimensions and components are own design'
rules.addProperty('App::PropertyString','DrivePath').DrivePath='JGB37 -> supported Z18 -> Z45 transverse transfer shaft -> service dog -> middle Z50 -> idler Z50 -> front/rear Z50'
rules.addProperty('App::PropertyString','WheelSupport').WheelSupport='per wheel: 2x61801 inboard + 61903 outer flange support'
rules.addProperty('App::PropertyString','Pressure').Pressure='P0/P1/P2 isolated, separately monitored, common service fill with check valves'
rules.addProperty('App::PropertyString','Service').Service='motor holder, side cover and each axle flange independently removable'
rules.addProperty('App::PropertyString','Release').Release='NO MACHINING RELEASE until actual purchased parts, full DN150 sweep, pressure and endurance tests'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevEJ.FCStd')
