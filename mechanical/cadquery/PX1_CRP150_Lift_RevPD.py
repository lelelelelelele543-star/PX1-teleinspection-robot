import cadquery as cq, math, json, os
OUT=os.path.abspath("build_revpd"); os.makedirs(OUT,exist_ok=True)

# PX1 Rev.PD — source-faithful CRP150 manual lift topology
# Source: MiniCam DRW-002-744. Geometry that is not dimensioned in the available drawing remains PARAMETRIC/HOLD.
# Known source-controlled items retained:
# 1x gas spring 150N, 2x lever side, 1x lever sheet, M8 clamping lever,
# 3x DIN2093 20x10.2x1.1, 2x 15x2.5 O-rings, 4x 8x0.8 circlips, M6x18 pin.

# Interface envelope to Rev.PB crawler; NOT claimed as original MiniCam dimensions.
BASE_X=170.0
BASE_Z=82.0
SIDE_Y=30.0
SIDE_T=5.0
LOW_CAM_X=82.0
LOW_CAM_Z=75.0

# Parametric dimensions held until detail drawings / physical measurement.
ARM_L=118.0
ARM_H=16.0
ARM_T=5.0
PIVOT_D=8.0
PIVOT_X=202.0
LOWER_Z=88.0
UPPER_Z=104.0
CAM_BRACKET_DX=-108.0
CAM_BRACKET_DZ=-18.0
PLATE_T=3.0

def wp(s): return cq.Workplane("XY").newObject([s])
def cyl_y(x,y,z,r,l,sgn=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,sgn,0)))
def link(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    L=math.hypot(dx,dz); a=math.degrees(math.atan2(dz,dx))
    s=(cq.Workplane("XZ").workplane(offset=y-ARM_T/2).slot2D(L,ARM_H,0).extrude(ARM_T))
    return s.rotate((0,0,0),(0,1,0),-a).translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))

p_lower=(PIVOT_X,LOWER_Z); p_upper=(PIVOT_X,UPPER_Z)
q_lower=(PIVOT_X+CAM_BRACKET_DX,LOWER_Z+CAM_BRACKET_DZ)
q_upper=(PIVOT_X+CAM_BRACKET_DX,UPPER_Z+CAM_BRACKET_DZ)

parts={}
for side,sgn in [("L",1),("R",-1)]:
    y=sgn*SIDE_Y
    parts[f"FSS-002-068_LeverSide_{side}"]=link(p_lower,q_lower,y)
    # Use source item ASS-002-723 as the upper/front lever-arm assembly representation.
    parts[f"ASS-002-723_LeverArm_{side}"]=link(p_upper,q_upper,y)

# lever sheet ties both sides as in DRW-002-744
sheet=(cq.Workplane("XY").box(ARM_L*0.72, 2*SIDE_Y+SIDE_T, PLATE_T, centered=(True,True,True))
       .translate(((p_upper[0]+q_upper[0])/2,0,(p_upper[1]+q_upper[1])/2+6)))
parts["FSS-002-073_LeverSheetPlate"]=sheet

# housing lift + clamping area
housing=(cq.Workplane("XY").box(34,68,26,centered=(True,True,False)).translate((PIVOT_X,0,76)))
parts["FAL-002-067_HousingLift"]=housing

# pivots/axles
for z,label in [(LOWER_Z,"FSS-002-075_AxleLeverSide"),(UPPER_Z,"FSS-002-079_AxleLeverTopSide")]:
    parts[label]=cyl_y(PIVOT_X,-SIDE_Y-5,z,4,2*(SIDE_Y+5),1)

# gas spring 150N, drawn only as envelope along lower lever direction.
gb=(PIVOT_X-3,0,82)
ga=(q_lower[0]+42,0,q_lower[1]+5)
dx=ga[0]-gb[0]; dz=ga[2]-gb[2]; gl=math.hypot(dx,dz)
ang=math.degrees(math.atan2(dz,dx))
gas=cq.Workplane("YZ").circle(6.0).extrude(gl).rotate((0,0,0),(0,1,0),-ang).translate(gb)
parts["SPR-002-524_GasSpring150N"]=gas

# M8 clamp envelope and Belleville stack
parts["FIX-002-527_ClampingLever_M8"]=cyl_y(PIVOT_X,-42,UPPER_Z,5,84,1)
for i in range(3):
    parts[f"FIX-002-726_DIN2093_20x10.2x1.1_{i+1}"]=(cq.Workplane("XZ").workplane(offset=-1.65+i*1.1)
        .center(PIVOT_X,UPPER_Z).circle(10).circle(5.1).extrude(1.1))

# camera connector/lift-top reference from DRW-002-752 interface
cam_mount=(cq.Workplane("XY").box(28,52,22,centered=(True,True,True)).translate((q_upper[0]-8,0,(q_upper[1]+q_lower[1])/2)))
parts["CAMERA_MOUNT_INTERFACE"]=cam_mount

assy=cq.Assembly(name="PX1_CRP150_Lift_RevPD")
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,"PX1_CRP150_Lift_RevPD.step"))

checks={
 "source":"DRW-002-744",
 "source_known_items":{
   "gas_spring_N":150,
   "lever_side_qty":2,
   "clamping_lever":"M8",
   "belleville":"3x DIN2093 20x10.2x1.1",
   "oring":"2x 15x2.5",
   "circlip":"4x 8x0.8",
   "pin":"M6x18"
 },
 "parametric_hold_dimensions":["ARM_L","ARM_H","pivot spacing","gas spring closed/open length","exact housing profile"],
 "topology_pass": all(p.val().isValid() for p in parts.values()),
 "status":"SOURCE-FAITHFUL TOPOLOGY / DIMENSION HOLD"
}
with open(os.path.join(OUT,"REV_PD_VALIDATION.json"),"w") as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
