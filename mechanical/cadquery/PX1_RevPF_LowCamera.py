import cadquery as cq
import math, json, os

# PX1 Rev.PF — Proteus-like low camera bay + manual lift + CAM026 integration
# Master intent:
# - CRP150-like body/side drive architecture
# - CAM026-class 120x73x73 camera
# - LOW gives useful forward image in DN150 without forcing full pan sweep
# - full +/-135 pan becomes available after modest manual lift
# - wet camera bay is open forward and self-draining; no blind water pocket

OUT=os.path.abspath("build_revpf")
os.makedirs(OUT,exist_ok=True)

L=307.0
BODY_W=92.0
BODY_Z0=8.0
BODY_Z1=90.0
PIPE_R=75.0
PIPE_Z=52.05
CAM_L=120.0
CAM_W=73.0
CAM_H=73.0
CAM_TX_LOW=10.0
CAM_Z_LOW=69.5
PAN_MIN=-135
PAN_MAX=135
LOW_SAFE_PAN=(-25,135)
FULL_PAN_AXIS_Z_MIN=86.1
WET_X1=140.0
WET_HALF_W=37.5
RAMP_Z_FRONT=25.0
RAMP_Z_REAR=29.0
BASE_X=220.0
BASE_LOWER_Z=82.0
BASE_UPPER_Z=98.0
SIDE_Y=49.0
ARM_T=5.0
ARM_H=14.0
LOW_REAR_X=130.0
LOW_Q_LOWER_Z=CAM_Z_LOW-8.0
LOW_Q_UPPER_Z=CAM_Z_LOW+8.0

def wp(s): return cq.Workplane("XY").newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return cq.Workplane("YZ").center(y,z).circle(r).extrude(l).translate((x0,0,0))
def link(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    ll=math.hypot(dx,dz); a=math.degrees(math.atan2(dz,dx))
    s=(cq.Workplane("XZ").workplane(offset=y-ARM_T/2).slot2D(ll,ARM_H,0).extrude(ARM_T))
    return s.rotate((0,0,0),(0,1,0),-a).translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))

outer=box(0,-BODY_W/2,BODY_Z0,L,BODY_W,BODY_Z1-BODY_Z0)
rear_inner=box(WET_X1,-34,14,L-WET_X1-8,68,66)
body=wp(outer.val().cut(rear_inner.val()))
for sgn in (1,-1):
    if sgn>0:
        pf=box(12,40.5,8,WET_X1-12,5.5,76); pr=box(WET_X1,38,8,295-WET_X1,8,76)
    else:
        pf=box(12,-46,8,WET_X1-12,5.5,76); pr=box(WET_X1,-46,8,295-WET_X1,8,76)
    body=wp(body.val().cut(pf.val()).cut(pr.val()))
wet_poly=[(0,RAMP_Z_FRONT),(WET_X1,RAMP_Z_REAR),(WET_X1,115),(0,115)]
wet=(cq.Workplane("XZ").workplane(offset=-WET_HALF_W).polyline(wet_poly).close().extrude(2*WET_HALF_W))
body=wp(body.val().cut(wet.val()))

def ring_x(x0,y,z,ro,ri,l): return cq.Workplane("YZ").center(y,z).circle(ro).circle(ri).extrude(l).translate((x0,0,0))
rear_outer=cyl_x(70,0,0,36.5,50); rear_inner=cyl_x(75,0,0,30.0,40)
rear_shell=rear_outer.cut(rear_inner); rear_guard=ring_x(112,0,0,36.5,30.5,8)
yokes=[]
for sgn in (1,-1):
    y0=sgn*30.5; t=6.0
    plate=(cq.Workplane("XZ").workplane(offset=y0-t/2).center(56,0).circle(36.5).circle(27.0).extrude(t))
    opening=(cq.Workplane("XZ").workplane(offset=y0-t/2-0.1).box(62,44,t+0.2,centered=(True,True,False)).translate((28,0,0)))
    yokes.append(plate.cut(opening))
head_outer=cyl_x(4,0,0,25.0,46); head_inner=cyl_x(8,0,0,20.5,36)
head=head_outer.cut(head_inner).union(ring_x(0,0,0,25,10.5,5)).union(cyl_x(0,0,0,10.5,3)).union(ring_x(45,0,0,25,8,4))
cam_fixed=rear_shell.union(rear_guard)
for yk in yokes: cam_fixed=cam_fixed.union(yk)
cam_fixed_low=cam_fixed.translate((CAM_TX_LOW,0,CAM_Z_LOW)); cam_head_low=head.translate((CAM_TX_LOW,0,CAM_Z_LOW))
arms=[]
for y in (-SIDE_Y,SIDE_Y):
    arms.append(link((BASE_X,BASE_LOWER_Z),(LOW_REAR_X,LOW_Q_LOWER_Z),y))
    arms.append(link((BASE_X,BASE_UPPER_Z),(LOW_REAR_X,LOW_Q_UPPER_Z),y))
gas=(cq.Workplane("XZ").workplane(offset=-5).slot2D(95,10,0).extrude(10).rotate((0,0,0),(0,1,0),-15).translate((172,0,72)))
pipe=(cq.Workplane("YZ").center(0,PIPE_Z).circle(PIPE_R).extrude(L+80).translate((-30,0,0)))
def camera_at_pan(deg):
    moving=head.rotate((48,0,0),(48,1,0),deg).translate((CAM_TX_LOW,0,CAM_Z_LOW))
    return cam_fixed_low.union(moving)
check_angles=[-135,-90,-45,-25,0,45,90,135]
checks_pan={}
for d in check_angles:
    c=camera_at_pan(d)
    checks_pan[str(d)]={"outside_DN150_mm3":round(c.val().cut(pipe.val()).Volume(),4),"body_intersection_mm3":round(c.val().intersect(body.val()).Volume(),4)}
arm_checks=[]
for a in arms:
    arm_checks.append({"body_intersection_mm3":round(a.val().intersect(body.val()).Volume(),4),"outside_DN150_mm3":round(a.val().cut(pipe.val()).Volume(),4)})
fov_half=math.radians(75/2); cone_radius_at_nose=CAM_TX_LOW*math.tan(fov_half)
validation={"revision":"Rev.PF","basis":["Rev.PB","Rev.PC","DRW-002-744"],"low_camera_axis_z_mm":CAM_Z_LOW,"pipe_axis_z_mm":PIPE_Z,"low_safe_pan_deg":list(LOW_SAFE_PAN),"full_pan_axis_z_min_mm":FULL_PAN_AXIS_Z_MIN,"wet_bay":{"open_front":True,"blind_pocket":False,"x_mm":[0,WET_X1],"half_width_mm":WET_HALF_W,"floor_z_front_rear_mm":[RAMP_Z_FRONT,RAMP_Z_REAR],"drain_strategy":"gravity to open front; no drain tube"},"forward_FOV":{"nominal_deg":75,"cone_radius_at_nose_plane_mm":round(cone_radius_at_nose,2),"vertical_clear_to_floor_at_nose_mm":round(CAM_Z_LOW-RAMP_Z_FRONT,2),"side_half_opening_mm":WET_HALF_W},"pan_checks":checks_pan,"arm_checks":arm_checks,"manual_lift_source_items":{"gas_spring_N":150,"clamping_lever":"M8","source":"DRW-002-744"},"hold":["exact arm detail dimensions","exact CAM026 replacement motor/seal details"],"status":"PROTEUS-LIKE LOW CAMERA BAY VALIDATION / NOT MACHINING RELEASE"}
assy=cq.Assembly(name="PX1_RevPF_LowCamera")
assy.add(body,name="CRP150_like_body_wet_camera_bay",color=cq.Color(0.65,0.67,0.7)); assy.add(cam_fixed_low,name="CAM026_fixed_LOW",color=cq.Color(0.25,0.25,0.28)); assy.add(cam_head_low,name="CAM026_head_0deg_LOW",color=cq.Color(0.18,0.18,0.2))
for i,a in enumerate(arms,1): assy.add(a,name=f"LiftArm_{i}",color=cq.Color(0.5,0.52,0.54))
assy.add(gas,name="GasSpring150N_envelope",color=cq.Color(0.2,0.2,0.2)); assy.save(os.path.join(OUT,"PX1_RevPF_LowCamera.step")); cq.exporters.export(body,os.path.join(OUT,"PX1_RevPF_Body_WetBay.step"))
with open(os.path.join(OUT,"REV_PF_VALIDATION.json"),"w") as f: json.dump(validation,f,indent=2)
print(json.dumps(validation,indent=2))
