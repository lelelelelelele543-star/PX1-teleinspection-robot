import cadquery as cq
import math, json, os

# PX-1 Rev.GJ — compact supported X200 bevel input and side-drive handoff
# Prototype engineering only; NOT machining release.
# Coordinates continue Rev.GC/Rev.GF: X forward->rear, Y transverse, Z vertical.

OUT=os.path.abspath('build_revgj')
os.makedirs(OUT,exist_ok=True)

# Pressure body / bay geometry
L=340.0
W=92.0
Z0=8.0
ZTOP=90.0
END=8.0
P0_HALF_OUT=46.0
P0_HALF_IN=34.0
BAY_INNER_Y=38.0
SIDE_COVER_T=5.0
SIDE_COVER_Y0=46.0
SIDE_COVER_OUT=51.0
BAY_Z0=6.0
BAY_H=80.0
COVER_X0=10.5
COVER_L=286.0

# Drivetrain axes
X200=200.0
ZDRV=45.0
MOTOR_Y=16.5
MOTOR_D=32.0
MOTOR_L=92.0
MOTOR_FRONT_X=237.0
MOTOR_REAR_X=MOTOR_FRONT_X+MOTOR_L

# Compact custom bevel candidate m1.25 z16/z40, 90-deg shafts.
# A standard stock KHK pair was checked separately and is not a drop-in because its mounting
# distances drive the large gear through the P0/P1 membrane at this motor-axis spacing.
M=1.25
ZP=16
ZG=40
R_CONE=0.5*M*math.sqrt(ZP**2+ZG**2)
DELTA_P=math.atan(ZP/ZG)
DELTA_G=math.atan(ZG/ZP)
PINION_APEX_TO_OUTER=R_CONE*math.cos(DELTA_P)
GEAR_APEX_TO_OUTER=R_CONE*math.cos(DELTA_G)
FACE=8.0
PINION_R_OUT=0.5*M*ZP+M
PINION_R_IN=max(3.0, PINION_R_OUT*(1-FACE/R_CONE))
GEAR_R_OUT=0.5*M*ZG+M
GEAR_R_IN=max(6.0, GEAR_R_OUT*(1-FACE/R_CONE))

# X200 shaft / bearings / seal / side handoff
OUT_BEAR_ID=10.0; OUT_BEAR_OD=19.0; OUT_BEAR_L=5.0  # 61800
SEAL_ID=18.0; SEAL_OD=30.0; SEAL_L=7.0             # 18x30x7
SIDE_JOURNAL=12.0
SIDE_GEAR_FACE=3.75
SIDE_GEAR_OD=52.0                                   # m1 z50 envelope incl addendum
SIDE_GEAR_Y0=42.125
SIDE_GEAR_Y1=SIDE_GEAR_Y0+SIDE_GEAR_FACE
COVER_BEAR_ID=12.0; COVER_BEAR_OD=18.0; COVER_BEAR_L=4.0 # 6701
COVER_BEAR_Y0=46.0
COVER_BEAR_Y1=50.0

# Pinion shaft support (source-inspired separate supported shaft)
PINION_BEAR_ID=12.0; PINION_BEAR_OD=21.0; PINION_BEAR_L=5.0 # 61801
PINION_GEAR_X0=X200+PINION_APEX_TO_OUTER-FACE
PINION_GEAR_X1=X200+PINION_APEX_TO_OUTER
PINION_BEAR_X0=230.0
PINION_BEAR_X1=235.0


def wp(shape): return cq.Workplane('XY').newObject([shape])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,1,0)))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter_vol(a,b): return a.val().intersect(b.val()).Volume()

# Keep full-width pressure body at 307 mm and absorb the 92-mm motor tails into a narrow
# central pressure extension. Side covers and side bays keep their previous geometry.
MAIN_L=307.0
POD_X0=299.0
POD_L=L-POD_X0
POD_HALF_W=38.0
POD_Z0=23.0
POD_Z1=67.0
main_outer=box(0,-P0_HALF_OUT,Z0,MAIN_L,W,ZTOP-Z0)
pod_outer=box(POD_X0,-POD_HALF_W,POD_Z0,POD_L,2*POD_HALF_W,POD_Z1-POD_Z0)
outer=fuse(main_outer,pod_outer)
main_inner=box(END,-P0_HALF_IN,Z0+6,MAIN_L-END,2*P0_HALF_IN,(ZTOP-Z0)-11)
pod_inner=box(POD_X0,-P0_HALF_IN,27.0,(L-END)-POD_X0,2*P0_HALF_IN,36.0)
inner=fuse(main_inner,pod_inner)
body=cut(outer,inner)

# Side bay pockets across the original side-drive span.
left_bay=box(COVER_X0,BAY_INNER_Y,BAY_Z0,COVER_L,P0_HALF_OUT-BAY_INNER_Y,BAY_H)
right_bay=box(COVER_X0,-P0_HALF_OUT,BAY_Z0,COVER_L,P0_HALF_OUT-BAY_INNER_Y,BAY_H)
body=cut(cut(body,left_bay),right_bay)
for s in (-1,1):
    bore=cyl_y(X200, P0_HALF_IN if s>0 else -P0_HALF_IN-4, ZDRV, 19.0, 4.0)
    body=cut(body,bore)

left_cover=box(COVER_X0,SIDE_COVER_Y0,BAY_Z0,COVER_L,SIDE_COVER_T,BAY_H)
right_cover=box(COVER_X0,-SIDE_COVER_OUT,BAY_Z0,COVER_L,SIDE_COVER_T,BAY_H)
left_cover=cut(left_cover,cyl_y(X200,46.0,ZDRV,COVER_BEAR_OD/2,4.0))
right_cover=cut(right_cover,cyl_y(X200,-50.0,ZDRV,COVER_BEAR_OD/2,4.0))

SIDE_ORING_ID=190.0; SIDE_RT_H=60.0; SIDE_RT_R=SIDE_RT_H/2
SIDE_RT_L=(math.pi*SIDE_ORING_ID-2*math.pi*SIDE_RT_R)/2 + 2*SIDE_RT_R

parts={}
for side,s in [('L',1),('R',-1)]:
    if s>0:
        boss=cyl_y(X200,30.0,ZDRV,19.0,12.0)
        shaft10=cyl_y(X200,20.0,ZDRV,5.0,15.0)
        seal_land=cyl_y(X200,35.0,ZDRV,9.0,7.0)
        journal=cyl_y(X200,42.0,ZDRV,SIDE_JOURNAL/2,8.0)
        bearing61800=cyl_y(X200,30.0,ZDRV,OUT_BEAR_OD/2,5.0)
        seal=cyl_y(X200,35.0,ZDRV,SEAL_OD/2,7.0)
        z50=cyl_y(X200,SIDE_GEAR_Y0,ZDRV,SIDE_GEAR_OD/2,SIDE_GEAR_FACE)
        b6701=cyl_y(X200,COVER_BEAR_Y0,ZDRV,COVER_BEAR_OD/2,COVER_BEAR_L)
    else:
        boss=cyl_y(X200,-42.0,ZDRV,19.0,12.0)
        shaft10=cyl_y(X200,-35.0,ZDRV,5.0,15.0)
        seal_land=cyl_y(X200,-42.0,ZDRV,9.0,7.0)
        journal=cyl_y(X200,-50.0,ZDRV,SIDE_JOURNAL/2,8.0)
        bearing61800=cyl_y(X200,-35.0,ZDRV,OUT_BEAR_OD/2,5.0)
        seal=cyl_y(X200,-42.0,ZDRV,SEAL_OD/2,7.0)
        z50=cyl_y(X200,-SIDE_GEAR_Y1,ZDRV,SIDE_GEAR_OD/2,SIDE_GEAR_FACE)
        b6701=cyl_y(X200,-COVER_BEAR_Y1,ZDRV,COVER_BEAR_OD/2,COVER_BEAR_L)
    shaft=fuse(fuse(shaft10,seal_land),journal)
    parts[f'boss_{side}']=boss
    parts[f'shaft_{side}']=shaft
    parts[f'bearing61800_{side}']=bearing61800
    parts[f'seal18x30x7_{side}']=seal
    parts[f'z50_input_{side}']=z50
    parts[f'bearing6701_{side}']=b6701

for side,s in [('L',1),('R',-1)]:
    y=s*MOTOR_Y
    motor=cyl_x(MOTOR_FRONT_X,y,ZDRV,MOTOR_D/2,MOTOR_L)
    pinion_bear=cyl_x(PINION_BEAR_X0,y,ZDRV,PINION_BEAR_OD/2,PINION_BEAR_L)
    pinion_shaft=cyl_x(PINION_GEAR_X0,y,ZDRV,6.0,MOTOR_FRONT_X-PINION_GEAR_X0)
    pinion=wp(cq.Solid.makeCone(PINION_R_IN,PINION_R_OUT,FACE,
                                cq.Vector(PINION_GEAR_X0,y,ZDRV),cq.Vector(1,0,0)))
    pinion_hub=cyl_x(PINION_GEAR_X1,y,ZDRV,8.0,230.0-PINION_GEAR_X1)
    pinion=fuse(pinion,pinion_hub)
    parts[f'motor_{side}']=motor
    parts[f'pinion_bearing_{side}']=pinion_bear
    parts[f'pinion_shaft_{side}']=pinion_shaft
    parts[f'pinion_Z16_{side}']=pinion
    if s>0:
        gy0=y+GEAR_APEX_TO_OUTER-FACE
        large=wp(cq.Solid.makeCone(GEAR_R_IN,GEAR_R_OUT,FACE,cq.Vector(X200,gy0,ZDRV),cq.Vector(0,1,0)))
        large_hub=cyl_y(X200,y+GEAR_APEX_TO_OUTER,ZDRV,15.0,30.0-(y+GEAR_APEX_TO_OUTER))
    else:
        gy0=y-(GEAR_APEX_TO_OUTER-FACE)
        large=wp(cq.Solid.makeCone(GEAR_R_IN,GEAR_R_OUT,FACE,cq.Vector(X200,gy0,ZDRV),cq.Vector(0,-1,0)))
        large_hub=cyl_y(X200,-30.0,ZDRV,15.0,30.0-(abs(y)+GEAR_APEX_TO_OUTER))
    parts[f'bevel_Z40_{side}']=fuse(large,large_hub)

# LOW camera envelope retained from Rev.GE; both traction motors point rearward.
CAM_X=83.557; CAM_Z=75.0; CAM_D=52.0; CAM_L=72.0
camera_low=cyl_x(CAM_X-CAM_L/2,0,CAM_Z,CAM_D/2,CAM_L)

checks={}
checks['motor_pair_intersection_mm3']=round(inter_vol(parts['motor_L'],parts['motor_R']),6)
checks['rear_motor_camera_intersection_mm3']={s:round(inter_vol(parts[f'motor_{s}'],camera_low),6) for s in ('L','R')}
checks['motor_rear_x_mm']=MOTOR_REAR_X
checks['p0_inner_rear_x_mm']=L-END
checks['main_fullwidth_body_length_mm']=MAIN_L
checks['rear_drive_tunnel_total_length_mm']=L-MAIN_L
checks['rear_drive_tunnel_outer_width_mm']=2*POD_HALF_W
checks['rear_drive_tunnel_outer_height_mm']=POD_Z1-POD_Z0
checks['rear_motor_end_clearance_mm']=(L-END)-MOTOR_REAR_X
checks['motor_side_clearance_to_p0_wall_mm']=P0_HALF_IN-(MOTOR_Y+MOTOR_D/2)
checks['motor_pair_gap_mm']=2*MOTOR_Y-MOTOR_D
checks['sidegear_to_inner_bay_wall_gap_mm']=SIDE_GEAR_Y0-BAY_INNER_Y
checks['sidegear_to_cover_gap_mm']=SIDE_COVER_Y0-SIDE_GEAR_Y1
checks['sidegear_plus_cover_bearing_axial_package_mm']=SIDE_GEAR_FACE+COVER_BEAR_L
checks['sidebay_depth_mm']=P0_HALF_OUT-BAY_INNER_Y
checks['sidecover_outside_skin_after_6701_mm']=SIDE_COVER_T-COVER_BEAR_L
checks['bevel_ratio']=ZG/ZP
checks['bevel_cone_distance_mm']=R_CONE
checks['pinion_pitch_angle_deg']=math.degrees(DELTA_P)
checks['gear_pitch_angle_deg']=math.degrees(DELTA_G)
checks['pinion_apex_to_outer_pitch_plane_mm']=PINION_APEX_TO_OUTER
checks['largegear_apex_to_outer_pitch_plane_mm']=GEAR_APEX_TO_OUTER
checks['bevel_face_mm']=FACE

for side in ('L','R'):
    motor=parts[f'motor_{side}']; large=parts[f'bevel_Z40_{side}']
    z50=parts[f'z50_input_{side}']; b6701=parts[f'bearing6701_{side}']
    cov=left_cover if side=='L' else right_cover
    checks[f'motor_body_shell_intersection_{side}_mm3']=round(inter_vol(motor,body),6)
    checks[f'6701_cover_solid_intersection_{side}_mm3']=round(inter_vol(b6701,cov),6)
    checks[f'z50_cover_intersection_{side}_mm3']=round(inter_vol(z50,cov),6)
    checks[f'z50_body_intersection_{side}_mm3']=round(inter_vol(z50,body),6)
    checks[f'large_bevel_motor_intersection_{side}_mm3']=round(inter_vol(large,motor),6)
    checks[f'large_bevel_z50_intersection_{side}_mm3']=round(inter_vol(large,z50),6)

cx=COVER_X0+COVER_L/2; cz=BAY_Z0+BAY_H/2
oring_vertical_sep=min(abs(ZDRV-(cz-SIDE_RT_H/2)),abs((cz+SIDE_RT_H/2)-ZDRV))
checks['x200_6701_to_side_oring_centerline_radial_margin_mm']=oring_vertical_sep-COVER_BEAR_OD/2

PIPE_R=75.0; PIPE_Z=52.0480547
checks['sidecover_lower_corner_clearance_mm']=PIPE_R-math.hypot(SIDE_COVER_OUT,BAY_Z0-PIPE_Z)
checks['sidecover_upper_corner_clearance_mm']=PIPE_R-math.hypot(SIDE_COVER_OUT,(BAY_Z0+BAY_H)-PIPE_Z)
checks['rear_drive_tunnel_lower_corner_clearance_mm']=PIPE_R-math.hypot(POD_HALF_W,POD_Z0-PIPE_Z)
checks['rear_drive_tunnel_upper_corner_clearance_mm']=PIPE_R-math.hypot(POD_HALF_W,POD_Z1-PIPE_Z)

# Performance screening. Exact motor SKU is not frozen; current 32x92 candidate is 24 V, 54 rpm,
# 14 kg.cm rated. Gear sizing is protected by a 1.0 N.m commanded torque ceiling until bench data exists.
kgcm_to_Nm=0.0980665
motor_rated_torque=14.0*kgcm_to_Nm
torque_limit=1.0
eta_bevel=0.85
side_torque=torque_limit*(ZG/ZP)*eta_bevel
wheel_rpm=54.0/(ZG/ZP)
wheel_speed_m_min=math.pi*0.09*wheel_rpm
checks['candidate_motor_rated_torque_Nm']=motor_rated_torque
checks['traction_command_torque_limit_Nm']=torque_limit
checks['candidate_side_torque_after_bevel_Nm']=side_torque
checks['candidate_wheel_rpm']=wheel_rpm
checks['candidate_linear_speed_m_min']=wheel_speed_m_min

# Preliminary Lewis screen only; real bevel-gear supplier rating/contact check remains a release gate.
Ft_N=torque_limit*1000.0/(M*ZP/2.0)
lewis_Y=0.30
sigma_lewis=Ft_N/(FACE*M*lewis_Y)
checks['custom_bevel_pinion_tangential_force_N']=Ft_N
checks['custom_bevel_pinion_lewis_nominal_MPa']=sigma_lewis
checks['custom_bevel_pinion_screening_2x_MPa']=2.0*sigma_lewis
checks['custom_bevel_face_to_cone_distance_ratio']=FACE/R_CONE
checks['custom_bevel_face_rule_R_over_3_mm']=R_CONE/3.0

must_zero=[k for k,v in checks.items() if ('intersection' in k and isinstance(v,(int,float)))]
pass_zero=all(abs(checks[k])<1e-5 for k in must_zero)
pass_camera=all(abs(v)<1e-5 for v in checks['rear_motor_camera_intersection_mm3'].values())
pass_dims=(checks['rear_motor_end_clearance_mm']>=2.0 and
           checks['motor_side_clearance_to_p0_wall_mm']>=1.0 and
           checks['motor_pair_gap_mm']>=0.8 and
           checks['sidegear_plus_cover_bearing_axial_package_mm'] <= checks['sidebay_depth_mm'] and
           checks['sidecover_outside_skin_after_6701_mm']>=1.0 and
           checks['x200_6701_to_side_oring_centerline_radial_margin_mm']>=8.0 and
           FACE <= R_CONE/3.0)
checks['pass_zero_unintended_collisions']=pass_zero
checks['pass_camera_clearance']=pass_camera
checks['pass_dimensional_rules']=pass_dims
checks['status']='PASS' if pass_zero and pass_camera and pass_dims else 'FAIL'

assy=cq.Assembly(name='PX1_X200_Drive_RevGJ')
assy.add(body,name='P0_Body_WithRearDriveTunnel')
assy.add(left_cover,name='SideCover_L')
assy.add(right_cover,name='SideCover_R')
assy.add(camera_low,name='LOW_Camera_Envelope')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_X200_Drive_RevGJ.step'))
for n in ['shaft_L','boss_L','pinion_shaft_L']:
    cq.exporters.export(parts[n],os.path.join(OUT,n+'.step'))
with open(os.path.join(OUT,'REV_GJ_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS': raise SystemExit(2)
