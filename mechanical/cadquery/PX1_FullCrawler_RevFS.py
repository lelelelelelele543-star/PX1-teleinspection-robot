import cadquery as cq
import math, json, os

# PX-1 Rev.FS — integrated CRP150-inspired 6-wheel crawler production candidate
# Own PX-1 geometry. Prototype engineering only; NOT a machining release.

L=307.0; W=92.0; Z0=8.0; ZTOP=90.0
PIPE_R=75.0; PIPE_Z=52.0480547
WX=[50.0,150.0,250.0]; IX=[100.0,200.0]; WHEEL_Z=45.0
COVER_T=5.0; COVER_L=286.0; COVER_H=86.0; COVER_X0=(L-COVER_L)/2
COVER_Z0=2.0
FLANGE_OD=50.0; FLANGE_EXT=3.0
GEAR_OD=52.0; GEAR_FACE=8.0; GEAR_Y=38.0
MOTOR_D=37.0; MOTOR_L=90.0; MOTOR_X=204.0; MOTOR_Y=19.0
CAM_OD=52.0; CAM_LEN=72.0; CAM_Z=75.0
BODY_PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=112.0
LINK_L=120.0; ARM_Y=26.0; ARM_T=5.0; ARM_H=18.0
TAIL_CABLE_OD=11.0

def plate_link(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    ang=math.degrees(math.atan2(dz,dx)); length=math.hypot(dx,dz)
    s=(cq.Workplane('XZ').workplane(offset=y-ARM_T/2)
       .slot2D(length,ARM_H,0).extrude(ARM_T))
    s=s.rotate((0,0,0),(0,1,0),-ang)
    s=s.translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))
    return s

def qpoints(z):
    mid=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
    th=math.asin((z-2.0-mid)/LINK_L)
    dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
    q1=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz)
    q2=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
    return th,q1,q2,(q1[0]+q2[0])/2

def wheel_shape(x,side):
    s=1 if side=='L' else -1
    y_inner=s*(W/2+COVER_T)
    y_crown=s*55.0
    y_outer=s*67.0
    crown_len=abs(y_crown-y_inner)
    taper_len=abs(y_outer-y_crown)
    crown=cq.Workplane('XZ').center(x,WHEEL_Z).circle(45.0).extrude(crown_len, combine=True)
    if s>0:
        crown=crown.translate((0,y_inner,0))
        taper=(cq.Workplane('XZ').center(x,WHEEL_Z).circle(45.0).workplane(offset=taper_len).circle(21.0).loft(combine=True).translate((0,y_crown,0)))
    else:
        crown=crown.translate((0,abs(y_inner),0)).mirror('XZ')
        taper=(cq.Workplane('XZ').center(x,WHEEL_Z).circle(45.0).workplane(offset=taper_len).circle(21.0).loft(combine=True).translate((0,abs(y_crown),0)).mirror('XZ'))
    return crown.union(taper)

def oriented_camera(cx,cz,tilt_deg):
    c=(cq.Workplane('YZ').circle(CAM_OD/2).extrude(CAM_LEN/2,both=True).translate((cx,0,cz)))
    return c.rotate((cx,0,cz),(cx,1,cz),tilt_deg)

def bbox_dims(shape):
    b=shape.val().BoundingBox(); return [b.xlen,b.ylen,b.zlen]

outer=cq.Workplane('XY').box(L,W,ZTOP-Z0,centered=(False,True,False)).translate((0,0,Z0))
inner=(cq.Workplane('XY').box(L-16,W-12,66,centered=(False,True,False)).translate((8,0,14)))
body=outer.cut(inner)
nose=(cq.Workplane('XY').box(100,62,40,centered=(False,True,False)).translate((30,0,53)))
body=body.cut(nose)
opening=(cq.Workplane('XY').box(160,74,20,centered=(False,True,False)).translate((135,0,85)))
body=body.cut(opening)
for s in (-1,1):
    boss=(cq.Workplane('XZ').center(200,WHEEL_Z).circle(19).extrude(10).translate((0,s*(W/2-2),0)))
    if s<0: boss=boss.mirror('XZ')
    body=body.union(boss)

TOP_X=136.0; TOP_L=158.0; TOP_W=74.0; TOP_T=5.0
cover_top=cq.Workplane('XY').box(TOP_L,TOP_W,TOP_T,centered=(False,True,False)).translate((TOP_X,0,ZTOP))
slotL=144.0; slotH=60.0; gw=3.0; gd=2.0
outerg=(cq.Workplane('XY').workplane(offset=ZTOP+TOP_T-gd).center(TOP_X+TOP_L/2,0).slot2D(slotL+gw,slotH+gw,0).extrude(gd))
innerg=(cq.Workplane('XY').workplane(offset=ZTOP+TOP_T-gd).center(TOP_X+TOP_L/2,0).slot2D(slotL-gw,slotH-gw,0).extrude(gd))
cover_top=cover_top.cut(outerg.cut(innerg))
for x in [142,176,210,244,278,288]:
    for y in (-34,34):
        cover_top=cover_top.faces('>Z').workplane().center(x-(TOP_X+TOP_L/2),y).hole(4.5)
for x in (142,288):
    cover_top=cover_top.faces('>Z').workplane().center(x-(TOP_X+TOP_L/2),0).hole(4.5)

side_covers=[]; flanges=[]
for side,s in [('L',1),('R',-1)]:
    c=(cq.Workplane('XZ').workplane(offset=s*W/2).box(COVER_L,COVER_H,COVER_T,centered=(True,True,False))
       .translate((L/2,0,COVER_Z0+COVER_H/2)))
    if s<0: c=c.mirror('XZ')
    for x in WX:
        hole=(cq.Workplane('XZ').workplane(offset=s*(W/2-1)).center(x,WHEEL_Z).circle(18).extrude(COVER_T+2))
        if s<0: hole=hole.mirror('XZ')
        c=c.cut(hole)
    side_covers.append((side,c))
    for x in WX:
        f=(cq.Workplane('XZ').workplane(offset=s*(W/2+COVER_T)).center(x,WHEEL_Z).circle(FLANGE_OD/2).extrude(FLANGE_EXT))
        if s<0: f=f.mirror('XZ')
        flanges.append((side,x,f))

gears=[]; wheels=[]
for side,s in [('L',1),('R',-1)]:
    for x in WX+IX:
        g=(cq.Workplane('XZ').workplane(offset=s*(GEAR_Y-GEAR_FACE/2)).center(x,WHEEL_Z).circle(GEAR_OD/2).extrude(GEAR_FACE))
        if s<0: g=g.mirror('XZ')
        gears.append((side,x,g))
    for x in WX: wheels.append((side,x,wheel_shape(x,side)))

motors=[]
for side,s in [('L',1),('R',-1)]:
    m=(cq.Workplane('YZ').center(s*MOTOR_Y,WHEEL_Z).circle(MOTOR_D/2).extrude(MOTOR_L).translate((MOTOR_X,0,0)))
    motors.append((side,m))

th,q1,q2,camx=qpoints(CAM_Z)
arms=[]
for y in (-ARM_Y,ARM_Y):
    arms.append(plate_link((BODY_PIVOT_X,PIVOT_Z_LOW),q1,y))
    arms.append(plate_link((BODY_PIVOT_X,PIVOT_Z_HIGH),q2,y))
cheeks=[]
for y in (-31.5,31.5):
    ch=(cq.Workplane('XZ').workplane(offset=y-2.5).box(24,60,5,centered=(True,True,False)).translate((camx,0,CAM_Z)))
    cheeks.append(ch)
bridge=cq.Workplane('XY').box(12,68,5,centered=True).translate((camx+40,0,CAM_Z))
camera=oriented_camera(camx,CAM_Z,0)
front_ret=(cq.Workplane('YZ').circle(26).circle(15).extrude(5).translate((camx-CAM_LEN/2-5,0,CAM_Z)))
rear_cap=(cq.Workplane('YZ').circle(26).extrude(5).translate((camx+CAM_LEN/2,0,CAM_Z)))

anchor=cq.Workplane('XY').box(22,42,34,centered=(False,True,False)).translate((L-12,0,28))
conn=(cq.Workplane('YZ').circle(22).extrude(5).translate((L,0,45)))
fill=(cq.Workplane('YZ').circle(6).extrude(12).translate((L-4,-27,69)))
boot=(cq.Workplane('YZ').circle(13).workplane(offset=100).circle(TAIL_CABLE_OD/2).loft().translate((L+5,0,45)))

assy=cq.Assembly(name='PX1_FullCrawler_RevFS')
assy.add(body,name='P0_MainBody'); assy.add(cover_top,name='P0_TopCover')
for side,c in side_covers: assy.add(c,name=f'P{1 if side=="L" else 2}_SideCover_{side}')
for side,x,f in flanges: assy.add(f,name=f'Flange_{side}_{int(x)}')
for side,x,g in gears: assy.add(g,name=f'Z50_{side}_{int(x)}')
for side,x,w in wheels: assy.add(w,name=f'Wheel_{side}_{int(x)}')
for side,m in motors: assy.add(m,name=f'JGB37_{side}')
for i,a in enumerate(arms): assy.add(a,name=f'LiftArm_{i+1}')
for i,ch in enumerate(cheeks): assy.add(ch,name=f'YokeCheek_{i+1}')
assy.add(bridge,name='YokeBridge'); assy.add(camera,name='CameraShell')
assy.add(front_ret,name='CameraFrontRetainer'); assy.add(rear_cap,name='CameraRearClosure')
assy.add(anchor,name='RearTetherAnchor'); assy.add(conn,name='RearConnectorAdapter'); assy.add(fill,name='PressureFillBoss'); assy.add(boot,name='TetherBendSupport')

out=os.path.abspath('build_revfs'); os.makedirs(out,exist_ok=True)
assy.save(os.path.join(out,'PX1_FullCrawler_RevFS.step'))
for nm,p in [('P0_MainBody_RevFS',body),('P0_TopCover_RevFS',cover_top),('CameraFrontRetainer_RevFS',front_ret),('RearConnectorAdapter_RevFS',conn),('RearTetherAnchor_RevFS',anchor)]:
    cq.exporters.export(p,os.path.join(out,nm+'.step'))

pipe=(cq.Workplane('YZ').circle(PIPE_R).extrude(L+30).translate((-10,0,PIPE_Z)))
check_parts={'body':body,'top_cover':cover_top,'front_retainer':front_ret,'rear_cap':rear_cap,'yoke_bridge':bridge}
for i,a in enumerate(arms): check_parts[f'arm_{i+1}']=a
for i,ch in enumerate(cheeks): check_parts[f'cheek_{i+1}']=ch
for side,c in side_covers: check_parts[f'cover_{side}']=c
for side,x,f in flanges: check_parts[f'flange_{side}_{int(x)}']=f
outside={name:p.cut(pipe).val().Volume() for name,p in check_parts.items()}
cam_tilt=[]
for deg in range(-105,106,3):
    c=oriented_camera(camx,CAM_Z,deg); cam_tilt.append((deg,c.cut(pipe).val().Volume()))
worst_cam=max(cam_tilt,key=lambda t:t[1])
wheel_out={f'{side}_{int(x)}':w.cut(pipe).val().Volume() for side,x,w in wheels}
def radial_clearance(y,z): return PIPE_R-math.hypot(y,z-PIPE_Z)
metrics={
 'body_bbox_mm':bbox_dims(body),
 'assembly_nominal_length_body_mm':L,
 'overall_wheel_outer_width_mm':134.0,
 'wheel_centers_x_mm':WX,
 'wheel_pitch_mm':100.0,
 'side_cover_bbox_mm':[COVER_L,COVER_T,COVER_H],
 'camera_axis_low_XZ_mm':[camx,CAM_Z],
 'lift_angle_low_deg':math.degrees(th),
 'dn150_nonwheel_outside_volume_mm3':outside,
 'dn150_camera_worst_outside_volume_mm3':worst_cam[1],
 'dn150_camera_worst_tilt_deg':worst_cam[0],
 'dn150_wheel_outside_volume_mm3':wheel_out,
 'critical_clearance_sidecover_lower_corner_mm':radial_clearance(51.0,COVER_Z0),
 'critical_clearance_flange_outer_low_mm':radial_clearance(54.0,WHEEL_Z-25.0),
 'critical_clearance_upper_lift_hardware_y31_z112_mm':radial_clearance(31.0,112.0),
 'status':'prototype integrated CAD; exact bought parts, screw heads, cable loop, ovality/deposits and physical tube sweep remain gates'
}
with open(os.path.join(out,'REV_FS_INTEGRATED_VALIDATION.json'),'w') as f: json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))