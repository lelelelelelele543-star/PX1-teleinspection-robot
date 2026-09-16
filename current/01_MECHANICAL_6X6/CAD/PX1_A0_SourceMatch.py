from pathlib import Path
import math, json
import cadquery as cq
from cadquery import exporters

OUT=Path(__file__).resolve().parent

# PX1 Rev.A A0 source-match drivetrain fixture
# Coordinate system follows current master: X front->rear, Y left/right, Z up.
# This is a drivetrain qualification fixture, NOT a pressure-body manufacturing release.

# Frozen crawler datums
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
Z_AXIS=45.0
Z50_N=50; M=1.0; Z50_PD=50.0; Z50_OD=52.0; Z50_FACE=4.0
Z16=16; Z40=40
MOTOR_Y=(-13.5,13.5)       # source drawing / current reconstructed pack centres
BEVEL_APEX_X=250.0

# Source-match motor/gearhead envelope.
# 2250 S 024 BX4 + 26/1 S, three-stage 66:1 candidate.
MOTOR_D=22.0; MOTOR_L=51.8
GH_D=26.0; GH_L=44.4
GH_SHAFT_D=5.0; GH_SHAFT_L=12.0
GH_PILOT_D=13.0; GH_BCD=20.0; GH_MOUNT_D=3.0
PACK_FACE_X=210.0             # front mounting face of 26/1S in A0 fixture
PACK_REAR_X=PACK_FACE_X-GH_L-MOTOR_L

# Pinion support from original ASS-002-386 concept
B61801_ID=12.0; B61801_OD=21.0; B61801_W=5.0
PINION_BEAR_X=227.0
PINION_SOCKET_START=214.0
PINION_SOCKET_END=222.0
PINION_NOSE_END=238.0

# Standard m1, 16/40, 90deg reference pitch geometry.
# Teeth remain source/purchased-part gated; these cones are mounting envelopes only.
DELTA1=math.atan(Z16/Z40)
DELTA2=math.pi/2-DELTA1
CONE_R=0.5*M*math.sqrt(Z16**2+Z40**2)
FACE=6.0
SMALL_OUTER_AXIAL=CONE_R*math.cos(DELTA1)  # 20.0 mm
BIG_OUTER_AXIAL=CONE_R*math.cos(DELTA2)    # 8.0 mm
SMALL_BACK_X=BEVEL_APEX_X-SMALL_OUTER_AXIAL

# A0 gear-train fixture: preserves pitch centres. Two 8mm plates around 4mm gears.
PLATE_T=8.0
GEAR_PLANE_Y=0.0
PLATE_Y=( -8.0, 8.0 )
PLATE_X0=20.0; PLATE_L=260.0; PLATE_Z0=8.0; PLATE_H=74.0
A0_SHAFT_D=12.0
A0_BEARING_OD=28.0   # generic 6001-2RS, bench-only support
A0_BEARING_ID=12.0
A0_BEARING_W=8.0


def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x(x,y,z,r,l,dir=1):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(dir,0,0)))
def cyl_y(x,y,z,r,l,dir=1):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,dir,0)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)

def bearing_y(x,y,z,id_,od,w):
    p=cq.Workplane('XZ').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    return p.translate((x,y,z))

def bearing_x(x,y,z,id_,od,w):
    p=cq.Workplane('YZ').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    return p.translate((x,y,z))

def make_spur_test_gear(teeth=50,module=1.0,face=4.0,bore=12.0,pressure_angle_deg=20.0):
    # A0 printable involute test gear. PA20 is a reference assumption, not OEM tooth release.
    rp=module*teeth/2; ra=rp+module; rf=max(module*0.2,rp-1.25*module)
    alpha=math.radians(pressure_angle_deg); rb=rp*math.cos(alpha)
    def invol(r):
        if r <= rb: return 0.0
        x=math.sqrt(max(0.0,(r/rb)**2-1.0))
        return x-math.acos(min(1.0,rb/r))
    half=math.pi/(2*teeth)+math.tan(alpha)-alpha
    pts=[]
    root_to_base=max(rf,rb)
    radii=[root_to_base+(ra-root_to_base)*j/9 for j in range(10)]
    for i in range(teeth):
        a=i*2*math.pi/teeth
        pts.append((rf*math.cos(a-half),rf*math.sin(a-half)))
        for r in radii:
            t=a-half+invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        for r in reversed(radii):
            t=a+half-invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        pts.append((rf*math.cos(a+half),rf*math.sin(a+half)))
    clean=[]
    for pt in pts:
        if not clean or math.dist(pt,clean[-1])>1e-7: clean.append(pt)
    # Build in XZ plane so axis is Y, matching crawler side train.
    g=cq.Workplane('XZ').polyline(clean).close().extrude(face/2,both=True)
    g=g.cut(cq.Workplane('XZ').circle(bore/2).extrude(face,both=True))
    return g

def spur_envelope(x,y,z):
    return make_spur_test_gear(Z50_N,M,Z50_FACE,A0_SHAFT_D,20.0).translate((x,y,z))

def source_motor_pack(y):
    # Axis along X, output toward +X.
    gh=cyl_x(PACK_FACE_X-GH_L,y,Z_AXIS,GH_D/2,GH_L)
    # front pilot, 2 mm representative mounting pilot envelope
    pilot=cyl_x(PACK_FACE_X,y,Z_AXIS,GH_PILOT_D/2,2.0)
    shaft=cyl_x(PACK_FACE_X,y,Z_AXIS,GH_SHAFT_D/2,GH_SHAFT_L)
    mot=cyl_x(PACK_REAR_X,y,Z_AXIS,MOTOR_D/2,MOTOR_L)
    # rear connector nub is intentionally omitted: not a collision-driving envelope for A0.
    return fuse([gh,pilot,shaft,mot])

def pinion_axle(y):
    # Bench/source-like adapter: 12mm bearing journal with 5mm rear socket.
    p=cyl_x(PINION_SOCKET_START,y,Z_AXIS,6.0,PINION_NOSE_END-PINION_SOCKET_START)
    socket=cyl_x(PINION_SOCKET_START-0.1,y,Z_AXIS,GH_SHAFT_D/2+0.03,PINION_SOCKET_END-PINION_SOCKET_START+0.2)
    p=cut(p,socket)
    # Two opposed M3 pinch screw clearance holes in the socket section (bench-only adapter).
    for xx in (217.0,220.0):
        h=cq.Workplane('XY').circle(1.6).extrude(7,both=True).translate((xx,y,Z_AXIS))
        p=cut(p,h)
    return p

def z16_envelope(y):
    # Reference cone frustum, back at x=230, narrows toward pitch apex.
    outer_r=0.5*(M*(Z16+2))
    inner_cone_dist=max(0.1,CONE_R-FACE)
    inner_r=outer_r*(inner_cone_dist/CONE_R)
    axial_face=FACE*math.cos(DELTA1)
    s=wp(cq.Solid.makeCone(outer_r,inner_r,axial_face,cq.Vector(SMALL_BACK_X,y,Z_AXIS),cq.Vector(1,0,0)))
    bore=cyl_x(SMALL_BACK_X-0.1,y,Z_AXIS,4.0,axial_face+0.2)
    return cut(s,bore)

def z40_envelope(side):
    y_apex=side*13.5
    # Outer back plane points inward from apex by ~8mm, gear face extends toward apex.
    y_back=y_apex-side*BIG_OUTER_AXIAL
    outer_r=0.5*(M*(Z40+2))
    inner_cone_dist=max(0.1,CONE_R-FACE)
    inner_r=outer_r*(inner_cone_dist/CONE_R)
    axial_face=FACE*math.cos(DELTA2)
    s=wp(cq.Solid.makeCone(outer_r,inner_r,axial_face,cq.Vector(BEVEL_APEX_X,y_back,Z_AXIS),cq.Vector(0,side,0)))
    bore=cyl_y(BEVEL_APEX_X,y_back-side*0.1,Z_AXIS,5.0,axial_face+0.2,dir=side)
    return cut(s,bore)

def motor_holder():
    # Two-piece A0 holder. Rear plate locates 26/1S pilot and M3/20mm BCD.
    rear=boxc(PACK_FACE_X-3.0,0,Z_AXIS,6.0,58.0,38.0)
    for y in MOTOR_Y:
        rear=cut(rear,cyl_x(PACK_FACE_X-6.1,y,Z_AXIS,GH_PILOT_D/2+0.05,6.2))
        for a in (45,135,225,315):
            yy=y+(GH_BCD/2)*math.cos(math.radians(a))
            zz=Z_AXIS+(GH_BCD/2)*math.sin(math.radians(a))
            rear=cut(rear,cyl_x(PACK_FACE_X-6.1,yy,zz,GH_MOUNT_D/2+0.15,6.2))
    # Front plate supports 61801 bearings for pinion axles.
    front=boxc(PINION_BEAR_X,0,Z_AXIS,7.0,58.0,38.0)
    for y in MOTOR_Y:
        front=cut(front,cyl_x(PINION_BEAR_X-3.6,y,Z_AXIS,B61801_OD/2+0.02,7.2))
    # top/bottom bridges; open central sides for assembly and visual access.
    bridge_top=boxc((PACK_FACE_X+PINION_BEAR_X)/2,0,Z_AXIS+18.0,PINION_BEAR_X-PACK_FACE_X,58.0,4.0)
    bridge_bot=boxc((PACK_FACE_X+PINION_BEAR_X)/2,0,Z_AXIS-18.0,PINION_BEAR_X-PACK_FACE_X,58.0,4.0)
    return fuse([rear,front,bridge_top,bridge_bot])

def side_fixture_plate(y):
    plate=boxc((PLATE_X0+PLATE_L/2),y,(PLATE_Z0+PLATE_H/2),PLATE_L,PLATE_T,PLATE_H)
    # Large windows lighten print/machining without touching bearing bosses.
    for x in (75,125,175,225):
        plate=cut(plate,boxc(x,y,45,32,PLATE_T+1,38))
    for x in GEAR_X:
        plate=cut(plate,cyl_y(x,y-PLATE_T/2-0.1,Z_AXIS,A0_BEARING_OD/2+0.05,PLATE_T+0.2))
        # four M4 fixture holes around each bearing for optional retainers
        for dx,dz in ((-18,-18),(-18,18),(18,-18),(18,18)):
            plate=cut(plate,cyl_y(x+dx,y-PLATE_T/2-0.1,Z_AXIS+dz,2.1,PLATE_T+0.2))
    # feet / bench mounting slots at ends
    for x in (35,265):
        for z in (16,74):
            plate=cut(plate,cyl_y(x,y-PLATE_T/2-0.1,z,2.6,PLATE_T+0.2))
    return plate

# Build A0 fixture / source-match study.
parts=[]
def add(name,shape): parts.append((name,shape)); return shape

# Gear train fixture centered around y=0 for one-side transmission proving.
for y in PLATE_Y:
    add(f'A0_FIXTURE_PLATE_Y{y:+g}',side_fixture_plate(y))
for x in GEAR_X:
    add(f'A0_Z50_ENVELOPE_X{x:g}',spur_envelope(x,GEAR_PLANE_Y,Z_AXIS))
    add(f'A0_6001_BEARING_L_X{x:g}',bearing_y(x,-8,Z_AXIS,A0_BEARING_ID,A0_BEARING_OD,A0_BEARING_W))
    add(f'A0_6001_BEARING_R_X{x:g}',bearing_y(x,8,Z_AXIS,A0_BEARING_ID,A0_BEARING_OD,A0_BEARING_W))
    add(f'A0_SHAFT_X{x:g}',cyl_y(x,-12,Z_AXIS,A0_SHAFT_D/2,24))

# Source-match two-motor module studied at real crawler rear input datums.
holder=add('A0_SOURCE_MATCH_MOTOR_HOLDER',motor_holder())
for side,y in ((-1,-13.5),(1,13.5)):
    add(f'FAULHABER_2250S024BX4_26_1S66_ENVELOPE_{side:+d}',source_motor_pack(y))
    add(f'A0_PINION_AXLE_5MM_SOCKET_61801_{side:+d}',pinion_axle(y))
    add(f'61801_PINION_SUPPORT_{side:+d}',bearing_x(PINION_BEAR_X,y,Z_AXIS,B61801_ID,B61801_OD,B61801_W))
    add(f'Z16_M1_REFERENCE_ENVELOPE_{side:+d}',z16_envelope(y))
    add(f'Z40_M1_REFERENCE_ENVELOPE_{side:+d}',z40_envelope(side))

# Keepout rails representing the closest allowable inward end of side-drive shaft packages.
# |Y| >= 28 mm leaves ~1.5 mm to Ø26 gearhead envelope at ±13.5 centres.
for side in (-1,1):
    add(f'SIDE_DRIVE_INNER_KEEPOUT_{side:+d}',boxc(165,side*30.5,Z_AXIS,230,5.0,22))

# Export compounds while keeping parts separate in STEP.
compound=cq.Compound.makeCompound([p.val() for _,p in parts])
exporters.export(compound,str(OUT/'PX1_A0_SourceMatch_Assembly.step'))
exporters.export(holder,str(OUT/'PX1_A0_SourceMatch_MotorHolder.step'))
for idx,y in enumerate(PLATE_Y,1):
    plate=side_fixture_plate(y)
    exporters.export(plate,str(OUT/f'PX1_A0_SideFixturePlate_{idx}.step'))
    exporters.export(plate,str(OUT/f'PX1_A0_SideFixturePlate_{idx}.stl'),tolerance=0.08,angularTolerance=0.15)
printgear=make_spur_test_gear(Z50_N,M,Z50_FACE,A0_SHAFT_D,20.0)
exporters.export(printgear,str(OUT/'PX1_A0_Z50_m1_PA20_TEST.step'))
exporters.export(printgear,str(OUT/'PX1_A0_Z50_m1_PA20_TEST.stl'),tolerance=0.04,angularTolerance=0.10)

# Validation / traceability values.
pack_half_width=max(abs(MOTOR_Y[0]),abs(MOTOR_Y[1]))+GH_D/2
keepout_inner=28.0
validation={
  'status':'A0_FIXTURE_READY_FOR_PART_CHECK__NOT_PRODUCTION_RELEASE',
  'frozen_topology':{'wheel_x':WHEEL_X,'gear_x':GEAR_X,'z50':'m1 Z50 x5 per side','rear_input_x':250.0},
  'source_match_motor_candidate':{
    'motor':'FAULHABER 2250S024BX4','motor_d_mm':MOTOR_D,'motor_l_mm':MOTOR_L,
    'gearhead':'FAULHABER 26/1 S 66:1 candidate','gearhead_d_mm':GH_D,'gearhead_l_mm':GH_L,
    'combined_body_l_mm':MOTOR_L+GH_L,'output_shaft_mm':'5 x 12','motor_centres_y_mm':MOTOR_Y,
    'provenance_note':'Envelope match to ASS-002-386 is strong but does not prove MiniCam MOT-001-760 vendor/ratio identity.'
  },
  'bevel_reference':{
    'module':M,'teeth':[Z16,Z40],'ratio':Z40/Z16,'axis_angle_deg':90.0,
    'pitch_cone_angles_deg':[math.degrees(DELTA1),math.degrees(DELTA2)],
    'cone_distance_mm':CONE_R,'face_width_reference_mm':FACE,
    'small_outer_apex_distance_mm':SMALL_OUTER_AXIAL,'big_outer_apex_distance_mm':BIG_OUTER_AXIAL,
    'note':'Reference mounting geometry only. Actual purchased/source gear tooth form, correction, material and heat treatment remain H04.'
  },
  'packaging':{
    'gearhead_pack_total_width_mm':2*13.5+GH_D,
    'pack_y_extent_mm':[-pack_half_width,pack_half_width],
    'side_drive_inner_keepout_abs_y_mm':keepout_inner,
    'nominal_clearance_to_keepout_each_side_mm':keepout_inner-pack_half_width,
    'body_cavity_target_width_mm':53.0,
    'fit_note':'Two Ø26 gearheads on 27 mm centres exactly occupy 53 mm overall; this matches the reconstructed CRP150 inner cavity screen and explains the source layout.'
  },
  'bench_fixture':{
    'gear_support':'6001-2RS 12x28x8, A0 only','plate_thickness_mm':PLATE_T,
    'shaft_centres_preserved':True,'production_bearing_package_preserved':False,
    'purpose':'prove centre distances, gear train, direction, backlash trend and motor/input behaviour before pressure-body release'
  }
}
(OUT/'PX1_A0_SourceMatch_Validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(validation,indent=2,ensure_ascii=False))
