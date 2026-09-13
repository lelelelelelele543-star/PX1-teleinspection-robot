import cadquery as cq
import math, json, os

# PX-1 Rev.B WB22A — photo-informed lift/camera integration correction.
# Engineering validation only. NOT machining/procurement release.
# Corrects two omissions in WB20/WB21:
#   1) WB20 wet-bay cut was extruded in the wrong Y direction in one audit model.
#   2) WB21 put four-bar end pivots effectively on the TILT axis, causing arm/head collisions.
# New logic: body -> four-bar -> rigid fixed head carrier -> sealed TILT camera.

OUT=os.path.abspath('build_wb22a'); os.makedirs(OUT, exist_ok=True)

# --- hard architecture lock ---
PIPE_R=75.0; PIPE_Z=52.0480547
BODY_L=307.0; BODY_W=92.0; HALF_OUT=46.0; HALF_IN=34.0; Z0=8.0; ZTOP=90.0; REAR_END=358.0
WHEEL_X=(50.0,150.0,250.0); GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0; WHEEL_CENTER_Y=59.0; WHEEL_OD=90.0; WHEEL_W=16.0
GEAR_Y=42.0; GEAR_OD=52.0; GEAR_FACE=3.75; GEAR_INNER_FACE=GEAR_Y-GEAR_FACE/2.0
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]
DECK_HALF_W=38.0; ROOF_T=5.0

# --- camera retained from WB20/WB21 ---
HEAD_R=26.0; HEAD_L=78.0
BOSS_OUTER_Y=34.0
YOKE_INNER_Y=35.0; YOKE_OUTER_Y=37.5; YOKE_CENTER_Y=36.25; YOKE_T=2.5
YOKE_R=29.0; YOKE_INNER_R=10.75
TILT_POD_OD=18.0; TILT_POD_X=56.0; TILT_WHEEL_Y=-16.75; WORM_CD=14.5
TILT_MIN=-105; TILT_MAX=105; TILT_STEP=1

# --- corrected lift ---
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=109.0          # WB21 112 -> 109: restores dirty-service clearance while retaining a 3 mm vertical plate gap
PIVOT_SEP=PIVOT_Z_HIGH-PIVOT_Z_LOW
PIVOT_AVG=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
LINK_L=90.0                 # shorter than WB21 120; allows physical carrier behind head
CAM_AXIS_OFFSET_Z=2.0
ARM_Y=31.0
ARM_T=4.0
ARM_H=14.0
CAM_ZS={'LOW':75.0,'MID':130.0,'HIGH':185.0}
LOW_CAM_X_TARGET=83.55688083875458   # preserve WB20 LOW optical-axis X

# Carrier X offset is derived, not guessed: preserve LOW camera axis while keeping parallel four-bar.
LOW_DZ=CAM_ZS['LOW']-CAM_AXIS_OFFSET_Z-PIVOT_AVG
LOW_THETA=math.asin(LOW_DZ/LINK_L)
LOW_END_X=BODY_PIVOT_X-LINK_L*math.cos(LOW_THETA)
CARRIER_X_OFFSET=LOW_END_X-LOW_CAM_X_TARGET

# Fixed carrier: side cheeks live outside moving head; rear upper tie is outside full swept head radius.
CROSSBAR_DX=48.0
CROSSBAR_DZ=30.0
CROSSBAR_X=8.0; CROSSBAR_Y=75.0; CROSSBAR_Z=5.0
PIVOT_PIN_D=8.0

# Gas spring screen (Proteus source logic: one 150 N spring).
GAS_ARTICLE='ACE GS-12-20-V4A'
GAS_FORCE_N=150.0; GAS_BODY_OD=12.0; GAS_ROD_OD=4.0; GAS_STROKE=20.0; GAS_EXTENDED=72.0
GAS_RETRACTED=GAS_EXTENDED-GAS_STROKE
GAS_BASE=(195.0,84.0)
GAS_ATTACH_FROM_LOWER_PIVOT=62.5
GAS_CENTER_Y=0.0

# --- helpers ---
def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
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
def radial_clear(part,tol=0.25):
    vv,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vv)
def floor_clear_mesh(part,tol=0.25):
    vv,_=part.val().tessellate(tol)
    return min(v.z-roof_top(v.x) for v in vv)

def theta_for(zcam):
    return math.asin((zcam-CAM_AXIS_OFFSET_Z-PIVOT_AVG)/LINK_L)
def end_pivots(zcam):
    th=theta_for(zcam); dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
    return (BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz),(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
def cam_x_for(zcam):
    lp,_=end_pivots(zcam); return lp[0]-CARRIER_X_OFFSET

def link_plate(p1,p2,y):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=cq.Workplane('XZ').workplane(offset=y-ARM_T/2).slot2D(L,ARM_H,0).extrude(ARM_T)
    p=p.rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))

def camera_moving(camx,camz):
    shell=cyl_x_center(camx,0,camz,HEAD_R,HEAD_L)
    bp=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,HEAD_R,camz),cq.Vector(0,1,0)))
    bn=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,-HEAD_R,camz),cq.Vector(0,-1,0)))
    pod=cyl_x_center(camx+12.0,TILT_WHEEL_Y,camz+WORM_CD,TILT_POD_OD/2,TILT_POD_X)
    return fuse_all([shell,bp,bn,pod])

def carrier_web(camx,camz,sign):
    # Photo-informed fixed side carrier, deliberately outside |Y|=34 moving-head envelope.
    pts=[
        (camx+18.0,camz-25.0),
        (camx+34.0,camz-18.0),
        (camx+52.0,camz+27.5),
        (camx+52.0,camz+32.5),
        (camx+44.0,camz+32.5),
        (camx+32.0,camz+14.0),
        (camx+24.0,camz+24.0),
        (camx+18.0,camz+24.0),
    ]
    if sign>0:
        return cq.Workplane('XZ',origin=(0,YOKE_OUTER_Y,0)).polyline(pts).close().extrude(YOKE_T)
    return cq.Workplane('XZ',origin=(0,-YOKE_INNER_Y,0)).polyline(pts).close().extrude(YOKE_T)

def carrier_parts(camx,camz,lp,up):
    yp=ring_y_center(camx,+YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    yn=ring_y_center(camx,-YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    wp_=carrier_web(camx,camz,+1); wn=carrier_web(camx,camz,-1)
    cross=boxc(camx+CROSSBAR_DX,0,camz+CROSSBAR_DZ,CROSSBAR_X,CROSSBAR_Y,CROSSBAR_Z)
    structural=fuse_all([yp,yn,wp_,wn,cross])
    pins=[]
    for s in (-1,1):
        for px,pz in (lp,up):
            # from arm plate across the 2 mm service gap and through 3 mm carrier cheek
            if s>0:
                ya=ARM_Y-ARM_T/2.0; yb=YOKE_OUTER_Y+0.5
            else:
                ya=-(YOKE_OUTER_Y+0.5); yb=-(ARM_Y-ARM_T/2.0)
            pins.append(cyl_y_center(px,(ya+yb)/2.0,pz,PIVOT_PIN_D/2.0,yb-ya))
    all_fixed=fuse_all([structural]+pins)
    return structural,pins,all_fixed

# --- corrected body (exact WB20 logic, but wet cut is centered correctly) ---
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
# XZ plane positive extrusion runs toward -Y. Start at +38 to finish at -38.
wet=cq.Workplane('XZ',origin=(0,+DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W)
wetbb=wet.val().BoundingBox()
assert abs(wetbb.ymin+DECK_HALF_W)<1e-7 and abs(wetbb.ymax-DECK_HALF_W)<1e-7
body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0)); body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
rear_outer=box0(242.0,-40.0,22.0,REAR_END-242.0,80.0,46.0); body=fuse(body,rear_outer)
rear_cav=box0(246.0,-36.0,26.0,REAR_END-252.0,72.0,38.0); body=cut(body,rear_cav)
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]; body=fuse(body,prism_x(218,pod_outer_pts,89))
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]; body=cut(body,prism_x(221,pod_inner_pts,83))
body=cut(body,box0(224,-33,84,76,66,10))

wheels=[(s,x,cyl_y_center(x,s*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)) for s in (-1,1) for x in WHEEL_X]
gears=[(s,x,cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE)) for s in (-1,1) for x in GEAR_X]
assert len(wheels)==6 and len(gears)==10

# --- moving-head radial invariants for all-angle collision proof ---
ref_moving=camera_moving(0,0)
mv,_=ref_moving.val().tessellate(0.18)
MOVING_SWEEP_R=max(math.hypot(v.x,v.z) for v in mv)
# Shell/pod Y extents are invariant under Y-axis TILT rotation.
SHELL_Y=HEAD_R
POD_Y_MIN=TILT_WHEEL_Y-TILT_POD_OD/2.0
POD_Y_MAX=TILT_WHEEL_Y+TILT_POD_OD/2.0

states={}
overall_tilt_pipe=1e9; overall_tilt_floor=1e9
all_ok=True
for name,zcam in CAM_ZS.items():
    th=theta_for(zcam); lp,up=end_pivots(zcam); camx=cam_x_for(zcam)
    arms=[link_plate((BODY_PIVOT_X,PIVOT_Z_LOW),lp,s*ARM_Y) for s in (-1,1)] + [link_plate((BODY_PIVOT_X,PIVOT_Z_HIGH),up,s*ARM_Y) for s in (-1,1)]
    structural,pins,fixed=carrier_parts(camx,zcam,lp,up)
    moving=camera_moving(camx,zcam)

    # Hard collision checks that do not involve intended pivot-pin/arm contact.
    arm_body=max(inter(a,body) for a in arms)
    arm_gear=max(inter(a,g) for a in arms for _,_,g in gears)
    arm_struct=max(inter(a,structural) for a in arms)
    fixed_body=inter(fixed,body)
    fixed_gear=max(inter(fixed,g) for _,_,g in gears)

    # All-angle arm/head proof: shell and pod separated in Y; boss can share Y but arm endpoint is outside boss XZ disc.
    arm_y_shell_gap=ARM_Y-ARM_T/2.0-SHELL_Y
    neg_arm_to_pod_gap=abs(-ARM_Y+ARM_T/2.0-POD_Y_MIN)
    # endpoint pivot radial distance from camera axis minus arm end radius versus 10 mm boss radius
    end_rel=[(lp[0]-camx,lp[1]-zcam),(up[0]-camx,up[1]-zcam)]
    arm_to_boss_radial_gap=min(math.hypot(dx,dz)-ARM_H/2.0-10.0 for dx,dz in end_rel)

    # Fixed carrier all-angle proof.
    carrier_side_y_gap=YOKE_INNER_Y-BOSS_OUTER_Y
    # nearest XZ distance from camera axis to rear crossbar rectangle
    xmin=CROSSBAR_DX-CROSSBAR_X/2.0; xmax=CROSSBAR_DX+CROSSBAR_X/2.0
    zmin=CROSSBAR_DZ-CROSSBAR_Z/2.0; zmax=CROSSBAR_DZ+CROSSBAR_Z/2.0
    xnear=0.0 if xmin<=0<=xmax else min(abs(xmin),abs(xmax))
    znear=0.0 if zmin<=0<=zmax else min(abs(zmin),abs(zmax))
    crossbar_sweep_gap=math.hypot(xnear,znear)-MOVING_SWEEP_R

    # Exact 1-degree TILT mesh screen against ideal DN150 and wet floor.
    verts,_=moving.val().tessellate(0.18)
    rel=[(v.x-camx,v.y,v.z-zcam) for v in verts]
    min_pipe=1e9; min_floor=1e9; worst_pipe=None; worst_floor=None
    for deg in range(TILT_MIN,TILT_MAX+1,TILT_STEP):
        a=math.radians(deg); c=math.cos(a); s=math.sin(a)
        mp=1e9; mf=1e9
        for dx,y,dz in rel:
            x=camx+dx*c+dz*s; z=zcam-dx*s+dz*c
            pc=PIPE_R-math.hypot(y,z-PIPE_Z)
            fc=z-roof_top(x)
            mp=min(mp,pc); mf=min(mf,fc)
        if mp<min_pipe: min_pipe=mp; worst_pipe=deg
        if mf<min_floor: min_floor=mf; worst_floor=deg
    overall_tilt_pipe=min(overall_tilt_pipe,min_pipe); overall_tilt_floor=min(overall_tilt_floor,min_floor)

    arm_pipe=min(radial_clear(a) for a in arms) if name=='LOW' else None
    carrier_pipe=radial_clear(fixed) if name=='LOW' else None
    carrier_floor=floor_clear_mesh(fixed)

    # Gas spring at this lift state.
    ax=BODY_PIVOT_X-GAS_ATTACH_FROM_LOWER_PIVOT*math.cos(th)
    az=PIVOT_Z_LOW+GAS_ATTACH_FROM_LOWER_PIVOT*math.sin(th)
    bx,bz=GAS_BASE
    gas=cyl_between((bx,GAS_CENTER_Y,bz),(ax,GAS_CENTER_Y,az),GAS_BODY_OD/2.0)
    gas_len=math.hypot(ax-bx,az-bz)
    fx=GAS_FORCE_N*(ax-bx)/gas_len; fz=GAS_FORCE_N*(az-bz)/gas_len
    gas_torque=(fx*GAS_ATTACH_FROM_LOWER_PIVOT*math.sin(th)+fz*GAS_ATTACH_FROM_LOWER_PIVOT*math.cos(th))/1000.0
    gas_body=inter(gas,body)
    gas_gear=max(inter(gas,g) for _,_,g in gears)
    gas_struct=inter(gas,structural)
    gas_arm=max(inter(gas,a) for a in arms)
    gas_pipe=radial_clear(gas) if name=='LOW' else None
    gas_floor=floor_clear_mesh(gas)

    state_ok=(
        arm_body<1e-4 and arm_gear<1e-4 and arm_struct<1e-4 and fixed_body<1e-4 and fixed_gear<1e-4 and
        arm_y_shell_gap>=1.0 and neg_arm_to_pod_gap>=1.0 and arm_to_boss_radial_gap>=3.0 and
        carrier_side_y_gap>=1.0-1e-9 and crossbar_sweep_gap>=2.0 and
        min_floor>=3.0 and carrier_floor>=3.0 and
        gas_body<1e-4 and gas_gear<1e-4 and gas_struct<1e-4 and gas_arm<1e-4 and gas_floor>=3.0 and
        GAS_RETRACTED+3.0<=gas_len<=GAS_EXTENDED-3.0 and gas_torque>=1.0
    )
    if name=='LOW':
        state_ok=state_ok and min_pipe>=3.0 and arm_pipe>=3.0 and carrier_pipe>=3.0 and gas_pipe>=5.0
    all_ok=all_ok and state_ok
    states[name]={
        'theta_deg':math.degrees(th),'camera_axis_xz_mm':[camx,zcam],
        'carrier_pivots_xz_mm':[list(lp),list(up)],
        'arm_vs_body_mm3':arm_body,'arm_vs_Z50_mm3':arm_gear,'arm_vs_carrier_structural_mm3':arm_struct,
        'carrier_vs_body_mm3':fixed_body,'carrier_vs_Z50_mm3':fixed_gear,
        'arm_to_shell_lateral_gap_mm':arm_y_shell_gap,
        'negative_arm_to_tilt_pod_lateral_gap_mm':neg_arm_to_pod_gap,
        'arm_to_tilt_boss_radial_gap_mm':arm_to_boss_radial_gap,
        'carrier_side_to_boss_lateral_gap_mm':carrier_side_y_gap,
        'rear_crossbar_to_full_moving_sweep_radial_gap_mm':crossbar_sweep_gap,
        'moving_head_min_ideal_DN150_clearance_mm':min_pipe if name=='LOW' else None,
        'moving_head_worst_DN150_deg':worst_pipe if name=='LOW' else None,
        'moving_head_min_wetfloor_clearance_mm':min_floor,'moving_head_worst_floor_deg':worst_floor,
        'arms_min_ideal_DN150_clearance_mm':arm_pipe,
        'carrier_min_ideal_DN150_clearance_mm':carrier_pipe,
        'carrier_min_wetfloor_clearance_mm':carrier_floor,
        'gas_length_mm':gas_len,'gas_assist_torque_Nm_at_150N':gas_torque,
        'gas_vs_body_mm3':gas_body,'gas_vs_Z50_mm3':gas_gear,'gas_vs_carrier_mm3':gas_struct,'gas_vs_arms_mm3':gas_arm,
        'gas_min_ideal_DN150_clearance_mm':gas_pipe,'gas_min_wetfloor_clearance_mm':gas_floor,
        'state_ok':state_ok
    }

# Additional dimensional sanity.
arm_vertical_gap=PIVOT_SEP-ARM_H
gas_lengths=[v['gas_length_mm'] for v in states.values()]
gas_margin=min(min(gas_lengths)-GAS_RETRACTED,GAS_EXTENDED-max(gas_lengths))
status='PASS_SCREEN / MANUFACTURING_HOLD / PROCUREMENT_HOLD' if all_ok and arm_vertical_gap>=2.0 else 'FAIL_SCREEN'

checks={
    'status':status,
    'architecture':{'wheel_stations_x_mm':list(WHEEL_X),'wheels_total':len(wheels),'z50_positions_x_mm':list(GEAR_X),'z50_total':len(gears),'rear_drive_x_mm':250.0,'rule':'3 AXLES / 6 WHEELS HARD LOCK'},
    'corrections':{
        'WB20_wet_cut':'XZ extrusion corrected to y=-38..+38 and asserted.',
        'WB21_lift_head':'end pivots no longer coincide with TILT axis; rigid carrier separates four-bar from sealed camera.',
        'photo_evidence_use':'service photos are topology/packaging evidence only; no unscaled photo dimensions were copied.'
    },
    'body':{'wet_cut_y_bbox_mm':[wetbb.ymin,wetbb.ymax],'wet_deck_half_width_mm':DECK_HALF_W,'body_valid':body.val().isValid()},
    'lift':{'body_pivot_x_mm':BODY_PIVOT_X,'body_pivot_z_mm':[PIVOT_Z_LOW,PIVOT_Z_HIGH],'pivot_separation_mm':PIVOT_SEP,'link_length_mm':LINK_L,'arm_y_mm':ARM_Y,'arm_section_mm':[ARM_T,ARM_H],'arm_vertical_edge_gap_at_pivots_mm':arm_vertical_gap,'carrier_axis_offset_x_mm':CARRIER_X_OFFSET},
    'camera':{'shell_ODxL_mm':[2*HEAD_R,HEAD_L],'tilt_range_deg':[TILT_MIN,TILT_MAX],'tilt_step_deg':TILT_STEP,'moving_sweep_radial_envelope_mm':MOVING_SWEEP_R},
    'carrier':{'yoke_inner_abs_y_mm':YOKE_INNER_Y,'yoke_outer_abs_y_mm':YOKE_OUTER_Y,'rear_crossbar_rel_xz_mm':[CROSSBAR_DX,CROSSBAR_DZ],'rear_crossbar_size_xyz_mm':[CROSSBAR_X,CROSSBAR_Y,CROSSBAR_Z],'pivot_pin_d_mm':PIVOT_PIN_D},
    'gas_spring':{'article':GAS_ARTICLE,'force_N':GAS_FORCE_N,'stroke_mm':GAS_STROKE,'extended_mm':GAS_EXTENDED,'retracted_mm':GAS_RETRACTED,'base_xz_mm':list(GAS_BASE),'moving_attach_from_lower_pivot_mm':GAS_ATTACH_FROM_LOWER_PIVOT,'center_y_mm':GAS_CENTER_Y,'end_margin_mm':gas_margin},
    'states':states,
}
with open(os.path.join(OUT,'WB22A_EXECUTED.json'),'w',encoding='utf-8') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if status.startswith('FAIL'):
    raise SystemExit(2)
