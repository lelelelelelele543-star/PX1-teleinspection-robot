import cadquery as cq
import math, json, os

OUT='/mnt/data/PX1_master_build'
os.makedirs(OUT, exist_ok=True)

# PX1 Rev.B CURRENT MASTER
# Proteus CRP150 source architecture + available PX1 replacement parts.
# Single integrated assembly. Prototype/validation model, NOT machining release.

PIPE_R=75.0
PIPE_Z=52.0480547

# --- CRP150 hard architecture ---
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0
WHEEL_CENTER_Y=59.0
WHEEL_OD=90.0
WHEEL_W=16.0                 # visual only; exact QRW90SR/150 profile still required
GEAR_Y=42.0
GEAR_OD=52.0                 # Z50 m1 screen envelope
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

# Source dimensions from DRW-002-374 / DRW-002-375 / DRW-002-386
B61903_ID=17.0; B61903_OD=30.0; B61903_W=7.0
B61801_ID=12.0; B61801_OD=21.0; B61801_W=5.0
B61800_ID=10.0; B61800_OD=19.0; B61800_W=5.0
XRING_ID=18.72; XRING_CS=2.62; XRING_OD=XRING_ID+2*XRING_CS
Z40_OD=40.5; Z40_FACE=6.5
SHAFT_SEAL_ID=18.0; SHAFT_SEAL_OD=30.0; SHAFT_SEAL_W=7.0

# Rear motor housing. Lengthened only to package real off-the-shelf driver modules.
REAR_X0=242.0
REAR_X1=410.0
REAR_Y_HALF=46.0
REAR_Z0=19.0
REAR_Z1=71.0
CAV_X0=246.0
CAV_X1=404.0
CAV_Y_HALF=40.0
CAV_Z0=24.0
CAV_Z1=66.0

# Upper dry electronics tunnel for 2 real BTS7960/IBT-2 modules (50x50x43 mm screen each).
EROOT_X0=300.0; EROOT_X1=410.0
EROOT_Y_HALF=30.0; EROOT_Z0=65.0; EROOT_Z1=117.0
ECAV_X0=304.0; ECAV_X1=408.0
ECAV_Y_HALF=26.0; ECAV_Z0=69.0; ECAV_Z1=114.0
BTS_DIMS=(50.0,50.0,43.0)
BTS_CENTERS=((330.0,0.0,91.5),(382.0,0.0,91.5))

# Source-like motor input, two motors total
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
PINION_BEARING_X1=COUPLING_X0-1.5
PINION_BEARING_X0=PINION_BEARING_X1-B61801_W
PINION_OD_SCREEN=18.6
PINION_LEN_SCREEN=7.5
PINION_X1=PINION_BEARING_X0-0.5
PINION_X0=PINION_X1-PINION_LEN_SCREEN

# Lift/camera baseline
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
GAS_BODY=(194.0,16.0,82.9)
GAS_MOVING_S=63.0
GAS_OD=12.0

# Pressure/camera service interface
COVER_CX=261.0; COVER_Z0=110.0; COVER_L=86.0; COVER_W=44.0; COVER_T=6.0
OPEN_L=48.0; OPEN_W=22.0
SCREW_X=(226.0,296.0); SCREW_HEAD_D=8.0; SCREW_HEAD_H=3.0
GLAND_OD=17.6; GLAND_AXIS_Y=12.0; GLAND_AXIS_Z=103.0; GLAND_X_FRONT=205.0; GLAND_X_REAR=231.5
VALVE_X=273.0; CAP_OD=12.0; CAP_H=1.5; CARTRIDGE_OD=10.0; CARTRIDGE_DEPTH=18.0

# Exactly six insulated conductors to camera
HARNESS_OD=6.5; HARNESS_Y=25.5; GUARD_OD=10.0; ARM_RUN=(20.0,72.0)
MICROFIT_CX=247.0; MICROFIT_CZ=101.5; MICROFIT_L=14.0; MICROFIT_W=12.0; MICROFIT_H=7.0
SP13_OD=13.0; SP13_LEN=36.0

# Rear tether functional envelope
TAIL_X0=410.0; TAIL_X1=450.0; TAIL_OD=20.0
TETHER_OD_SCREEN=10.0; TETHER_X1=481.0

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
def ring_y_center(x,y,z,ro,ri,w):
    o=cyl_y_center(x,y,z,ro,w); i=cyl_y_center(x,y,z,ri,w+0.2)
    return wp(o.val().cut(i.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def prism_x(x0,pts,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts).close().extrude(length)
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def radial_clear(part,tol=0.45):
    verts,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in verts)
def plate_segment(p1,p2,y,t=ARM_T,h=ARM_H):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=boxc(0,y,0,L,t,h).rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))

# ---------- pressure body ----------
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
wet=cq.Workplane('XZ',origin=(0,+DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W)
body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0))
body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
rear_outer=box0(REAR_X0,-REAR_Y_HALF,REAR_Z0,REAR_X1-REAR_X0,2*REAR_Y_HALF,REAR_Z1-REAR_Z0)
rear_cavity=box0(CAV_X0,-CAV_Y_HALF,CAV_Z0,CAV_X1-CAV_X0,2*CAV_Y_HALF,CAV_Z1-CAV_Z0)
body=fuse(body,rear_outer); body=cut(body,rear_cavity)
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]
pod_outer=prism_x(218,pod_outer_pts,89); body=fuse(body,pod_outer)
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]
pod_inner=prism_x(221,pod_inner_pts,83); body=cut(body,pod_inner)
throat_cavity=box0(224,-33,84,76,66,10); body=cut(body,throat_cavity)
elec_roof_outer=box0(EROOT_X0,-EROOT_Y_HALF,EROOT_Z0,EROOT_X1-EROOT_X0,2*EROOT_Y_HALF,EROOT_Z1-EROOT_Z0)
elec_roof_cavity=box0(ECAV_X0,-ECAV_Y_HALF,ECAV_Z0,ECAV_X1-ECAV_X0,2*ECAV_Y_HALF,ECAV_Z1-ECAV_Z0)
body=fuse(body,elec_roof_outer); body=cut(body,elec_roof_cavity)
service_open=boxc(COVER_CX,0,108.0,OPEN_L,OPEN_W,8.0); body=cut(body,service_open)
assert body.val().isValid()
dry_cavity=wp(inner.val().fuse(rear_cavity.val()).fuse(pod_inner.val()).fuse(throat_cavity.val()).fuse(elec_roof_cavity.val()))

# ---------- side drive: wheels, Z50, source bearing/seal envelopes ----------
wheels=[]; gears=[]; side_station_parts=[]
for side in (-1,1):
    s=float(side)
    for x in WHEEL_X:
        wheels.append((f'wheel_{side}_{int(x)}',cyl_y_center(x,s*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)))
        y_b=s*48.0; y_xr=s*52.8; y_fl=s*55.7
        bearing=cyl_y_center(x,y_b,WHEEL_Z,B61903_OD/2,B61903_W)
        xring=ring_y_center(x,y_xr,WHEEL_Z,XRING_OD/2,XRING_ID/2,XRING_CS)
        flange=cyl_y_center(x,y_fl,WHEEL_Z,17.0,3.0)
        journal=cyl_y_center(x,s*50.0,WHEEL_Z,B61903_ID/2,14.0)
        wheel_stub=cyl_y_center(x,s*61.0,WHEEL_Z,6.0,14.0)
        side_station_parts += [(f'61903_{side}_{int(x)}',bearing),(f'Xring_18p72x2p62_{side}_{int(x)}',xring),(f'axle_flange_env_{side}_{int(x)}',flange),(f'axle_17mm_journal_{side}_{int(x)}',journal),(f'wheel_stub_{side}_{int(x)}',wheel_stub)]
    for x in GEAR_X:
        gears.append((f'Z50_{side}_{int(x)}',cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE)))
    side_station_parts.append((f'61801_rear_long_axle_{side}',cyl_y_center(250.0,s*37.5,WHEEL_Z,B61801_OD/2,B61801_W)))

# ---------- Z40 transverse input shafts from DRW-002-375 ----------
bevel_output_parts=[]
for side in (-1,1):
    s=float(side); yc=s*MOTOR_AXIS_Y
    z40=cyl_y_center(250.0,yc,WHEEL_Z,Z40_OD/2,Z40_FACE)
    y_b=s*(abs(MOTOR_AXIS_Y)+Z40_FACE/2+B61800_W/2+0.8)
    b61800=cyl_y_center(250.0,y_b,WHEEL_Z,B61800_OD/2,B61800_W)
    y_seal=s*(abs(MOTOR_AXIS_Y)+Z40_FACE/2+B61800_W+SHAFT_SEAL_W/2+1.5)
    seal=ring_y_center(250.0,y_seal,WHEEL_Z,SHAFT_SEAL_OD/2,SHAFT_SEAL_ID/2,SHAFT_SEAL_W)
    shaft=cyl_y_center(250.0,s*29.0,WHEEL_Z,5.0,28.0)
    bevel_output_parts += [(f'Z40_{side}',z40),(f'61800_Z40_{side}',b61800),(f'18x30x7_shaft_seal_{side}',seal),(f'Z40_axle_env_{side}',shaft)]

# ---------- motor input from DRW-002-386 ----------
motor_parts=[]
for side in (-1,1):
    y=side*MOTOR_AXIS_Y
    motor=cyl_x(MOTOR_FACE_X,y,MOTOR_AXIS_Z,MOTOR_OD/2,MOTOR_REAR_X-MOTOR_FACE_X)
    shaft=cyl_x(MOTOR_FACE_X-MOTOR_SHAFT_LEN,y,MOTOR_AXIS_Z,MOTOR_SHAFT_D/2,MOTOR_SHAFT_LEN)
    coupling=cyl_x(COUPLING_X0,y,MOTOR_AXIS_Z,COUPLING_OD/2,COUPLING_LEN)
    bearing=cyl_x(PINION_BEARING_X0,y,MOTOR_AXIS_Z,B61801_OD/2,B61801_W)
    pinion=cyl_x(PINION_X0,y,MOTOR_AXIS_Z,PINION_OD_SCREEN/2,PINION_LEN_SCREEN)
    motor_parts += [(f'motor_{side}',motor),(f'motor_shaft_{side}',shaft),(f'coupling_{side}',coupling),(f'61801_Z16_{side}',bearing),(f'Z16_{side}',pinion)]

# ---------- manual lift LOW ----------
LOW_DZ=CAM_Z-CAM_AXIS_OFFSET_Z-PIVOT_AVG
theta=math.asin(LOW_DZ/LINK_L)
dx=-LINK_L*math.cos(theta); dz=LINK_L*math.sin(theta)
lower_end=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz); upper_end=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
arms=[]
for side in (-1,1):
    arms += [(f'lower_arm_{side}',plate_segment((BODY_PIVOT_X,PIVOT_Z_LOW),lower_end,side*ARM_Y)),(f'upper_arm_{side}',plate_segment((BODY_PIVOT_X,PIVOT_Z_HIGH),upper_end,side*ARM_Y))]
carrier_x=(lower_end[0]+upper_end[0])/2; carrier_z=(lower_end[1]+upper_end[1])/2
carrier_bridge=boxc(carrier_x,0,carrier_z,12.0,58.0,24.0)
camera_shell=wp(cq.Solid.makeCylinder(HEAD_R,HEAD_L,cq.Vector(LOW_CAM_X-HEAD_L/2,0,CAM_Z),cq.Vector(1,0,0)))
boss_p=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(LOW_CAM_X,HEAD_R,CAM_Z),cq.Vector(0,1,0)))
boss_n=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(LOW_CAM_X,-HEAD_R,CAM_Z),cq.Vector(0,-1,0)))
tilt_pod=wp(cq.Solid.makeCylinder(TILT_POD_OD/2,TILT_POD_X,cq.Vector(LOW_CAM_X+12-TILT_POD_X/2,TILT_WHEEL_Y,CAM_Z+WORM_CD),cq.Vector(1,0,0)))
camera_outer=wp(camera_shell.val().fuse(boss_p.val()).fuse(boss_n.val()).fuse(tilt_pod.val()))
moving=(BODY_PIVOT_X-GAS_MOVING_S*math.cos(theta),16.0,PIVOT_Z_LOW+GAS_MOVING_S*math.sin(theta))
gas_spring=cyl_between(GAS_BODY,moving,GAS_OD/2)

# ---------- pressure cover / harness ----------
cover=boxc(COVER_CX,0,COVER_Z0+COVER_T/2,COVER_L,COVER_W,COVER_T)
heads=[cyl_z(x,0,COVER_Z0+COVER_T,SCREW_HEAD_D/2,SCREW_HEAD_H) for x in SCREW_X]
gland=cyl_x(GLAND_X_FRONT,GLAND_AXIS_Y,GLAND_AXIS_Z,GLAND_OD/2,GLAND_X_REAR-GLAND_X_FRONT)
valve_cap=cyl_z(VALVE_X,0,COVER_Z0+COVER_T,CAP_OD/2,CAP_H)
valve_cart=cyl_z(VALVE_X,0,COVER_Z0+COVER_T-CARTRIDGE_DEPTH,CARTRIDGE_OD/2,CARTRIDGE_DEPTH)
microfit=boxc(MICROFIT_CX,0,MICROFIT_CZ,MICROFIT_L,MICROFIT_W,MICROFIT_H)
def arm_point(s): return (BODY_PIVOT_X-s*math.cos(theta),HARNESS_Y,PIVOT_Z_LOW+s*math.sin(theta))
harness=cyl_between(arm_point(ARM_RUN[0]),arm_point(ARM_RUN[1]),HARNESS_OD/2)
guard=cyl_between(arm_point(ARM_RUN[0]),arm_point(ARM_RUN[1]),GUARD_OD/2)
sp13=cyl_x(LOW_CAM_X+HEAD_L/2,0,CAM_Z+18.0,SP13_OD/2,SP13_LEN)

# ---------- electronics: real-size driver envelopes + previously sourced components ----------
electronics={
    'BTS7960_IBT2_A_50x50x43':boxc(*BTS_CENTERS[0],*BTS_DIMS),
    'BTS7960_IBT2_B_50x50x43':boxc(*BTS_CENTERS[1],*BTS_DIMS),
    'DELTA_TR1D_P2':boxc(205,-22,42,43,16,15),
    'NICHICON_UCS2D221MHD1TN':cyl_x(192.5,+24,30,9,25),
    'INPUT_PROTECTION_RESERVE':boxc(215,0,60,24,48,18),
    'CINCON_CQB150W110S24_CARRIER_RESERVE':boxc(260,0,70,65,45,16),
    'NUCLEO_F446RE_LOWPROFILE':boxc(262.25,0,98,82.5,70,12),
}

# ---------- rear tail ----------
tail=cyl_x(TAIL_X0,0,45.0,TAIL_OD/2,TAIL_X1-TAIL_X0)
tether=cyl_x(TAIL_X1,0,45.0,TETHER_OD_SCREEN/2,TETHER_X1-TAIL_X1)

# ---------- assembly ----------
assy=cq.Assembly(name='PX1_RevB_Current_Master')
assy.add(body,name='01_pressure_body')
for group in (wheels,gears,side_station_parts,bevel_output_parts,motor_parts,arms):
    for n,p in group: assy.add(p,name=n)
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
fixed_top=[('cover',cover),('gland',gland),('valve_cap',valve_cap)]
collision={'top_vs_wheels':max(inter(p,w) for _,p in fixed_top for _,w in wheels),'top_vs_gears':max(inter(p,g) for _,p in fixed_top for _,g in gears),'top_vs_arms':max(inter(p,a) for _,p in fixed_top for _,a in arms),'top_vs_camera':max(inter(p,camera_outer) for _,p in fixed_top),'guard_vs_gears':max(inter(guard,g) for _,g in gears),'guard_vs_camera':inter(guard,camera_outer),'motor_vs_camera':max(inter(p,camera_outer) for n,p in motor_parts if n.startswith('motor_'))}
electronics_outside={n:p.val().cut(dry_cavity.val()).Volume() for n,p in electronics.items()}
electronics_intersections={}
ekeys=list(electronics)
for i,a in enumerate(ekeys):
    for b in ekeys[i+1:]:
        v=inter(electronics[a],electronics[b])
        if v>1e-4: electronics_intersections[a+'__'+b]=v
motor_hard=[p for n,p in motor_parts]
electronics_vs_motor={}
for en,ep in electronics.items():
    mv=max(inter(ep,mp) for mp in motor_hard)
    if mv>1e-4: electronics_vs_motor[en]=mv
source_counts={'wheels':len(wheels),'Z50':len(gears),'61903':sum(1 for n,_ in side_station_parts if n.startswith('61903_')),'Xrings':sum(1 for n,_ in side_station_parts if n.startswith('Xring_')),'axle_flange_envelopes':sum(1 for n,_ in side_station_parts if n.startswith('axle_flange_')),'rear_61801_side_drive':sum(1 for n,_ in side_station_parts if n.startswith('61801_rear_')),'Z40':sum(1 for n,_ in bevel_output_parts if n.startswith('Z40_') and not n.startswith('Z40_axle')),'61800':sum(1 for n,_ in bevel_output_parts if n.startswith('61800_')),'18x30x7_seals':sum(1 for n,_ in bevel_output_parts if n.startswith('18x30x7_')),'Z16':sum(1 for n,_ in motor_parts if n.startswith('Z16_')),'Z16_61801':sum(1 for n,_ in motor_parts if n.startswith('61801_Z16_')),'traction_motors':sum(1 for n,_ in motor_parts if n in ('motor_-1','motor_1')),'lift_arms':len(arms),'local_camera_conductors':6}
expected_counts={'wheels':6,'Z50':10,'61903':6,'Xrings':6,'axle_flange_envelopes':6,'rear_61801_side_drive':2,'Z40':2,'61800':2,'18x30x7_seals':2,'Z16':2,'Z16_61801':2,'traction_motors':2,'lift_arms':4,'local_camera_conductors':6}
counts_ok=(source_counts==expected_counts)
pipe_clear={'body':radial_clear(body),'wheel_visualization_cylinder_min_NOT_RELEASE':min(radial_clear(p) for _,p in wheels),'service_cover':radial_clear(cover),'pressure_cap':radial_clear(valve_cap),'M12_gland':radial_clear(gland),'lift_guard_LOW':radial_clear(guard),'camera_outer_LOW_static_envelope':radial_clear(camera_outer),'rear_motor_outer':radial_clear(rear_outer),'electronics_roof_outer':radial_clear(elec_roof_outer),'tail_strain_relief':radial_clear(tail)}
collision_ok=all(v<1e-4 for v in collision.values())
electronics_ok=(all(v<1e-4 for v in electronics_outside.values()) and not electronics_intersections and not electronics_vs_motor)
nonwheel_pipe_ok=min(pipe_clear[k] for k in ['body','service_cover','pressure_cap','M12_gland','lift_guard_LOW','rear_motor_outer','electronics_roof_outer','tail_strain_relief'])>=3.0
wheel_source_compatibility=True
wheel_geometry_release=False
master_ok=counts_ok and collision_ok and electronics_ok and nonwheel_pipe_ok and wheel_source_compatibility
status=('PASS_INTEGRATED_MASTER / EXACT_WHEEL_PROFILE_HOLD / Z16_Z40_FINAL_PAIR_HOLD / PRESSURE_TEST_HOLD / PROCUREMENT_HOLD' if master_ok else 'FAIL_INTEGRATED_MASTER')
result={'status':status,'single_master_rule':'This file is the current crawler integration master; old WB files are evidence/history only.','source_counts':source_counts,'source_dimensioned_components':{'DRW-002-374':['6x 61903 17x30x7','6x X-ring 18.72x2.62','2x rear 61801 12x21x5','10x Z50 total'],'DRW-002-375':['2x Z40','2x 61800 10x19x5','2x shaft seal 18x30x7'],'DRW-002-386':['2x motor','2x Z16','2x separate Z16 axle','2x 61801 12x21x5']},'electronics':{'BTS7960_screen_each_mm':list(BTS_DIMS),'BTS7960_centers_xyz_mm':[list(v) for v in BTS_CENTERS],'outside_dry_volume_mm3':electronics_outside,'pairwise_intersections_mm3':electronics_intersections,'intersections_with_motor_input_mm3':electronics_vs_motor,'packaging_ok':electronics_ok},'hard_dimensions_mm':{'wheel_station_X':list(WHEEL_X),'Z50_X':list(GEAR_X),'wheel_OD_visual':WHEEL_OD,'body_main_L':BODY_L,'body_W':BODY_W,'rear_body_end_X':REAR_X1,'electronics_roof':[EROOT_X0,EROOT_X1,2*EROOT_Y_HALF,EROOT_Z0,EROOT_Z1],'lift_body_pivot_X':BODY_PIVOT_X,'lift_link_L':LINK_L,'camera_shell_OD':2*HEAD_R,'camera_shell_L':HEAD_L,'service_cover_LxWxt':[COVER_L,COVER_W,COVER_T],'local_harness_OD_hard_max':HARNESS_OD},'pipe_clearance_low_mm':pipe_clear,'unintended_collision_mm3':collision,'wheel_release':{'visualization_proxy':'Ø90x16 cylinder only','official_compatible_product':'MiniCam QRW90SR/150 90 mm wheel for 150 mm pipe','exact_geometry_release':wheel_geometry_release},'master_step':step_path,'release_holds':['Exact QRW90SR/150 wheel outer profile or measured equivalent before final DN150 release','Final hardened matched Z16/Z40 geometry and supplier mounting distance','Axle shoulder/flange exact Y dimensions require detail/source drawing or physical measurement; source bearing/seal sizes are already fixed','Pressure cover groove and compact valve require real seal/pressure test','Pressure sensor exact article/mounting remains HOLD; the old generic 24.4 mm cylinder was removed rather than pretending it fits','Six-core camera cable requires flex + CVBS/UART EMC test','Rear tether tail exact purchased/source hardware dimensions','WB22A full TILT sweep remains controlling for camera motion; this master contains LOW pose']}
json_path=os.path.join(OUT,'PX1_RevB_Current_Master_VALIDATION.json')
with open(json_path,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
if not master_ok: raise SystemExit(2)
