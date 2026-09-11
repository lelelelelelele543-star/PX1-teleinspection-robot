import cadquery as cq
import math, json, os
import numpy as np

# PX-1 Rev.B WB21 — constant-length local camera harness at the manual-lift pivot.
# Engineering validation only. NOT machining release.
OUT=os.path.abspath("build_wb21")
os.makedirs(OUT,exist_ok=True)

PIPE_R=75.0
PIPE_Z=52.0480547
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0
GEAR_Y=42.0
GEAR_OD=52.0
GEAR_FACE=3.75
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]

BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=112.0
LINK_L=120.0
CAM_AXIS_OFFSET_Z=2.0
CAM_ZS={"LOW":75.0,"MID":130.0,"HIGH":205.0}
ARM_Y=26.0
ARM_T=5.0
ARM_H=18.0

HEAD_R=26.0
HEAD_L=78.0
BOSS_OUTER_Y=34.0
YOKE_INNER_Y=34.5
YOKE_OUTER_Y=37.5
YOKE_CENTER_Y=36.0
YOKE_R=29.0
YOKE_INNER_R=10.75
YOKE_T=3.0
TILT_POD_OD=18.0
TILT_POD_X=56.0
TILT_WHEEL_Y=-16.75
WORM_CD=14.5

GAS_BASE=(194.0,82.9)
GAS_ATTACH=63.0
GAS_Y=16.0
GAS_OD=12.0

# WB21 local harness
CABLE_ARTICLE="igus chainflex CF99.PLUS.01.08"
CABLE_OD=8.0
CABLE_R=CABLE_OD/2.0
R_REQUIRED=40.0             # 5xd service-life screen at -25..+80 C
FREE_L=52.8
FREE_TOL=0.5
CLAMP_D=60.0
CLAMP_Y=-13.0
GUIDE=np.array([190.5097408066,-13.0,95.7383125126])
GLAND_ARTICLE="LAPP SKINTOP MS-M M16x1.5 53112010"
GLAND_MOUNT=np.array([180.0,0.0,60.0])
GLAND_OD=22.0
GLAND_EXT=26.0              # conservative external envelope from 33 max overall - 7 thread
BOSS_OD=26.0
SUPPORT_OD=12.0

def wp(s): return cq.Workplane("XY").newObject([s])
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def cyl_between(p1,p2,r):
    p1=np.array(p1,float); p2=np.array(p2,float); v=p2-p1; L=float(np.linalg.norm(v))
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(*p1),cq.Vector(*(v/L))))
def cyl_x_center(x,y,z,r,L):
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(x-L/2,y,z),cq.Vector(1,0,0)))
def cyl_y_center(x,y,z,r,L):
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(x,y-L/2,z),cq.Vector(0,1,0)))
def boxc(x,y,z,dx,dy,dz):
    return cq.Workplane("XY").box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def ring_y_center(x,y,z,ro,ri,L):
    o=cyl_y_center(x,y,z,ro,L); i=cyl_y_center(x,y,z,ri,L+0.2)
    return wp(o.val().cut(i.val()))
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def inter(a,b): return a.val().intersect(b.val()).Volume()
def mesh_radial_clear(part,tol=0.3):
    v,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(p.y,p.z-PIPE_Z) for p in v)
def theta_for(zcam):
    return math.asin((zcam-CAM_AXIS_OFFSET_Z-(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0)/LINK_L)
def cam_x_for(zcam):
    t=theta_for(zcam); return BODY_PIVOT_X-LINK_L*math.cos(t)
def point_lower(zcam,d,y):
    t=theta_for(zcam)
    return np.array([BODY_PIVOT_X-d*math.cos(t),y,PIVOT_Z_LOW+d*math.sin(t)])
def camera_pivots(zcam):
    t=theta_for(zcam); dx=-LINK_L*math.cos(t); dz=LINK_L*math.sin(t)
    return (BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz),(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
def link_plate(p1,p2,y):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=(cq.Workplane("XZ").workplane(offset=y-ARM_T/2).slot2D(L,ARM_H,0).extrude(ARM_T))
    p=p.rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))
def arc_radius(c,L):
    if L<=c: return float("inf")
    lo,hi=1e-9,math.pi*1.99
    target=c/L
    for _ in range(100):
        a=(lo+hi)/2
        if 2*math.sin(a/2)/a>target: lo=a
        else: hi=a
    a=(lo+hi)/2
    return L/a
def arc_points(p1,p2,L,n=41):
    # Free-tangent minor circular arc. Pick the side with the best floor clearance.
    a=np.array([p1[0],p1[2]],float); b=np.array([p2[0],p2[2]],float)
    d=b-a; c=float(np.linalg.norm(d)); R=arc_radius(c,L)
    mid=(a+b)/2; h=math.sqrt(max(R*R-(c/2)**2,0))
    perp=np.array([-d[1],d[0]])/c
    candidates=[]
    for cen in (mid+h*perp,mid-h*perp):
        a0=math.atan2(a[1]-cen[1],a[0]-cen[0])
        a1=math.atan2(b[1]-cen[1],b[0]-cen[0])
        delta=(a1-a0+math.pi)%(2*math.pi)-math.pi
        pts=[]
        for i in range(n):
            q=a0+delta*i/(n-1)
            pts.append(np.array([cen[0]+R*math.cos(q),CLAMP_Y,cen[1]+R*math.sin(q)]))
        candidates.append((min(p[2]-roof_top(p[0])-CABLE_R for p in pts),R,pts))
    _,R,pts=max(candidates,key=lambda x:x[0])
    return R,pts
def tube(points,r):
    return fuse_all([cyl_between(points[i],points[i+1],r) for i in range(len(points)-1)])
def camera_parts(camx,camz):
    shell=cyl_x_center(camx,0,camz,HEAD_R,HEAD_L)
    bp=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,HEAD_R,camz),cq.Vector(0,1,0)))
    bn=wp(cq.Solid.makeCylinder(10.0,BOSS_OUTER_Y-HEAD_R,cq.Vector(camx,-HEAD_R,camz),cq.Vector(0,-1,0)))
    pod=cyl_x_center(camx+12.0,TILT_WHEEL_Y,camz+WORM_CD,TILT_POD_OD/2,TILT_POD_X)
    moving=fuse_all([shell,bp,bn,pod])
    yp=ring_y_center(camx,+YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    yn=ring_y_center(camx,-YOKE_CENTER_Y,camz,YOKE_R,YOKE_INNER_R,YOKE_T)
    bridge=boxc(camx+58.0,0,camz+20.0,8.0,2*YOKE_OUTER_Y,8.0)
    return moving,fuse_all([yp,yn,bridge])
def rotate_y(part,x,z,deg):
    return part.rotate((x,0,z),(x,1,z),deg)

# Fixed body-side ingress envelope.
gv=GUIDE-GLAND_MOUNT
gu=gv/np.linalg.norm(gv)
gland_end=GLAND_MOUNT+GLAND_EXT*gu
gland=cyl_between(GLAND_MOUNT,gland_end,GLAND_OD/2)
boss=cyl_between(GLAND_MOUNT-3*gu,GLAND_MOUNT+3*gu,BOSS_OD/2)
static_cable=cyl_between(gland_end,GUIDE,CABLE_R)
support=cyl_between(gland_end,GUIDE,SUPPORT_OD/2)

gears=[cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE) for s in (-1,1) for x in GEAR_X]
states={}
for name,zcam in CAM_ZS.items():
    lp,up=camera_pivots(zcam)
    arms=[link_plate((200,92),lp,y) for y in (-ARM_Y,ARM_Y)] + [link_plate((200,112),up,y) for y in (-ARM_Y,ARM_Y)]
    clamp=point_lower(zcam,CLAMP_D,CLAMP_Y)
    R,pts=arc_points(GUIDE,clamp,FREE_L)
    cable=tube(pts,CABLE_R)
    camx=cam_x_for(zcam)
    moving,fixed=camera_parts(camx,zcam)
    max_mov=0.0
    for deg in range(-105,106):
        max_mov=max(max_mov,inter(cable,rotate_y(moving,camx,zcam,deg)))
    t=theta_for(zcam)
    gas_end=(200-GAS_ATTACH*math.cos(t),GAS_Y,92+GAS_ATTACH*math.sin(t))
    gas=cyl_between((GAS_BASE[0],GAS_Y,GAS_BASE[1]),gas_end,GAS_OD/2)
    c=float(np.linalg.norm(GUIDE-clamp))
    states[name]={
      "clamp_xyz_mm":[float(x) for x in clamp],
      "chord_mm":c,
      "radius_nominal_mm":R,
      "radius_at_plus_0p5_length_mm":arc_radius(c,FREE_L+FREE_TOL),
      "floor_clearance_nominal_mm":min(float(p[2]-roof_top(float(p[0]))-CABLE_R) for p in pts),
      "ideal_DN150_clearance_nominal_mm":min(float(PIPE_R-math.hypot(float(p[1]),float(p[2])-PIPE_Z)-CABLE_R) for p in pts),
      "arm_collision_mm3":max(inter(cable,a) for a in arms),
      "camera_fixed_collision_mm3":inter(cable,fixed),
      "camera_moving_max_collision_mm3_1deg":max_mov,
      "gland_vs_arms_mm3":max(inter(gland,a) for a in arms),
      "boss_vs_arms_mm3":max(inter(boss,a) for a in arms),
      "support_vs_arms_mm3":max(inter(support,a) for a in arms),
      "dynamic_cable_vs_gas_mm3":inter(cable,gas),
      "support_vs_gas_mm3":inter(support,gas),
      "dynamic_cable_vs_gears_mm3":max(inter(cable,g) for g in gears)
    }

min_tol_R=min(v["radius_at_plus_0p5_length_mm"] for v in states.values())
status="PASS_SCREEN / MANUFACTURING_HOLD / PROCUREMENT_HOLD" if (
    min_tol_R>=R_REQUIRED and
    states["LOW"]["ideal_DN150_clearance_nominal_mm"]>=5.0 and
    all(v["arm_collision_mm3"]<1e-4 and v["camera_fixed_collision_mm3"]<1e-4 and v["camera_moving_max_collision_mm3_1deg"]<1e-4 and v["dynamic_cable_vs_gears_mm3"]<1e-4 and v["dynamic_cable_vs_gas_mm3"]<1e-4 for v in states.values())
) else "FAIL_SCREEN"

checks={
 "status":status,
 "cable":CABLE_ARTICLE,
 "cable_OD_mm":CABLE_OD,
 "required_dynamic_radius_mm":R_REQUIRED,
 "free_length_mm":FREE_L,
 "free_length_tolerance_mm":FREE_TOL,
 "guide_xyz_mm":[float(x) for x in GUIDE],
 "gland":GLAND_ARTICLE,
 "gland_mount_xyz_mm":[float(x) for x in GLAND_MOUNT],
 "gland_end_xyz_mm":[float(x) for x in gland_end],
 "gland_ideal_DN150_clearance_mm":mesh_radial_clear(gland),
 "boss_ideal_DN150_clearance_mm":mesh_radial_clear(boss),
 "static_cable_ideal_DN150_clearance_mm":mesh_radial_clear(static_cable),
 "states":states
}
with open(os.path.join(OUT,"WB21_EXECUTED.json"),"w",encoding="utf-8") as f:
    json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if status.startswith("FAIL"):
    raise SystemExit(2)
