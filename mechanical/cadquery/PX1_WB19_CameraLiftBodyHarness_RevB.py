import cadquery as cq
import math, json, os

# PX-1 Rev.B WB19 — camera + lift datum + crawler body + external head-harness integration screen
# Engineering validation only. NOT machining release.
# Corrects WB16's use of camera-axis motion as a proxy for the actual SP13 cable-exit motion.

OUT='/mnt/data/build_wb19'
os.makedirs(OUT, exist_ok=True)

# ---- hard architecture lock ----
PIPE_R=75.0
PIPE_Z=52.0480547
WHEEL_X=(50.0,150.0,250.0)
WHEEL_Z=45.0
WHEEL_CENTER_Y=59.0
WHEEL_OD=90.0
WHEEL_W=16.0

# ---- crawler body, copied from active Rev.PR screen ----
BODY_L=307.0
BODY_W=92.0
HALF_OUT=BODY_W/2
HALF_IN=34.0
Z0=8.0
ZTOP=90.0
FLOOR=6.0
DECK_HALF_W=38.0
ROOF_T=5.0
ROOF_PTS=[(0.0,38.0),(120.0,42.0),(200.0,77.0),(220.0,90.0)]
POD_X0=218.0
POD_X1=307.0
POD_TOP_Z=110.0

# ---- active Rev.FN lift datums used by WB16/WB18 ----
CAM_POS={
    'LOW':(83.557,75.0),
    'MID':(82.851,130.0),
    'HIGH':(135.200,205.0),
}
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=112.0
LINK_L=120.0
ARM_Y=26.0
ARM_T=5.0
ARM_H=18.0

# ---- WB18 camera hard envelope ----
HEAD_OD=52.0
HEAD_R=26.0
HEAD_L=78.0
BOSS_OUTER_Y=40.0
YOKE_CENTRE_Y=43.5
YOKE_T=5.5
YOKE_OUTER_Y=46.25
YOKE_R=29.0
YOKE_INNER_R=10.75
TILT_POD_OD=18.0
TILT_POD_X=56.0
TILT_WHEEL_Y=-16.75
WORM_CENTRE_DIST=14.5
TILT_MIN=-105.0
TILT_MAX=105.0

# WB18 structural rear bridge remains low and unchanged.
BRIDGE_DX=58.0
BRIDGE_DZ=20.0
BRIDGE_X=8.0
BRIDGE_Y=2*YOKE_OUTER_Y
BRIDGE_Z=10.0

# WEIPU envelopes from WB18/WB16
SP13_PANEL_OD=19.5
SP13_FRONT_L=9.5
SP13_REAR_OD=13.0
SP13_REAR_L=9.7
SP13_PLUG_OD=18.8
SP13_PLUG_L=49.0

# Current WB18 connector placement (for failure comparison)
CURRENT_PANEL_DX=62.0
CURRENT_AXIS_DZ=20.0

# WB19 candidate: keep +X connector axis and low structural bridge,
# but move the panel forward and upward on an integrated fixed-yoke support.
# This creates a controlled R55 S-bend before the Rev.PR controller saddle.
CANDIDATE_PANEL_DX=45.3
CANDIDATE_AXIS_DZ=37.25

# WB16 cable article / routing rule
CABLE_OD=6.7
CABLE_R=CABLE_OD/2
R_ROUTE=55.0
BODY_CLEAR_DESIGN=3.0
PIPE_CLEAR_DESIGN=5.0
LOW_ROUTE_Z=116.35
BODY_ANCHOR=(280.0, LOW_ROUTE_Z)  # fixed strain-relief / interface datum; article remains HOLD

# ---- helpers ----
def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_x_center(x,y,z,r,l): return cyl_x(x-l/2,y,z,r,l)
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def prism_x(x0,pts_yz,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts_yz).close().extrude(length)
def ring_y_center(x,y,z,ro,ri,l):
    outer=cyl_y_center(x,y,z,ro,l)
    inner=cyl_y_center(x,y,z,ri,l+0.2)
    return wp(outer.val().cut(inner.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def mesh_radial_required(part,tol=0.45):
    verts,_=part.val().tessellate(tol)
    if not verts: return 0.0
    return max(math.hypot(v.y, v.z-PIPE_Z) for v in verts)
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def body_top_central(x):
    if POD_X0 <= x <= POD_X1:
        return POD_TOP_Z
    if 0 <= x <= 220.0:
        return roof_top(x)
    return ZTOP

def rotate_y(part,camx,camz,deg):
    return part.rotate((camx,0,camz),(camx,1,camz),deg)

# ---- exact active Rev.PR pressure-body outer/cavity screen ----
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,Z0+FLOOR),(299.0,Z0+FLOOR),(299.0,85.0),(220.0,85.0),
            (200.0,72.0),(120.0,37.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
deck_poly=ROOF_PTS+[(220.0,105.0),(0.0,105.0)]
deck_cut=cq.Workplane('XZ',origin=(0,DECK_HALF_W,0)).polyline(deck_poly).close().extrude(2*DECK_HALF_W)
body=cut(body,deck_cut)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0))
body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
# Controller saddle from Rev.PR (this is the key WB19 obstacle).
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]
pod_outer=prism_x(218,pod_outer_pts,min(89.0,BODY_L-218.0)); body=fuse(body,pod_outer)
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]
pod_cav=prism_x(221,pod_inner_pts,min(83.0,BODY_L-224.0)); body=cut(body,pod_cav)
throat=box0(224,-33,84,min(76.0,BODY_L-224.0),66,10); body=cut(body,throat)

# ---- wheel architecture refs ----
wheels=[]
for side in (-1,1):
    for x in WHEEL_X:
        wheels.append((side,x,cyl_y_center(x,side*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)))
assert len(wheels)==6 and WHEEL_X==(50.0,150.0,250.0)

# ---- lift arms at an indexed position ----
def lift_points(camx,camz):
    # Active Rev.FN has parallel equal links and 20 mm pivot separation.
    return ((BODY_PIVOT_X,PIVOT_Z_LOW),(camx,PIVOT_Z_LOW+(camz-102.0)),
            (BODY_PIVOT_X,PIVOT_Z_HIGH),(camx,PIVOT_Z_HIGH+(camz-102.0)))

def link_plate(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    ang=math.degrees(math.atan2(dz,dx))
    length=math.hypot(dx,dz)
    plate=(cq.Workplane('XZ').workplane(offset=y-ARM_T/2)
           .slot2D(length,ARM_H,0).extrude(ARM_T))
    plate=plate.rotate((0,0,0),(0,1,0),-ang)
    plate=plate.translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))
    return plate

# ---- camera/yoke outer hard parts for a lift position ----
def camera_package(camx,camz,panel_dx,axis_dz,include_support=False):
    shell=cyl_x_center(camx,0,camz,HEAD_R,HEAD_L)
    boss_pos=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,HEAD_R,camz),cq.Vector(0,1,0)))
    boss_neg=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,-HEAD_R,camz),cq.Vector(0,-1,0)))
    tilt_pod=cyl_x_center(camx+12.0,TILT_WHEEL_Y,camz+WORM_CENTRE_DIST,TILT_POD_OD/2,TILT_POD_X)
    moving=fuse_all([shell,boss_pos,boss_neg,tilt_pod])

    yp=ring_y_center(camx,+YOKE_CENTRE_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    yn=ring_y_center(camx,-YOKE_CENTRE_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    bridge=boxc(camx+BRIDGE_DX,0,camz+BRIDGE_DZ,BRIDGE_X,BRIDGE_Y,BRIDGE_Z)

    panel_x=camx+panel_dx
    axis_z=camz+axis_dz
    sp13_front=cyl_x(panel_x,0,axis_z,SP13_PANEL_OD/2,SP13_FRONT_L)
    sp13_rear=cyl_x(panel_x-SP13_REAR_L,0,axis_z,SP13_REAR_OD/2,SP13_REAR_L)
    sp13_plug=cyl_x(panel_x+SP13_FRONT_L,0,axis_z,SP13_PLUG_OD/2,SP13_PLUG_L)
    fixed_parts=[yp,yn,bridge,sp13_front,sp13_rear,sp13_plug]

    # Exact support bracket is intentionally not part of the PASS condition yet.
    # It is a WB20 release item because any bracket can consume the narrow DN150 margin.
    if include_support:
        support1=boxc(camx+48.0,+8.0,camz+28.0,22.0,4.0,5.0).rotate((camx+48,+8,camz+28),(camx+48,+9,camz+28),-24)
        support2=boxc(camx+48.0,-8.0,camz+28.0,22.0,4.0,5.0).rotate((camx+48,-8,camz+28),(camx+48,-7,camz+28),-24)
        fixed_parts += [support1,support2]
    fixed=fuse_all(fixed_parts)
    outlet=(panel_x+SP13_FRONT_L+SP13_PLUG_L, axis_z)
    return moving,fixed,outlet,dict(panel_x=panel_x,axis_z=axis_z,bridge=bridge,sp13_front=sp13_front,sp13_rear=sp13_rear,sp13_plug=sp13_plug)

# ---- cable geometry math ----
def max_deflection_for_forward_run(dx,R=R_ROUTE):
    if dx<=0: return 0.0
    if dx>=R: return R
    return R-math.sqrt(R*R-dx*dx)

def required_forward_run_for_deflection(h,R=R_ROUTE):
    if h<0 or h>R: return None
    return math.sqrt(max(0.0,2*R*h-h*h))

def symmetric_s_curve(P,h,R=R_ROUTE,n=41):
    # Two equal opposite-curvature arcs. Start/end tangent +X; vertical offset h.
    sign=1.0 if h>=0 else -1.0
    hh=abs(h)
    if hh>2*R: raise ValueError('S offset exceeds 2R')
    theta=math.acos(1-hh/(2*R))
    pts=[]
    for i in range(n):
        t=theta*i/(n-1)
        x=P[0]+R*math.sin(t)
        z=P[1]+sign*R*(1-math.cos(t))
        pts.append((x,z))
    p1=pts[-1]
    for i in range(1,n):
        t=theta*i/(n-1)
        x=p1[0]+R*(math.sin(theta)-math.sin(theta-t))
        z=p1[1]+sign*R*(math.cos(theta-t)-math.cos(theta))
        pts.append((x,z))
    return pts,2*R*math.sin(theta),2*R*theta

def tangent_to_point_path(P,A,R=R_ROUTE,n_arc=50,n_line=50):
    # Start tangent +X, one R arc, then straight to a free-tangent fixed datum.
    best=None
    for s in (+1,-1):
        C=(P[0],P[1]+s*R)
        dx=A[0]-C[0]; dz=A[1]-C[1]; d=math.hypot(dx,dz)
        if d < R: continue
        ux,uz=dx/d,dz/d
        hh=math.sqrt(max(0,d*d-R*R))
        for q in (+1,-1):
            T=(C[0]+(R*R/d)*ux + q*(R*hh/d)*(-uz),
               C[1]+(R*R/d)*uz + q*(R*hh/d)*(ux))
            th0=math.atan2(P[1]-C[1],P[0]-C[0])
            tht=math.atan2(T[1]-C[1],T[0]-C[0])
            if s==1:
                delta=(tht-th0)%(2*math.pi)
                tang=(-math.sin(tht),math.cos(tht))
            else:
                delta=(th0-tht)%(2*math.pi)
                tang=(math.sin(tht),-math.cos(tht))
            lv=(A[0]-T[0],A[1]-T[1]); ll=math.hypot(*lv)
            dot=1 if ll<1e-12 else (tang[0]*lv[0]+tang[1]*lv[1])/ll
            if dot<0.999: continue
            total=R*delta+ll
            if delta > math.pi: continue
            rec=(total,s,C,T,delta,ll)
            if best is None or total<best[0]: best=rec
    if best is None: return None
    total,s,C,T,delta,ll=best
    th0=math.atan2(P[1]-C[1],P[0]-C[0])
    pts=[]
    for i in range(n_arc):
        f=i/(n_arc-1)
        th=th0 + (delta*f if s==1 else -delta*f)
        pts.append((C[0]+R*math.cos(th),C[1]+R*math.sin(th)))
    for i in range(1,n_line):
        f=i/(n_line-1)
        pts.append((T[0]+f*(A[0]-T[0]),T[1]+f*(A[1]-T[1])))
    return dict(points=pts,total_length_mm=total,turn_deg=math.degrees(delta),tangent_point=T)

def cable_pipe_clearance(points):
    return min(PIPE_R-abs(z-PIPE_Z)-CABLE_R for x,z in points)

def cable_body_clearance(points):
    vals=[]
    for x,z in points:
        if 0<=x<=BODY_L:
            vals.append(z-body_top_central(x)-CABLE_R)
    return min(vals) if vals else 1e9

# ---- current WB18 failure screen ----
lowx,lowz=CAM_POS['LOW']
_,current_fixed,current_outlet,_=camera_package(lowx,lowz,CURRENT_PANEL_DX,CURRENT_AXIS_DZ,False)
current_dx_to_pod=POD_X0-current_outlet[0]
current_deflect=max_deflection_for_forward_run(current_dx_to_pod)
required_center_over_pod=POD_TOP_Z+CABLE_R+BODY_CLEAR_DESIGN
current_required_rise=required_center_over_pod-current_outlet[1]
current_required_run=required_forward_run_for_deflection(current_required_rise)
current_side_required=39.0+CABLE_R+BODY_CLEAR_DESIGN
current_side_run=required_forward_run_for_deflection(current_side_required)

# ---- candidate LOW package and tilt sweep ----
low_moving,cand_fixed,cand_outlet,cand_parts=camera_package(lowx,lowz,CANDIDATE_PANEL_DX,CANDIDATE_AXIS_DZ,False)
min_moving_pipe=1e9; worst_angle=None; max_move_fixed=0.0
for deg in range(-105,106):
    m=rotate_y(low_moving,lowx,lowz,float(deg))
    clr=PIPE_R-mesh_radial_required(m,0.55)
    if clr<min_moving_pipe: min_moving_pipe=clr; worst_angle=deg
    iv=inter(m,cand_fixed)
    if iv>max_move_fixed: max_move_fixed=iv
cand_fixed_pipe=PIPE_R-mesh_radial_required(cand_fixed,0.45)

# Candidate LOW R55 S route to clear controller saddle, then horizontal to anchor.
h=LOW_ROUTE_Z-cand_outlet[1]
spts,srun,sarc=symmetric_s_curve(cand_outlet,h)
route_low=list(spts)
endx,endz=route_low[-1]
if BODY_ANCHOR[0] < endx: raise RuntimeError('body anchor before S-route end')
for i in range(1,81):
    f=i/80
    route_low.append((endx+f*(BODY_ANCHOR[0]-endx), endz))

# MID/HIGH free-route screens to the same fixed strain-relief datum.
position_routes={}
position_outlets={}
for name,(cx,cz) in CAM_POS.items():
    outlet=(cx+CANDIDATE_PANEL_DX+SP13_FRONT_L+SP13_PLUG_L, cz+CANDIDATE_AXIS_DZ)
    position_outlets[name]=outlet
    if name=='LOW':
        position_routes[name]=dict(points=route_low,total_length_mm=sarc+(BODY_ANCHOR[0]-endx),turn_deg='S +/- %.3f'%math.degrees(math.acos(1-abs(h)/(2*R_ROUTE))))
    else:
        position_routes[name]=tangent_to_point_path(outlet,BODY_ANCHOR)

route_metrics={}
for name,r in position_routes.items():
    pts=r['points']
    route_metrics[name]={
        'outlet_xz_mm':position_outlets[name],
        'screen_path_length_mm':r['total_length_mm'],
        'min_ideal_DN150_cable_clearance_mm':cable_pipe_clearance(pts) if name=='LOW' else None,
        'min_central_body_clearance_mm':cable_body_clearance(pts),
        'turn_screen':r.get('turn_deg'),
    }

outlet_displacements={}
base=position_outlets['LOW']
for name,p in position_outlets.items():
    outlet_displacements[name]={
        'dx_from_LOW_mm':p[0]-base[0],
        'dz_from_LOW_mm':p[1]-base[1],
        'distance_from_LOW_mm':math.hypot(p[0]-base[0],p[1]-base[1])
    }

architecture_ok=(len(wheels)==6 and WHEEL_X==(50.0,150.0,250.0))
current_routing_fail=(current_required_run is None or current_required_run>current_dx_to_pod)
candidate_low_ok=(
    cand_fixed_pipe>=5.0 and
    min_moving_pipe>=3.0 and
    max_move_fixed<1e-4 and
    route_metrics['LOW']['min_ideal_DN150_cable_clearance_mm']>=5.0 and
    route_metrics['LOW']['min_central_body_clearance_mm']>=2.999 and
    route_low[-1][0]<=BODY_ANCHOR[0]+1e-9
)
status='PASS_SCREEN / MANUFACTURING_HOLD' if architecture_ok and current_routing_fail and candidate_low_ok else 'FAIL_SCREEN'

checks={
    'status':status,
    'architecture':{
        'axles':3,'wheels_total':len(wheels),'wheel_x_mm':list(WHEEL_X),'drive_station_x_mm':250.0,
        'rule':'3 AXLES / 6 WHEELS HARD LOCK'
    },
    'wb16_correction':{
        'reason':'WB16 used camera-axis/head-pivot motion as proxy for actual SP13 cable-exit motion; WB19 uses actual connector offset',
        'current_WB18_SP13_cable_exit_offset_from_camera_axis_xz_mm':[CURRENT_PANEL_DX+SP13_FRONT_L+SP13_PLUG_L,CURRENT_AXIS_DZ],
        'actual_current_outlets_xz_mm':{
            k:[v[0]+CURRENT_PANEL_DX+SP13_FRONT_L+SP13_PLUG_L,v[1]+CURRENT_AXIS_DZ] for k,v in CAM_POS.items()
        },
        'candidate_outlet_displacement_from_LOW_mm':outlet_displacements,
    },
    'current_WB18_routing_failure':{
        'LOW_current_outlet_xz_mm':current_outlet,
        'controller_saddle_front_x_mm':POD_X0,
        'available_forward_run_before_saddle_mm':current_dx_to_pod,
        'max_R55_vertical_or_lateral_deflection_in_available_run_mm':current_deflect,
        'required_center_z_for_design_body_clearance_mm':required_center_over_pod,
        'required_vertical_rise_mm':current_required_rise,
        'minimum_forward_run_for_that_R55_rise_mm':current_required_run,
        'minimum_side_offset_for_design_saddle_clearance_mm':current_side_required,
        'minimum_forward_run_for_side_R55_offset_mm':current_side_run,
        'conclusion':'CURRENT WB18 SP13 POSITION CANNOT REACH THE DESIGN-CLEAR ROUTE AROUND/OVER Rev.PR SADDLE WITH R55 BEFORE X218'
    },
    'candidate_SP13':{
        'structural_bridge':'retained at WB18 DX +58 / DZ +20',
        'panel_offset_from_camera_axis_xz_mm':[CANDIDATE_PANEL_DX,CANDIDATE_AXIS_DZ],
        'LOW_panel_x_mm':cand_parts['panel_x'],
        'LOW_axis_z_mm':cand_parts['axis_z'],
        'LOW_cable_outlet_xz_mm':cand_outlet,
        'fixed_package_min_ideal_DN150_clearance_mm':cand_fixed_pipe,
        'moving_camera_min_ideal_DN150_clearance_mm':min_moving_pipe,
        'moving_camera_worst_tilt_deg':worst_angle,
        'max_moving_vs_candidate_fixed_collision_mm3':max_move_fixed,
        'interpretation':'SP13 remains fixed to non-TILT yoke support and keeps +X cable axis; only support position changes'
    },
    'R55_harness_screen':{
        'cable':'LAPP 0027429 UNITRONIC FD CY 7X0.25',
        'OD_mm':CABLE_OD,
        'design_min_bend_radius_mm':R_ROUTE,
        'LOW_route_target_z_mm':LOW_ROUTE_Z,
        'LOW_S_curve_horizontal_run_mm':srun,
        'LOW_S_curve_arc_length_mm':sarc,
        'fixed_strain_relief_screen_xz_mm':BODY_ANCHOR,
        'position_routes':route_metrics,
        'note':'LOW uses an R55 S-route to become horizontal before the Rev.PR saddle; MID/HIGH are free R55 tangent-route screens. Final constant cut length and clamp/guide details remain physical-jig HOLD.'
    },
    'release_holds':[
        'Rev.PF physical/detail dimensions still block machining release of exact CRP150 lift arm geometry',
        'candidate SP13 support bracket must be detailed with real fasteners and stiffness check',
        'body-side harness strain-relief/feedthrough article and sealed mounting boss are not frozen',
        'LOW cable guide/saddle material and wear geometry must be selected and wet-cycle tested',
        'constant final cable cut length must be solved on physical LOW/MID/HIGH lift jig; do not freeze from shortest-path screens',
        'actual LAPP 0027429 OD and bend behavior must be measured',
        'real SP13 dimensions and moulded strain relief must be measured',
        'physical DN150 tube sweep with wheel profile, pipe ovality/debris allowance and fastener heads',
        'WB18 camera component physical-sample holds remain active'
    ],
    'execution':{'engine':'CadQuery 2.8.0','model':'WB19','type':'hard-part solid + analytic R55 centerline integration screen'}
}

# ---- assembly export, LOW candidate ----
assy=cq.Assembly(name='PX1_WB19_CAMERA_LIFT_BODY_HARNESS')
assy.add(body,name='RevPR_Body')
for side,x,w in wheels: assy.add(w,name=f'Wheel_S{side:+d}_X{int(x)}')
camx,camz=CAM_POS['LOW']
mid=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
s=(camz-2.0-mid)/LINK_L
th=math.asin(s)
dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
q1=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz); q2=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
for yy in (-ARM_Y,ARM_Y):
    assy.add(link_plate((BODY_PIVOT_X,PIVOT_Z_LOW),q1,yy),name=f'LiftLower_{yy:+.0f}')
    assy.add(link_plate((BODY_PIVOT_X,PIVOT_Z_HIGH),q2,yy),name=f'LiftUpper_{yy:+.0f}')
assy.add(low_moving,name='WB18_MovingCamera_Tilt0')
assy.add(cand_fixed,name='WB19_FixedYoke_SP13_Candidate')

assy.save(os.path.join(OUT,'PX1_WB19_CAMERA_LIFT_BODY_HARNESS.step'))
with open(os.path.join(OUT,'REV_B_WB19_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if status.startswith('FAIL'): raise SystemExit(2)
