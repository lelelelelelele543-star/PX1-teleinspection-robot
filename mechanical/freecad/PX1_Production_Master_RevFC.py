import FreeCAD as App, Part, math
# PX-1 Rev.FC — production-oriented mechanical master
# Replaces pure packaging boxes with candidate machinable body, side covers,
# wheel flanges, X200 bevel bearing/seal bosses, lift plates, camera shell and rear bulkhead.
# NOT A MACHINING RELEASE: exact purchased parts and physical qualification remain mandatory.

doc = App.newDocument('PX1_Production_Master_RevFC')

# ---------------- DATUMS ----------------
L = 307.0
W = 92.0
Z0 = 8.0
ZTOP = 90.0
FLOOR = 6.0
SIDE = 6.0
END = 8.0
TOP_T = 5.0
PIPE_R = 75.0
PIPE_Z = 52.0480547
WHEEL_Z = 45.0
WX = [50.0,150.0,250.0]
IX = [100.0,200.0]
COVER_T = 5.0
COVER_Y = W/2.0
CAM_OD = 52.0
CAM_LEN = 72.0
CAM_Z_LOW = 75.0
LIFT_PIVOT = App.Vector(200.0,0,94.0)
LINK_L = 120.0


def add_feature(name, shape, **props):
    o = doc.addObject('Part::Feature', name)
    o.Shape = shape
    for k,v in props.items():
        o.addProperty('App::PropertyString',k)
        setattr(o,k,str(v))
    return o


def cyl_y(r,l,x,y,z,s):
    return Part.makeCylinder(r,l,App.Vector(x,y,z),App.Vector(0,s,0))

# ---------------- DN150 REFERENCE ----------------
pipe = add_feature('DN150_ID_REF', Part.makeCylinder(PIPE_R,L+120,App.Vector(-60,0,PIPE_Z),App.Vector(1,0,0)),
                   Note='ideal ID150 reference only')

# ---------------- P0 MACHINABLE BODY ----------------
outer = Part.makeBox(L,W,ZTOP-Z0,App.Vector(0,-W/2,Z0))
inner = Part.makeBox(L-2*END,W-2*SIDE,(ZTOP-Z0)-FLOOR-TOP_T,
                     App.Vector(END,-W/2+SIDE,Z0+FLOOR))
body = outer.cut(inner)
# folded-camera roof recess
recess = Part.makeBox(96.0,62.0,40.0,App.Vector(34.0,-31.0,53.0))
body = body.cut(recess)
# top service opening behind the folded-camera pocket
opening = Part.makeBox(158.0,74.0,30.0,App.Vector(136.0,-37.0,ZTOP-TOP_T-1.0))
body = body.cut(opening)

# X200 output-shaft boss material is represented as reinforced cylinders fused to side walls
for s in (-1,1):
    boss = Part.makeCylinder(18.0,10.0,App.Vector(200.0,s*(W/2-2.0),WHEEL_Z),App.Vector(0,s,0))
    body = body.fuse(boss)

p0 = add_feature('P0_MainBody_MachiningCandidate',body,
                 Material='EN AW-6082 T6 candidate',
                 Pressure='P0 +0.20..+0.30 bar normal',
                 Status='prototype machining candidate')

# Top service cover
cover_top = Part.makeBox(158.0,74.0,TOP_T,App.Vector(136.0,-37.0,ZTOP))
add_feature('P0_TopServiceCover',cover_top,Seal='closed-loop FKM face O-ring; exact groove after ring selection')

# ---------------- SIDE DRIVE COVERS P1/P2 ----------------
for side,s in [('L',1),('R',-1)]:
    y0 = COVER_Y if s>0 else -COVER_Y-COVER_T
    plate = Part.makeBox(276.0,COVER_T,81.0,App.Vector(15.5,y0,5.0))
    add_feature(f'P{1 if s>0 else 2}_SideCover_{side}',plate,
                Seal='closed-loop FKM face seal',Fasteners='M4 A4, screw line outside seal')

# ---------------- WHEEL FLANGES / STATIONS ----------------
for x in WX:
    for side,s in [('L',1),('R',-1)]:
        fy = s*(W/2+COVER_T)
        flange = Part.makeCylinder(25.0,7.0,App.Vector(x,fy,WHEEL_Z),App.Vector(0,s,0))
        # central through bore candidate; stepped detail remains separate part drawing
        bore = Part.makeCylinder(9.0,9.0,App.Vector(x,fy-1*s,WHEEL_Z),App.Vector(0,s,0))
        flange = flange.cut(bore)
        add_feature(f'AxleFlange_{side}_{int(x)}',flange,
                    Bearing='61903 outer; inner 61801 supports in bay',Seal='local FKM static + dynamic lip/X seal')

# ---------------- FIVE Z50 GEARS PER SIDE ----------------
for side,s in [('L',1),('R',-1)]:
    gy = s*38.0
    for x in WX+IX:
        g = Part.makeCylinder(26.0,8.0,App.Vector(x,gy,WHEEL_Z),App.Vector(0,s,0))
        add_feature(f'Z50_{side}_{int(x)}',g,Spec='m1 Z50 OD52 face8 envelope')

# ---------------- X200 BEVEL OUTPUT BOSSES ----------------
for side,s in [('L',1),('R',-1)]:
    # output shaft envelope through P0 wall toward side bay
    shaft = Part.makeCylinder(9.0,36.0,App.Vector(200.0,s*10.0,WHEEL_Z),App.Vector(0,s,0))
    add_feature(f'X200_OutputShaft_{side}',shaft,
                Stack='Ø10 gear/bearing -> Ø18 seal land -> Ø12 service coupling')
    b = Part.makeCylinder(9.5,5.0,App.Vector(200.0,s*27.0,WHEEL_Z),App.Vector(0,s,0))
    add_feature(f'B61800_{side}',b,Spec='61800 10x19x5 class')
    seal = Part.makeCylinder(15.0,7.0,App.Vector(200.0,s*33.0,WHEEL_Z),App.Vector(0,s,0))
    add_feature(f'Seal18x30x7_{side}',seal,Spec='FKM 18x30x7 class, exact article HOLD')

# ---------------- MOTOR HOLDER ----------------
holder = Part.makeBox(100.0,80.0,44.0,App.Vector(196.0,-40.0,23.0))
add_feature('PairedMotorHolder',holder,Architecture='both JGB37 + supported bevel pinion shafts; removable from top')
for side,s in [('L',1),('R',-1)]:
    m = Part.makeCylinder(18.5,90.0,App.Vector(204.0,s*19.0,WHEEL_Z),App.Vector(1,0,0))
    add_feature(f'JGB37_555_{side}',m,Status='exact purchased sample required')

# ---------------- LIFT PLATES LOW POSE ----------------
def pose(z):
    off = 10.0
    a = math.asin((z-(LIFT_PIVOT.z+off))/LINK_L)
    return App.Vector(LIFT_PIVOT.x-LINK_L*math.cos(a),0,LIFT_PIVOT.z+LINK_L*math.sin(a))

upper = pose(CAM_Z_LOW)
for y in (-24.0,24.0):
    p1 = App.Vector(LIFT_PIVOT.x,y,LIFT_PIVOT.z)
    p2 = App.Vector(upper.x,y,upper.z)
    v = p2-p1
    link = Part.makeBox(v.Length,5.0,18.0,App.Vector(0,-2.5,-9.0))
    link.rotate(App.Vector(0,0,0),App.Vector(0,1,0),-math.degrees(math.atan2(v.z,v.x)))
    link.translate(p1)
    add_feature(f'LiftPlate_{"L" if y>0 else "R"}',link,
                Pivot='Ø8 replaceable bushings',Clamp='M8 manual clamp + Belleville stack')

# ---------------- CAMERA SHELL ----------------
cam_x = upper.x
shell_outer = Part.makeCylinder(CAM_OD/2,CAM_LEN,App.Vector(cam_x-CAM_LEN/2,0,CAM_Z_LOW),App.Vector(1,0,0))
shell_inner = Part.makeCylinder((CAM_OD-5.0)/2,CAM_LEN-10.0,App.Vector(cam_x-CAM_LEN/2+5,0,CAM_Z_LOW),App.Vector(1,0,0))
shell = shell_outer.cut(shell_inner)
add_feature('DigitalCameraShell',shell,
            Video='fully digital; no coax/CVBS',Motion='TILT +-105; internal continuous ROLL 360',Material='Al 6082 candidate')

# ---------------- REAR BULKHEAD STRUCTURAL BOSSES ----------------
# Keep exact connector hole as adapter-plate gate.
anchor = Part.makeBox(24.0,40.0,30.0,App.Vector(L-12.0,-20.0,30.0))
add_feature('RearTetherAnchorBoss',anchor,LoadPath='strength member directly into body; target >=1kN pending tether spec')
connplate = Part.makeCylinder(22.0,5.0,App.Vector(L,0,45.0),App.Vector(1,0,0))
add_feature('RearConnectorAdapterPlate',connplate,Status='replaceable plate; hole pattern after exact connector qualification')
fill = Part.makeCylinder(6.0,10.0,App.Vector(L-4.0,-28.0,70.0),App.Vector(1,0,0))
add_feature('PressureFillBoss',fill,Function='common fill -> check valves -> P0/P1/P2')

# ---------------- RULES ----------------
rules = doc.addObject('App::FeaturePython','RevFC_Rules')
for name,val in {
    'Architecture':'CRP150-inspired six-wheel crawler, own PX-1 geometry',
    'Drive':'X200 bevel input, 2.5:1 candidate, five equal Z50 per side',
    'Pressure':'P0/P1/P2 isolated positive pressure zones',
    'Camera':'digital Ø52x72 target, low-folded DN150 pose',
    'Tail':'structural tether anchor independent from connector',
    'Release':'PROTOTYPE SOLID MASTER ONLY; no machining release until exact parts and tests'
}.items():
    rules.addProperty('App::PropertyString',name)
    setattr(rules,name,val)

doc.recompute()
doc.saveAs('PX1_Production_Master_RevFC.FCStd')
