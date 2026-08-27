import FreeCAD as App, Part
# PX-1 Rev.EE — CRP150-source-aligned six-wheel master.
# Main corrections from Rev.DX:
# - wheel stations use Ø12 inner / Ø17 outer stepped shafts;
# - 2x61801 inner + 61903 outer bearing philosophy;
# - local axle flanges with 32x1.5-class static seals;
# - paired motor-holder subsystem rather than unrelated mounts;
# - cover screw keep-outs considered for DN150.
# Catalog gears are envelope solids only; NOT a machining release.

doc = App.newDocument('PX1_CRP150_6W_Master_RevEE')

BODY_L = 307.0
BODY_W = 92.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
COVER_T = 5.0
COVER_X0 = 15.5
COVER_L = 276.0
COVER_Z0 = 5.0
COVER_H = 81.0
COVER_Y = BODY_W/2.0
WHEEL_X = [50.0,150.0,250.0]
IDLER_X = [100.0,200.0]
WHEEL_Z = 45.0
PIPE_R = 75.0
PIPE_AXIS_Z = 52.0480547

GEAR_OD = 52.0
GEAR_FACE = 8.0
GEAR_Y = 38.0

INNER_SHAFT_D = 12.0
OUTER_SHAFT_D = 17.0
B61801_OD = 21.0
B61801_W = 5.0
B61903_OD = 30.0
B61903_W = 7.0
FLANGE_OD = 50.0
FLANGE_EXT = 7.0

WHEEL_INNER_Y = COVER_Y + COVER_T
WHEEL_CROWN_END_Y = 54.0
WHEEL_OUTER_Y = 67.0
WHEEL_R = 45.0
WHEEL_OUTER_R = 21.0

MOTOR_D = 37.0
MOTOR_L = 90.0
# Paired holder orientation remains a packaging variable; current candidate is transverse pair.
MOTOR_Y = 19.0
MOTOR_Z = 45.0

BEVEL_SMALL_OD = 30.86
BEVEL_LARGE_OD = 68.18
BEVEL_SMALL_LEN = 21.97
BEVEL_LARGE_LEN = 21.10
BEVEL_X = 150.0

CAM_R = 26.0
CAM_LEN = 72.0
CAM_X = 64.1
CAM_Z = 75.0


def cyl_y(r,l,x,y,z,sign=1):
    return Part.makeCylinder(r,l,App.Vector(x,y,z),App.Vector(0,sign,0))


def wheel_envelope(x,side):
    s=1 if side=='L' else -1
    crown=cyl_y(WHEEL_R,WHEEL_CROWN_END_Y-WHEEL_INNER_Y,x,s*WHEEL_INNER_Y,WHEEL_Z,s)
    taper=Part.makeCone(WHEEL_R,WHEEL_OUTER_R,WHEEL_OUTER_Y-WHEEL_CROWN_END_Y,
                        App.Vector(x,s*WHEEL_CROWN_END_Y,WHEEL_Z),App.Vector(0,s,0))
    return crown.fuse(taper)

# DN150 reference
pipe=doc.addObject('Part::Feature','DN150_ID_Reference')
pipe.Shape=Part.makeCylinder(PIPE_R,BODY_L+100,App.Vector(-50,0,PIPE_AXIS_Z),App.Vector(1,0,0))
pipe.addProperty('App::PropertyString','Note').Note='Ideal ID150 reference only; traction crown intentional contact'

# P0 body envelope
body=doc.addObject('Part::Feature','PressureBody_P0')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_Z1-BODY_Z0,App.Vector(0,-BODY_W/2,BODY_Z0))
body.addProperty('App::PropertyString','Pressure').Pressure='P0 isolated, normal +0.20..+0.30 bar'

# Side covers P1/P2
for side,s in [('L',1),('R',-1)]:
    y0=COVER_Y if s>0 else -COVER_Y-COVER_T
    cover=doc.addObject('Part::Feature',f'SideCover_{side}')
    cover.Shape=Part.makeBox(COVER_L,COVER_T,COVER_H,App.Vector(COVER_X0,y0,COVER_Z0))
    cover.addProperty('App::PropertyString','Seal').Seal='molded FKM ~190mm ID class; section/groove after path calculation'
    cover.addProperty('App::PropertyString','Fasteners').Fasteners='flush/countersunk lower screw line required for DN150'
    cover.addProperty('App::PropertyString','Pressure').Pressure=f'P{1 if side=="L" else 2} isolated drive bay'

# Five Z50 gears per side
for side,s in [('L',1),('R',-1)]:
    d=App.Vector(0,s,0)
    gy=s*GEAR_Y
    for x in WHEEL_X:
        g=doc.addObject('Part::Feature',f'WheelGear_Z50_{side}_{int(x)}')
        g.Shape=Part.makeCylinder(GEAR_OD/2,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Spec').Spec='m1 Z50 OD52 face8; Ø12 keyed axle seat'
    for x in IDLER_X:
        g=doc.addObject('Part::Feature',f'Idler_Z50_{side}_{int(x)}')
        g.Shape=Part.makeCylinder(GEAR_OD/2,GEAR_FACE,App.Vector(x,gy,WHEEL_Z),d)
        g.addProperty('App::PropertyString','Spec').Spec='m1 Z50; fixed support, serviceable bearing/bushing'

# Six source-aligned stepped wheel stations
for x in WHEEL_X:
    for side,s in [('L',1),('R',-1)]:
        # external wheel
        w=doc.addObject('Part::Feature',f'Wheel_{side}_{int(x)}')
        w.Shape=wheel_envelope(x,side)
        w.addProperty('App::PropertyString','Mount').Mount='stepped Ø12->Ø17 shaft, 4x4 key, M6 axial retainer'

        # shaft: inner Ø12 section and outer Ø17 support section
        shaft=doc.addObject('Part::Feature',f'WheelShaft_{side}_{int(x)}')
        inner=cyl_y(INNER_SHAFT_D/2,22.0,x,s*31.0,WHEEL_Z,s)
        outer=cyl_y(OUTER_SHAFT_D/2,26.0,x,s*53.0,WHEEL_Z,s)
        shaft.Shape=inner.fuse(outer)
        shaft.addProperty('App::PropertyString','Stack').Stack='2x61801 inner philosophy + 61903 outer in removable flange; dynamic seal outboard'

        # two inner 61801 envelope positions
        for j,yabs in enumerate((32.0,45.0),start=1):
            b=doc.addObject('Part::Feature',f'B61801_{side}_{int(x)}_{j}')
            b.Shape=cyl_y(B61801_OD/2,B61801_W,x,s*yabs,WHEEL_Z,s)

        # removable flange + outer 61903
        fy=s*(COVER_Y+COVER_T)
        flg=doc.addObject('Part::Feature',f'AxleFlange_{side}_{int(x)}')
        flg.Shape=Part.makeCylinder(FLANGE_OD/2,FLANGE_EXT,App.Vector(x,fy,WHEEL_Z),App.Vector(0,s,0))
        flg.addProperty('App::PropertyString','StaticSeal').StaticSeal='FKM 32x1.5 nominal class; exact groove supplier-controlled'
        flg.addProperty('App::PropertyString','Fasteners').Fasteners='3xM4 PCD40 candidate'

        b3=doc.addObject('Part::Feature',f'B61903_{side}_{int(x)}')
        b3.Shape=Part.makeCylinder(B61903_OD/2,B61903_W,App.Vector(x,s*52.0,WHEEL_Z),App.Vector(0,s,0))
        b3.addProperty('App::PropertyString','Spec').Spec='61903-2RS 17x30x7 outer wheel-load bearing'

        seal=doc.addObject('Part::Feature',f'DynamicSeal_{side}_{int(x)}_Envelope')
        seal.Shape=Part.makeCylinder(11.0,5.0,App.Vector(x,s*59.0,WHEEL_Z),App.Vector(0,s,0))
        seal.addProperty('App::PropertyString','Status').Status='FKM quad/X-ring or compact lip seal; exact article HOLD'

# Paired motor-holder system
holder=doc.addObject('Part::Feature','PairedTractionMotorHolder_Envelope')
holder.Shape=Part.makeBox(98.0,80.0,44.0,App.Vector(50.0,-40.0,23.0))
holder.addProperty('App::PropertyString','Reference').Reference='system concept from DRW-002-386: two motors + two supported bevel pinion axles in one removable holder'
holder.addProperty('App::PropertyString','Orientation').Orientation='current transverse pair candidate; installed orientation remains full-solid gate'

for side,s in [('L',1),('R',-1)]:
    m=doc.addObject('Part::Feature',f'JGB37_555_{side}_Envelope')
    m.Shape=Part.makeCylinder(MOTOR_D/2,MOTOR_L,App.Vector(55.0,s*MOTOR_Y,MOTOR_Z),App.Vector(1,0,0))
    m.addProperty('App::PropertyString','Mount').Mount='paired holder, not independent body drilling'

    pin=doc.addObject('Part::Feature',f'KHK_SB1_5_1845H_{side}_Envelope')
    pin.Shape=Part.makeCone(BEVEL_SMALL_OD/2,8.0,BEVEL_SMALL_LEN,
                            App.Vector(BEVEL_X-BEVEL_SMALL_LEN,s*MOTOR_Y,WHEEL_Z),App.Vector(1,0,0))
    pin.addProperty('App::PropertyString','Limit').Limit='prototype pinion torque <=1.50 Nm until bench calibration'

    large=doc.addObject('Part::Feature',f'KHK_SB1_5_4518H_{side}_Envelope')
    ystart=s*(36.0-BEVEL_LARGE_LEN)
    large.Shape=Part.makeCone(BEVEL_LARGE_OD/2,18.0,BEVEL_LARGE_LEN,
                              App.Vector(BEVEL_X,ystart,WHEEL_Z),App.Vector(0,s,0))
    large.addProperty('App::PropertyString','Spec').Spec='m1.5 Z45 mate, ratio2.5; H version required'

# Camera safe envelope
cam=doc.addObject('Part::Feature','CameraHead_DN150_SAFE')
cam.Shape=Part.makeCylinder(CAM_R,CAM_LEN,App.Vector(CAM_X-CAM_LEN/2,0,CAM_Z),App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Motion').Motion='Ø52x72 envelope; tilt -105..+105, roll continuous; full lift solids still gate'

rules=doc.addObject('App::FeaturePython','RevEE_Rules')
rules.addProperty('App::PropertyString','Source').Source='DRW-002-374/375/386 architecture alignment; own PX-1 dimensions'
rules.addProperty('App::PropertyString','WheelSupport').WheelSupport='Ø12 inner gear journals, 2x61801 philosophy, Ø17 outer 61903 support'
rules.addProperty('App::PropertyString','MotorUnit').MotorUnit='paired removable holder with separately supported pinion axles'
rules.addProperty('App::PropertyString','Sealing').Sealing='P0/P1/P2 independent pressure zones; local flange seals + main side-cover seal'
rules.addProperty('App::PropertyString','Release').Release='NO MACHINING RELEASE: real parts + full DN150 solids + pressure endurance required'

doc.recompute()
doc.saveAs('PX1_CRP150_6W_Master_RevEE.FCStd')
