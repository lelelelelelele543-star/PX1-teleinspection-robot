import cadquery as cq
import math, json, os

# PX-1 Rev.PC — serviceable CAM026-like camera mechanical reconstruction
# Published CAM026 control envelope: 120 x 73 x 73 mm, 360 rotate, +/-135 pan, 75 deg FOV.
# Mechanical source references: ASS-001-801 / 802 / 803 / 917 / 919 / 920 / 998.
# Proprietary focus system intentionally deleted from PX-1 baseline.

OUT=os.path.abspath('build_revpc')
os.makedirs(OUT,exist_ok=True)

L=120.0; W=73.0; H=73.0
RMAX=36.5
FRONT_HEAD_X=22.0
HEAD_OD=50.0
HEAD_LEN=46.0
REAR_ROT_X=70.0
REAR_ROT_LEN=50.0
REAR_OD=73.0
YOKE_T=6.0
YOKE_Y=30.5
PAN_AXIS_X=48.0
PAN_AXIS_Z=0.0


def cyl_x(x0,y,z,r,l):
    return cq.Workplane('YZ').center(y,z).circle(r).extrude(l).translate((x0,0,0))

def ring_x(x0,y,z,ro,ri,l):
    return cq.Workplane('YZ').center(y,z).circle(ro).circle(ri).extrude(l).translate((x0,0,0))

rear_outer=cyl_x(REAR_ROT_X,0,0,REAR_OD/2,REAR_ROT_LEN)
rear_inner=cyl_x(REAR_ROT_X+5,0,0,30.0,REAR_ROT_LEN-10)
rear_shell=rear_outer.cut(rear_inner)
rear_guard=ring_x(112,0,0,36.5,30.5,8)

yokes={}
for side,sgn in [('L',1),('R',-1)]:
    y0=sgn*YOKE_Y
    plate=(cq.Workplane('XZ').workplane(offset=y0-YOKE_T/2).center(56,0)
           .circle(36.5).circle(27.0).extrude(YOKE_T))
    opening=(cq.Workplane('XZ').workplane(offset=y0-YOKE_T/2-0.1)
             .box(62,44,YOKE_T+0.2,centered=(True,True,False)).translate((28,0,0)))
    plate=plate.cut(opening)
    bore=(cq.Workplane('XZ').workplane(offset=y0-YOKE_T/2-0.1).center(PAN_AXIS_X,0).circle(5).extrude(YOKE_T+0.2))
    plate=plate.cut(bore)
    yokes[side]=plate

head_outer=cyl_x(4,0,0,HEAD_OD/2,HEAD_LEN)
head_inner=cyl_x(8,0,0,20.5,HEAD_LEN-10)
head_shell=head_outer.cut(head_inner)
front_plate=ring_x(0,0,0,25.0,10.5,5.0)
window=cyl_x(0,0,0,10.5,3.0)
head_rear=ring_x(45,0,0,25.0,8.0,4.0)

pan_axles={}
for side,sgn in [('L',1),('R',-1)]:
    pan_axles[side]=cq.Workplane('XZ').workplane(offset=sgn*24).center(PAN_AXIS_X,0).circle(4).extrude(12.5*sgn)

leds={}
angles=[115,145,175,-115,-145,-175]
for i,a in enumerate(angles,1):
    y=17.2*math.cos(math.radians(a)); z=17.2*math.sin(math.radians(a))
    leds[i]=cyl_x(0.0,y,z,3.2,4.5)

board_cam=cq.Workplane('YZ').box(28,28,3,centered=(True,True,False)).translate((12,0,0))
lens=cyl_x(0,0,0,7.0,18.0)
pan_motor=cyl_x(54,22,18,5.0,22.0)
rotate_motor=cyl_x(84,-18,17,5.0,24.0)
slip_outer=cyl_x(88,0,0,8.0,20.0)
slip_inner=cyl_x(88,0,0,3.0,20.0)
slip_ring=slip_outer.cut(slip_inner)

protectors={
 'L':cq.Workplane('XY').box(20,7,38,centered=(False,True,True)).translate((4,32,0)),
 'R':cq.Workplane('XY').box(20,7,38,centered=(False,True,True)).translate((4,-32,0))
}

parts={'RearRotateShell':rear_shell,'RearGuard':rear_guard,'Yoke_L':yokes['L'],'Yoke_R':yokes['R'],
       'PanHeadShell':head_shell,'FrontRetainer':front_plate,'OpticalWindow':window,'PanHeadRear':head_rear,
       'PanAxle_L':pan_axles['L'],'PanAxle_R':pan_axles['R'],'FixedFocusBoardCamera':board_cam,'LensEnvelope':lens,
       'PanMotorEnvelope':pan_motor,'RotateMotorEnvelope':rotate_motor,'SlipRing6wayEnvelope':slip_ring,
       'RubberProtector_L':protectors['L'],'RubberProtector_R':protectors['R']}
for i,l in leds.items(): parts[f'LED_{i}']=l

assy=cq.Assembly(name='PX1_CAM026_Replacement_RevPC')
for n,p in parts.items():
    if 'Yoke' in n: col=cq.Color(0.68,0.70,0.66)
    elif 'Shell' in n or 'Retainer' in n or 'Guard' in n or 'Axle' in n: col=cq.Color(0.30,0.31,0.32)
    elif 'LED' in n: col=cq.Color(0.92,0.92,0.80)
    elif 'Rubber' in n: col=cq.Color(0.04,0.04,0.04)
    elif 'Motor' in n: col=cq.Color(0.34,0.42,0.55)
    elif 'Window' in n: col=cq.Color(0.45,0.70,0.82,0.5)
    else: col=cq.Color(0.5,0.5,0.5)
    assy.add(p,name=n,color=col)
assy.save(os.path.join(OUT,'PX1_CAM026_Replacement_RevPC.step'))

head_union=head_shell.val().fuse(front_plate.val()).fuse(head_rear.val()).fuse(window.val())
bbox_ref=cq.Solid.makeBox(120,73,73,cq.Vector(0,-36.5,-36.5))
pan_out={}
for deg in [-135,-90,-45,0,45,90,135]:
    rot=head_union.rotate(cq.Vector(PAN_AXIS_X,0,0),cq.Vector(PAN_AXIS_X,1,0),deg)
    pan_out[str(deg)]=round(rot.cut(bbox_ref).Volume(),4)

shape=None
for p in parts.values(): shape=p.val() if shape is None else shape.fuse(p.val())
bb=shape.BoundingBox()
checks={
 'published_target_mm':[120,73,73],
 'current_bbox_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],
 'published_pan_deg':[-135,135],
 'published_rotate_deg':'continuous 360',
 'published_fov_deg':75,
 'six_led_layout':'2 clusters x 3 LEDs',
 'focus_system':'deleted; fixed-focus baseline',
 'proprietary_camera_pcbs':'deleted from baseline',
 'slip_ring_function':'6-way source function retained; exact current article TBD',
 'pan_head_outside_120x73x73_reference_mm3':pan_out,
 'status':'SOURCE-ARCHITECTURE CAMERA BASELINE; exact yoke profile, motor articles, seals and optical window remain detailed gates'
}
with open(os.path.join(OUT,'REV_PC_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))