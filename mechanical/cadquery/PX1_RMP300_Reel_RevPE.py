import cadquery as cq, math, json, os
OUT=os.path.abspath("build_revpe"); os.makedirs(OUT,exist_ok=True)

# PX1 Rev.PE — RMP300-like manual reel baseline
# Source: ASS-004-097, ASS-002-710, ASS-002-711, ASS-002-712,
# ASS-002-696 / ASS-004-092, ASS-004-093/094/095.
# Use only source-supported hard dimensions where available:
SPINDLE_L=272.0
BAR_L=362.0
HANDLE_L=160.0
MAIN_SHAFT_REF=292.0  # source naming "REEL AXLE 292", treated as source designation/reference length
FRAME_W=BAR_L          # direct use of named 362 mm bar as frame cross member
FRAME_D=340.0          # assembly-derived envelope; HOLD
FRAME_H=420.0          # assembly-derived envelope; HOLD
SIDE_T=6.0
DRUM_OD=300.0          # assembly-derived envelope; HOLD
DRUM_CORE_OD=150.0     # HOLD
DRUM_W=230.0           # HOLD

def wp(s): return cq.Workplane("XY").newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z0),cq.Vector(0,0,1)))

# coordinate: X frame width, Y depth, Z height
parts={}
# side plates / frame
parts["Frame_Left"]=box(-FRAME_W/2,-FRAME_D/2,0,SIDE_T,FRAME_D,FRAME_H)
parts["Frame_Right"]=box(FRAME_W/2-SIDE_T,-FRAME_D/2,0,SIDE_T,FRAME_D,FRAME_H)
parts["FSS-002-397_Bar_362mm"]=cq.Workplane("YZ").circle(8).extrude(BAR_L).translate((-BAR_L/2,FRAME_D/2-24,FRAME_H-28))
for i,z in enumerate([36,FRAME_H-36],1):
    parts[f"DistanceTube_{i}"]=cq.Workplane("YZ").circle(7).extrude(FRAME_W-2*SIDE_T).translate((-FRAME_W/2+SIDE_T,-FRAME_D/2+22,z))
parts["DistanceTube_3"]=cq.Workplane("YZ").circle(7).extrude(FRAME_W-2*SIDE_T).translate((-FRAME_W/2+SIDE_T,FRAME_D/2-22,FRAME_H-80))

# drum oriented along X
cx=0; cy=0; cz=215
outer=cq.Workplane("YZ").center(cy,cz).circle(DRUM_OD/2).extrude(DRUM_W/2,both=True)
inner=cq.Workplane("YZ").center(cy,cz).circle(DRUM_CORE_OD/2).extrude(DRUM_W/2+2,both=True)
drum=outer.cut(inner)
# add core cylinder
core=cq.Workplane("YZ").center(cy,cz).circle(DRUM_CORE_OD/2).extrude(DRUM_W/2,both=True)
parts["ASS-004-093_KernAssy"]=drum.union(core)

# main shaft reference 292
parts["ASS-002-711_MainShaft_292"]=cyl_x(-MAIN_SHAFT_REF/2,cy,cz,10,MAIN_SHAFT_REF)

# crank handle 160 mm
crank=cq.Workplane("XY").box(HANDLE_L,12,8,centered=(False,True,True)).translate((FRAME_W/2,0,cz))
grip=cyl_z(FRAME_W/2+HANDLE_L-8,0,cz,8,75)
parts["ASS-002-712_ReelHandle_160mm"]=crank.union(grip)

# layering spindle 272 mm across front/top
sp_z=110; sp_y=FRAME_D/2-35
parts["FAL-002-379_LayeringSpindle_272mm"]=cyl_x(-SPINDLE_L/2,sp_y,sp_z,8,SPINDLE_L)
slider=box(-18,sp_y-18,sp_z-18,36,36,36)
parts["RSP-002-003_004_GlidingHousing"]=slider

# measurement unit: big roller D29 is source-controlled; measuring wheel exact diameter not stated in source, leave 40 ref HOLD
mr_y=FRAME_D/2-62; mr_z=72
parts["FBR-002-391_Roller_D29"]=cyl_x(-25,mr_y,mr_z,14.5,50)
parts["FAL-002-145_MeasuringWheel_REF"]=cyl_x(25,mr_y,mr_z,20,10)

# chain/brake side reserve, based on source topology not detailed geometry
parts["BrakeDisk_REF"]=cyl_x(-DRUM_W/2-8,cy,cz,72,6)
parts["BrakeScrew_REF"]=cyl_y(-FRAME_W/2+18,-FRAME_D/2+50,cz,6,50)

assy=cq.Assembly(name="PX1_RMP300_Reel_RevPE")
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,"PX1_RMP300_Reel_RevPE.step"))

checks={
 "source_hard_dimensions_mm":{"layering_spindle":272,"crank_handle":160,"frame_bar":362,"main_shaft_designation":292},
 "source_topology":{
   "measure_unit":"ASS-002-696",
   "layering_spindle":"ASS-002-710",
   "main_shaft":"ASS-002-711",
   "handle":"ASS-002-712",
   "kern":"ASS-004-093",
   "left_side":"ASS-004-094",
   "right_side":"ASS-004-095"
 },
 "replacement_electronics":{
   "original_12pole_slipring":"function retained; use readily available 6-12 circuit slip ring to match PX1 conductor count",
   "original_meter_counter_pcb":"delete; replace by standard magnetic/optical encoder module on measuring wheel",
   "reel_motor":"none; manual reel retained"
 },
 "hold_dimensions":["frame depth/height","drum OD/core OD/width","chain sprocket geometry","brake disk diameter","exact measuring wheel diameter"],
 "all_solids_valid":all(p.val().isValid() for p in parts.values()),
 "status":"RMP300 SOURCE-ARCHITECTURE BASELINE / HARD-DIMENSION PARTIAL"
}
with open(os.path.join(OUT,"REV_PE_VALIDATION.json"),"w") as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
