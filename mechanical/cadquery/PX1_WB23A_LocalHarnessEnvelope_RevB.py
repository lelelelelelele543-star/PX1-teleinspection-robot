import cadquery as cq
import math, json, os

# PX-1 Rev.B WB23A — photo/source-informed local camera harness envelope correction.
# Engineering validation only. NOT machining/procurement release.
# Scope is deliberately limited to the protected STATIC middle run on the lower lift arm.
# End flex zones remain FLEX_TEST_HOLD and are not falsely promoted to PASS.

OUT=os.path.abspath('build_wb23a'); os.makedirs(OUT,exist_ok=True)

# ---- hard architecture ----
PIPE_R=75.0; PIPE_Z=52.0480547
BODY_L=307.0; BODY_W=92.0; HALF_OUT=46.0; HALF_IN=34.0; Z0=8.0; ZTOP=90.0; REAR_END=358.0
WHEEL_X=(50.0,150.0,250.0); GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0; WHEEL_CENTER_Y=59.0; WHEEL_OD=90.0; WHEEL_W=16.0
GEAR_Y=42.0; GEAR_OD=52.0; GEAR_FACE=3.75
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]
DECK_HALF_W=38.0; ROOF_T=5.0

# ---- WB22A lift/camera baseline: unchanged ----
HEAD_R=26.0; HEAD_L=78.0
BOSS_OUTER_Y=34.0
YOKE_INNER_Y=35.0; YOKE_OUTER_Y=37.5; YOKE_CENTER_Y=36.25; YOKE_T=2.5
YOKE_R=29.0; YOKE_INNER_R=10.75
TILT_POD_OD=18.0; TILT_POD_X=56.0; TILT_WHEEL_Y=-16.75; WORM_CD=14.5
TILT_MIN=-105; TILT_MAX=105
BODY_PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=109.0; PIVOT_SEP=PIVOT_Z_HIGH-PIVOT_Z_LOW; PIVOT_AVG=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
LINK_L=90.0; CAM_AXIS_OFFSET_Z=2.0
ARM_Y=31.0; ARM_T=4.0; ARM_H=14.0
CAM_Z_LOW=75.0; CAM_Z_HIGH=185.0
LOW_CAM_X_TARGET=83.55688083875458
LOW_DZ=CAM_Z_LOW-CAM_AXIS_OFFSET_Z-PIVOT_AVG
LOW_THETA=math.asin(LOW_DZ/LINK_L)
LOW_END_X=BODY_PIVOT_X-LINK_L*math.cos(LOW_THETA)
CARRIER_X_OFFSET=LOW_END_X-LOW_CAM_X_TARGET
CROSSBAR_DX=48.0; CROSSBAR_DZ=30.0; CROSSBAR_X=8.0; CROSSBAR_Y=75.0; CROSSBAR_Z=5.0

# ---- WB23A local harness envelope ----
# Source basis: MiniCam CAB-002-461 is M12x1.5 for 3.5..5 mm cable; CRP300 source has a dedicated lift-arm cover.
# PX1 candidate gland is current LAPP SKINTOP MS-M M12x1.5 53112000 (3.5..7 mm), but it is not purchase-released here.
LOCAL_HARNESS_OD=5.0
LOCAL_HARNESS_R=LOCAL_HARNESS_OD/2.0
LOCAL_HARNESS_Y=25.5
STATIC_SETBACK=25.0
STATIC_LENGTH=LINK_L-2.0*STATIC_SETBACK
COVER_Y=25.5
COVER_T_Y=7.0
COVER_H_XZ=7.0
COVER_WALL_TARGET=1.0
GLAND_CANDIDATE='LAPP SKINTOP MS-M M12x1.5 53112000'
GLAND_CLAMP_RANGE=(3.5,7.0)
PROTOTYPE_CABLE_CANDIDATE='Autonics CID9S-2 donor cable / 8 insulated conductors + shield / approx OD5'

# ---- helpers ----
def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_x_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))
def cyl_between(p1,p2,r):
    a=cq.Vector(*p1); b=cq.Vector(*p2); v=b-a; L=v.Length
    return wp(cq.Solid.makeCylinder(r,L,a,v.normalized()))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def inter(a,b): return a.val().intersect(b.val()).Volume()
def prism_x(x0,pts,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts).close().extrude(length)
def ring_y_center(x,y,z,ro,ri,l):
    o=cyl_y_center(x,y,z,ro,l); i=cyl_y_center(x,y,z,ri,l+0.2)
    return wp(o.val().cut(i.val()))
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def radial_clear(part,tol=0.3):
    vv,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vv)
def floor_clear(part,tol=0.3):
    vv,_=part.val().tessellate(tol)
    return min(v.z-roof_top(v.x) for v in vv)
def link_plate(p1,p2,y,t=ARM_T,h=ARM_H):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=cq.Workplane('XZ').workplane(offset=y-t/2.0).slot2D(L,h,0).extrude(t)
    p=p.rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2.0,0,(z1+z2)/2.0))
def camera_moving(camx,camz):
    shell=cyl_x_center(camx,0,camz,HEAD_R,HEAD_L)
    bp=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,HEAD_R,camz),cq.Vector(0,1,0)))
    bn=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,-HEAD_R,camz),cq.Vector(0,-1,0)))
    pod=cyl_x_center(camx+12.0,TILT_WHEEL_Y,camz+WORM_CD,TILT_POD_OD/2.0,TILT_POD_X)
    return fuse_all([shell,bp,bn,pod])
def carrier_web(camx,camz,sign):
    pts=[(camx+18.0,camz-25.0),(camx+34.0,camz-18.0),(camx+52.0,camz+27.5),(camx+52.0,camz+32.5),(camx+44.0,camz+32.5),(camx+32.0,camz+14.0),(camx+24.0,camz+24.0),(camx+18.0,camz+24.0)]
    if sign>0: return cq.Workplane('XZ',origin=(0,YOKE_OUTER_Y,0)).polyline(pts).close().extrude(YOKE_T)
    return cq.Workplane('XZ',origin=(0,-YOKE_INNER_Y,0)).polyline(pts).close().extrude(YOKE_T)
def carrier_structural(camx,camz):
    yp=ring_y_center(camx,+YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    yn=ring_y_center(camx,-YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    cross=boxc(camx+CROSSBAR_DX,0,camz+CROSSBAR_DZ,CROSSBAR_X,CROSSBAR_Y,CROSSBAR_Z)
    return fuse_all([yp,yn,carrier_web(camx,camz,+1),carrier_web(camx,camz,-1),cross])

# ---- exact WB22A body / gears ----
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN); body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
wet=cq.Workplane('XZ',origin=(0,+DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W)
wetbb=wet.val().BoundingBox(); assert abs(wetbb.ymin+38.0)<1e-7 and abs(wetbb.ymax-38.0)<1e-7
body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0)); body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
rear_outer=box0(242.0,-40.0,22.0,REAR_END-242.0,80.0,46.0); body=fuse(body,rear_outer)
rear_cav=box0(246.0,-36.0,26.0,REAR_END-252.0,72.0,38.0); body=cut(body,rear_cav)
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]; body=fuse(body,prism_x(218,pod_outer_pts,89))
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]; body=cut(body,prism_x(221,pod_inner_pts,83))
body=cut(body,box0(224,-33,84,76,66,10))
gears=[cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2.0,GEAR_FACE) for s in (-1,1) for x in GEAR_X]
assert len(gears)==10

ref=camera_moving(0,0); rv,_=ref.val().tessellate(0.18)
MOVING_SWEEP_R=max(math.hypot(v.x,v.z) for v in rv)
th_low=math.asin((CAM_Z_LOW-CAM_AXIS_OFFSET_Z-PIVOT_AVG)/LINK_L)
th_high=math.asin((CAM_Z_HIGH-CAM_AXIS_OFFSET_Z-PIVOT_AVG)/LINK_L)

worst={'cable_vs_body_mm3':0.0,'cable_vs_Z50_mm3':0.0,'cable_vs_arms_mm3':0.0,'cable_vs_carrier_mm3':0.0,'cover_vs_body_mm3':0.0,'cover_vs_Z50_mm3':0.0,'cover_vs_arms_mm3':0.0,'cover_vs_carrier_mm3':0.0,'min_floor_cable_mm':1e9,'min_floor_cover_mm':1e9,'min_full_tilt_radial_margin_cable_mm':1e9,'min_full_tilt_radial_margin_cover_mm':1e9}
low={}; critical=None
SOLID_SAMPLES=43
for i in range(SOLID_SAMPLES):
    th=th_low+(th_high-th_low)*i/(SOLID_SAMPLES-1.0)
    u=(-math.cos(th),math.sin(th))
    lp=(BODY_PIVOT_X+LINK_L*u[0],PIVOT_Z_LOW+LINK_L*u[1]); up=(lp[0],lp[1]+PIVOT_SEP)
    b=(BODY_PIVOT_X+STATIC_SETBACK*u[0],LOCAL_HARNESS_Y,PIVOT_Z_LOW+STATIC_SETBACK*u[1])
    e=(lp[0]-STATIC_SETBACK*u[0],LOCAL_HARNESS_Y,lp[1]-STATIC_SETBACK*u[1])
    cable=cyl_between(b,e,LOCAL_HARNESS_R)
    cover=link_plate((b[0],b[2]),(e[0],e[2]),COVER_Y,t=COVER_T_Y,h=COVER_H_XZ)
    arms=[link_plate((BODY_PIVOT_X,PIVOT_Z_LOW),lp,s*ARM_Y) for s in (-1,1)] + [link_plate((BODY_PIVOT_X,PIVOT_Z_HIGH),up,s*ARM_Y) for s in (-1,1)]
    zcam=PIVOT_AVG+LINK_L*math.sin(th)+CAM_AXIS_OFFSET_Z; camx=lp[0]-CARRIER_X_OFFSET
    do_carrier=(i in (0,(SOLID_SAMPLES-1)//2,SOLID_SAMPLES-1)); carrier=carrier_structural(camx,zcam) if do_carrier else None
    cvb=inter(cable,body); cvg=max(inter(cable,g) for g in gears); cva=max(inter(cable,a) for a in arms); cvc=inter(cable,carrier) if do_carrier else 0.0
    ovb=inter(cover,body); ovg=max(inter(cover,g) for g in gears); ova=max(inter(cover,a) for a in arms); ovc=inter(cover,carrier) if do_carrier else 0.0
    worst['cable_vs_body_mm3']=max(worst['cable_vs_body_mm3'],cvb); worst['cable_vs_Z50_mm3']=max(worst['cable_vs_Z50_mm3'],cvg); worst['cable_vs_arms_mm3']=max(worst['cable_vs_arms_mm3'],cva); worst['cable_vs_carrier_mm3']=max(worst['cable_vs_carrier_mm3'],cvc)
    worst['cover_vs_body_mm3']=max(worst['cover_vs_body_mm3'],ovb); worst['cover_vs_Z50_mm3']=max(worst['cover_vs_Z50_mm3'],ovg); worst['cover_vs_arms_mm3']=max(worst['cover_vs_arms_mm3'],ova); worst['cover_vs_carrier_mm3']=max(worst['cover_vs_carrier_mm3'],ovc)
    worst['min_floor_cable_mm']=min(worst['min_floor_cable_mm'],floor_clear(cable)); worst['min_floor_cover_mm']=min(worst['min_floor_cover_mm'],floor_clear(cover))
    if i==0:
        low={'theta_deg':math.degrees(th),'static_start_xyz_mm':list(b),'static_end_xyz_mm':list(e),'cable_min_ideal_DN150_clearance_mm':radial_clear(cable),'cover_min_ideal_DN150_clearance_mm':radial_clear(cover),'cable_min_wetfloor_clearance_mm':floor_clear(cable),'cover_min_wetfloor_clearance_mm':floor_clear(cover)}

worst['min_full_tilt_radial_margin_cable_mm']=1e9; worst['min_full_tilt_radial_margin_cover_mm']=1e9; critical=None
for j in range(1001):
    th=th_low+(th_high-th_low)*j/1000.0; u=(-math.cos(th),math.sin(th))
    lp=(BODY_PIVOT_X+LINK_L*u[0],PIVOT_Z_LOW+LINK_L*u[1]); zcam=PIVOT_AVG+LINK_L*math.sin(th)+CAM_AXIS_OFFSET_Z; camx=lp[0]-CARRIER_X_OFFSET
    P=(BODY_PIVOT_X,PIVOT_Z_LOW); U=(u[0],u[1]); CAM=(camx,zcam)
    sproj=(CAM[0]-P[0])*U[0]+(CAM[1]-P[1])*U[1]; sclamp=max(STATIC_SETBACK,min(LINK_L-STATIC_SETBACK,sproj))
    q=(P[0]+sclamp*U[0],P[1]+sclamp*U[1]); centre_dist=math.hypot(q[0]-CAM[0],q[1]-CAM[1])
    cable_margin=centre_dist-LOCAL_HARNESS_R-MOVING_SWEEP_R; cover_margin=centre_dist-COVER_H_XZ/2.0-MOVING_SWEEP_R
    worst['min_full_tilt_radial_margin_cable_mm']=min(worst['min_full_tilt_radial_margin_cable_mm'],cable_margin); worst['min_full_tilt_radial_margin_cover_mm']=min(worst['min_full_tilt_radial_margin_cover_mm'],cover_margin)
    if critical is None or cover_margin<critical['cover_margin_mm']: critical={'theta_deg':math.degrees(th),'camera_axis_xz_mm':[camx,zcam],'nearest_static_s_mm':sclamp,'centreline_to_camera_axis_xz_mm':centre_dist,'cover_margin_mm':cover_margin,'cable_margin_mm':cable_margin}

collision_fields=[k for k in worst if '_vs_' in k]
static_ok=(all(worst[k]<1e-4 for k in collision_fields) and worst['min_floor_cable_mm']>=3.0 and worst['min_floor_cover_mm']>=3.0 and worst['min_full_tilt_radial_margin_cable_mm']>=2.0 and worst['min_full_tilt_radial_margin_cover_mm']>=2.0 and low['cable_min_ideal_DN150_clearance_mm']>=5.0 and low['cover_min_ideal_DN150_clearance_mm']>=5.0)
status='PASS_STATIC_PACKAGING / FLEX_TEST_HOLD / MANUFACTURING_HOLD / PROCUREMENT_HOLD' if static_ok else 'FAIL_STATIC_PACKAGING'
checks={'status':status,'architecture':{'wheel_stations_x_mm':list(WHEEL_X),'z50_total':10,'rear_drive_x_mm':250.0,'rule':'3 AXLES / 6 WHEELS HARD LOCK'},'wb22a_retained':{'body_pivot_x_mm':BODY_PIVOT_X,'pivot_z_mm':[PIVOT_Z_LOW,PIVOT_Z_HIGH],'link_length_mm':LINK_L,'arm_y_mm':ARM_Y,'arm_section_mm':[ARM_T,ARM_H],'carrier_axis_offset_x_mm':CARRIER_X_OFFSET},'source_basis':{'proteus_local_gland':'CAB-002-461 M12x1.5 d3.5-5mm in DRW-002-752 / DRW-002-745 / ASS-002-890','proteus_arm_protection':'FSS-003-127 LIFT ARM COVER in ASS-003-121 / DRW-003-121','interpretation':'source controls topology only; PX1 dimensions are independently validated'},'local_harness':{'max_target_OD_mm':LOCAL_HARNESS_OD,'centre_y_mm':LOCAL_HARNESS_Y,'static_setback_each_end_mm':STATIC_SETBACK,'protected_static_length_mm':STATIC_LENGTH,'conductor_allocation':'8 insulated conductors: 2x +12V, 2x GND, UART TX, UART RX, CVBS signal, CVBS return; shield is EMC only','prototype_cable_candidate':PROTOTYPE_CABLE_CANDIDATE,'prototype_cable_rule':'no manufacturer continuous-flex radius assumed; physical flex test mandatory before release'},'cover_envelope':{'centre_y_mm':COVER_Y,'outer_y_thickness_mm':COVER_T_Y,'outer_xz_height_mm':COVER_H_XZ,'nominal_wall_target_mm':COVER_WALL_TARGET},'body_ingress_candidate':{'article':GLAND_CANDIDATE,'thread':'M12x1.5','clamping_range_mm':list(GLAND_CLAMP_RANGE),'state':'candidate only; pressure boss/orientation and proof test remain HOLD'},'full_lift_screen':{'solid_samples':SOLID_SAMPLES,'theta_range_deg':[math.degrees(th_low),math.degrees(th_high)],**worst,'critical_full_tilt_clearance':critical},'low_dn150':low,'holds':['body-side flex chamber/path is not released','carrier-side flex chamber/path to fixed head connector is not released','prototype cable must be bought/measured and flex-cycled wet/grit before release','M12 pressure boss/gland orientation and +0.25 bar leak proof remain open','final cover screw heads/drainage/anti-snag details remain open']}
with open(os.path.join(OUT,'WB23A_EXECUTED.json'),'w',encoding='utf-8') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if not static_ok: raise SystemExit(2)
