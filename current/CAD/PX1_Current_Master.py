import cadquery as cq
from cadquery import exporters
import math, json, csv, os, hashlib, textwrap
from pathlib import Path

ROOT=Path(os.environ.get('PX1_OUT', str(Path(__file__).resolve().parents[1])))
CAD=ROOT/'CAD'; METAL=CAD/'Metal_HOLD'; PRINT=CAD/'Print_STL'; IMG=ROOT/'images'
for d in (ROOT,CAD,METAL,PRINT,IMG): d.mkdir(parents=True, exist_ok=True)

# -------------------------------
# PX1 CURRENT MASTER — Proteus CRP-150 derived
# Coordinates: X longitudinal front->rear, Y left/right, Z up.
# Exact source/purchased dimensions are used where available.
# Any reconstruction lacking a controlled source dimension is named HOLD/ТРЕБУЕТСЯ_ЗАМЕР.
# -------------------------------

# Source-confirmed / source-reconstructed drivetrain datums
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0
Z50_TEETH=50; Z50_MOD=1.0; Z50_PD=50.0; Z50_OD=52.0; Z50_FACE=4.0
Z16_TEETH=16; Z40_TEETH=40; BEVEL_MOD=1.0
Z16_OD=17.86; Z40_OD=40.74
B61801=(12.0,21.0,5.0)
B61903=(17.0,30.0,7.0)
B61800=(10.0,19.0,5.0)
XRING=(18.72,2.62)
SEAL_18_30_7=(18.0,30.0,7.0)
SIDE_ORING=(190.0,1.5)
SIDE_COVER_L=262.0; SIDE_COVER_H=60.0; SIDE_COVER_T=7.0   # DRW-002-374 side cover ~262x60x7, DERIVED
# F17 ballast blocks in free cavity space (bbox search, 0.5 mm shrink, motor-extraction keep-out). Material: STEEL (user decision 2026-11-19).
# F14: block 5 split around the rear plate-screw boss (was 266..287 x Z25..54): 5 = X270..287 Z25..55.75 (MPRLS-0.5),
#      6 = X266..270 above the boss Z39..55.75. Net volume -289 mm3 (-2.3 g steel).
BALLAST_BOXES=[(25.0,-21.5,25.0,90.0,-11.5,66.0),(25.0,11.5,25.0,90.0,21.5,66.0),(117.0,-25.5,25.0,188.0,25.5,30.0),(266.0,10.5,25.0,287.0,25.5,68.0),(270.0,-25.5,25.0,287.0,-10.5,55.75),(266.0,-25.5,39.0,270.0,-10.5,55.75)]
QRW_HUB_R=22.0   # F17 aluminium hub radius inside D90 tyre, ESTIMATED from Mini-Cam ASS-004-496 view (hub ~0.5 D)
# F11 FSS-002-060 weight plate (DRW-002-375 A-A, 1:1): stainless, in external bottom recess, flush.
WEIGHT_PLATE_W=50.3; WEIGHT_PLATE_H=12.0     # DERIVED from 1:1 section (±0.1)
WEIGHT_PLATE_X0=24.5; WEIGHT_PLATE_X1=272.0  # ESTIMATED: front ~5 mm from housing end per side view; rear not visible
CAVITY_FLOOR_Z=24.0                           # was 23; leaves 1.0 Al over plate (Proteus ~1.4 under Z40), ESTIMATED
# F14 plate fixing: DRW-002-375 pos.15 FIX-002-764 M8x16 DIN 7984 x2, pos.16 FIX-002-741 M8 spring washer x2.
# Side view 1:1 measured at 600 dpi (housing 278.07 over 278 -> scale 1.000). Drawing right end = PX1 front (X18).
PLATE_SCREW_XY=((46.0,0.0),(263.0,-15.5))   # #1: 28.0 from front end, DERIVED (±0.2); Y0 ESTIMATED (centre-plane section)
                                            # #2: not visible on DRW-002-375; PX1 position clear of Z40 pair, ESTIMATED
DIN7984_M8=(6.5,5.0,5.0)      # head dk/2, k, socket s — DIN 7984 M8, CONFIRMED standard (drawing k 5.1)
PLATE_SCREW_L=16.0            # FIX-002-764 M8 X 16, CONFIRMED (part list)
SPRING_WASHER_M8=(4.05,7.4,2.0)  # DIN 127 B M8 d1/2, d2/2, s, CONFIRMED standard
PLATE_CBORE_R=7.5             # Ø15.0 counterbore in plate, DERIVED (15.0)
PLATE_CBORE_LIG=4.0           # plate ligament under counterbore floor, DERIVED (4.0)
PLATE_SCREW_HOLE_R=4.2        # Ø8.4 through hole (ISO 273 fine; drawing ~8.1), ESTIMATED
M8_COSMETIC_THREAD_R=4.0      # tapped hole drawn at major Ø8 (cosmetic thread), ISO 262 M8, CONFIRMED standard
PLATE_TAP_TOP_Z=37.0          # thread Z23..37 = 14 mm (allows M8x20 option), ESTIMATED
PLATE_BOSS_R=6.5; PLATE_BOSS_TOP_Z=38.5   # Ø13 Al boss from cavity floor, 1.5 mm closed cap (pressure housing), ESTIMATED
# F10 side-cover seal SEA-002-102 190x1.5, lobed track around Z50 gears (DRW-002-374 top view):
SIDE_SEAL_R=28.0        # lobe radius about each Z50 centre, DERIVED from drawing (~27.5-28)
SIDE_SEAL_CUSP=19.0     # track distance from axis between gears, DERIVED from drawing (~18.4-19)
SIDE_SEAL_W=2.0; SIDE_SEAL_D=1.15   # groove in cover inner face, ESTIMATED (23% squeeze)
FLANGE_ORING=(32.0,1.5)
M6_COSMETIC_THREAD_R=3.0         # F13: shaft-end tapped hole shown at major Ø6 (cosmetic thread), ISO 262 M6 — CONFIRMED standard
# F13 Mini-Cam ASS-002-103 "Crawler Wheel Bolt - ASSY" (section A-A 2:1 + top view 2:1, measured at 600 dpi,
# scale checked on M6 thread 6.01 mm and button head dk 10.50 mm). Local axis from disk flange back face.
WD_FLANGE_T=6.0          # FSS-002-065 flange thickness, DERIVED (6.01)
WD_FLANGE_R=8.27         # cam profile circle radius, DERIVED (section r8.25 at 90°, top view r8.78 lobe)
WD_FLANGE_E=0.51         # cam profile eccentricity toward lobe, DERIVED (top view r8.78 / r7.11)
WD_FLAT=7.11             # flat on the side opposite the lobe, distance from axis, DERIVED (top view)
WD_FACE_R=6.54           # outer face radius before 45° chamfer, DERIVED
WD_SPIGOT_R=5.2          # spigot Ø10.4, DERIVED (10.37)
WD_SPIGOT_FLAT=3.9       # spigot D-flat (lobe side), DERIVED (top view)
WD_SPIGOT_L=2.6          # spigot length, DERIVED (2.60)
WD_LIP_R=5.5; WD_LIP_D=1.04         # Ø11.0 entry lip retaining the O-ring, DERIVED
WD_GROOVE_R=6.5; WD_GROOVE_D=3.32   # Ø13.0 O-ring groove from face 1.04..3.32, DERIVED
WD_SEAT_R=5.5; WD_SEAT_D=4.5        # Ø11.0 washer seat 3.32..4.50, DERIVED
WD_HOLE_R=3.2                        # Ø6.4 clearance for M6, ESTIMATED (ISO 273 medium)
ISO7380_M6=(5.25,3.3,4.0)            # dk/2, k, hex s — ISO 7380 M6, CONFIRMED standard
WD_HEAD_BEAR_D=3.42                  # head bearing face below disk outer face, DERIVED
WHEEL_SCREW_L=14.0                   # FIX-002-105 M6x14, CONFIRMED (part list)
SCHNORR_M6=(3.2,5.0,1.06)            # FIX-002-104 spring washer ri/ro/installed h, DERIVED (Ø6.4 std, Ø10 measured)
WD_ORING=(5.6,0.88,2.2)              # SEA-002-106 10x1.8 installed: torus major r / tube r / centre below face, DERIVED
SHAFT_SPIGOT_BORE_R=5.3; SHAFT_SPIGOT_BORE_D=2.7   # shaft-end counterbore for disk spigot, ESTIMATED
SHAFT_END_Y=60.9                     # wheel-shaft end face |Y| (unchanged), DERIVED from model
WD_BACK_Y=60.95                      # disk flange back |Y|, 0.05 above shaft end, ESTIMATED
# F05 axle-flange face seal, DRW-002-374 section A-A (layout DERIVED, sizes ESTIMATED):
COVER_BEARING_BORE_R=15.0      # 61903 OD30 seat in side cover, CONFIRMED bearing OD
COVER_BEARING_SHOULDER_R=13.5  # Ø27 <= SKF Da max 28 for 61903, ESTIMATED
FLANGE_GROOVE_RI=16.0          # = O-ring ID32/2, zero stretch, ESTIMATED
FLANGE_GROOVE_RO=18.1          # width 2.1, ESTIMATED
FLANGE_GROOVE_DEPTH=1.15       # 23% squeeze of CS1.5, ESTIMATED
FLANGE_COLLAR_T=2.6            # was 2.0; 1.45 above groove, M3x6 engages 3.4 in cover, ESTIMATED
# F08 fasteners per DRW-002-374 (pos.15 FIX-000-359 M3x8, pos.16 FIX-002-738 M3x6, Torx button head):
COVER_SCREW_DX=(-125.0,-75.0,-25.0,25.0,75.0,125.0)  # about X150, DERIVED from DRW374 view (±0.2)
COVER_SCREW_DZ=(-24.0,24.0)                           # about Z45, DERIVED
COVER_SCREW_CBORE=(3.25,3.0)                          # Ø6.5 x 3 head recess, ESTIMATED (8-long screw in 7 cover)
FLANGE_SCREW_R=20.9                                   # 4x at 45°, DERIVED from DRW374 view
ISO7380_M3=(2.85,1.65)                                # head r, height — ISO 7380 M3, CONFIRMED standard
FLANGE_ORING_INST_RO=FLANGE_GROOVE_RI+math.pi*.75**2/FLANGE_GROOVE_DEPTH  # area-equal installed section

# Current reconstructed global CRP150/PX1 screen from recovered CAD audits.
# These are NOT released manufacturing dimensions unless separately called out.
BODY_L_SOURCE_SCREEN=278.0
BODY_HALF_W_SCREEN=34.0
BODY_Z0=11.0
BODY_TOP=75.0
PIPE_R=75.0
WHEEL_CENTRE_Y=54.5
WHEEL_CROWN_R=45.0
# DERIVED: paired lower-wall crown contacts, not an arbitrary fit translation.
PIPE_CENTER_Z=WHEEL_Z-WHEEL_CROWN_R+math.sqrt(PIPE_R**2-WHEEL_CENTRE_Y**2)
# ESTIMATED asymmetric outer shoulder; retains D90 and total width133.
# F04 (2026-11-19): outer shoulder r34.5->r28.5 @y8, edge r27.5->r20.5 @y12.
# DERIVED limit for >=3 mm radial gap in nominal ID150 at contact pose:
#   r <= sqrt((PIPE_R-3)^2-(WHEEL_CENTRE_Y+y)^2)-(PIPE_CENTER_Z-WHEEL_Z) -> 29.22@y8, 21.08@y12.
# Crown r45@y0 (contact) and inner side unchanged; values themselves ESTIMATED, not OEM QRW90.
WHEEL_PROFILE=[(26,-12),(32,-12),(42,-8),(45,0),(28.5,8),(20.5,12),(8,12),(8,-2),(26,-2)]
WHEEL_MIN_NONCONTACT_GAP=3.0

# F16 Proteus-class drive envelope (DRW-002-386 1:1: gearhead D26.0x44.6, motor D22.2x51.7 — DERIVED).
# Candidate ZHAOWEI ZWSMD026026 3-stage (44.9) + D22 motor, NOT seller-verified (see F12 report).
# Motor length 53.0 >= Proteus 51.7, so the envelope also covers the original-class motor.
MOTOR_OD=22.2; MOTOR_LEN=53.0; GEARHEAD_OD=26.0; GEARHEAD_LEN=44.9  # 53.0 DERIVED (ZHAOWEI total 97.9 - gearhead 44.9); rear X91.6
MOTOR_SHAFT_D=4.0; MOTOR_SHAFT_L=17.5
MOTOR_FACE=189.5; MOTOR_Y=13.5
MOTOR_PILOT_D=6.4; MOTOR_PILOT_L=2.0
COUPLING_OD=20.0; COUPLING_L=24.0; COUPLING_BORE=6.0 # NBK MLR-20C-6-6

# Purchased exact / published component dims
LAPP_OD=17.6; LAPP_CMAX=26.5; LAPP_THREAD_L=6.5; LAPP_SW=16.0
ACE_BODY_OD=12.0; ACE_ROD_OD=4.0; ACE_STROKE=80.0; ACE_EXTENDED=192.0
SP13_PLUG_OD=18.0; SP13_PLUG_L=48.0 # retailer/manufacturer class dimensions, exact connector still sample-gated
SP17_PLUG_OD=24.6; SP17_PLUG_L=56.5; SP17_PANEL_OD=25.0; SP17_PANEL_THREAD=17.0; SP17_PANEL_L=19.7
NUCLEO=(82.5,70.0,12.0)
CINCON=(57.9,36.8,12.7)
MPRLS=(17.8,16.7,7.5)
NICHICON_D=18.0; NICHICON_L=25.0
BTS_SCREEN=(50.0,50.0,43.0) # board-dependent HOLD
POLOLU_5577=(25.4,25.4,9.0)
POLOLU_5571=(25.4,25.4,9.0)
WAVESHARE_27479=(42.8,15.2,4.75)
VIDEO_SCREEN=(43.0,16.0,15.0)  # Delta TR-1D*P2 packaging screen

# Current PX1 service cover engineering prototype dimensions
SERVICE_CX=184.5; SERVICE_L=205.0; SERVICE_W=68.0; SERVICE_T=7.0; SERVICE_Z=75.0
SERVICE_OPEN_X0=90.0;  SERVICE_OPEN_X1=278.0; SERVICE_OPEN_W=53.0
SERVICE_SCREW_X=(85.0,284.0); SERVICE_SCREW_Y=(-30.5,30.5)
# ESTIMATED static face-seal gland: 1.5 section, 20% nominal squeeze,
# 77.5% cross-section fill; exact closed seal/material and leak test unresolved.
SERVICE_GROOVE_CX=184.0; SERVICE_GROOVE_L=194.0; SERVICE_GROOVE_W=58.0
SERVICE_GROOVE_RADIUS=3.0; SERVICE_GROOVE_WIDTH=1.9; SERVICE_GROOVE_DEPTH=1.2

# F18 camera lift per DRW-002-744 (Crawler Lift Parts) + DRW-002-752 (Lift Housing), folded state theta=0.
# Origin A = clamp axle FSS-002-089 (M10, 3x DIN2093) = pivot of central lever ASS-002-723.
# In PX1 coordinates "toward camera" = -X. Tags: CONFIRMED / DERIVED / ESTIMATED.
LIFT_BASE_L=55.0; LIFT_BASE_W=68.7            # FAL-002-067 54.8..55.5 x 68.7, DERIVED (744 top/side 1:1.5)
LIFT_A_ABOVE_BASE=22.9                         # A above base seating face, DERIVED (744 side view)
LIFT_BASE_BEHIND_A=10.2                        # base rear end behind A, DERIVED (744 side view)
LIFT_A_X=250.0                                 # ESTIMATED: Proteus boss/pocket at X~250 (375 A-A) gives A~262;
                                               # PX1 -12 to free cover strip X262..287 for valve + camera gland
LIFT_A_Z=SERVICE_Z+SERVICE_T+LIFT_A_ABOVE_BASE # 104.9: base on PX1 removable cover (Proteus: on housing top, A~97.9), DERIVED+ESTIMATED
LIFT_AB=(38.2,-12.5)                           # side-link base pivot FSS-002-075 rel. A, DERIVED (|AB|=40.2)
LINK_L=200.1                                   # AC = BD (central lever / side links FSS-002-068), DERIVED (200.1/200.0)
LIFT_THETA_MAX=69.0                            # DERIVED: asin((257-70)/LINK_L)=69.2 from CRP150 catalogue 70..257 (stop ESTIMATED)
LIFT_CAT_RANGE=(70.0,257.0)                    # CRP150 catalogue manual lift, camera axis above floor, CONFIRMED
LIFT_GAS_E=(7.0,-16.8)                         # gas spring lower eye rel. A; Proteus (7.0,-24.8) DERIVED sits in housing pocket,
                                               # PX1 +8 up because base sits on 7 mm cover without pocket, ESTIMATED
LIFT_GAS_G=(125.0,1.0)                         # upper eye on lever rel. A, DERIVED (744, +-2)
LIFT_SIDE_Y=25.2; LIFT_SIDE_T=4.0; LIFT_SIDE_H=15.0  # side links: 744 top view Y+-27.9 t4 h15 DERIVED; Y-2.7 ESTIMATED for cover-screw tool access
LIFT_LEVER_PLATE_W=54.4                        # FSS-002-073 lever sheet plate width, DERIVED
LIFT_CHEEK_Y=(6.6,9.6)                         # central-lever cheeks (fork 24 wide at C, DERIVED) around gas spring, ESTIMATED
LIFT_HOUSING_W=46.0; LIFT_HOUSING_L=52.0       # DRW-002-752 lift housing ~48 wide / 52 long, DERIVED 1:1; simplified block ESTIMATED
CAM026_ENVELOPE=(120.0,74.0,74.0)              # GAP catalogue sy1083 L x W x H, CONFIRMED (0.864 kg)
CAM026_MASS_KG=0.864                           # CONFIRMED catalogue
CAM_Z=70.0                                     # camera axis folded = catalogue lower bound, CONFIRMED (interpretation: axis above floor)
CAM_REAR_X=-40.5                               # camera rear face = lift-housing front -0.5, ESTIMATED
CAM_DROP=LIFT_A_Z-CAM_Z                        # C/A level to camera axis, DERIVED from catalogue (752 interface ESTIMATED)
CAM026_MEASURED_BASE_OD=62.5; CAM_R=CAM026_MEASURED_BASE_OD/2; CAM_LEN=132.0  # ASM000 boom variant (head 132), DERIVED reference only
CAM_GLAND_XY=(272.0,0.0); VALVE_XY=(272.0,18.0) # camera cable M12 gland + pressure valve in cover rear strip, ESTIMATED

# Integrated packaging datums: ESTIMATED engineering dimensions, mm.
# Same six-wheel topology; no change to gear or motor axes.
MIDDLE_INNER_Y=26.8
MIDDLE_BUSH_W=3.0
IDLER_PIN_INNER_Y=27.0
SUPPORT_BOSS_INNER_Y=26.5
HARNESS_TOP_Z=117.5   # camera cable over the folded lever (static folded routing), ESTIMATED

# ------------------------------- helpers

def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def box0(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cyl_x(x,y,z,r,l,dir=1):
    base=cq.Vector(x,y,z)
    return wp(cq.Solid.makeCylinder(r,l,base,cq.Vector(dir,0,0)))
def cyl_y(x,y,z,r,l,dir=1):
    base=cq.Vector(x,y,z)
    return wp(cq.Solid.makeCylinder(r,l,base,cq.Vector(0,dir,0)))
def cyl_z(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,0,1)))
def ring_y(x,y,z,ro,ri,w):
    o=cyl_y(x,y-w/2,z,ro,w); i=cyl_y(x,y-w/2-0.2,z,ri,w+0.4)
    return wp(o.val().cut(i.val()))
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def cut(a,b): return wp(a.val().cut(b.val()))
def intervol(a,b):
    return a.val().intersect(b.val()).Volume() # errors must propagate, never become zero

def between(p1,p2,r):
    a=cq.Vector(*p1); b=cq.Vector(*p2); v=b-a
    return wp(cq.Solid.makeCylinder(r,v.Length,a,v.normalized()))

def plate_between(p1,p2,y,t=4,h=14):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=boxc(0,y,0,L,t,h).rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))

def make_spur_gear(teeth=50,module=1.0,face=4.0,bore=12.0,axis='Y'):
    # Analytical involute reference at 20 degrees. Source pressure angle is unknown.
    # This is explicitly HOLD; never export as a manufacturing tooth definition.
    rp=module*teeth/2; ra=rp+module; rf=rp-1.25*module
    alpha=math.radians(20); rb=rp*math.cos(alpha)
    invol=lambda r: math.sqrt(max(0,(r/rb)**2-1))-math.acos(min(1,rb/r)) if r>=rb else 0
    half=math.pi/(2*teeth)+math.tan(alpha)-alpha
    pts=[]
    for i in range(teeth):
        a=i*2*math.pi/teeth
        for r in [rf]+[max(rf,rb)+(ra-max(rf,rb))*j/7 for j in range(8)]:
            t=a-half+invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        for r in list(reversed([max(rf,rb)+(ra-max(rf,rb))*j/7 for j in range(8)]))+[rf]:
            t=a+half-invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
    clean=[]
    for pt in pts:
        if not clean or math.dist(pt,clean[-1])>1e-9: clean.append(pt)
    g=cq.Workplane('XY').polyline(clean).close().extrude(face/2,both=True)
    g=g.cut(cq.Workplane('XY').circle(bore/2).extrude(face,both=True))
    if axis=='Y': g=g.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': g=g.rotate((0,0,0),(0,1,0),90)
    return g

def make_bearing(id_,od,w,axis='Y'):
    # Manufacturer boundary envelope: correct full width, not internal rolling geometry.
    p=cq.Workplane('XY').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    if axis=='Y': p=p.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': p=p.rotate((0,0,0),(0,1,0),90)
    return p

def make_seal(id_,od,w,axis='Y'):
    p=cq.Workplane('XY').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    if axis=='Y': p=p.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': p=p.rotate((0,0,0),(0,1,0),90)
    return p

def make_button_screw(x,y,z,length,axis_dir):
    """ISO 7380 M3 button head; head on +axis_dir side, shank goes -axis_dir from bearing face y."""
    hr,hh=ISO7380_M3
    head=cyl_y(x,y,z,hr,hh,dir=axis_dir)
    shank=cyl_y(x,y,z,1.5,length,dir=-axis_dir)
    return fuse_all([head,shank])
def _wd_local_to_world(shape,x,side):
    """Local build: axis +Z from disk back face, lobe toward local -Y. Maps local Z->|Y|, local -Y->+Z (key side)."""
    sh=shape.rotate((0,0,0),(1,0,0),-90).translate((0,WD_BACK_Y,0))
    if side<0: sh=sh.mirror('XZ')
    return sh.translate((x,0,45))
def make_wheel_bolt_assy(x,side):
    """Mini-Cam ASS-002-103 wheel bolt assembly, shown in the 'aligned' state: lobe and spigot D-flat toward the
    key (spigot flat clears the 4x4 key, DERIVED). Turning CW swings the lobe over the hub pocket floor."""
    T=WD_FLANGE_T
    prof=(cq.Workplane('XY').center(0,-WD_FLANGE_E).circle(WD_FLANGE_R).extrude(T)
          .cut(cq.Workplane('XY').box(40,20,T+2,centered=(True,False,False)).translate((0,WD_FLAT,-1))))
    cone=cq.Workplane('XY').add(cq.Solid.makeCone(WD_FACE_R+T,WD_FACE_R,T,cq.Vector(0,0,0),cq.Vector(0,0,1)))
    disk=prof.intersect(cone)
    spig=(cq.Workplane('XY').circle(WD_SPIGOT_R).extrude(-WD_SPIGOT_L)
          .cut(cq.Workplane('XY').box(20,10,WD_SPIGOT_L+2,centered=(True,False,False)).translate((0,-WD_SPIGOT_FLAT-10,-WD_SPIGOT_L-1))))
    disk=disk.union(spig)
    for r,d0,d1 in ((WD_LIP_R,0,WD_LIP_D),(WD_GROOVE_R,WD_LIP_D,WD_GROOVE_D),(WD_SEAT_R,WD_GROOVE_D,WD_SEAT_D)):
        disk=disk.cut(cq.Workplane('XY').circle(r).extrude(d1-d0+.001).translate((0,0,T-d1)))
    disk=disk.cut(cq.Workplane('XY').circle(WD_HOLE_R).extrude(T+WD_SPIGOT_L+2).translate((0,0,-WD_SPIGOT_L-1)))
    hr,hk,hs=ISO7380_M6; zb=T-WD_HEAD_BEAR_D; Rs=(hr*hr+hk*hk)/(2*hk)
    head=cq.Workplane('XY').add(cq.Solid.makeSphere(Rs,cq.Vector(0,0,zb+hk-Rs),angleDegrees1=-90,angleDegrees2=90))
    head=head.intersect(cq.Workplane('XY').circle(hr).extrude(hk).translate((0,0,zb)))
    head=head.cut(cq.Workplane('XY').polygon(6,hs/math.cos(math.pi/6)).extrude(2.0).translate((0,0,zb+hk-2.0)))
    shank=cq.Workplane('XY').circle(M6_COSMETIC_THREAD_R).extrude(-WHEEL_SCREW_L).translate((0,0,zb))
    screw=head.union(shank)
    wri,wro,wh=SCHNORR_M6
    washer=cq.Workplane('XY').circle(wro).circle(wri).extrude(wh).translate((0,0,T-WD_SEAT_D+.005))
    R0,rt,dc=WD_ORING
    oring=cq.Workplane('XY').add(cq.Solid.makeTorus(R0,rt,cq.Vector(0,0,T-dc),cq.Vector(0,0,1)))
    return [('FSS002065_WHEEL_DISK_CAM_ASS002103',_wd_local_to_world(disk,x,side),'metal'),
            ('FIX002105_M6x14_ISO7380_WHEEL_BOLT',_wd_local_to_world(screw,x,side),'shaft'),
            ('FIX002104_M6_SPRING_WASHER_SCHNORR',_wd_local_to_world(washer,x,side),'metal'),
            ('SEA002106_ORING_10x1p8_WHEEL_DISK',_wd_local_to_world(oring,x,side),'seal')]
def lobed_seal_face(o):
    """Closed lobed track (offset o from centreline) in local XY: x=X, y=Z-45. DERIVED, see F10."""
    R=SIDE_SEAL_R; c=SIDE_SEAL_CUSP; half=25.0
    rf=((c*c+half*half)-R*R)/(2*(R-c)); zc=c+rf
    cx=[g for g in GEAR_X]; Rg=R+o; Rf=rf-o
    def P(cxx,cy,r,a): return (cxx+r*math.cos(a),cy+r*math.sin(a))
    phi=math.atan2(zc,half)
    w=cq.Workplane('XY').moveTo(*P(cx[0],0,Rg,math.pi))
    for sgn in (1,-1):
        seq=cx if sgn>0 else cx[::-1]
        for k,g in enumerate(seq):
            first,last=k==0,k==len(seq)-1
            if sgn>0:
                a0=math.pi if first else math.pi-phi; a1=0.0 if last else phi
            else:
                a0=0.0 if first else -phi; a1=-math.pi if last else -(math.pi-phi)
            if sgn>0: am=(a0+a1)/2
            else: am=(a0+a1)/2
            w=w.threePointArc(P(g,0,Rg,am),P(g,0,Rg,a1))
            if not last:
                nx=g+sgn*50; fx=(g+nx)/2; fy=sgn*zc
                b0=math.atan2(-sgn*zc,(g-fx)); b1=math.atan2(-sgn*zc,(nx-fx))
                w=w.threePointArc(P(fx,fy,Rf,-sgn*math.pi/2),P(fx,fy,Rf,b1))
    return w.close()
def lobed_band(o_in,o_out,depth,side,y_face):
    outer=lobed_seal_face(o_out).extrude(depth); inner=lobed_seal_face(o_in).extrude(depth)
    band=wp(outer.val().cut(inner.val()))
    band=band.rotate((0,0,0),(1,0,0),90)          # local y->Z, extrusion -> -Y
    if side>0: return band.translate((0,y_face+depth,45))
    return band.translate((0,-y_face,45))
def make_coupling():
    p=cyl_x(0,0,0,COUPLING_OD/2,COUPLING_L)
    bore=cyl_x(-0.5,0,0,COUPLING_BORE/2,COUPLING_L+1)
    p=cut(p,bore)
    # clamp slot + screw heads (visual)
    p=cut(p,boxc(COUPLING_L/2,0,8.0,2,COUPLING_OD+2,4))
    return p

def make_sp13_plug():
    body=cyl_x(0,0,0,SP13_PLUG_OD/2,SP13_PLUG_L)
    collar=cyl_x(8,0,0,SP13_PLUG_OD/2+2,12)
    backshell=cyl_x(SP13_PLUG_L-15,0,0,7.0,15)
    return cut(fuse_all([body,collar,backshell]),cyl_x(SP13_PLUG_L-12,0,0,2.8,12.1))

def make_sp17_panel():
    body=cyl_x(0,0,0,SP17_PANEL_OD/2,SP17_PANEL_L)
    thread=cyl_x(-4,0,0,SP17_PANEL_THREAD/2,8)
    flange=boxc(2,0,0,4,32,32)
    return fuse_all([body,thread,flange])

def make_gland():
    # LAPP M12 brass gland, simplified exact envelope with hex wrench section
    thread=cyl_x(0,0,0,6.0,LAPP_THREAD_L)
    hexp=cq.Workplane('YZ').polygon(6,LAPP_SW/math.cos(math.pi/6)).extrude(8).translate((LAPP_THREAD_L,0,0))
    tail=cyl_x(LAPP_THREAD_L+8,0,0,LAPP_OD/2,max(0.1,LAPP_CMAX-LAPP_THREAD_L-8))
    return cut(fuse_all([thread,hexp,tail]),cyl_x(-.1,0,0,3.5,LAPP_CMAX+.2))


# SOURCE-DRIVEN RECONSTRUCTION. GRAPHIC_APPROX dimensions are not manufacturing tolerances.
components=[]; side_covers=[]
def add(n,p,c): components.append((n,p,c)); return p
profile=[(18,17),(24,11),(278,11),(296,29),(296,73),(294,75),(20,75),(18,73)]
body=cq.Workplane('XZ',origin=(0,34,0)).polyline(profile).close().extrude(68)
body=cut(body,box0(24,-26.5,CAVITY_FLOOR_Z,264,53,75.1-CAVITY_FLOOR_Z))
body=cut(body,box0(WEIGHT_PLATE_X0,-WEIGHT_PLATE_W/2,BODY_Z0-.1,WEIGHT_PLATE_X1-WEIGHT_PLATE_X0,WEIGHT_PLATE_W,WEIGHT_PLATE_H+.1))  # plate recess
body=wp(body.val().fuse(box0(24,-26.5,71,264,53,4).val()))
# F14: threaded bosses for FIX-002-764 (blind, closed top), part of the housing solid.
for _px,_py in PLATE_SCREW_XY:
    body=wp(body.val().fuse(cyl_z(_px,_py,CAVITY_FLOOR_Z-.5,PLATE_BOSS_R,PLATE_BOSS_TOP_Z-CAVITY_FLOOR_Z+.5).val()))
    body=cut(body,cyl_z(_px,_py,BODY_Z0+WEIGHT_PLATE_H-.05,M8_COSMETIC_THREAD_R,PLATE_TAP_TOP_Z-BODY_Z0-WEIGHT_PLATE_H+.05))
body=cut(body,box0(SERVICE_OPEN_X0,-SERVICE_OPEN_W/2,70.9,
                  SERVICE_OPEN_X1-SERVICE_OPEN_X0,SERVICE_OPEN_W,4.2))
# Four M3 pilot holes in solid rails, nominal 8 mm engagement. Threads unmodelled.
for sx in SERVICE_SCREW_X:
    for sy in SERVICE_SCREW_Y: body=cut(body,cyl_z(sx,sy,67,1.25,8.1))
for side in (-1,1):
    pockets=fuse_all([cyl_y(x,side*27.6,45,26.5,6.5,dir=side) for x in GEAR_X])
    body=cut(body,pockets)
    # Extend supported middle/idler seats into the pocket, rather than leaving
    # shortened shafts floating. Boss faces stop at the gear face Y29.8.
    for bx,br in [(150,8.5),(100,7.0),(200,7.0)]:
        body=wp(body.val().fuse(cyl_y(bx,side*SUPPORT_BOSS_INNER_Y,45,br,
                     29.8-SUPPORT_BOSS_INNER_Y,dir=side).val()))
    for x,r,y,w in [(50,10.5,24,5),(150,7,26.4,3.5),(250,15,22,12)]:
        body=cut(body,cyl_y(x,side*y,45,r,w+.1,dir=side))
    for x in (100,200): body=cut(body,cyl_y(x,side*24,45,5,10.2,dir=side))
    cv=boxc(150,side*(34.0+SIDE_COVER_T/2),45,SIDE_COVER_L,SIDE_COVER_T,SIDE_COVER_H).edges('|Y').chamfer(1)
    # F05 per DRW-002-374 A-A: 61903 straddles cover/flange joint, no flange spigot.
    for x in WHEEL_X:
        cv=cut(cv,cyl_y(x,side*33.9,45,COVER_BEARING_SHOULDER_R,5.2,dir=side)) # outer-race shoulder
        cv=cut(cv,cyl_y(x,side*38.9,45,COVER_BEARING_BORE_R,2.2,dir=side))     # 61903 OD30 seat
    for dx in COVER_SCREW_DX:
        for dz in COVER_SCREW_DZ:
            sx,sz=150+dx,45+dz
            cv=cut(cv,cyl_y(sx,side*33.9,45+dz,1.7,7.2,dir=side))                 # clearance Ø3.4
            cv=cut(cv,cyl_y(sx,side*(41-COVER_SCREW_CBORE[1]),sz,COVER_SCREW_CBORE[0],COVER_SCREW_CBORE[1]+.1,dir=side))
            body=cut(body,cyl_y(sx,side*34.1,sz,1.5,5.1,dir=-side))                # M3 cosmetic thread, depth 5
    for x in WHEEL_X:
        for a in (45,135,225,315):  # M3 cosmetic taps for flange screws, depth 4
            fx=x+FLANGE_SCREW_R*math.cos(math.radians(a)); fz=45+FLANGE_SCREW_R*math.sin(math.radians(a))
            cv=cut(cv,cyl_y(fx,side*41.1,fz,1.5,4.1,dir=-side))
    cv=cut(cv,lobed_band(-SIDE_SEAL_W/2,SIDE_SEAL_W/2,SIDE_SEAL_D,side,34.0))   # F10 groove
    side_covers.append((f'HOLD_SIDE_COVER_{side}_GRAPHIC262x60x7',cv));add(side_covers[-1][0],cv,'metal')
    _hw=math.pi*.75**2/SIDE_SEAL_D/2   # area-equal installed section half-width
    add(f'HOLD_SIDE_ORING_190x1p5_{side}_LOBED_GLAND_INSTALLED',lobed_band(-_hw,_hw,SIDE_SEAL_D,side,34.0),'seal')
    for dx in COVER_SCREW_DX:
        for dz in COVER_SCREW_DZ:
            add(f'FIX000359_M3x8_ISO7380_COVER_{side}_{int(150+dx)}_{int(45+dz)}',
                make_button_screw(150+dx,side*(41-COVER_SCREW_CBORE[1]),45+dz,8,side),'shaft')
    for j,x in enumerate(GEAR_X):
        gear=make_spur_gear(50,1,4,12,'Y')
        if j%2:gear=gear.rotate((0,0,0),(0,1,0),3.6)
        add(f'HOLD_Z50_{side}_{int(x)}_PROFILE_UNCONFIRMED',gear.translate((x,side*31.8,45)),'gear')
        if j%2:
            add(f'IDLE_BUSH_10_12_4_{side}_{x}',ring_y(x,side*31.8,45,6,5,4),'bearing')
            add(f'HOLD_IDLE_PIN_{side}_{x}',cyl_y(x,side*IDLER_PIN_INNER_Y,45,5,34-IDLER_PIN_INNER_Y,dir=side),'shaft')
    add(f'61801_SIDE_{side}_50_SOURCE_ONE_PER_SIDE',make_bearing(12,21,5).translate((50,side*26.5,45)),'bearing')
    add(f'MIDDLE_BUSH_12_14_3_{side}',ring_y(150,side*(MIDDLE_INNER_Y+MIDDLE_BUSH_W/2),45,7,6,MIDDLE_BUSH_W),'bearing')
    for x in WHEEL_X:
        inner_y=MIDDLE_INNER_Y if x==150 else 23.0
        shaft=fuse_all([cyl_y(x,side*inner_y,45,6,39-inner_y,dir=side),cyl_y(x,side*39,45,8.5,7,dir=side),
          cyl_y(x,side*46,45,9,2.8,dir=side),cyl_y(x,side*48.8,45,8,12.1,dir=side)])
        key=boxc(x,side*54.9,52,4,12,4);shaft=cut(shaft,key)
        # F13: shaft end per ASS-002-103 — counterbore for the FSS-002-065 spigot + M6 tapped hole drawn at
        # major Ø6 (cosmetic thread). Screw tip at |Y|49.53, hole bottom 48.9 -> tip gap 0.63 mm, DERIVED.
        shaft=cut(shaft,cyl_y(x,side*(SHAFT_END_Y-SHAFT_SPIGOT_BORE_D),45,SHAFT_SPIGOT_BORE_R,SHAFT_SPIGOT_BORE_D+.1,dir=side))
        _tap0=SHAFT_END_Y-SHAFT_SPIGOT_BORE_D+.05; _tapbot=WD_BACK_Y+WD_FLANGE_T-WD_HEAD_BEAR_D-WHEEL_SCREW_L-0.63
        shaft=cut(shaft,cyl_y(x,side*_tap0,45,M6_COSMETIC_THREAD_R,_tap0-_tapbot,dir=-side))
        add(f'HOLD_WHEEL_SHAFT_{side}_{x}_GRAPHIC_AXIAL_PACKAGE',shaft,'shaft')
        add(f'KEY_4x4x12_{side}_{x}',key,'shaft')
        add(f'61903_SIDE_{side}_{x}',make_bearing(17,30,7).translate((x,side*42.5,45)),'bearing')
        flange=fuse_all([cyl_y(x,side*41,45,17,7.8,dir=side),cyl_y(x,side*41,45,25,FLANGE_COLLAR_T,dir=side)])
        flange=cut(flange,cyl_y(x,side*40.9,45,9.08,8.2,dir=side))
        flange=cut(flange,cyl_y(x,side*40.9,45,15,5.1,dir=side))
        # Face-seal groove in flange underside (DRW374 pos.11 location; dims ESTIMATED).
        flange=cut(flange,ring_y(x,side*(41+FLANGE_GROOVE_DEPTH/2-.05),45,FLANGE_GROOVE_RO,FLANGE_GROOVE_RI,FLANGE_GROOVE_DEPTH+.1))
        flange=cut(flange,cyl_y(x,side*46,45,11.4,2.8,dir=side))
        fscrews=[]
        for a in (45,135,225,315):
            fx=x+FLANGE_SCREW_R*math.cos(math.radians(a)); fz=45+FLANGE_SCREW_R*math.sin(math.radians(a))
            flange=cut(flange,cyl_y(fx,side*40.9,fz,1.7,FLANGE_COLLAR_T+.2,dir=side))
            fscrews.append((a,fx,fz))
        add(f'HOLD_AXLE_FLANGE_{side}_{x}_GRAPHIC_CONTOUR',flange,'metal')
        for a,fx,fz in fscrews:
            add(f'FIX002738_M3x6_ISO7380_FLANGE_{side}_{int(x)}_{a}',
                make_button_screw(fx,side*(41+FLANGE_COLLAR_T),fz,6,side),'shaft')
        add(f'HOLD_XRING_INSTALLED_{side}_{x}_FREE18p72x2p62',ring_y(x,side*47.4,45,11.4,9,2.8),'seal')
        add(f'HOLD_FLANGE_ORING_32x1p5_{side}_{x}_FACE_GLAND_INSTALLED',
            ring_y(x,side*(41+FLANGE_GROOVE_DEPTH/2),45,FLANGE_ORING_INST_RO,FLANGE_GROOVE_RI,FLANGE_GROOVE_DEPTH),'seal')
        pts=list(WHEEL_PROFILE)
        if side<0:pts=[(r,-yy) for r,yy in pts]
        tyre=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(0,1)).translate((x,side*WHEEL_CENTRE_Y,WHEEL_Z))
        tyre=cut(tyre,key)
        # F13: pocket in the Al hub for the FSS-002-065 cam disk (Ø20.4 vs disk max r8.78), ESTIMATED.
        tyre=cut(tyre,cyl_y(x,side*SHAFT_END_Y,45,10.2,5.7,dir=side))
        hubcyl=cyl_y(x,side*30,45,QRW_HUB_R,40,dir=side)
        hub=wp(tyre.val().intersect(hubcyl.val())); tyre=cut(tyre,hubcyl)
        add(f'HOLD_QRW90SR150_WHEEL_{side}_{x}_ENGINEERED_OUTER_SHOULDER',tyre,'wheel')
        add(f'HOLD_QRW90_HUB_AL_{side}_{x}_ESTIMATED',hub,'metal')
        for nm,part,cat in make_wheel_bolt_assy(x,side):
            add(f'{nm}_{side}_{int(x)}',part,cat)
def candidate_motor_pack(y):
    # Provisional conservative family envelope; leads and exact 138:1 outline unresolved.
    return fuse_all([
        cyl_x(MOTOR_FACE-GEARHEAD_LEN-MOTOR_LEN,y,45,MOTOR_OD/2,MOTOR_LEN),
        cyl_x(MOTOR_FACE-GEARHEAD_LEN,y,45,GEARHEAD_OD/2,GEARHEAD_LEN),
        cyl_x(MOTOR_FACE,y,45,MOTOR_PILOT_D/2,MOTOR_PILOT_L),
        cyl_x(MOTOR_FACE,y,45,MOTOR_SHAFT_D/2,MOTOR_SHAFT_L)])
# F06 bevel pair, built once. Layout DERIVED: apex (250,±MOTOR_Y,45); Z16 pitch circle X230,
# Z40 pitch circle |Y|5.5. m1, 20°, face 6, backlash .05, tip clearance .1 — ESTIMATED (H04).
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor_py'))
import cq_gears
BEVEL_FACE_W=6.0; BEVEL_BACKLASH=0.05; BEVEL_CLEARANCE=0.1
_bp=cq_gears.BevelGearPair(module=BEVEL_MOD,gear_teeth=Z40_TEETH,pinion_teeth=Z16_TEETH,face_width=BEVEL_FACE_W,
                           backlash=BEVEL_BACKLASH,clearance=BEVEL_CLEARANCE)
_ba=_bp.assemble(build_gear=True,build_pinion=True,transform_pinion=True)
def _child(asm,key):
    c=[ch for ch in asm.children if key(ch.name)][0]
    o=c.obj.val() if hasattr(c.obj,'val') else c.obj
    return o.moved(c.loc)
BEVEL_GEAR_SOLID=_child(_ba,lambda n:'gear' in n and 'pinion' not in n)
BEVEL_PINION_SOLID=_child(_ba,lambda n:'pinion' in n)
BEVEL_CONE_H=float(_bp.gear.cone_h)    # apex height above Z40 back face in library frame
BEVEL_APEX_Y=MOTOR_Y
motor_holder=boxc(MOTOR_FACE+1.5,0,45,3,52.8,30)
pinion_holder=boxc(227,0,45,5,52.8,26)
for side in (-1,1):
    y=side*MOTOR_Y
    # F06: straight bevel teeth (cq_gears), common apex at Z40 axis x Z16 axis.
    def place(sh):
        sh=sh.rotate(cq.Vector(0,0,0),cq.Vector(1,0,0),-90*side)
        return wp(sh.translate(cq.Vector(250,side*(BEVEL_APEX_Y-BEVEL_CONE_H),45)))
    z40=place(BEVEL_GEAR_SOLID)
    z40=cut(z40,cyl_y(250,side*(BEVEL_APEX_Y-BEVEL_CONE_H-.1),45,9.7,5.5-(BEVEL_APEX_Y-BEVEL_CONE_H)+.15,dir=side)) # 61800 clearance counterbore, ESTIMATED
    z40=cut(z40,cyl_y(250,side*.4,45,5,15,dir=side))   # bore on Z40 output shaft r5
    z16=place(BEVEL_PINION_SOLID)
    z16=cut(z16,cyl_x(228,y,45,3,12))                  # bore on Z16 shaft r3
    add(f'HOLD_Z40_BEVEL_{side}_STRAIGHT_M1_TEETH',z40,'bevel');add(f'HOLD_Z16_BEVEL_{side}_STRAIGHT_M1_TEETH',z16,'bevel')
    axle=fuse_all([cyl_y(250,side*.5,45,5,19.5,dir=side),cyl_y(250,side*20,45,9,9.8,dir=side)])
    axle=cut(axle,cyl_y(250,side*23,45,6,6.9,dir=side))
    add(f'HOLD_Z40_OUTPUT_SHAFT_{side}_SOCKET_TORQUE_TRANSFER_HOLD',axle,'shaft')
    add(f'61800_Z40_{side}',make_bearing(10,19,5).translate((250,side*3,45)),'bearing')
    add(f'SHAFT_SEAL_Z40_{side}_18x30x7',make_seal(18,30,7).translate((250,side*25.5,45)),'seal')
    pin=fuse_all([cyl_x(209,y,45,3,15.5),cyl_x(224.5,y,45,6,5),cyl_x(229.5,y,45,3,7.5)])
    add(f'HOLD_Z16_SHAFT_{side}',pin,'shaft')
    add(f'61801_Z16_SUPPORT_{side}',make_bearing(12,21,5,'X').translate((227,y,45)),'bearing')
    pinion_holder=cut(pinion_holder,cyl_x(224.4,y,45,10.5,5.2))
    add(f'HOLD_NBK_MLR20C_6_6_COUPLING_{side}_EXTERNAL_DETAIL',make_coupling().translate((199.5,y,45)),'purchased')
    adapter=cut(cyl_x(199.5,y,45,3,8),cyl_x(199.4,y,45,2,8.2))
    adapter=cut(adapter,boxc(203.5,y+2.75,45,8.2,1.5,.5))
    add(f'HOLD_MOTOR_SPLIT_ADAPTER_6_TO_4_{side}',adapter,'shaft')
    add(f'TRACTION_MOTOR_{side}_PROTEUS_CLASS_GP26_D22_ESTIMATED_HOLD',candidate_motor_pack(y),'purchased')
    motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-.1,y,45,3.3,3.2))
    # ESTIMATED 4-hole pattern; exact supplied variant and body attachment HOLD.
    for angle in (45,135,225,315):
        a=math.radians(angle)
        motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-.1,y+9.5*math.cos(a),45+9.5*math.sin(a),1.35,3.2))
add('HOLD_PAIRED_MOTOR_HOLDER_GP26_ESTIMATED',motor_holder,'metal')
add('HOLD_PAIRED_PINION_BEARING_HOLDER',pinion_holder,'metal')
cover=boxc(SERVICE_CX,0,78.5,SERVICE_L,SERVICE_W,SERVICE_T)
for x in SERVICE_SCREW_X:
    for y in SERVICE_SCREW_Y:cover=cut(cover,cyl_z(x,y,74.9,1.7,7.2))
cover=cut(cover,cyl_z(VALVE_XY[0],VALVE_XY[1],74.9,5.05,7.2))   # F18: valve moved to cover rear strip, ESTIMATED
cover=cut(cover,cyl_z(CAM_GLAND_XY[0],CAM_GLAND_XY[1],74.9,6.05,7.2)) # F18: M12 camera-cable gland thread, ESTIMATED
outer=boxc(SERVICE_GROOVE_CX,0,75+(SERVICE_GROOVE_DEPTH-.1)/2,
           SERVICE_GROOVE_L+SERVICE_GROOVE_WIDTH,SERVICE_GROOVE_W+SERVICE_GROOVE_WIDTH,
           SERVICE_GROOVE_DEPTH+.1).edges('|Z').fillet(SERVICE_GROOVE_RADIUS+SERVICE_GROOVE_WIDTH/2)
inner=boxc(SERVICE_GROOVE_CX,0,75+(SERVICE_GROOVE_DEPTH-.1)/2,
           SERVICE_GROOVE_L-SERVICE_GROOVE_WIDTH,SERVICE_GROOVE_W-SERVICE_GROOVE_WIDTH,
           SERVICE_GROOVE_DEPTH+.3).edges('|Z').fillet(SERVICE_GROOVE_RADIUS-SERVICE_GROOVE_WIDTH/2)
cover=cut(cover,cut(outer,inner))
add('HOLD_PRESSURE_ELECTRONICS_COVER_SERVICE205x68x7',cover,'metal')
VX,VY=VALVE_XY
valve_body=cut(cyl_z(VX,VY,78,5,14),cyl_z(VX,VY,77.9,2.1,14.2))
add('HOLD_PRESSURE_VALVE_BODY_SOURCE_FAMILY',valve_body,'valve')
add('HOLD_PRESSURE_VALVE_CAP',cyl_z(VX,VY,92,6,1.5),'valve')
add('HOLD_PRESSURE_VALVE_4MM_BALL',cq.Workplane('XY').sphere(2).translate((VX,VY,88)),'valve')
# F18: camera cable enters the cover through a vertical M12 gland behind the lift base (Proteus: M12 entry, DRW-002-745).
lapp=make_gland().rotate((0,0,0),(0,1,0),-90).translate((CAM_GLAND_XY[0],CAM_GLAND_XY[1],SERVICE_Z+.5))
add('HOLD_LAPP_SKINTOP_53112000_M12x1p5_CAMERA_CABLE_IN_COVER',lapp,'purchased')

# ---------------- F18 camera lift DRW-002-744 / DRW-002-752 (folded, theta=0) ----------------
AX,AZ=LIFT_A_X,LIFT_A_Z
def lift_rel(d): return (AX-d[0],AZ+d[1])        # toward camera = -X
LB=lift_rel(LIFT_AB)                             # side-link base pivot B
LC=(AX-LINK_L,AZ)                                # central lever top pivot C (on lift housing)
LD=(LB[0]-LINK_L,LB[1])                          # side-link top pivot D: exact parallelogram, CD=AB
LE=lift_rel(LIFT_GAS_E); LG=lift_rel(LIFT_GAS_G) # gas spring eyes
BASE_X0=AX-(LIFT_BASE_L-LIFT_BASE_BEHIND_A); BASE_X1=AX+LIFT_BASE_BEHIND_A; BASE_Z0=SERVICE_Z+SERVICE_T
SW_IN=LIFT_SIDE_Y-LIFT_SIDE_T/2; SW_OUT=LIFT_SIDE_Y+LIFT_SIDE_T/2
# Base FAL-002-067: 8 mm plate (ESTIMATED) on the cover, A-cheeks, B-lugs, gas-spring slot and side-link reliefs.
lbase=box0(BASE_X0,-LIFT_BASE_W/2,BASE_Z0,LIFT_BASE_L,LIFT_BASE_W,8)
for sy in (-1,1):
    lbase=lbase.union(box0(AX-10,sy*12.2-2,BASE_Z0+8,20,4,AZ+10-BASE_Z0-8))                      # A cheeks Y+-10.2..14.2
    lbase=lbase.union(box0(LB[0]-6.5,(SW_OUT+.2) if sy>0 else -LIFT_BASE_W/2,BASE_Z0+8,14,
                           LIFT_BASE_W/2-SW_OUT-.2,LB[1]+8-BASE_Z0-8))                             # B lugs outside links
    lbase=cut(lbase,box0(BASE_X0-.1,(SW_IN-.3) if sy>0 else -(SW_OUT+.2),BASE_Z0-.1,LB[0]+8-BASE_X0,SW_OUT-SW_IN+.5,8.2))
lbase=cut(lbase,box0(BASE_X0-.1,-6.5,BASE_Z0-.1,LE[0]+6.5-BASE_X0+.1,13,8.2))                     # gas-spring slot
lbase=cut(lbase,cyl_y(AX,-15,AZ,5.1,30)); lbase=cut(lbase,cyl_y(LB[0],-35,LB[1],4.05,70))
lbase=cut(lbase,cyl_y(LE[0],-12.1,LE[1],3.05,24.2))
add('HOLD_LIFT_BASE_FAL002067_ON_SERVICE_COVER',lbase,'lift')
# Clamp axle FSS-002-089 (M10, M8 end), washer FSS-002-077, 3x DIN2093 20x10.2x1.1, 2x ISO4035 M10, clamp lever FIX-002-527 M8.
caxle=fuse_all([cyl_y(AX,-20.35,AZ,4.95,44.55),cyl_y(AX,-28.35,AZ,4.0,8.0)])
add('HOLD_LIFT_CLAMP_AXLE_FSS002089_M10',caxle,'lift')
add('HOLD_LIFT_CLAMP_WASHER_FSS002077',ring_y(AX,-14.95,AZ,10,5.1,1.5),'lift')
for i,yc in enumerate((-16.475,-18.025,-19.575),1):
    add(f'HOLD_LIFT_DISC_SPRING_DIN2093_20x10p2x1p1_{i}',ring_y(AX,yc,AZ,10,5.1,1.55),'lift')
def hex_nut_y(y0,w):
    n=cq.Workplane('XZ').polygon(6,17/math.cos(math.pi/6)).extrude(-w).translate((AX,y0,AZ))
    return cut(n,cyl_y(AX,y0-.1,AZ,5.0,w+.2))
for i,y0 in enumerate((14.2,19.2),1):add(f'HOLD_LIFT_NUT_ISO4035_M10_{i}',hex_nut_y(y0,5),'lift')
clamp=fuse_all([cyl_y(AX,-28.35,AZ,8,8),between((AX,-24.35,AZ),(AX-70,-24.35,AZ),3.5)])
clamp=cut(clamp,cyl_y(AX,-28.45,AZ,4.05,8.2))
add('HOLD_LIFT_CLAMP_LEVER_M8_FIX002527',clamp,'lift')
# Central lever ASS-002-723 + lever sheet plate FSS-002-073 (AC = LINK_L).
lever=[cyl_y(AX,-10,AZ,9,20),boxc((LC[0]+14+AX-11)/2,0,AZ+7.5,AX-11-LC[0]-14,LIFT_LEVER_PLATE_W,3)]
for sy in (-1,1):
    yc=sy*sum(LIFT_CHEEK_Y)/2; tc=LIFT_CHEEK_Y[1]-LIFT_CHEEK_Y[0]
    lever.append(plate_between((AX,AZ+.25),(LC[0],AZ+.25),yc,tc,11.5))
    lever.append(cyl_y(LC[0],yc-tc/2,LC[1],7,tc))
lever=fuse_all(lever)
lever=cut(lever,cyl_y(AX,-10.1,AZ,5.1,20.2)); lever=cut(lever,cyl_y(LC[0],-10,LC[1],4.05,20))
lever=cut(lever,cyl_y(LG[0],-10,LG[1],3.05,20))
add('HOLD_LIFT_CENTRAL_LEVER_ASS002723_FSS002073',lever,'lift')
# Side links FSS-002-068 (BD = LINK_L) with axles FSS-002-075 (base) and FSS-002-079 (lift housing).
for sy in (-1,1):
    yc=sy*LIFT_SIDE_Y
    link=fuse_all([plate_between(LB,LD,yc,LIFT_SIDE_T,LIFT_SIDE_H),
                   cyl_y(LB[0],yc-LIFT_SIDE_T/2,LB[1],7.5,LIFT_SIDE_T),cyl_y(LD[0],yc-LIFT_SIDE_T/2,LD[1],7.5,LIFT_SIDE_T)])
    for px,pz in (LB,LD):link=cut(link,cyl_y(px,yc-LIFT_SIDE_T/2-.1,pz,4.05,LIFT_SIDE_T+.2))
    add(f'HOLD_LIFT_SIDE_LINK_FSS002068_{sy}',link,'lift')
    add(f'HOLD_LIFT_SIDE_AXLE_FSS002075_{sy}',fuse_all([cyl_y(LB[0],sy*SW_IN,LB[1],3.95,(LIFT_BASE_W/2-SW_IN),dir=sy),
        cyl_y(LB[0],sy*LIFT_BASE_W/2,LB[1],6,1.5,dir=sy)]),'lift')
    add(f'HOLD_LIFT_TOP_AXLE_FSS002079_{sy}',fuse_all([cyl_y(LD[0],sy*16,LD[1],3.95,SW_OUT-16,dir=sy),
        cyl_y(LD[0],sy*SW_OUT,LD[1],6,1.5,dir=sy)]),'lift')
# Gas spring SPR-002-524 150 N -> ACE GS-12-80-V4A (eye-to-eye 112..192), pins M6x18 FIX-002-749.
E3=cq.Vector(LE[0],0,LE[1]); G3=cq.Vector(LG[0],0,LG[1]); gu=(G3-E3).normalized()
gas_length=(G3-E3).Length; body_pt=E3.toTuple(); moving=G3.toTuple()
gbody=fuse_all([ring_y(LE[0],0,LE[1],5,3.05,6),between((E3+gu*4).toTuple(),(E3+gu*7.2).toTuple(),3),
                between((E3+gu*7).toTuple(),(E3+gu*100).toTuple(),ACE_BODY_OD/2)])
add('HOLD_ACE_GS12_80_V4A_150N_BODY_END_FITTINGS',gbody,'purchased')
grod=fuse_all([between((E3+gu*100).toTuple(),(G3-gu*4).toTuple(),ACE_ROD_OD/2),ring_y(LG[0],0,LG[1],4.5,3.05,5)])
add('HOLD_ACE_GS12_80_ROD',grod,'purchased')
add('HOLD_LIFT_GAS_SPRING_PIN_M6x18_FIX002749',cyl_y(LE[0],-9,LE[1],2.95,18),'lift')
add('HOLD_LIFT_GAS_SPRING_UPPER_PIN',cyl_y(LG[0],-LIFT_CHEEK_Y[1],LG[1],2.95,2*LIFT_CHEEK_Y[1]),'lift')
# Camera harness: SP13 (in lift housing) -> up behind the housing -> over the folded lever -> M12 gland in cover.
harness_points=[(8,0,CAM_Z),(15,0,CAM_Z),(15,0,HARNESS_TOP_Z),(CAM_GLAND_XY[0]-8,0,HARNESS_TOP_Z),
                (CAM_GLAND_XY[0],0,104),(CAM_GLAND_XY[0],0,96)]
def poly_tube(points,radius):
    return fuse_all([between(a,b,radius) for a,b in zip(points,points[1:]) if math.dist(a,b)>1e-5])
# Lift housing DRW-002-752 (simplified interface): camera socket block, D lug, C arm.
LHX1=14.0
lh=fuse_all([box0(LHX1-LIFT_HOUSING_L-2,-LIFT_HOUSING_W/2,CAM_Z-24,LIFT_HOUSING_L+2,LIFT_HOUSING_W,48),
             box0(2,-LIFT_HOUSING_W/2+.5,LD[1]-7.4,19,LIFT_HOUSING_W-1,15),
             box0(0,-6.4,91,LC[0]+7.1,12.8,21)])
lh=cut(lh,cyl_x(LHX1-LIFT_HOUSING_L-2.1,0,CAM_Z,11.5,LIFT_HOUSING_L+2.2))
lh=cut(lh,cyl_y(LD[0],-LIFT_HOUSING_W/2-.1,LD[1],4.05,LIFT_HOUSING_W+.2))
lh=cut(lh,cyl_y(LC[0],-6.5,LC[1],4.05,13))
lh=cut(lh,box0(11.7,-3.3,CAM_Z+6,6.6,6.6,HARNESS_TOP_Z-CAM_Z-7))   # harness slot behind the camera socket (box: robust STEP)
add('HOLD_LIFT_HOUSING_DRW002752_SIMPLIFIED_INTERFACE',lh,'lift')
add('HOLD_LIFT_TOP_LEVER_AXLE_FSS002076',cyl_y(LC[0],-LIFT_CHEEK_Y[1],LC[1],3.95,2*LIFT_CHEEK_Y[1]),'lift')
# CAM026 catalogue envelope 120x74x74 (rear rotate housing + pan/tilt head + window).
cam_rear=CAM_REAR_X; cam_front=cam_rear-CAM026_ENVELOPE[0]
add('HOLD_CAM026_ROTATE_HOUSING_GRAPHIC_OD62p5',cyl_x(cam_rear-60,0,CAM_Z,CAM_R,60),'camera')
head=boxc(cam_front+1+29.5,0,CAM_Z,59,CAM026_ENVELOPE[1],CAM026_ENVELOPE[2]).edges('|X').fillet(12)
add('HOLD_CAM026_PAN_TILT_HEAD_ENVELOPE_120x74x74',head,'camera')
add('HOLD_CAM026_FRONT_WINDOW_DIAMETER_UNKNOWN',cyl_x(cam_front,0,CAM_Z,12,1),'camera')
sp13=make_sp13_plug().translate((-36,0,CAM_Z));add('HOLD_WEIPU_SP1310_S6I_N_AND_PANEL_INTERFACE',sp13,'connector')
jacket=poly_tube(harness_points,2.7)
for i,name in enumerate(['12V','GND','TX','RX','CVBS_SIGNAL','CVBS_RETURN']):
    core=poly_tube([(x,y+(i-2.5)*.65,z) for x,y,z in harness_points],.22)
    jacket=cut(jacket,core);add(f'CAMERA_HARNESS_CORE_{i+1}_{name}_ROUTE_HOLD',core,'wire')
add('HOLD_LAPP_0028679_CAMERA_HARNESS_6CORE_ROUTE',jacket,'cable')
hx=150.0
hguard=cut(between((hx-6,0,HARNESS_TOP_Z),(hx+6,0,HARNESS_TOP_Z),4.5),between((hx-6.1,0,HARNESS_TOP_Z),(hx+6.1,0,HARNESS_TOP_Z),3.2))
hguard=cut(hguard,box0(hx-6.2,-5,AZ,12.4,10,HARNESS_TOP_Z-3.5-AZ))
hguard=cut(hguard,boxc(hx,0,HARNESS_TOP_Z+4,14,4,5));add('PX1_LIFT_HARNESS_CLIP_ON_LEVER_OPEN_PROFILE',hguard,'print')
controller=cq.importers.importStep(str(CAD/'vendor'/'WeAct_F4_64Pin_V11_Manufacturer.step'))
controller=wp(cq.Compound.makeCompound(controller.vals()))
b=controller.val().BoundingBox();controller=controller.translate((-(b.xmin+b.xmax)/2,-(b.ymin+b.ymax)/2,-b.zmin))
controller=controller.rotate((0,0,0),(0,0,1),90).translate((208,0,60.1))
add('WEACT_STM32F446RET6_V11_MANUFACTURER_STEP',controller,'electronics')
g2=cq.importers.importStep(str(CAD/'vendor'/'Pololu_G2_24v13_Manufacturer.step')).translate((-16.51,-10.16,0))
for i,(x,z) in enumerate(((47,59),(99,24.5)),1):add(f'POLOLU_2992_G2_24v13_{i}_MANUFACTURER_STEP',g2.translate((x,0,z)),'electronics')  # F16: #2 lowered under motors; F14: #1 raised Z26->59 above the balun (clears M8 plate-screw boss)
add('HOLD_CINCON_CQB150W110S24_BODY_PINS_THERMAL_HOLD',boxc(155,0,65,*CINCON),'electronics')  # F16: +1 mm over D26 gearheads
add('NICHICON_UCS2D221MHD1TN_BODY18x25',cyl_z(278,0,30,9,25),'electronics')
add('ADAFRUIT_MPRLS_3965_ENVELOPE',boxc(277.5,-17.5,60,*MPRLS),'electronics')
add('HOLD_POLOLU_5577_D42V55F12_ENVELOPE',boxc(211.5,-13.5,29,*POLOLU_5577),'electronics')
add('HOLD_POLOLU_5571_D42V55F5_ENVELOPE',boxc(211.5,13.5,29,*POLOLU_5571),'electronics')
add('HOLD_WAVESHARE_27479_ISOLATED_RS485_C_ENVELOPE',boxc(264,0,68,*WAVESHARE_27479),'electronics')
add('HOLD_DELTA_TR1D_P2_VIDEO_BALUN',boxc(52,0,50,*VIDEO_SCREEN),'electronics_hold')  # F16: moved forward of motors
body=cut(body,cyl_x(287.9,0,45,8.6,8.2))
add('HOLD_WEIPU_SP1712_7PIN_REAR_PANEL_6_USED',make_sp17_panel().translate((296,0,45)),'connector')
strain=cut(cyl_x(316,0,45,12,32),cyl_x(315.9,0,45,10,32.2))
cone=cq.Workplane('YZ').circle(10).workplane(offset=30).circle(6).loft(combine=True).translate((316,0,45))
cone=cut(cone,cyl_x(315.9,0,45,4.5,32.2))
add('HOLD_REAR_TETHER_STRAIN_SLEEVE',strain,'metal');add('HOLD_REAR_TETHER_ARAMID_CONE',cone,'metal')
add('HOLD_MAIN_TETHER_6CORE_REINFORCED_ARTICLE_UNKNOWN',cyl_x(348,0,45,4.5,80),'cable')
plate=box0(WEIGHT_PLATE_X0,-WEIGHT_PLATE_W/2,BODY_Z0,WEIGHT_PLATE_X1-WEIGHT_PLATE_X0,WEIGHT_PLATE_W,WEIGHT_PLATE_H)
_cb_floor=BODY_Z0+WEIGHT_PLATE_H-PLATE_CBORE_LIG          # Z19.0
_wri,_wro,_ws=SPRING_WASHER_M8; _hr,_hk,_hs=DIN7984_M8
_bear=_cb_floor-_ws                                         # head bearing face Z17.0; head bottom Z12.0 (1.0 recessed)
for _i,(_px,_py) in enumerate(PLATE_SCREW_XY,1):
    plate=cut(plate,cyl_z(_px,_py,BODY_Z0-.1,PLATE_CBORE_R,_cb_floor-BODY_Z0+.1))
    plate=cut(plate,cyl_z(_px,_py,_cb_floor-.1,PLATE_SCREW_HOLE_R,PLATE_CBORE_LIG+.2))
    head=cut(cyl_z(_px,_py,_bear-_hk,_hr,_hk),
             cq.Workplane('XY').polygon(6,_hs/math.cos(math.pi/6)).extrude(3.0).translate((_px,_py,_bear-_hk-.01)))
    screw=fuse_all([head,cyl_z(_px,_py,_bear,M8_COSMETIC_THREAD_R,PLATE_SCREW_L)])   # tip Z33.0, engagement 10.0
    add(f'FIX002764_M8x16_DIN7984_PLATE_{_i}',screw,'shaft')
    add(f'FIX002741_M8_SPRING_WASHER_{_i}',cut(cyl_z(_px,_py,_bear,_wro,_ws),cyl_z(_px,_py,_bear-.1,_wri,_ws+.2)),'shaft')
add('FSS002060_WEIGHT_PLATE_STAINLESS_M8_FIXING_HOLD',plate,'metal')
for i,b in enumerate(BALLAST_BOXES,1):
    add(f'HOLD_BALLAST_{i}_STEEL',box0(b[0],b[1],b[2],b[3]-b[0],b[4]-b[1],b[5]-b[2]),'metal')
components.insert(0,('HOLD_PRESSURE_BODY_CRP150_GRAPHIC278x68x64_CAVITY_UNRESOLVED',body,'body'))
from release_tools import finish_build
finish_build(globals())
