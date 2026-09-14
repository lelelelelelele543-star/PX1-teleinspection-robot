import cadquery as cq
import math, json, os

OUT='/mnt/data/PX1_master_build'
os.makedirs(OUT, exist_ok=True)

# =========================
# PX1 Rev.B CURRENT MASTER
# Proteus CRP150 source architecture + approved PX1 replacements.
# One integrated assembly. Validation / prototype handoff, not machining release.
# =========================

PIPE_R=75.0
PIPE_Z=52.0480547

# ---- hard crawler architecture from CRP150 source / Rev.B lock ----
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0
WHEEL_CENTER_Y=59.0
WHEEL_OD=90.0
WHEEL_W=16.0
GEAR_Y=42.0
GEAR_OD=52.0       # m1 Z50 envelope including allowance
GEAR_FACE=3.75
BODY_L=307.0
BODY_W=92.0
HALF_OUT=46.0
HALF_IN=34.0
Z0=8.0
ZTOP=90.0
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]
DECK_HALF_W=38.0
ROOF_T=5.0

# Rear motor housing reconciled to existing WB04 screen.
REAR_X0=242.0
REAR_X1=384.0
REAR_Y_HALF=46.0
REAR_Z0=19.0
REAR_Z1=71.0
CAV_X0=246.0
CAV_X1=378.0
CAV_Y_HALF=40.0
CAV_Z0=24.0
CAV_Z1=66.0

# ---- source-like motor input, two motors total ----
DRIVE_X=250.0
MOTOR_AXIS_Y=18.0
MOTOR_AXIS_Z=45.0
MOTOR_OD=32.0
MOTOR_TOTAL=92.0
MOTOR_SHAFT_D=6.0
MOTOR_SHAFT_LEN=12.0
MOTOR_FACE_X=293.0
MOTOR_REAR_X=MOTOR_FACE_X+(MOTOR_TOTAL-MOTOR_SHAFT_LEN)
COUPLING_OD=20.0
COUPLING_LEN=24.0
COUPLING_X1=MOTOR_FACE_X-5.0
COUPLING_X0=COUPLING_X1-COUPLING_LEN
BEARING_OD=21.0
BEARING_W=5.0
BEARING_X1=COUPLING_X0-1.5
BEARING_X0=BEARING_X1-BEARING_W
PINION_OD_SCREEN=18.6
PINION_LEN_SCREEN=7.5
PINION_X1=BEARING_X0-0.5
PINION_X0=PINION_X1-PINION_LEN_SCREEN

# ---- WB22A lift/camera ----
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=109.0
PIVOT_AVG=100.5
LINK_L=90.0
ARM_Y=31.0
ARM_T=4.0
ARM_H=14.0
CAM_AXIS_OFFSET_Z=2.0
CAM_Z=75.0
LOW_CAM_X=83.55688083875458
HEAD_R=26.0
HEAD_L=78.0
BOSS_OUTER_Y=34.0
TILT_POD_OD=18.0
TILT_WHEEL_Y=-16.75
WORM_CD=14.5
TILT_POD_X=56.0

# manual lift source feature
GAS_BODY=(194.0,16.0,82.9)
GAS_MOVING_S=63.0
GAS_OD=12.0

# ---- WB23E service cover ----
COVER_CX=261.0
COVER_Z0=110.0
COVER_L=86.0
COVER_W=44.0
COVER_T=6.0
OPEN_L=48.0
OPEN_W=22.0
SCREW_X=(226.0,296.0)
SCREW_HEAD_D=8.0
SCREW_HEAD_H=3.0
GLAND_OD=17.6
GLAND_AXIS_Y=12.0
GLAND_AXIS_Z=103.0
GLAND_X_FRONT=205.0
GLAND_X_REAR=231.5

# ---- WB24A flush pressure valve ----
VALVE_X=273.0
CAP_OD=12.0
CAP_H=1.5
CARTRIDGE_OD=10.0
CARTRIDGE_DEPTH=18.0

# ---- six-core local harness ----
HARNESS_OD=6.5
HARNESS_Y=25.5
GUARD_OD=10.0
ARM_RUN=(20.0,72.0)

# ---- dry connector / camera connector envelopes ----
MICROFIT_CX=247.0
MICROFIT_CZ=101.5
MICROFIT_L=14.0
MICROFIT_W=12.0
MICROFIT_H=7.0
SP13_OD=13.0
SP13_LEN=36.0  # compact connector envelope only; backshell/service length remains HOLD

# ---- rear tether tail, source-function placeholder ----
TAIL_X0=384.0
TAIL_X1=424.0
TAIL_OD=20.0
TETHER_OD_SCREEN=10.0
TETHER_X1=455.0

# ---- dry internal electronics envelopes from previous full-body packaging screen ----
# These are physical/reserve envelopes already used in the integrated Proteus-like body study.
# Exact mounting brackets remain to be drawn; no body enlargement is introduced here.
ELECTRONICS_NAMES=(
    'TRACTION_DRIVER_L_RESERVE','TRACTION_DRIVER_R_RESERVE','DELTA_TR1D_P2',
    'NICHICON_UCS2D221MHD1TN','INPUT_PROTECTION_RESERVE',
    'CINCON_CQB150W110S24_CARRIER_RESERVE','PRESSURE_SENSOR_RESERVE','NUCLEO_F446RE_LOWPROFILE'
)

# ---------- helpers ----------
def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,h): return wp(cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_between(p1,p2,r):
    a=cq.Vector(*p1); b=cq.Vector(*p2); v=b-a
    return wp(cq.Solid.makeCylinder(r,v.Length,a,v.normalized()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def prism_x(x0,pts,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts).close().extrude(length)
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def radial_clear(part,tol=0.4):
    verts,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in verts)
def plate_segment(p1,p2,y,t=ARM_T,h=ARM_H):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=boxc(0,y,0,L,t,h)
    p=p.rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))

# ---------- body exact from WB23E, with rear housing expanded to current WB04 ----------
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
wet=cq.Workplane('XZ',origin=(0,+DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W)
body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0))
body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
# rear pressure extension reconciled to motor package
rear_outer=box0(REAR_X0,-REAR_Y_HALF,REAR_Z0,REAR_X1-REAR_X0,2*REAR_Y_HALF,REAR_Z1-REAR_Z0)
rear_cavity=box0(CAV_X0,-CAV_Y_HALF,CAV_Z0,CAV_X1-CAV_X0,2*CAV_Y_HALF,CAV_Z1-CAV_Z0)
body=fuse(body,rear_outer)
body=cut(body,rear_cavity)
# top pressure pod
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]
body=fuse(body,prism_x(218,pod_outer_pts,89))
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]
pod_inner=prism_x(221,pod_inner_pts,83)
body=cut(body,pod_inner)
body=cut(body,box0(224,-33,84,76,66,10))
# service opening
service_open=boxc(COVER_CX,0,108.0,OPEN_L,OPEN_W,8.0)
body=cut(body,service_open)
# dry service/electronics union used only to prove that packaged modules remain inside the dry volume
throat_cavity=box0(224,-33,84,76,66,10)
dry_cavity=wp(inner.val().fuse(rear_cavity.val()).fuse(pod_inner.val()).fuse(throat_cavity.val()))
assert body.val().isValid()

# ---------- drivetrain ----------
wheels=[]
gears=[]
for side in (-1,1):
    for x in WHEEL_X:
        wheels.append((f'wheel_{side}_{int(x)}',cyl_y_center(x,side*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)))
    for x in GEAR_X:
        gears.append((f'Z50_{side}_{int(x)}',cyl_y_center(x,side*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE)))

# simplified axle envelopes at wheel stations, source-style outside-to-body path
axles=[]
for side in (-1,1):
    y0=side*(HALF_OUT-1.0)
    direction=1 if side>0 else -1
    for x in WHEEL_X:
        # local shaft envelope from body wall into wheel
        a=wp(cq.Solid.makeCylinder(6.0,16.0,cq.Vector(x,y0,WHEEL_Z),cq.Vector(0,direction,0)))
        axles.append((f'axle_{side}_{int(x)}',a))

# ---------- motor input package ----------
motor_parts=[]
for side in (-1,1):
    y=side*MOTOR_AXIS_Y
    motor=cyl_x(MOTOR_FACE_X,y,MOTOR_AXIS_Z,MOTOR_OD/2,MOTOR_REAR_X-MOTOR_FACE_X)
    shaft=cyl_x(MOTOR_FACE_X-MOTOR_SHAFT_LEN,y,MOTOR_AXIS_Z,MOTOR_SHAFT_D/2,MOTOR_SHAFT_LEN)
    coupling=cyl_x(COUPLING_X0,y,MOTOR_AXIS_Z,COUPLING_OD/2,COUPLING_LEN)
    bearing=cyl_x(BEARING_X0,y,MOTOR_AXIS_Z,BEARING_OD/2,BEARING_W)
    pinion=cyl_x(PINION_X0,y,MOTOR_AXIS_Z,PINION_OD_SCREEN/2,PINION_LEN_SCREEN)
    motor_parts += [
        (f'motor_{side}',motor),(f'motor_shaft_{side}',shaft),(f'coupling_{side}',coupling),
        (f'pinion_bearing_{side}',bearing),(f'Z16_pinion_envelope_{side}',pinion)
    ]

# ---------- manual lift LOW ----------
LOW_DZ=CAM_Z-CAM_AXIS_OFFSET_Z-PIVOT_AVG
theta=math.asin(LOW_DZ/LINK_L)
dx=-LINK_L*math.cos(theta); dz=LINK_L*math.sin(theta)
lower_end=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz)
upper_end=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
LOW_END_X=lower_end[0]
CARRIER_X_OFFSET=LOW_END_X-LOW_CAM_X
arms=[]
for side in (-1,1):
    arms.append((f'lower_arm_{side}',plate_segment((BODY_PIVOT_X,PIVOT_Z_LOW),lower_end,side*ARM_Y)))
    arms.append((f'upper_arm_{side}',plate_segment((BODY_PIVOT_X,PIVOT_Z_HIGH),upper_end,side*ARM_Y)))

# fixed carrier: two cheek plates plus cross bridge; envelope only, derived from corrected separated-fourbar architecture
carrier_x=(lower_end[0]+upper_end[0])/2
carrier_z=(lower_end[1]+upper_end[1])/2
carrier_bridge=boxc(carrier_x,0,carrier_z,12.0,58.0,24.0)
# camera outer envelope
camera_shell=wp(cq.Solid.makeCylinder(HEAD_R,HEAD_L,cq.Vector(LOW_CAM_X-HEAD_L/2,0,CAM_Z),cq.Vector(1,0,0)))
boss_p=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(LOW_CAM_X,HEAD_R,CAM_Z),cq.Vector(0,1,0)))
boss_n=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(LOW_CAM_X,-HEAD_R,CAM_Z),cq.Vector(0,-1,0)))
tilt_pod=wp(cq.Solid.makeCylinder(TILT_POD_OD/2,TILT_POD_X,cq.Vector(LOW_CAM_X+12-TILT_POD_X/2,TILT_WHEEL_Y,CAM_Z+WORM_CD),cq.Vector(1,0,0)))
camera_outer=wp(camera_shell.val().fuse(boss_p.val()).fuse(boss_n.val()).fuse(tilt_pod.val()))

# gas spring source-function envelope to lower arm point
moving=(BODY_PIVOT_X-GAS_MOVING_S*math.cos(theta),16.0,PIVOT_Z_LOW+GAS_MOVING_S*math.sin(theta))
gas_spring=cyl_between(GAS_BODY,moving,GAS_OD/2)

# ---------- service cover / valve / gland / harness ----------
cover=boxc(COVER_CX,0,COVER_Z0+COVER_T/2,COVER_L,COVER_W,COVER_T)
heads=[cyl_z(x,0,COVER_Z0+COVER_T,SCREW_HEAD_D/2,SCREW_HEAD_H) for x in SCREW_X]
gland=cyl_x(GLAND_X_FRONT,GLAND_AXIS_Y,GLAND_AXIS_Z,GLAND_OD/2,GLAND_X_REAR-GLAND_X_FRONT)
valve_cap=cyl_z(VALVE_X,0,COVER_Z0+COVER_T,CAP_OD/2,CAP_H)
valve_cart=cyl_z(VALVE_X,0,COVER_Z0+COVER_T-CARTRIDGE_DEPTH,CARTRIDGE_OD/2,CARTRIDGE_DEPTH)
microfit=boxc(MICROFIT_CX,0,MICROFIT_CZ,MICROFIT_L,MICROFIT_W,MICROFIT_H)

def arm_point(s): return (BODY_PIVOT_X-s*math.cos(theta),HARNESS_Y,PIVOT_Z_LOW+s*math.sin(theta))
harness=cyl_between(arm_point(ARM_RUN[0]),arm_point(ARM_RUN[1]),HARNESS_OD/2)
guard=cyl_between(arm_point(ARM_RUN[0]),arm_point(ARM_RUN[1]),GUARD_OD/2)

# SP13 marker fixed on carrier rear/toward body side; compact envelope only
sp13_x0=LOW_CAM_X+HEAD_L/2
sp13=cyl_x(sp13_x0,0,CAM_Z+18.0,SP13_OD/2,SP13_LEN)

# ---------- dry internal electronics ----------
electronics={
    'TRACTION_DRIVER_L_RESERVE':boxc(167,+16,22,34,22,14),
    'TRACTION_DRIVER_R_RESERVE':boxc(167,-16,22,34,22,14),
    'DELTA_TR1D_P2':boxc(205,-22,42,43,16,15),
    'NICHICON_UCS2D221MHD1TN':cyl_x(192.5,+24,30,9,25),
    'INPUT_PROTECTION_RESERVE':boxc(215,0,60,24,48,18),
    'CINCON_CQB150W110S24_CARRIER_RESERVE':boxc(260,0,70,65,45,16),
    'PRESSURE_SENSOR_RESERVE':cyl_z(280,0,35,12.2,25),
    'NUCLEO_F446RE_LOWPROFILE':boxc(262.25,0,98,82.5,70,12),
}

# ---------- rear tail ----------
tail=cyl_x(TAIL_X0,0,45.0,TAIL_OD/2,TAIL_X1-TAIL_X0)
tether=cyl_x(TAIL_X1,0,45.0,TETHER_OD_SCREEN/2,TETHER_X1-TAIL_X1)

# ---------- assembly ----------
assy=cq.Assembly(name='PX1_RevB_Current_Master')
assy.add(body,name='01_pressure_body')
for n,p in wheels: assy.add(p,name=n)
for n,p in gears: assy.add(p,name=n)
for n,p in axles: assy.add(p,name=n)
for n,p in motor_parts: assy.add(p,name=n)
for n,p in arms: assy.add(p,name=n)
assy.add(carrier_bridge,name='lift_fixed_carrier')
assy.add(camera_outer,name='sealed_camera_outer')
assy.add(gas_spring,name='manual_lift_150N_gas_spring_envelope')
assy.add(cover,name='PRESSURE_CAMERA_service_cover')
for i,h in enumerate(heads,1): assy.add(h,name=f'service_cover_M4_head_{i}')
assy.add(gland,name='M12_camera_harness_gland')
assy.add(valve_cap,name='flush_pressure_valve_cap')
assy.add(valve_cart,name='flush_pressure_valve_cartridge')
assy.add(microfit,name='J_CAM_LIFT_6way_MicroFit')
assy.add(harness,name='six_core_camera_harness')
assy.add(guard,name='lift_harness_guard_envelope')
assy.add(sp13,name='SP13_camera_connector_envelope')
assy.add(tail,name='rear_tether_strain_relief_envelope')
assy.add(tether,name='six_core_main_tether_envelope')
for n,p in electronics.items(): assy.add(p,name='internal_'+n)

step_path=os.path.join(OUT,'PX1_RevB_Current_Master.step')
assy.save(step_path)

# ---------- validation ----------
# Intended contacts/overlaps excluded. Check key non-contact groups.
fixed_top=[('cover',cover),('gland',gland),('valve_cap',valve_cap)]
collision={}
collision['top_vs_wheels']=max(inter(p,w) for _,p in fixed_top for _,w in wheels)
collision['top_vs_gears']=max(inter(p,g) for _,p in fixed_top for _,g in gears)
collision['top_vs_arms']=max(inter(p,a) for _,p in fixed_top for _,a in arms)
collision['top_vs_camera']=max(inter(p,camera_outer) for _,p in fixed_top)
collision['guard_vs_gears']=max(inter(guard,g) for _,g in gears)
collision['guard_vs_camera']=inter(guard,camera_outer)
collision['motor_vs_camera']=max(inter(p,camera_outer) for n,p in motor_parts if n.startswith('motor_'))
# Internal electronic envelopes must be inside the recovered dry-volume union and not overlap each other.
electronics_outside={n:p.val().cut(dry_cavity.val()).Volume() for n,p in electronics.items()}
electronics_intersections={}
ekeys=list(electronics)
for i,a in enumerate(ekeys):
    for b in ekeys[i+1:]:
        v=inter(electronics[a],electronics[b])
        if v>1e-4: electronics_intersections[a+'__'+b]=v

# Pipe clearances of driving low-state items
pipe_clear={
    'body':radial_clear(body),
    'wheel_visualization_cylinder_min_NOT_RELEASE':min(radial_clear(p) for _,p in wheels),
    'service_cover':radial_clear(cover),
    'pressure_cap':radial_clear(valve_cap),
    'M12_gland':radial_clear(gland),
    'lift_guard_LOW':radial_clear(guard),
    'camera_outer_LOW_static_envelope':radial_clear(camera_outer),
    'rear_motor_outer':radial_clear(rear_outer),
    'tail_strain_relief':radial_clear(tail),
}

# Counts / architecture gates
counts={'wheels':len(wheels),'Z50_gears':len(gears),'traction_motors':2,'lift_arms':len(arms),'local_camera_conductors':6}
architecture_ok=(counts=={'wheels':6,'Z50_gears':10,'traction_motors':2,'lift_arms':4,'local_camera_conductors':6})
collision_ok=all(v<1e-4 for v in collision.values())
# The current wheel solid is only a simple Ø90 x 16 visualization cylinder.
# It is deliberately NOT a DN150 release envelope: MiniCam officially specifies
# QRW90SR/150 90 mm wheels for 150 mm pipe, while the exact crowned/tapered wheel
# solid is not present in the recovered drawing pack.  Keep wheel geometry on HOLD
# instead of redesigning the crawler around a known-bad cylinder proxy.
nonwheel_pipe_ok=min(pipe_clear[k] for k in ['body','service_cover','pressure_cap','M12_gland','lift_guard_LOW','rear_motor_outer','tail_strain_relief'])>=3.0
wheel_source_compatibility=True  # QRW90SR/150 -> recommended 150 mm pipe (MiniCam current catalogue)
wheel_geometry_release=False     # exact FSS-002-065 / QRW90SR/150 outer solid not recovered

electronics_ok=all(v<1e-4 for v in electronics_outside.values()) and not electronics_intersections
master_geometry_ok=architecture_ok and collision_ok and nonwheel_pipe_ok and wheel_source_compatibility and electronics_ok
status=('PASS_INTEGRATED_MASTER / WHEEL_GEOMETRY_DN150_HOLD / PRESSURE_TEST_HOLD / PROCUREMENT_HOLD'
        if master_geometry_ok else 'FAIL_INTEGRATED_MASTER')

result={
    'status':status,
    'source_architecture':{
        'crawler':'Proteus CRP150 six-wheel / three stations per side / five Z50 per side / rear X250 input',
        'drive':'two motors, supported Z16 input into source-like Z40/rear axle architecture',
        'lift':'manual four-arm lift with 150 N gas spring principle',
        'pressure_service':'removable top service cover, compact pressure valve, M12 cable gland',
        'camera':'separately sealed removable head, six electrical functions',
    },
    'counts':counts,
    'internal_electronics':{
        'envelopes':list(electronics.keys()),
        'outside_dry_volume_mm3':electronics_outside,
        'pairwise_intersections_mm3':electronics_intersections,
        'packaging_ok':electronics_ok
    },
    'hard_dimensions_mm':{
        'wheel_station_X':list(WHEEL_X),'Z50_X':list(GEAR_X),'wheel_OD':WHEEL_OD,
        'body_main_L':BODY_L,'body_W':BODY_W,'rear_motor_housing_end_X':REAR_X1,
        'lift_body_pivot_X':BODY_PIVOT_X,'lift_link_L':LINK_L,'camera_shell_OD':2*HEAD_R,'camera_shell_L':HEAD_L,
        'service_cover_LxWxt':[COVER_L,COVER_W,COVER_T], 'service_opening_LxW':[OPEN_L,OPEN_W],
        'local_harness_OD_hard_max':HARNESS_OD,
    },
    'pipe_clearance_low_mm':pipe_clear,
    'wheel_release':{
        'visualization_proxy':'Ø90 x 16 straight cylinder only; not a production wheel solid',
        'official_compatible_product':'QRW90SR/150',
        'official_recommended_pipe_mm':150,
        'source_compatibility_accepted_for_master':wheel_source_compatibility,
        'exact_geometry_release':wheel_geometry_release,
        'gate':'replace visualization cylinders with measured/purchased QRW90SR/150 or recovered exact wheel solid before physical DN150 release'
    },
    'unintended_collision_mm3':collision,
    'master_step':step_path,
    'release_holds':[
        'Z16/Z40 exact matched bevel geometry and mounting distance remains sample/drawing gate',
        'rear tail currently represents the ASS-002-090 / ASS-002-364 connector-housing / spring / gland / PU-sleeve / crimp / heatshrink / cable-cup functional stack; exact dimensions remain to freeze',
        'exact QRW90SR/150 wheel solid/profile remains required for final geometric DN150 release; official catalogue compatibility is 150 mm',
        'SP13 exact mounting bracket and numeric pin orientation require physical pair',
        'pressure valve seat/shaft detail requires pressure test',
        'service-cover O-ring groove depth requires real seal sample',
        'six-core cable requires flex/EMC test',
        'WB22A full TILT sweep validation remains controlling for camera clearance; this master shows LOW static envelope',
        'no machining release until physical pressure and DN150 jig tests pass'
    ]
}
json_path=os.path.join(OUT,'PX1_RevB_Current_Master_VALIDATION.json')
with open(json_path,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
if not master_geometry_ok: raise SystemExit(2)
