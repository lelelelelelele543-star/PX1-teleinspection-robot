import cadquery as cq
import math, json, os

# PX-1 Rev.GC — Group B pressure structure, explicit-global-coordinate CAD
# Prototype engineering only. Independent P0/P1/P2 pressure zones retained.

OUT=os.path.abspath('build_revgc')
os.makedirs(OUT,exist_ok=True)

L=307.0; W=92.0; Z0=8.0; ZTOP=90.0
PIPE_R=75.0; PIPE_Z=52.0480547
FLOOR=6.0; ROOF=5.0; END=8.0
P0_INNER_W=68.0; P0_HALF_IN=P0_INNER_W/2; P0_HALF_OUT=W/2
WHEEL_Z=45.0; WX=[50.0,150.0,250.0]; IX=[100.0,200.0]

# Side bay is milled into 12 mm side wall: y 38..46 (left), -46..-38 (right).
BAY_X0=10.5; BAY_L=286.0; BAY_Z0=6.0; BAY_H=80.0; BAY_DEPTH=8.0
BAY_INNER_Y=P0_HALF_OUT-BAY_DEPTH
SIDE_COVER_T=5.0; SIDE_COVER_OUT_Y=P0_HALF_OUT+SIDE_COVER_T
GEAR_Y=42.0; GEAR_FACE=8.0; GEAR_OD=52.0

# Corrected traction packaging envelope.
MOTOR_D=32.0; MOTOR_L=95.0; MOTOR_Y=16.5; MOTOR_X=204.0

TOP_X0=136.0; TOP_L=158.0; TOP_W=74.0; TOP_T=5.0
TOP_CS=2.5; TOP_GW=3.2; TOP_GD=2.0; TOP_SLOT_L=144.0; TOP_SLOT_H=60.0

SIDE_ORING_ID=190.0; SIDE_CS=1.5; SIDE_GW=1.9; SIDE_GD=1.2
SIDE_RT_H=60.0; SIDE_RT_R=SIDE_RT_H/2
SIDE_CIRC=math.pi*SIDE_ORING_ID
SIDE_RT_L=(SIDE_CIRC-2*math.pi*SIDE_RT_R)/2 + 2*SIDE_RT_R

REAR_PLATE_W=52.0; REAR_PLATE_H=52.0; REAR_PLATE_T=6.0
REAR_GENERIC_BORE=24.0; REAR_PCD=42.0; REAR_BODY_PILOT=36.0


def wp(shape): return cq.Workplane('XY').newObject([shape])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l,sgn=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def radial_clearance(y,z): return PIPE_R-math.hypot(y,z-PIPE_Z)
def pm(p):
    v=p.val(); b=v.BoundingBox();
    return {'valid':v.isValid(),'volume_mm3':round(v.Volume(),2),'bbox':[round(b.xmin,3),round(b.ymin,3),round(b.zmin,3),round(b.xmax,3),round(b.ymax,3),round(b.zmax,3)]}

# P0 shell
body=box(0,-P0_HALF_OUT,Z0,L,W,ZTOP-Z0)
body=cut(body,box(END,-P0_HALF_IN,Z0+FLOOR,L-2*END,P0_INNER_W,(ZTOP-Z0)-FLOOR-ROOF))
# folded-camera recess and top service opening
body=cut(body,box(30,-31,53,100,62,40))
body=cut(body,box(TOP_X0,-TOP_W/2,ZTOP-ROOF-1,TOP_L,TOP_W,20))

# Independent side bays: pockets only in the wall, 4 mm membrane remains to P0.
left_pocket=box(BAY_X0,BAY_INNER_Y,BAY_Z0,BAY_L,BAY_DEPTH,BAY_H)
right_pocket=box(BAY_X0,-P0_HALF_OUT,BAY_Z0,BAY_L,BAY_DEPTH,BAY_H)
body=cut(cut(body,left_pocket),right_pocket)

# X200 seal-cartridge seats through 4 mm membrane (Ø38), plus 4x M4 clearance/tapped interface candidates.
body=cut(body,cyl_y(200,P0_HALF_IN,WHEEL_Z,19.0,P0_HALF_OUT-P0_HALF_IN,1))
body=cut(body,cyl_y(200,-P0_HALF_IN,WHEEL_Z,19.0,P0_HALF_OUT-P0_HALF_IN,-1))
for a in range(0,360,90):
    rr=23.0; x=200+rr*math.cos(math.radians(a)); z=WHEEL_Z+rr*math.sin(math.radians(a))
    body=cut(body,cyl_y(x,P0_HALF_IN,z,2.1,P0_HALF_OUT-P0_HALF_IN,1))
    body=cut(body,cyl_y(x,-P0_HALF_IN,z,2.1,P0_HALF_OUT-P0_HALF_IN,-1))

# Side covers
cover_holes=[(8,5),(62,5),(116,5),(170,5),(224,5),(278,5),
             (8,75),(62,75),(116,75),(170,75),(224,75),(278,75)]
side_covers={}
for side in ('L','R'):
    y0=P0_HALF_OUT if side=='L' else -P0_HALF_OUT-SIDE_COVER_T
    cov=box(BAY_X0,y0,BAY_Z0,BAY_L,SIDE_COVER_T,BAY_H)
    # flange pilots and cover screws
    for x in WX:
        cov=cut(cov,cyl_y(x,y0-1 if side=='L' else y0+SIDE_COVER_T+1,WHEEL_Z,18.0,SIDE_COVER_T+2,1 if side=='L' else -1))
    for xl,zl in cover_holes:
        cov=cut(cov,cyl_y(BAY_X0+xl,y0-1 if side=='L' else y0+SIDE_COVER_T+1,BAY_Z0+zl,1.7,SIDE_COVER_T+2,1 if side=='L' else -1))
    # 190x1.5-derived racetrack groove. XZ extrusion direction is -Y; place explicitly.
    cx=BAY_X0+BAY_L/2; cz=BAY_Z0+BAY_H/2
    outer=(cq.Workplane('XZ').center(cx,cz).slot2D(SIDE_RT_L+SIDE_GW,SIDE_RT_H+SIDE_GW,0).extrude(SIDE_GD))
    inner=(cq.Workplane('XZ').center(cx,cz).slot2D(SIDE_RT_L-SIDE_GW,SIDE_RT_H-SIDE_GW,0).extrude(SIDE_GD))
    ring=outer.cut(inner)
    if side=='L':
        # ring initially y=-1.2..0, shift to y=46..47.2
        ring=ring.translate((0,P0_HALF_OUT+SIDE_GD,0))
    else:
        ring=ring.translate((0,P0_HALF_OUT+SIDE_GD,0)).mirror('XZ')
    cov=cut(cov,ring)
    side_covers[side]=cov

# Top cover and groove from bottom face z90..92.
top=box(TOP_X0,-TOP_W/2,ZTOP,TOP_L,TOP_W,TOP_T)
og=(cq.Workplane('XY').center(TOP_X0+TOP_L/2,0).slot2D(TOP_SLOT_L+TOP_GW,TOP_SLOT_H+TOP_GW,0).extrude(TOP_GD).translate((0,0,ZTOP)))
ig=(cq.Workplane('XY').center(TOP_X0+TOP_L/2,0).slot2D(TOP_SLOT_L-TOP_GW,TOP_SLOT_H-TOP_GW,0).extrude(TOP_GD).translate((0,0,ZTOP)))
top=cut(top,og.cut(ig))
TOP_H=[]
for x in [142,176,210,244,278,288]:
    for y in (-34,34): TOP_H.append((x,y))
TOP_H += [(142,0),(288,0)]
for x,y in TOP_H: top=cut(top,wp(cq.Solid.makeCylinder(2.25,TOP_T+2,cq.Vector(x,y,ZTOP-1),cq.Vector(0,0,1))))
for x,y in [(150,-28),(280,28)]: top=cut(top,wp(cq.Solid.makeCylinder(1.5,TOP_T+2,cq.Vector(x,y,ZTOP-1),cq.Vector(0,0,1))))

# Rear adapter plate and body interface.
conn=box(L,-REAR_PLATE_W/2,45-REAR_PLATE_H/2,REAR_PLATE_T,REAR_PLATE_W,REAR_PLATE_H)
conn=cut(conn,cyl_x(L-1,0,45,REAR_GENERIC_BORE/2,REAR_PLATE_T+2))
for a in range(0,360,90):
    r=REAR_PCD/2; y=r*math.cos(math.radians(a)); z=45+r*math.sin(math.radians(a))
    conn=cut(conn,cyl_x(L-1,y,z,2.25,REAR_PLATE_T+2))
body=cut(body,cyl_x(L-END-1,0,45,REAR_BODY_PILOT/2,END+2))
for a in range(0,360,90):
    r=REAR_PCD/2; y=r*math.cos(math.radians(a)); z=45+r*math.sin(math.radians(a))
    body=cut(body,cyl_x(L-END-1,y,z,2.1,END+2))

# Structural towing/recovery clevis above connector.
recovery=box(L-24,-5,64,22,10,26)
recovery=cut(recovery,cyl_y(L-13,-6,78,4.0,12,1))
fill=cyl_x(L-4,-28,70,6.0,10)
sensor=cyl_x(L-4,28,70,6.0,10)

# Motor envelopes, explicit X-axis cylinders.
motors={
 'L':cyl_x(MOTOR_X,MOTOR_Y,WHEEL_Z,MOTOR_D/2,MOTOR_L),
 'R':cyl_x(MOTOR_X,-MOTOR_Y,WHEEL_Z,MOTOR_D/2,MOTOR_L)
}

# Assembly/export
assy=cq.Assembly(name='PX1_GroupB_RevGC')
for n,p in [('DRW-PX1-100_MainBody',body),('DRW-PX1-101_TopCover',top),('DRW-PX1-433_SideCover_L',side_covers['L']),('DRW-PX1-433_SideCover_R',side_covers['R']),('DRW-PX1-103_ConnectorAdapter',conn),('DRW-PX1-102_TetherClevis',recovery),('PressureFillBoss',fill),('PressureSensorBoss',sensor),('Motor32_L_Envelope',motors['L']),('Motor32_R_Envelope',motors['R'])]: assy.add(p,name=n)
parts={'DRW-PX1-100_MainBody':body,'DRW-PX1-101_TopCover':top,'DRW-PX1-433_SideCover_L':side_covers['L'],'DRW-PX1-433_SideCover_R':side_covers['R'],'DRW-PX1-103_ConnectorAdapter':conn,'DRW-PX1-102_TetherClevis':recovery,'PressureFillBoss':fill,'PressureSensorBoss':sensor}
for n,p in parts.items(): cq.exporters.export(p,os.path.join(OUT,n+'.step'))
assy.save(os.path.join(OUT,'PX1_GroupB_RevGC.step'))

# Validation
pipe=wp(cq.Solid.makeCylinder(PIPE_R,L+80,cq.Vector(-20,0,PIPE_Z),cq.Vector(1,0,0)))
res={n:pm(p) for n,p in parts.items()}
res['dn150_outside_volume_mm3']={n:round(p.val().cut(pipe.val()).Volume(),6) for n,p in parts.items()}
res['motor_body_intersection_mm3']={n:round(m.val().intersect(body.val()).Volume(),6) for n,m in motors.items()}
res['checks']={
 'p0_inner_width':P0_INNER_W,'p0_side_wall':P0_HALF_OUT-P0_HALF_IN,'sidebay_depth':BAY_DEPTH,'remaining_membrane':(P0_HALF_OUT-P0_HALF_IN)-BAY_DEPTH,
 'sidebay_left_y':[BAY_INNER_Y,P0_HALF_OUT],'sidecover_left_y':[P0_HALF_OUT,P0_HALF_OUT+SIDE_COVER_T],
 'motor_pack_halfwidth':MOTOR_Y+MOTOR_D/2,'motor_clearance_each':P0_HALF_IN-(MOTOR_Y+MOTOR_D/2),
 'gear_face_left_y':[GEAR_Y-GEAR_FACE/2,GEAR_Y+GEAR_FACE/2],
 'sidecover_lower_corner_clearance':round(radial_clearance(SIDE_COVER_OUT_Y,BAY_Z0),3),
 'sidecover_upper_corner_clearance':round(radial_clearance(SIDE_COVER_OUT_Y,BAY_Z0+BAY_H),3),
 'side_oring_centerline_LxH':[round(SIDE_RT_L,3),SIDE_RT_H],'side_oring_squeeze':round(1-SIDE_GD/SIDE_CS,4),'side_oring_fill':round((math.pi*(SIDE_CS/2)**2)/(SIDE_GW*SIDE_GD),4),
 'top_oring_squeeze':round(1-TOP_GD/TOP_CS,4),'top_oring_fill':round((math.pi*(TOP_CS/2)**2)/(TOP_GW*TOP_GD),4),
 'pressure_architecture':'P0/P1/P2 isolated; common fill via check valves','status':'prototype candidate; exact seal/motor/connector articles remain HOLD'
}
with open(os.path.join(OUT,'REV_GC_GROUP_B_VALIDATION.json'),'w') as f: json.dump(res,f,indent=2)
print(json.dumps(res,indent=2))
