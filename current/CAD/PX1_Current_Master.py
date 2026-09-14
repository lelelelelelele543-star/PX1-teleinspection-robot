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
BODY_L_SOURCE_SCREEN=307.0
BODY_HALF_W_SCREEN=46.0
BODY_Z0=8.0
BODY_TOP=90.0
PIPE_R=75.0
PIPE_CENTER_Z=52.0480547

# New motor adaptation — exact product envelope where published
MOTOR_OD=36.0; MOTOR_LEN=92.0; MOTOR_SHAFT_D=6.0; MOTOR_SHAFT_L=16.3
MOTOR_FACE=307.3; MOTOR_Y=19.0 # integration datums HOLD; maximum OD36 per linked ISL drawing
COUPLING_OD=20.0; COUPLING_L=24.0; COUPLING_BORE=6.0 # NBK MLR-20C-6-6

# Purchased exact / published component dims
LAPP_OD=17.6; LAPP_CMAX=26.5; LAPP_THREAD_L=6.5; LAPP_SW=16.0
ACE_BODY_OD=12.0; ACE_ROD_OD=4.0; ACE_STROKE=20.0; ACE_EXTENDED=72.0
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
SERVICE_CX=261.0; SERVICE_L=86.0; SERVICE_W=44.0; SERVICE_T=6.0; SERVICE_Z=111.0
SERVICE_OPEN=(48.0,22.0)
SERVICE_SCREW_X=(226.0,296.0)

# Lift kinematics recovered in current project
PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=109.0; LINK_L=90.0
ARM_Y=31.0; ARM_T=4.0; ARM_H=14.0
CAM_Z=75.0; CAM026_MEASURED_BASE_OD=62.5; CAM_R=CAM026_MEASURED_BASE_OD/2; CAM_LEN=78.0

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

def make_wheel_visual():
    # QRW90SR/150 exact OD is source-confirmed; width/tread/hub are not.
    # Use a visibly treaded reference solid, named HOLD; never used for final DN150 PASS.
    width=12.0
    base=cq.Workplane('XZ').circle(45.0).circle(14.0).extrude(width,both=True)
    # central metal hub
    hub=cq.Workplane('XZ').circle(18).circle(8.5).extrude(width-2,both=True)
    p=base.union(hub)
    # tread grooves as shallow boxes around circumference
    for i in range(24):
        a=i*15
        groove=boxc(0,0,45.0,width+2,5,4).rotate((0,0,0),(0,1,0),a)
        p=p.cut(groove)
    return p

def make_motor():
    # Dimensions explicitly printed on the drawing linked by the ISL product page.
    # Rear motor OD36 conflicts with catalog diameter32; sample correspondence remains HOLD.
    gearbox=cyl_x(0,0,0,16,34.9)
    motor=cyl_x(34.9,0,0,18,57.1)
    pilot=cyl_x(-3,0,0,9,3)
    shaft=cyl_x(-16.3,0,0,3,16.3)
    shaft=cut(shaft,box0(-16.3,-4,2.5,12,8,2)) # printed D-flat 5.50 across remaining shaft
    p=fuse_all([gearbox,motor,pilot,shaft])
    for ang in (45,135,225,315):
        y=13*math.cos(math.radians(ang)); z=13*math.sin(math.radians(ang))
        p=cut(p,cyl_x(-.1,y,z,1.5,5.6))
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

def make_gas_spring_extended():
    # exact ACE GS-12-20-V4A main body/rod diameters + extended length envelope.
    body_len=ACE_EXTENDED-ACE_STROKE-10
    body=cyl_x(0,0,0,ACE_BODY_OD/2,body_len)
    rod=cyl_x(body_len,0,0,ACE_ROD_OD/2,ACE_STROKE+10)
    return fuse_all([body,rod])

def make_board(dx,dy,dz,terminal=True,heatsink=False):
    pcb=boxc(0,0,0,dx,dy,1.6)
    parts=[pcb]
    if terminal:
        parts += [boxc(-dx/2+6,0,3.8,9,dy*0.7,6), boxc(dx/2-6,0,3.8,9,dy*0.7,6)]
    if heatsink:
        # base + fins
        parts.append(boxc(0,0,8,dx*0.65,dy*0.65,5))
        for y in [-dy*.24,-dy*.12,0,dy*.12,dy*.24]: parts.append(boxc(0,y,18,dx*.6,2,25))
    return fuse_all(parts)

# ------------------------------- BODY / PRESSURE STRUCTURE
# Proteus-like side profile: current reconstruction screen only.
profile=[(0,10),(300,10),(307,18),(307,66),(291,78),(230,86),(218,110),(205,110),(195,79),(140,31),(0,26)]
outer=cq.Workplane('XZ',origin=(0,BODY_HALF_W_SCREEN,0)).polyline(profile).close().extrude(2*BODY_HALF_W_SCREEN)
# internal dry cavity: offset-like simplified profile; preserve walls 4-8 mm
inner_profile=[(8,15),(298,15),(300,22),(300,61),(286,72),(225,80),(214,102),(210,102),(201,74),(137,25),(8,21)]
inner=cq.Workplane('XZ',origin=(0,38,0)).polyline(inner_profile).close().extrude(76)
body=wp(outer.val().cut(inner.val()))
# rear motor/electronics extension to accommodate real 92 mm motors without separate cassette
rear_outer=cq.Workplane('YZ',origin=(295,0,63)).rect(92,90).workplane(offset=115).rect(84,90).loft(combine=True)
rear_inner=cq.Workplane('YZ',origin=(301,0,63.5)).rect(78,79).workplane(offset=103).rect(76,79).loft(combine=True)
body=wp(body.val().fuse(rear_outer.val()).cut(rear_inner.val()))
# top service opening
service_open=boxc(SERVICE_CX,0,SERVICE_Z-2,SERVICE_OPEN[0],SERVICE_OPEN[1],14)
body=cut(body,service_open)
# rear access opening/cap land
rear_open=boxc(407,0,62,10,62,58)
body=cut(body,rear_open)
# internal longitudinal motor service tunnels; remain within common dry pressure volume
for _y in (-17.0,17.0):
    body=cut(body,cyl_x(280,_y,WHEEL_Z,18.0,124.0))

# Correct source topology: a closed side cover and five gears, with two idle bushings.
# All housing and shoulder coordinates below are inherited/adapted integration dimensions,
# not dimensions extracted by scaling a factory illustration. Every custom part is HOLD.
components=[]; side_housings=[]; side_covers=[]
for side in (-1,1):
    sgn=side
    # Remove obsolete overlapping side-rail solid before rebuilding the same side-drive bay.
    body=cut(body,boxc(150,sgn*44,45,286,24,70))
    discs=[cyl_y(x,sgn*30,WHEEL_Z,31,12,dir=sgn) for x in GEAR_X]
    housing=fuse_all(discs+[boxc(150,sgn*36,45,200,12,54)])
    pockets=[cyl_y(x,sgn*32,WHEEL_Z,27.5,11,dir=sgn) for x in GEAR_X]
    pocket=fuse_all(pockets+[boxc(150,sgn*37.5,45,200,11,48)])
    housing=cut(housing,pocket)
    # Source front support: one 61801 per side, not two at every station.
    housing=cut(housing,cyl_y(50,sgn*26.9,45,10.5,5.2,dir=sgn))
    # Middle shaft support bushing 12-14-4 belongs to DRW-002-375.
    housing=cut(housing,cyl_y(150,sgn*27.9,45,7,4.2,dir=sgn))
    # Rear rotary seal / output path.
    housing=cut(housing,cyl_y(250,sgn*21.9,45,15,10.2,dir=sgn))
    body=wp(body.val().fuse(housing.val()))
    cover_parts=[cyl_y(x,sgn*42,WHEEL_Z,30,4,dir=sgn) for x in GEAR_X]
    cov=fuse_all(cover_parts+[boxc(150,sgn*44,45,200,4,50)])
    # The former bridge 'lightening windows' breached the pressure boundary; removed.
    for x in WHEEL_X: cov=cut(cov,cyl_y(x,sgn*41.9,45,17.05,4.2,dir=sgn))
    side_covers.append((f'HOLD_SIDE_COVER_{side}_GROOVE_CONTOUR_MEASURE',cov))
    components.append((side_covers[-1][0],cov,'metal'))
    for j,x in enumerate(GEAR_X):
        gear=make_spur_gear(50,1,4,12,'Y')
        if j%2: gear=gear.rotate((0,0,0),(0,1,0),180/50)
        components.append((f'HOLD_Z50_{side}_{int(x)}_20DEG_TOOTH_UNCONFIRMED',gear.translate((x,sgn*35,45)),'gear'))
        if x in (100,200):
            components.append((f'IDLE_BUSH_10_12_4_{side}_{int(x)}',ring_y(x,sgn*35,45,6,5,4),'bearing'))
            components.append((f'HOLD_IDLE_PIN_{side}_{int(x)}',cyl_y(x,sgn*28,45,5,10,dir=sgn),'shaft'))
    components.append((f'61801_SIDE_{side}_50_SOURCE_ONE_PER_SIDE',make_bearing(12,21,5,'Y').translate((50,sgn*29.5,45)),'bearing'))
    components.append((f'MIDDLE_BUSH_12_14_4_{side}',ring_y(150,sgn*30,45,7,6,4),'bearing'))
    for x in WHEEL_X:
        # Shoulder positions remain H02; exact journal diameters are distinguished from positions.
        seg=[cyl_y(x,sgn*24,45,6,20,dir=sgn),cyl_y(x,sgn*44,45,8.5,7.5,dir=sgn),
             cyl_y(x,sgn*51.5,45,9,3.8,dir=sgn),cyl_y(x,sgn*55.3,45,8.5,14.7,dir=sgn)]
        shaft=fuse_all(seg)
        # Positive wheel drive and captive bolt bore; exact wheel lock remains H01.
        key=boxc(x,sgn*62,45+7.5,4,12,4)
        shaft=cut(shaft,key); shaft=cut(shaft,cyl_y(x,sgn*60,45,2.5,10.5,dir=sgn))
        components.append((f'HOLD_WHEEL_SHAFT_{side}_{int(x)}',shaft,'shaft'))
        components.append((f'KEY_4x4x12_{side}_{int(x)}',key,'shaft'))
        bearing=make_bearing(17,30,7,'Y').translate((x,sgn*48,45))
        flange=cyl_y(x,sgn*42,45,17,13.3,dir=sgn)
        flange=cut(flange,cyl_y(x,sgn*41.9,45,9.08,13.6,dir=sgn))
        flange=cut(flange,cyl_y(x,sgn*44.5,45,15,7,dir=sgn))
        flange=cut(flange,cyl_y(x,sgn*52,45,11.4,2.8,dir=sgn))
        # Nominal assembled gland volume, not invented elastomer deformation.
        xr=ring_y(x,sgn*53.4,45,11.4,9,2.8)
        components.extend([(f'61903_SIDE_{side}_{int(x)}',bearing,'bearing'),
          (f'HOLD_AXLE_FLANGE_{side}_{int(x)}',flange,'metal'),
          (f'HOLD_XRING_INSTALLED_{side}_{int(x)}_FREE18p72x2p62',xr,'seal'),
          (f'HOLD_QRW90SR150_WHEEL_{side}_{int(x)}_WIDTH_PROFILE_UNKNOWN',make_wheel_visual().translate((x,sgn*59,45)),'wheel')])
        washer=ring_y(x,sgn*71,45,10,3.2,2)
        bolt=cyl_y(x,sgn*61,45,3,10,dir=sgn)
        components.append((f'HOLD_WHEEL_RETENTION_WASHER_{side}_{int(x)}',washer,'metal'))
        components.append((f'HOLD_WHEEL_RETENTION_M6_{side}_{int(x)}',bolt,'shaft'))
        # Flange static seal: nominal source size; detailed installed groove H03.
        tor=cq.Solid.makeTorus(16.75,.75,cq.Vector(x,sgn*43,45),cq.Vector(0,1,0))
        components.append((f'HOLD_FLANGE_ORING_32x1p5_{side}_{int(x)}',wp(tor),'seal'))

# Correct 90-degree bevel orientation. Tooth and mounting-distance data are still H04.
# Conical envelopes replace the incorrect spur-tooth representations.
for side in (-1,1):
    y=side*MOTOR_Y
    # The two pitch cones share an apex at (250,+/-19,45).
    z40=wp(cq.Solid.makeCone(20.37,14.3,2.41,cq.Vector(250,side*11,45),cq.Vector(0,side,0)))
    z40=cut(z40,cyl_y(250,side*10.9,45,5,3,dir=side))
    z16=wp(cq.Solid.makeCone(2.0,8.93,6.96,cq.Vector(263.04,y,45),cq.Vector(1,0,0)))
    z16=cut(z16,cyl_x(262.9,y,45,3,7.5))
    axle=fuse_all([cyl_y(250,side*5.5,45,5,14.5,dir=side),cyl_y(250,side*20,45,9,12,dir=side)])
    axle=cut(axle,cyl_y(250,side*24,45,6,8.1,dir=side))
    components.extend([(f'HOLD_Z40_BEVEL_{side}_CONICAL_ENVELOPE',z40,'bevel'),(f'HOLD_Z16_BEVEL_{side}_CONICAL_ENVELOPE',z16,'bevel'),
      (f'HOLD_Z40_OUTPUT_SHAFT_{side}_KEYED_SOCKET_UNRESOLVED',axle,'shaft'),
      (f'61800_Z40_{side}',make_bearing(10,19,5,'Y').translate((250,side*8,45)),'bearing'),
      (f'SHAFT_SEAL_Z40_{side}_18x30x7',make_seal(18,30,7,'Y').translate((250,side*25.5,45)),'seal')])
    shaft=fuse_all([cyl_x(263,y,45,3,9.5),cyl_x(272.5,y,45,6,5),cyl_x(277.5,y,45,3,13)])
    components.extend([(f'HOLD_Z16_SHAFT_{side}',shaft,'shaft'),
      (f'61801_Z16_SUPPORT_{side}',make_bearing(12,21,5,'X').translate((275,y,45)),'bearing'),
      (f'HOLD_NBK_MLR20C_6_6_COUPLING_{side}_EXTERNAL_DETAIL',make_coupling().translate((278.5,y,45)),'purchased'),
      (f'HOLD_ISL_PGM32P_MOTOR_{side}_DRAWING_OD36_CATALOG_OD32',make_motor().translate((MOTOR_FACE,y,45)),'purchased')])

# One conventional paired motor mounting plate, with published four-hole pattern per motor.
motor_holder=boxc(MOTOR_FACE-1.5,0,45,3,76,44)
for side in (-1,1):
    motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-3.1,side*MOTOR_Y,45,9.1,3.2))
    for a in (45,135,225,315):
        yy=side*MOTOR_Y+13*math.cos(math.radians(a));zz=45+13*math.sin(math.radians(a))
        motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-3.1,yy,zz,1.65,3.2))
components.append(('HOLD_PAIRED_MOTOR_HOLDER_OD36_ADAPTATION',motor_holder,'metal'))

# Restore the electronic pockets already present in the earlier current master.
pod=box0(218,-39,84,89,78,27)
pod_cavity=box0(222,-35.5,86,81,71,22)
rear_pod=box0(300,-30,65,110,60,52)
rear_pod_cavity=box0(304,-26,69,104,52,45)
body=wp(body.val().fuse(pod.val()).fuse(rear_pod.val()))
body=cut(body,pod_cavity);body=cut(body,rear_pod_cavity)
body=cut(body,box0(230,-30,72,62,60,18))
body=cut(body,box0(218,-33,84,81,66,18))
body=cut(body,box0(242,-34,17,61,68,66))
body=cut(body,service_open)
body=cut(body,box0(404,-38,26,12,76,78))
body=cut(body,box0(404,-26,104,12,52,10))
for yy in (-MOTOR_Y,MOTOR_Y): body=cut(body,cyl_x(280,yy,45,18.3,124))
# Complete the missing mating holes in the inherited CAD. Coordinates remain H02.
for side in (-1,1):
    for x in (100,200): body=cut(body,cyl_y(x,side*27.9,45,5,10.2,dir=side))
    body=cut(body,cyl_y(150,side*23.9,45,6,8.2,dir=side))
    body=cut(body,cyl_y(150,side*27.9,45,7,4.2,dir=side))
body=cut(body,motor_holder) # provisional shared motor-plate seat; fastening/land H05
components.insert(0,('HOLD_PRESSURE_BODY_INHERITED_SCREEN_NOT_FACTORY_DIMENSIONS',body,'body'))

# ------------------------------- LIFT / CAMERA
# low position parallelogram, camera held upright
PAVG=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2
cam_axis_target_z=CAM_Z
# solve approximate link angle from average pivot to carrier center
th=math.asin((cam_axis_target_z-PAVG)/LINK_L)
dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
lo_end=(PIVOT_X+dx,PIVOT_Z_LOW+dz); hi_end=(PIVOT_X+dx,PIVOT_Z_HIGH+dz)
for side in (-1,1):
    for name,z0,end in [('LOWER',PIVOT_Z_LOW,lo_end),('UPPER',PIVOT_Z_HIGH,hi_end)]:
        arm=plate_between((PIVOT_X,z0),end,side*ARM_Y)
        for xx,zz in [(PIVOT_X,z0),end]: arm=cut(arm,cyl_y(xx,side*ARM_Y-3,zz,5,6))
        components.append((f'LIFT_{name}_ARM_{side}_PROTOTYPE_RECONSTRUCTED',arm,'lift'))
    # pivot bosses
    for x,z in [(PIVOT_X,PIVOT_Z_LOW),(PIVOT_X,PIVOT_Z_HIGH),lo_end,hi_end]:
        components.append((f'LIFT_PIVOT_BOSS_{side}_{int(x)}_{int(z)}',cyl_y(x,side*(ARM_Y-2),z,5,8,dir=1 if side>0 else -1),'lift'))
carrier_x=(lo_end[0]+hi_end[0])/2; carrier_z=(lo_end[1]+hi_end[1])/2
carrier=boxc(carrier_x,0,carrier_z,16,58,26)
carrier=cut(carrier,cyl_x(carrier_x-9,0,93,11.5,18))
components.append(('LIFT_CAMERA_CARRIER_PROTOTYPE',carrier,'lift'))
# camera shell: CAM026-derived reference architecture. User photo with caliper gives ~62.5 mm base OD.
# Other camera dimensions require H08 measurement; this is an inherited envelope, not CAM026 CAD.
cam_x=carrier_x-8-CAM_LEN/2 # rear mounting face meets the carrier; previous offset buried it in the shell
shell=cyl_x(cam_x-CAM_LEN/2,0,CAM_Z,CAM_R,CAM_LEN)
inner_cam=cyl_x(cam_x-CAM_LEN/2+4,0,CAM_Z,CAM_R-4,CAM_LEN-8)
shell=cut(shell,inner_cam)
front_ring=cq.Workplane('YZ').circle(CAM_R-2.5).circle(16).extrude(5).translate((cam_x-CAM_LEN/2,0,CAM_Z))
lens=cyl_x(cam_x-CAM_LEN/2-2,0,CAM_Z,12,4)
back_ring=cq.Workplane('YZ').circle(CAM_R-2.0).circle(CAM_R-7.0).extrude(5).translate((cam_x+CAM_LEN/2-5,0,CAM_Z))
cam=fuse_all([shell,front_ring,lens,back_ring])
# six LED bosses around lens
for i in range(6):
    a=math.radians(i*60); yy=20*math.cos(a); zz=CAM_Z+20*math.sin(a)
    cam=wp(cam.val().fuse(cyl_x(cam_x-CAM_LEN/2-3,yy,zz,2.5,3).val()))
components.append(('CAMERA_SEALED_HOUSING_CAM026_DERIVED_OD62p5_APPROX_OTHER_DIMS_HOLD',cam,'camera'))
# CAM026 disassembly evidence: hollow central rotor, internal ring gear, thrust bearing and multi-stage reduction.
# Geometry below is a packaging/reference reconstruction only; all internal dimensions remain HOLD.
rotor_tube=cq.Workplane('YZ').circle(11).circle(6).extrude(18).translate((cam_x-4,0,CAM_Z))
ring_gear=cq.Workplane('YZ').circle(27.5).circle(23.5).extrude(5).translate((cam_x+8,0,CAM_Z))
thrust_race1=cq.Workplane('YZ').circle(23).circle(10).extrude(1.0).translate((cam_x+3,0,CAM_Z))
thrust_rollers=cq.Workplane('YZ').circle(21.5).circle(11.5).extrude(1.4).translate((cam_x+4.1,0,CAM_Z))
thrust_race2=cq.Workplane('YZ').circle(23).circle(10).extrude(1.0).translate((cam_x+5.6,0,CAM_Z))
pinion=cyl_x(cam_x+8,18,CAM_Z,4.2,5)
cam_motor=cyl_x(cam_x-8,-17,CAM_Z-8,7.5,28)
compound1=cyl_x(cam_x+1,-10,CAM_Z-7,7.0,4)
compound2=cyl_x(cam_x+5,1,CAM_Z-8,5.0,4)
components += [
 ('CAM026_REFERENCE_HOLLOW_CENTRAL_ROTOR_HOLD',rotor_tube,'camera'),
 ('CAM026_REFERENCE_INTERNAL_RING_GEAR_HOLD',ring_gear,'gear'),
 ('CAM026_REFERENCE_THRUST_BEARING_RACE_A_HOLD',thrust_race1,'bearing'),
 ('CAM026_REFERENCE_THRUST_BEARING_ROLLER_PACK_HOLD',thrust_rollers,'bearing'),
 ('CAM026_REFERENCE_THRUST_BEARING_RACE_B_HOLD',thrust_race2,'bearing'),
 ('CAM026_REFERENCE_FINAL_PINION_HOLD',pinion,'gear'),
 ('CAM026_REFERENCE_PAN_MOTOR_ENVELOPE_HOLD',cam_motor,'purchased'),
 ('CAM026_REFERENCE_COMPOUND_GEAR_STAGE_1_HOLD',compound1,'gear'),
 ('CAM026_REFERENCE_COMPOUND_GEAR_STAGE_2_HOLD',compound2,'gear'),
]
sp13=make_sp13_plug().translate((cam_x+CAM_LEN/2+2,0,93))
components.append(('HOLD_WEIPU_SP13_6PIN_CAMERA_CONNECTOR',sp13,'connector'))

# Gas spring has rigid body length; only the exposed rod changes, never uniform scaling.
body_pt=(194.0,16.0,82.9);move_s=63.0
moving=(PIVOT_X-move_s*math.cos(th),16.0,PIVOT_Z_LOW+move_s*math.sin(th))
v=cq.Vector(*moving)-cq.Vector(*body_pt);gas_length=v.Length
gas_body_length=ACE_EXTENDED-ACE_STROKE
joint=cq.Vector(*body_pt)+v.normalized()*gas_body_length
gas=between(body_pt,joint.toTuple(),ACE_BODY_OD/2)
rod=between(joint.toTuple(),moving,ACE_ROD_OD/2)
components.extend([('HOLD_ACE_GS12_20_V4A_150N_BODY_END_FITTINGS',gas,'purchased'),('HOLD_ACE_GS12_ROD',rod,'purchased')])
# clamping lever visual
lever_hub=cyl_y(PIVOT_X,37,PIVOT_Z_HIGH,8,8)
lever_arm=boxc(PIVOT_X+18,41,PIVOT_Z_HIGH+10,36,6,7).rotate((PIVOT_X,41,PIVOT_Z_HIGH),(PIVOT_X,42,PIVOT_Z_HIGH),-25)
components += [('M8_MANUAL_CLAMP_LEVER_AND_HANDLE',fuse_all([lever_hub,lever_arm]),'lift')]

# ------------------------------- SERVICE COVER / VALVE / GLAND / HARNESS
cover=boxc(SERVICE_CX,0,SERVICE_Z+SERVICE_T/2,SERVICE_L,SERVICE_W,SERVICE_T)
# R3 visual corner rounding where feasible
try: cover=cover.edges('|Z').fillet(3)
except: pass
# screw holes and provisional seal groove visible on underside
for x in SERVICE_SCREW_X:
    cover=cut(cover,cyl_z(x,0,SERVICE_Z-1,2.25,SERVICE_T+2))
cover=cut(cover,cyl_z(273,0,SERVICE_Z-1,5.05,SERVICE_T+2))
# service cover is PX1-engineered, groove remains hold
components.append(('PRESSURE_CAMERA_SERVICE_COVER_86x44x6_PROTOTYPE_SEAL_GROOVE_HOLD',cover,'metal'))
# compact source-family valve cartridge: dimensions are prototype, explicitly test-hold
valve_body=cyl_z(273,0,SERVICE_Z-12,5,14)
valve_cap=cyl_z(273,0,SERVICE_Z+SERVICE_T,6,1.5)
valve_ball=cq.Workplane('XY').sphere(2).translate((273,0,SERVICE_Z-3))
components += [('HOLD_PRESSURE_VALVE_BODY_SOURCE_FAMILY',valve_body,'valve'),('PRESSURE_VALVE_CAP_PROTOTYPE',valve_cap,'valve'),('PRESSURE_VALVE_4MM_BALL',valve_ball,'valve')]
# LAPP gland on side boss, axis X
lapp=make_gland().rotate((0,0,0),(0,0,1),180).translate((215,12,103))
components.append(('LAPP_SKINTOP_53112000_M12x1p5',lapp,'purchased'))
# Continuous six-core service route, ending at the gland and at the SP13 backshell.
# Route and jacket OD are integration-only until actual cable bend radius is supplied.
harness_points=[(188.5,12,103),(182,20,101),(166,20,101),(cam_x+CAM_LEN/2+50,0,93)]
def poly_tube(points, radius):
    parts=[between(a,b,radius) for a,b in zip(points,points[1:])]
    parts += [cq.Workplane('XY').sphere(radius).translate(v) for v in points[1:-1]]
    return fuse_all(parts)
jacket=poly_tube(harness_points,2.7) # LAPP 0028679 nominal OD5.4; radius of route still H07
cores=[]
for i,(name,a) in enumerate(zip(['12V','GND','TX','RX','CVBS_SIGNAL','CVBS_RETURN'],range(0,360,60))):
    yy=1.8*math.cos(math.radians(a));zz=1.8*math.sin(math.radians(a))
    core=poly_tube([(x,y+yy,z+zz) for x,y,z in harness_points],.35) # conductor display only; insulation dimensions unknown
    cores.append(core);jacket=cut(jacket,core)
    components.append((f'CAMERA_HARNESS_CORE_{i+1}_{name}_ROUTE_HOLD',core,'wire'))
components.append(('HOLD_LAPP_0028679_CAMERA_HARNESS_6CORE_R27_UNRESOLVED',jacket,'cable'))
hguard=between(harness_points[1],harness_points[2],5)
hguard=cut(hguard,between(harness_points[1],harness_points[2],3.6))
hguard=cut(hguard,boxc(174,20,106,22,4,8))
components.append(('PX1_LIFT_HARNESS_GUARD_OPEN_PROFILE',hguard,'print'))

# ------------------------------- REAR CONNECTOR / TETHER STRAIN RELIEF
rear_panel=make_sp17_panel().translate((416,0,62))
components.append(('WEIPU_SP1712_7PIN_REAR_PANEL_6_USED_1_SPARE',rear_panel,'connector'))
# mechanical Kevlar termination eye and strain sleeve are separate from contacts
strain=cut(cyl_x(436,0,62,12,32),cyl_x(435.9,0,62,10,32.2))
cone=cq.Workplane('YZ').circle(10).workplane(offset=30).circle(6).loft(combine=True).translate((436,0,62))
cone=cut(cone,cyl_x(435.9,0,62,4.5,32.2))
components += [('HOLD_REAR_TETHER_STRAIN_SLEEVE',strain,'metal'),('HOLD_REAR_TETHER_ARАMID_CONE',cone,'metal')]
# main tether visual, exact article HOLD
tether=cyl_x(468,0,62,4.5,80)
components.append(('HOLD_MAIN_TETHER_6CORE_REINFORCED_ARTICLE_ТРЕБУЕТСЯ_ВЫБОР',tether,'cable'))

# ------------------------------- INTERNAL ELECTRONICS
# Real published outer dimensions when known, otherwise explicitly module-envelope HOLD.
nucleo=boxc(260,0,92,*NUCLEO);components.append(('HOLD_NUCLEO_F446RE_PCB82p5x70_HEIGHT12_UNCONFIRMED',nucleo,'electronics'))
cincon=boxc(261,0,78,*CINCON);components.append(('HOLD_CINCON_CQB150W110S24_BODY_ONLY_PINS_MISSING',cincon,'electronics'))
cap=cyl_x(211.5,20,31,9,25);components.append(('NICHICON_UCS2D221MHD1TN_BODY18x25',cap,'electronics'))
prs=boxc(210,0,70,*MPRLS);components.append(('ADAFRUIT_MPRLS_3965_ENVELOPE',prs,'electronics'))
for i,x in enumerate((330,382),1): components.append((f'HOLD_BTS7960_IBT2_{i}_50x50x43',boxc(x,0,92.5,50,50,43),'electronics_hold'))
components.append(('HOLD_POLOLU_5577_D42V55F12_ENVELOPE',boxc(215,0,48,*POLOLU_5577),'electronics'))
components.append(('HOLD_POLOLU_5571_D42V55F5_ENVELOPE',boxc(291,0,59,*POLOLU_5571),'electronics'))
components.append(('HOLD_WAVESHARE_27479_ISOLATED_RS485_C_ENVELOPE',boxc(263,0,23,*WAVESHARE_27479),'electronics'))
components.append(('HOLD_DELTA_TR1D_P2_VIDEO_BALUN',boxc(205,-20,42,*VIDEO_SCREEN),'electronics_hold'))

# ------------------------------- rear cover
rear_cover=fuse_all([boxc(413,0,63,6,84,90),boxc(413,0,112.5,6,60,9)])
# connector clearance through cover
rear_cover=cut(rear_cover,cyl_x(409.9,0,62,13,6.2))
try: rear_cover=rear_cover.edges('|X').fillet(3)
except: pass
components.append(('REAR_SERVICE_COVER_PROTOTYPE_SEAL_GROOVE_HOLD',rear_cover,'metal'))

# Retire fictitious CAM026 internals from the old master. Photos establish topology,
# not dimensions; omitted internals are explicitly listed as unmodelled in H08/BOM.
components=[(n,p,c) for n,p,c in components if not n.startswith('CAM026_REFERENCE_')]
# Correct local pressure-cover and gland mating cuts without claiming a sealing release.
body=cut(body,cover)
body=cut(body,cyl_x(208.4,12,103,6,7))
body=cut(body,cyl_x(184,12,103,9.3,24.4))
components[0]=(components[0][0],body,'body')


# Apply one unambiguous release policy to legacy prototype names.
components=[((n if ('HOLD' in n or c in ('bearing','wire','print') or n.startswith(('KEY_','NICHICON_','ADAFRUIT_','SHAFT_SEAL_'))) else 'HOLD_'+n),p,c) for n,p,c in components]
from release_tools import finish_build
finish_build(globals())
