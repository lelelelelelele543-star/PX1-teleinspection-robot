import cadquery as cq
import math, json, os

# PX-1 Rev.B WB23G — six-core local camera/lift harness packaging correction.
# Validation screen only. Not machining/procurement release.
OUT=os.path.abspath('build_wb23g'); os.makedirs(OUT, exist_ok=True)

PIPE_R=75.0; PIPE_Z=52.0480547
BODY_L=307.0; BODY_W=92.0; HALF_OUT=46.0; HALF_IN=34.0; Z0=8.0; ZTOP=90.0; REAR_END=358.0
WHEEL_X=(50.0,150.0,250.0); GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0; WHEEL_CENTER_Y=59.0; WHEEL_OD=90.0; WHEEL_W=16.0
GEAR_Y=42.0; GEAR_OD=52.0; GEAR_FACE=3.75
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]
DECK_HALF_W=38.0; ROOF_T=5.0
BODY_PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=109.0; PIVOT_AVG=100.5
LINK_L=90.0; ARM_Y=31.0; ARM_T=4.0; ARM_H=14.0; CAM_AXIS_OFFSET_Z=2.0
CAM_ZS={'LOW':75.0,'MID':130.0,'HIGH':185.0}
LOW_CAM_X_TARGET=83.55688083875458
LOW_DZ=CAM_ZS['LOW']-CAM_AXIS_OFFSET_Z-PIVOT_AVG
LOW_THETA=math.asin(LOW_DZ/LINK_L)
LOW_END_X=BODY_PIVOT_X-LINK_L*math.cos(LOW_THETA)
CARRIER_X_OFFSET=LOW_END_X-LOW_CAM_X_TARGET
HEAD_R=26.0; HEAD_L=78.0; BOSS_OUTER_Y=34.0; TILT_POD_OD=18.0; TILT_WHEEL_Y=-16.75; WORM_CD=14.5; TILT_POD_X=56.0

# WB23E service-cover geometry retained exactly.
COVER_CX=261.0; COVER_CY=0.0; COVER_Z0=110.0; COVER_L=86.0; COVER_W=44.0; COVER_T=6.0
OPEN_L=48.0; OPEN_W=22.0
SCREW_X=(226.0,296.0); SCREW_Y=0.0; SCREW_HOLE_D=4.5; SCREW_HEAD_D=8.0; SCREW_HEAD_H=3.0
GROOVE_OFFSET_FROM_OPEN=4.0; GROOVE_W=2.5
PRESSURE_PORT_CX=273.0; PRESSURE_PORT_CY=0.0; PRESSURE_PORT_OD=14.0; PRESSURE_PORT_H=6.0
GLAND_OD=17.6; GLAND_AXIS_Y=12.0; GLAND_AXIS_Z=103.0; GLAND_X_FRONT=205.0; GLAND_X_REAR=231.5

# WB23G correction: exactly six insulated conductors, one per camera function.
HARNESS_CORES=6
CONDUCTOR_TARGET_MM2=0.25
HARNESS_OD_MAX=6.5
HARNESS_OD_PREFERRED=(5.5,6.0)
HARNESS_Y=25.5
GUARD_OD=10.0
ARM_RUN=(20.0,72.0)
DRY_CONNECTOR='Molex Micro-Fit 3.0 43025-0600 + 43020-0601'
DRY_CONNECTOR_L=14.0
DRY_CONNECTOR_W_SCREEN=12.0
FUNCTIONS=['+12V_HEAD','GND_HEAD','UART_TX','UART_RX','CVBS_SIGNAL','CVBS_RETURN']

def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,h): return wp(cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cyl_x_between(x0,x1,y,z,r):
    a=min(x0,x1); L=abs(x1-x0)
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(a,y,z),cq.Vector(1,0,0)))
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
def radial_clear(part,tol=0.3):
    vv,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vv)
def plate_segment(p1,p2,y,t=ARM_T,h=ARM_H):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=boxc(0,y,0,L,t,h)
    p=p.rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2.0,0,(z1+z2)/2.0))
def theta_for(zcam): return math.asin((zcam-CAM_AXIS_OFFSET_Z-PIVOT_AVG)/LINK_L)
def end_pivots(zcam):
    th=theta_for(zcam); dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
    return (BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz),(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
def cam_x_for(zcam): return end_pivots(zcam)[0][0]-CARRIER_X_OFFSET
def camera_outer(camx,camz):
    shell=wp(cq.Solid.makeCylinder(HEAD_R,HEAD_L,cq.Vector(camx-HEAD_L/2,0,camz),cq.Vector(1,0,0)))
    bp=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,HEAD_R,camz),cq.Vector(0,1,0)))
    bn=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,-HEAD_R,camz),cq.Vector(0,-1,0)))
    pod=wp(cq.Solid.makeCylinder(TILT_POD_OD/2,TILT_POD_X,cq.Vector(camx+12-TILT_POD_X/2,TILT_WHEEL_Y,camz+WORM_CD),cq.Vector(1,0,0)))
    return wp(shell.val().fuse(bp.val()).fuse(bn.val()).fuse(pod.val()))

# Exact corrected WB22A body / WB23E opening.
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN); body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
wet=cq.Workplane('XZ',origin=(0,+DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W)
wetbb=wet.val().BoundingBox(); assert abs(wetbb.ymin+38)<1e-7 and abs(wetbb.ymax-38)<1e-7
body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0)); body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
rear_outer=box0(242.0,-40.0,22.0,REAR_END-242.0,80.0,46.0); body=fuse(body,rear_outer)
rear_cav=box0(246.0,-36.0,26.0,REAR_END-252.0,72.0,38.0); body=cut(body,rear_cav)
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]; body=fuse(body,prism_x(218,pod_outer_pts,89))
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]; body=cut(body,prism_x(221,pod_inner_pts,83))
body=cut(body,box0(224,-33,84,76,66,10)); assert body.val().isValid()
service_open=boxc(COVER_CX,0,108.0,OPEN_L,OPEN_W,8.0); body_with_service=cut(body,service_open); assert body_with_service.val().isValid()

wheels=[cyl_y_center(x,s*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W) for s in (-1,1) for x in WHEEL_X]
gears=[cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE) for s in (-1,1) for x in GEAR_X]
assert len(wheels)==6 and len(gears)==10
cover=boxc(COVER_CX,0,COVER_Z0+COVER_T/2,COVER_L,COVER_W,COVER_T)
port=cyl_z(PRESSURE_PORT_CX,0,COVER_Z0+COVER_T,PRESSURE_PORT_OD/2,PRESSURE_PORT_H)
gland=cyl_x_between(GLAND_X_FRONT,GLAND_X_REAR,GLAND_AXIS_Y,GLAND_AXIS_Z,GLAND_OD/2)
heads=[cyl_z(x,SCREW_Y,COVER_Z0+COVER_T,SCREW_HEAD_D/2,SCREW_HEAD_H) for x in SCREW_X]
fixed=[('cover',cover),('pressure_port',port),('gland',gland)]+[(f'M4_head_{i+1}',h) for i,h in enumerate(heads)]

open_x0=COVER_CX-OPEN_L/2; open_x1=COVER_CX+OPEN_L/2; open_y0=-OPEN_W/2; open_y1=OPEN_W/2
cover_x0=COVER_CX-COVER_L/2; cover_x1=COVER_CX+COVER_L/2
opening_inside_pod=(open_x0>=218 and open_x1<=307 and open_y0>=-32.5 and open_y1<=32.5)
cover_supported_by_pod=(cover_x0>=218 and cover_x1<=307)
gland_crosses_front_wall=(min(GLAND_X_FRONT,GLAND_X_REAR)<218<max(GLAND_X_FRONT,GLAND_X_REAR))
groove_outer_half_x=OPEN_L/2+GROOVE_OFFSET_FROM_OPEN+GROOVE_W/2; groove_outer_half_y=OPEN_W/2+GROOVE_OFFSET_FROM_OPEN+GROOVE_W/2
screw_hole_r=SCREW_HOLE_D/2
screw_to_groove_web=min(abs(x-COVER_CX)-groove_outer_half_x-screw_hole_r for x in SCREW_X)
head_to_cover_edge=min(COVER_L/2-abs(x-COVER_CX)-SCREW_HEAD_D/2 for x in SCREW_X)
groove_to_cover_edge_y=COVER_W/2-groove_outer_half_y
dry_connector_fits_opening=(DRY_CONNECTOR_L<=OPEN_L and DRY_CONNECTOR_W_SCREEN<=OPEN_W)

worst={'fixed_vs_Z50_mm3':0.0,'fixed_vs_wheels_mm3':0.0,'fixed_vs_lift_arms_mm3':0.0,'fixed_vs_camera_outer_mm3':0.0,'guard_vs_fixed_mm3':0.0,'guard_vs_Z50_mm3':0.0,'guard_vs_camera_mm3':0.0}
states={}
for name,zcam in CAM_ZS.items():
    lp,up=end_pivots(zcam)
    arms=[plate_segment((BODY_PIVOT_X,PIVOT_Z_LOW),lp,s*ARM_Y) for s in (-1,1)] + [plate_segment((BODY_PIVOT_X,PIVOT_Z_HIGH),up,s*ARM_Y) for s in (-1,1)]
    cam=camera_outer(cam_x_for(zcam),zcam); th=theta_for(zcam)
    def arm_point(s): return (BODY_PIVOT_X-s*math.cos(th),HARNESS_Y,PIVOT_Z_LOW+s*math.sin(th))
    a=arm_point(ARM_RUN[0]); b=arm_point(ARM_RUN[1]); guard=cyl_between(a,b,GUARD_OD/2)
    fixed_arm=max(inter(fp,a_) for _,fp in fixed for a_ in arms); fixed_cam=max(inter(fp,cam) for _,fp in fixed)
    guard_fixed=max(inter(guard,fp) for _,fp in fixed); guard_gear=max(inter(guard,g) for g in gears); guard_cam=inter(guard,cam)
    worst['fixed_vs_lift_arms_mm3']=max(worst['fixed_vs_lift_arms_mm3'],fixed_arm); worst['fixed_vs_camera_outer_mm3']=max(worst['fixed_vs_camera_outer_mm3'],fixed_cam)
    worst['guard_vs_fixed_mm3']=max(worst['guard_vs_fixed_mm3'],guard_fixed); worst['guard_vs_Z50_mm3']=max(worst['guard_vs_Z50_mm3'],guard_gear); worst['guard_vs_camera_mm3']=max(worst['guard_vs_camera_mm3'],guard_cam)
    states[name]={'camera_axis_xz_mm':[cam_x_for(zcam),zcam],'guard_dn150_clearance_mm':radial_clear(guard),'guard_vs_camera_mm3':guard_cam,'guard_vs_Z50_mm3':guard_gear}
worst['fixed_vs_Z50_mm3']=max(inter(fp,g) for _,fp in fixed for g in gears); worst['fixed_vs_wheels_mm3']=max(inter(fp,w) for _,fp in fixed for w in wheels)
fixed_dn150={n:radial_clear(p) for n,p in fixed}
collision_ok=all(v<1e-4 for v in worst.values())
checks_ok=(body_with_service.val().isValid() and opening_inside_pod and cover_supported_by_pod and gland_crosses_front_wall and screw_to_groove_web>=3.0 and head_to_cover_edge>=3.0 and groove_to_cover_edge_y>=4.0 and dry_connector_fits_opening and collision_ok and min(fixed_dn150.values())>=3.0 and states['LOW']['guard_dn150_clearance_mm']>=5.0)
status='PASS_SIX_CORE_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / CABLE_SAMPLE_HOLD / PROCUREMENT_HOLD' if checks_ok else 'FAIL_SIX_CORE_PACKAGING_SCREEN'

rho=0.0175
peak_A=2.92
voltage_drop={}
for L in (0.4,0.5,0.6):
    loop_R=rho*(2*L)/CONDUCTOR_TARGET_MM2
    drop=peak_A*loop_R
    voltage_drop[f'{L:.1f}m']={'loop_R_ohm':loop_R,'drop_V_20C':drop,'drop_percent_12V':100*drop/12.0,'drop_V_plus20pct_R':drop*1.2,'drop_percent_plus20pct_R':100*drop*1.2/12.0}

result={
 'status':status,
 'architecture':{'wheels':len(wheels),'z50_gears':len(gears),'body_pivot_x_mm':BODY_PIVOT_X,'wb23e_service_cover_retained':True},
 'local_harness':{'insulated_cores':HARNESS_CORES,'functions':FUNCTIONS,'shield':'overall EMC shield only; never DC return','target_conductor_mm2':CONDUCTOR_TARGET_MM2,'hard_max_OD_mm':HARNESS_OD_MAX,'preferred_OD_mm':list(HARNESS_OD_PREFERRED),'guard_envelope_OD_mm':GUARD_OD},
 'dry_service_connector':{'candidate':DRY_CONNECTOR,'screen_envelope_LxW_mm':[DRY_CONNECTOR_L,DRY_CONNECTOR_W_SCREEN],'fits_48x22_opening':dry_connector_fits_opening},
 'fixed_dn150_clearance_mm':fixed_dn150,
 'lift_states':states,
 'worst_unintended_collision_mm3':worst,
 'seal_land':{'minimum_screw_hole_to_groove_web_mm':screw_to_groove_web,'minimum_screw_head_to_cover_edge_mm':head_to_cover_edge,'minimum_groove_to_cover_y_edge_mm':groove_to_cover_edge_y},
 'voltage_drop_screen':{'peak_current_A':peak_A,'copper_resistivity_assumed_ohm_mm2_per_m':rho,'note':'screen only; purchased cable core resistance must be measured',**voltage_drop},
 'release_note':'Six-core topology is controlled. Cable article, flex life, actual resistance, shield termination and connector contacts remain qualification/procurement HOLD.'
}
with open(os.path.join(OUT,'REV_B_WB23G_VALIDATION.json'),'w',encoding='utf-8') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
if not checks_ok: raise SystemExit(2)
