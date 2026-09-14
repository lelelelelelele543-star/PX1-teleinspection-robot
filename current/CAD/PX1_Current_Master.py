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
FLANGE_ORING=(32.0,1.5)

# Current reconstructed global CRP150/PX1 screen from recovered CAD audits.
# These are NOT released manufacturing dimensions unless separately called out.
BODY_L_SOURCE_SCREEN=278.0
BODY_HALF_W_SCREEN=34.0
BODY_Z0=11.0
BODY_TOP=75.0
PIPE_R=75.0
PIPE_CENTER_Z=52.0480547

# New motor adaptation — exact product envelope where published
MOTOR_OD=25.0; MOTOR_LEN=53.8; MOTOR_SHAFT_D=4.0; MOTOR_SHAFT_L=12.5
MOTOR_FACE=195.5; MOTOR_Y=13.5 # integration datums HOLD
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
SERVICE_CX=208.0; SERVICE_L=158.0; SERVICE_W=53.0; SERVICE_T=7.0; SERVICE_Z=75.0
SERVICE_OPEN=(48.0,22.0)
SERVICE_SCREW_X=(132.0,284.0)

# Lift kinematics recovered in current project
PIVOT_X=240.0; PIVOT_Z_LOW=96.0; PIVOT_Z_HIGH=110.0; LINK_L=200.0
ARM_Y=36.0; ARM_T=3.0; ARM_H=15.0
CAM_Z=70.0; CAM026_MEASURED_BASE_OD=62.5; CAM_R=CAM026_MEASURED_BASE_OD/2; CAM_LEN=132.0

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
body=cut(body,box0(24,-26.5,23,264,53,52.1))
body=wp(body.val().fuse(box0(24,-26.5,71,264,53,4).val()))
body=cut(body,box0(138,-18.5,70.9,140,37,4.2))
for side in (-1,1):
    pockets=fuse_all([cyl_y(x,side*27.6,45,26.5,6.5,dir=side) for x in GEAR_X])
    body=cut(body,pockets)
    for x,r,y,w in [(50,10.5,24,5),(150,7,24,4),(250,15,22,12)]:
        body=cut(body,cyl_y(x,side*y,45,r,w+.1,dir=side))
    for x in (100,200): body=cut(body,cyl_y(x,side*24,45,5,10.2,dir=side))
    cv=boxc(150,side*37.5,45,262,7,60).edges('|Y').chamfer(1)
    for x in WHEEL_X: cv=cut(cv,cyl_y(x,side*33.9,45,17.05,7.2,dir=side))
    side_covers.append((f'HOLD_SIDE_COVER_{side}_GRAPHIC262x60x7',cv));add(side_covers[-1][0],cv,'metal')
    for j,x in enumerate(GEAR_X):
        gear=make_spur_gear(50,1,4,12,'Y')
        if j%2:gear=gear.rotate((0,0,0),(0,1,0),3.6)
        add(f'HOLD_Z50_{side}_{int(x)}_PROFILE_UNCONFIRMED',gear.translate((x,side*31.8,45)),'gear')
        if j%2:
            add(f'IDLE_BUSH_10_12_4_{side}_{x}',ring_y(x,side*31.8,45,6,5,4),'bearing')
            add(f'HOLD_IDLE_PIN_{side}_{x}',cyl_y(x,side*24,45,5,10,dir=side),'shaft')
    add(f'61801_SIDE_{side}_50_SOURCE_ONE_PER_SIDE',make_bearing(12,21,5).translate((50,side*26.5,45)),'bearing')
    add(f'MIDDLE_BUSH_12_14_4_{side}',ring_y(150,side*26,45,7,6,4),'bearing')
    for x in WHEEL_X:
        shaft=fuse_all([cyl_y(x,side*23,45,6,16,dir=side),cyl_y(x,side*39,45,8.5,7,dir=side),
          cyl_y(x,side*46,45,9,2.8,dir=side),cyl_y(x,side*48.8,45,8,12.1,dir=side)])
        key=boxc(x,side*54.9,52,4,12,4);shaft=cut(shaft,key)
        shaft=cut(shaft,cyl_y(x,side*51,45,2.1,10,dir=side))
        add(f'HOLD_WHEEL_SHAFT_{side}_{x}_GRAPHIC_AXIAL_PACKAGE',shaft,'shaft')
        add(f'KEY_4x4x12_{side}_{x}',key,'shaft')
        add(f'61903_SIDE_{side}_{x}',make_bearing(17,30,7).translate((x,side*42.5,45)),'bearing')
        flange=fuse_all([cyl_y(x,side*38,45,17,10.8,dir=side),cyl_y(x,side*41,45,25,2,dir=side)])
        flange=cut(flange,cyl_y(x,side*37.9,45,9.08,11.2,dir=side))
        flange=cut(flange,cyl_y(x,side*39,45,15,7,dir=side))
        flange=cut(flange,cyl_y(x,side*46,45,11.4,2.8,dir=side))
        add(f'HOLD_AXLE_FLANGE_{side}_{x}_GRAPHIC_CONTOUR',flange,'metal')
        add(f'HOLD_XRING_INSTALLED_{side}_{x}_FREE18p72x2p62',ring_y(x,side*47.4,45,11.4,9,2.8),'seal')
        add(f'HOLD_FLANGE_ORING_32x1p5_{side}_{x}',wp(cq.Solid.makeTorus(16.75,.75,cq.Vector(x,side*40.5,45),cq.Vector(0,1,0))),'seal')
        pts=[(26,-12),(32,-12),(42,-8),(45,0),(42,8),(32,12),(8,12),(8,-2),(26,-2)]
        if side<0:pts=[(r,-yy) for r,yy in pts]
        tyre=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(0,1)).translate((x,side*54.5,45))
        tyre=cut(tyre,key)
        add(f'HOLD_QRW90SR150_WHEEL_{side}_{x}_PHOTO_PROFILE',tyre,'wheel')
        add(f'HOLD_WHEEL_RETENTION_WASHER_{side}_{x}',ring_y(x,side*61.5,45,8,2.7,2),'metal')
        bolt=fuse_all([cyl_y(x,side*51.5,45,2.5,11,dir=side),cyl_y(x,side*62.5,45,4.25,3.5,dir=side)])
        add(f'HOLD_WHEEL_RETENTION_M5_{side}_{x}_QUICKLOCK_UNRESOLVED',bolt,'shaft')
motor_vendor=cq.importers.importStep(str(CAD/'vendor'/'Pololu_25D_75_99_Manufacturer.step'))
motor_vendor=motor_vendor.translate((-30.875,0,-18.375)).rotate((0,0,0),(0,1,0),90)
motor_holder=boxc(197,0,45,3,52.8,30)
pinion_holder=boxc(227,0,45,5,52.8,26)
for side in (-1,1):
    y=side*MOTOR_Y
    z40=wp(cq.Solid.makeCone(20.37,14.3,2.41,cq.Vector(250,side*5.5,45),cq.Vector(0,side,0)))
    z40=cut(z40,cyl_y(250,side*5.4,45,5,3,dir=side))
    z16=wp(cq.Solid.makeCone(8.93,2,6.96,cq.Vector(230,y,45),cq.Vector(1,0,0)))
    z16=cut(z16,cyl_x(229.9,y,45,3,7.2))
    add(f'HOLD_Z40_BEVEL_{side}_CONICAL_ENVELOPE',z40,'bevel');add(f'HOLD_Z16_BEVEL_{side}_CONICAL_ENVELOPE',z16,'bevel')
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
    add(f'POLOLU_5707_MOTOR_{side}_MANUFACTURER_STEP',motor_vendor.translate((MOTOR_FACE,y,45)),'purchased')
    motor_holder=cut(motor_holder,cyl_x(195.4,y,45,3.6,3.2))
    for zz in (36.5,53.5):motor_holder=cut(motor_holder,cyl_x(195.4,y,zz,1.65,3.2))
add('HOLD_PAIRED_MOTOR_HOLDER_25D_ADAPTATION',motor_holder,'metal')
add('HOLD_PAIRED_PINION_BEARING_HOLDER',pinion_holder,'metal')
cover=boxc(SERVICE_CX,0,78.5,SERVICE_L,SERVICE_W,SERVICE_T)
for x in SERVICE_SCREW_X:
    for y in (-19,19):cover=cut(cover,cyl_z(x,y,74.9,2.25,7.2))
cover=cut(cover,cyl_z(264,18,74.9,5.05,7.2))
cover=cut(cover,cyl_z(245,0,74.9,4,7.2))
add('HOLD_PRESSURE_ELECTRONICS_COVER_GRAPHIC158x53x7',cover,'metal')
valve_body=cut(cyl_z(264,18,78,5,14),cyl_z(264,18,77.9,2.1,14.2))
add('HOLD_PRESSURE_VALVE_BODY_SOURCE_FAMILY',valve_body,'valve')
add('HOLD_PRESSURE_VALVE_CAP',cyl_z(264,18,92,6,1.5),'valve')
add('HOLD_PRESSURE_VALVE_4MM_BALL',cq.Workplane('XY').sphere(2).translate((264,18,88)),'valve')
gland_boss=boxc(229,0,88.5,43,22,13)
gland_boss=cut(gland_boss,cyl_x(207.4,0,88.5,6,44))
gland_boss=cut(gland_boss,cyl_z(245,0,74.9,4,14))
add('HOLD_PRESSURE_LIFT_CABLE_BOSS_SOURCE_TOPOLOGY',gland_boss,'metal')
lapp=make_gland().rotate((0,0,0),(0,0,1),180).translate((214,0,88.5))
add('HOLD_LAPP_SKINTOP_53112000_M12x1p5',lapp,'purchased')
th=0.0;lo_end=(40,96);hi_end=(78,110)
for side in (-1,1):
    arm=plate_between((240,96),lo_end,side*ARM_Y,3,15)
    for x in (40,240):arm=cut(arm,cyl_y(x,side*ARM_Y-2,96,4,4))
    add(f'HOLD_LIFT_SIDE_ARM_{side}_GRAPHIC200',arm,'lift')
    for x in (40,240):add(f'HOLD_LIFT_SIDE_PIN_{side}_{x}',cyl_y(x,side*(ARM_Y-1.5),96,4,3,dir=side),'lift')
central=[]
for y in (-12,12):
    arm=plate_between((278,110),hi_end,y,2,12)
    for x in (78,278):arm=cut(arm,cyl_y(x,y-1.1,110,3,2.2))
    central.append(arm)
central.append(boxc(178,0,116,200,26,2))
add('HOLD_LIFT_CENTRAL_LEVER_ASS002723_GRAPHIC200',fuse_all(central),'lift')
carrier=fuse_all([boxc(46,0,95,70,50,5),boxc(13.5,0,81.25,5,50,27.5),boxc(77,0,104,5,26,14)])
carrier=cut(carrier,cyl_x(10.9,0,70,10,5.2))
carrier=cut(carrier,cyl_y(78,-13.1,110,3,26.2))
add('HOLD_LIFT_CAMERA_CARRIER_SOURCE_INTERFACE_UNKNOWN',carrier,'lift')
base=boxc(260,0,88,46,53,12)
for y in (-13.5,13.5):base=cut(base,cyl_x(236.9,y,88,4,46.2))
base=cut(base,gland_boss);add('HOLD_LIFT_BASE_ON_REMOVABLE_PRESSURE_COVER',base,'lift')
body_pt=(235,16,89);moving=(47,16,96);gas_length=math.dist(body_pt,moving);gas_move_s=193
v=(cq.Vector(*moving)-cq.Vector(*body_pt)).normalized();joint=cq.Vector(*body_pt)+v*112
add('HOLD_ACE_GS12_80_V4A_150N_BODY_END_FITTINGS',between(body_pt,joint.toTuple(),6),'purchased')
add('HOLD_ACE_GS12_80_ROD',between(joint.toTuple(),moving,2),'purchased')
hub=cut(cyl_y(240,37,96,8,8),cyl_y(240,36.9,96,4,8.2));lever=boxc(225,41,91,30,6,7)
add('HOLD_M8_MANUAL_CLAMP_LEVER_AND_HANDLE',fuse_all([hub,lever]),'lift')
cam_rear=10;cam_front=cam_rear-132
cam_rear_body=cut(cyl_x(cam_rear-68,0,CAM_Z,31.25,68),cyl_x(cam_rear-67.9,0,CAM_Z,27,63.9))
cam_rear_body=cut(cam_rear_body,cyl_x(cam_rear-4.1,0,CAM_Z,7,4.2))
add('HOLD_CAM026_ROTATE_HOUSING_GRAPHIC_OD62p5',cam_rear_body,'camera')
fork=[boxc(cam_front+31,y,CAM_Z,62,4,46) for y in (-27,27)]
add('HOLD_CAM026_SIDE_FRAME_GRAPHIC',fuse_all(fork),'camera')
optical=cq.Workplane('XY').sphere(25).translate((cam_front+26,0,CAM_Z))
optical=cut(optical,boxc(cam_front-9,0,CAM_Z,20,60,60))
add('HOLD_CAM026_OPTICAL_HOUSING_GRAPHIC',optical,'camera')
add('HOLD_CAM026_FRONT_WINDOW_DIAMETER_UNKNOWN',cyl_x(cam_front-1,0,CAM_Z,12,2),'camera')
sp13=make_sp13_plug().translate((16,0,70));add('HOLD_WEIPU_SP1310_S6I_N_AND_PANEL_INTERFACE',sp13,'connector')
harness_points=[(187.5,0,88.5),(160,0,88.5)]
for i in range(1,25):
    a=math.pi*i/24;harness_points.append((160-27*math.sin(a),27-27*math.cos(a),88.5))
harness_points += [(92,54,88.5),(64,0,70)]
def poly_tube(points,radius):
    return fuse_all([between(a,b,radius) for a,b in zip(points,points[1:]) if math.dist(a,b)>1e-5])
jacket=poly_tube(harness_points,2.7)
for i,name in enumerate(['12V','GND','TX','RX','CVBS_SIGNAL','CVBS_RETURN']):
    core=poly_tube([(x,y,z+(i-2.5)*.65) for x,y,z in harness_points],.22)
    jacket=cut(jacket,core);add(f'CAMERA_HARNESS_CORE_{i+1}_{name}_ROUTE_HOLD',core,'wire')
add('HOLD_LAPP_0028679_CAMERA_HARNESS_6CORE_ROUTE',jacket,'cable')
hguard=cut(between((166,0,88.5),(178,0,88.5),4.5),between((165.9,0,88.5),(178.1,0,88.5),3.2))
hguard=cut(hguard,boxc(172,0,92.5,14,4,5));add('PX1_LIFT_HARNESS_GUARD_OPEN_PROFILE',hguard,'print')
controller=cq.importers.importStep(str(CAD/'vendor'/'WeAct_F4_64Pin_V11_Manufacturer.step'))
controller=wp(cq.Compound.makeCompound(controller.vals()))
b=controller.val().BoundingBox();controller=controller.translate((-(b.xmin+b.xmax)/2,-(b.ymin+b.ymax)/2,-b.zmin))
controller=controller.rotate((0,0,0),(0,0,1),90).translate((208,0,59.5))
add('WEACT_STM32F446RET6_V11_MANUFACTURER_STEP',controller,'electronics')
g2=cq.importers.importStep(str(CAD/'vendor'/'Pololu_G2_24v13_Manufacturer.step')).translate((-16.51,-10.16,0))
for i,x in enumerate((47,99),1):add(f'POLOLU_2992_G2_24v13_{i}_MANUFACTURER_STEP',g2.translate((x,0,26)),'electronics')
add('HOLD_CINCON_CQB150W110S24_BODY_PINS_THERMAL_HOLD',boxc(155,0,64,*CINCON),'electronics')
add('NICHICON_UCS2D221MHD1TN_BODY18x25',cyl_z(278,0,41,9,25),'electronics')
add('ADAFRUIT_MPRLS_3965_ENVELOPE',boxc(277.5,-17.5,60,*MPRLS),'electronics')
add('HOLD_POLOLU_5577_D42V55F12_ENVELOPE',boxc(208,-13.5,29,*POLOLU_5577),'electronics')
add('HOLD_POLOLU_5571_D42V55F5_ENVELOPE',boxc(208,13.5,29,*POLOLU_5571),'electronics')
add('HOLD_WAVESHARE_27479_ISOLATED_RS485_C_ENVELOPE',boxc(264,0,68,*WAVESHARE_27479),'electronics')
add('HOLD_DELTA_TR1D_P2_VIDEO_BALUN',boxc(263,0,31,*VIDEO_SCREEN),'electronics_hold')
body=cut(body,cyl_x(287.9,0,45,8.6,8.2))
add('HOLD_WEIPU_SP1712_7PIN_REAR_PANEL_6_USED',make_sp17_panel().translate((296,0,45)),'connector')
strain=cut(cyl_x(316,0,45,12,32),cyl_x(315.9,0,45,10,32.2))
cone=cq.Workplane('YZ').circle(10).workplane(offset=30).circle(6).loft(combine=True).translate((316,0,45))
cone=cut(cone,cyl_x(315.9,0,45,4.5,32.2))
add('HOLD_REAR_TETHER_STRAIN_SLEEVE',strain,'metal');add('HOLD_REAR_TETHER_ARAMID_CONE',cone,'metal')
add('HOLD_MAIN_TETHER_6CORE_REINFORCED_ARTICLE_UNKNOWN',cyl_x(348,0,45,4.5,80),'cable')
components.insert(0,('HOLD_PRESSURE_BODY_CRP150_GRAPHIC278x68x64_CAVITY_UNRESOLVED',body,'body'))
from release_tools import finish_build
finish_build(globals())
