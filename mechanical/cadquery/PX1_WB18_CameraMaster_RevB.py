import cadquery as cq
import math, json, os

# PX-1 Rev.B WB18 — integrated camera/yoke package against HARD 3-AXLE / 6-WHEEL master
# Engineering validation model, NOT machining release.

OUT='/mnt/data/build_wb18'
os.makedirs(OUT, exist_ok=True)

# ---- hard crawler architecture lock ----
PIPE_R=75.0
PIPE_Z=52.0480547
WHEEL_X=(50.0,150.0,250.0)
WHEEL_Z=45.0
WHEEL_CENTER_Y=59.0
WHEEL_OD=90.0
WHEEL_W=16.0

# ---- LOW camera/lift datum from active Rev.FN/WB17 ----
CAM_X=83.557
CAM_Z=75.0
TILT_MIN=-105.0
TILT_MAX=105.0

# optical shell hard target
HEAD_OD=52.0
HEAD_R=HEAD_OD/2
HEAD_L=78.0
HEAD_WALL=2.5
HEAD_IN_R=HEAD_R-HEAD_WALL

# real WB17 tilt side stack
PIVOT_D=8.0
PIVOT_BORE=4.0
SEAL_OD=16.0
SEAL_W=7.0
BEARING_OD=16.0
BEARING_ID=8.0
BEARING_W=4.0
STACK_SPACER=1.0
STACK_RETAINER=1.5
BOSS_OD=20.0
STACK_SERVICE_MARGIN=0.5
BOSS_OUTER_Y=HEAD_R + SEAL_W + STACK_SPACER + BEARING_W + STACK_RETAINER + STACK_SERVICE_MARGIN
BOSS_LEN=BOSS_OUTER_Y-HEAD_R
BOSS_GAP_TO_YOKE=0.75
YOKE_T=5.5
YOKE_INNER_Y=BOSS_OUTER_Y+BOSS_GAP_TO_YOKE
YOKE_CENTRE_Y=YOKE_INNER_Y+YOKE_T/2
YOKE_OUTER_Y=YOKE_CENTRE_Y+YOKE_T/2
YOKE_R=29.0
YOKE_INNER_R=10.75

# cable side sealed cap/pod over hollow fixed pivot
CABLE_POD_OD=24.0
CABLE_POD_LEN=14.0
CABLE_POD_START_Y=YOKE_OUTER_Y

# tilt worm wheel / moving worm set
TILT_WHEEL_M=0.5
TILT_WHEEL_Z=40
TILT_WHEEL_PD=TILT_WHEEL_M*TILT_WHEEL_Z
TILT_WHEEL_OD=21.5
TILT_WHEEL_FACE=5.0
TILT_WHEEL_Y=-16.75
WORM_PD=9.0
WORM_OD=10.0
WORM_LEN=18.0
WORM_CENTRE_DIST=(TILT_WHEEL_PD+WORM_PD)/2.0
TILT_POD_X=56.0
TILT_POD_OD=18.0
TILT_POD_INNER_D=15.0
TILT_POD_Y=TILT_POD_OD
TILT_POD_Z=TILT_POD_OD
TILT_POD_CX=CAM_X+12.0
TILT_POD_CY=TILT_WHEEL_Y
TILT_POD_CZ=CAM_Z+WORM_CENTRE_DIST

# roll package
ROLL_BRG_OD=26.0
ROLL_BRG_ID=17.0
ROLL_BRG_W=5.0
ROLL_BRG_X1=CAM_X+7.0
ROLL_BRG_X2=CAM_X+23.0
ROLL_GEAR_OD=26.5
ROLL_GEAR_ID=17.0
ROLL_GEAR_W=3.0
ROLL_GEAR_X=CAM_X+0.0
M125_OD=12.5
M125_L=13.5
M125_X=CAM_X+20.0
RUNCAM_X0=CAM_X-32.0
RUNCAM_L=20.0
RUNCAM_W=19.0
RUNCAM_H=20.0
ROLL_MOTOR_L=34.0
ROLL_MOTOR_W=10.0
ROLL_MOTOR_H=10.0
ROLL_MOTOR_X0=CAM_X-38.0
ROLL_MOTOR_CY=16.0
ROLL_MOTOR_CZ=CAM_Z
ROLL_PINION_OD=9.5
ROLL_PINION_W=3.0

# front optics / light ring
WINDOW_D=28.0
WINDOW_T=3.0
LED_PCD=40.0
LED_BOARD=8.0
LED_T=1.5
LED_X=CAM_X-36.0

# fixed rear bridge + SP13 (fixed relative to TILT yoke, axis +X toward crawler)
BRIDGE_CX=CAM_X+58.0
BRIDGE_CZ=CAM_Z+20.0
BRIDGE_X=8.0
BRIDGE_Y=2*YOKE_OUTER_Y
BRIDGE_Z=10.0
SP13_PANEL_OD=19.5
SP13_FRONT_L=9.5
SP13_REAR_OD=13.0
SP13_REAR_L=9.7
SP13_PLUG_OD=18.8
SP13_PLUG_L=49.0
SP13_AXIS_Y=0.0
SP13_AXIS_Z=BRIDGE_CZ
SP13_PANEL_X=BRIDGE_CX+BRIDGE_X/2

wp=lambda s: cq.Workplane('XY').newObject([s])
def cyl_x(x0,y,z,r,l):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_x_center(x,y,z,r,l):
    return cyl_x(x-l/2,y,z,r,l)
def cyl_y(y0,x,z,r,l,sgn=1):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cyl_y_center(x,y,z,r,l):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def boxc(x,y,z,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def ring_x_center(x,y,z,ro,ri,l):
    return cq.Workplane('YZ').center(y,z).circle(ro).circle(ri).extrude(l/2,both=True).translate((x,0,0))
def ring_y_center(x,y,z,ro,ri,l):
    outer=cyl_y_center(x,y,z,ro,l)
    inner=cyl_y_center(x,y,z,ri,l+0.2)
    return wp(outer.val().cut(inner.val()))
def rotate_y(part,deg):
    return part.rotate((CAM_X,0,CAM_Z),(CAM_X,1,CAM_Z),deg)
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def intersect_vol(a,b):
    return a.val().intersect(b.val()).Volume()
def outside_vol(a,b):
    return a.val().cut(b.val()).Volume()
def mesh_radial_required(part,tol=0.45):
    verts,_=part.val().tessellate(tol)
    if not verts: return 0.0
    return max(math.hypot(v.y, v.z-PIPE_Z) for v in verts)

# HARD LOCK: exactly three wheel stations per side / six wheels total.
wheels=[]
for side in (-1,1):
    for x in WHEEL_X:
        wheels.append((side,x,cyl_y_center(x,side*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)))
assert len(wheels)==6 and WHEEL_X==(50.0,150.0,250.0)

# moving P3 outer hard parts at TILT=0
shell=cyl_x_center(CAM_X,0,CAM_Z,HEAD_R,HEAD_L)
boss_pos=cyl_y(HEAD_R,CAM_X,CAM_Z,BOSS_OD/2,BOSS_LEN,1)
boss_neg=cyl_y(-HEAD_R,CAM_X,CAM_Z,BOSS_OD/2,BOSS_LEN,-1)
tilt_pod=cyl_x_center(TILT_POD_CX,TILT_POD_CY,TILT_POD_CZ,TILT_POD_OD/2,TILT_POD_X)
front_ring=ring_x_center(CAM_X-36.0,0,CAM_Z,HEAD_R,WINDOW_D/2,4.0)
moving_outer=fuse_all([shell,boss_pos,boss_neg,tilt_pod,front_ring])

# fixed yoke hard parts
yoke_pos=ring_y_center(CAM_X,+YOKE_CENTRE_Y,CAM_Z,YOKE_R,YOKE_INNER_R,YOKE_T)
yoke_neg=ring_y_center(CAM_X,-YOKE_CENTRE_Y,CAM_Z,YOKE_R,YOKE_INNER_R,YOKE_T)
bridge=boxc(BRIDGE_CX,0,BRIDGE_CZ,BRIDGE_X,BRIDGE_Y,BRIDGE_Z)
cable_pod=cyl_y(CABLE_POD_START_Y,CAM_X,CAM_Z,CABLE_POD_OD/2,CABLE_POD_LEN,1)
sp13_front=cyl_x(SP13_PANEL_X,SP13_AXIS_Y,SP13_AXIS_Z,SP13_PANEL_OD/2,SP13_FRONT_L)
sp13_rear=cyl_x(SP13_PANEL_X-SP13_REAR_L,SP13_AXIS_Y,SP13_AXIS_Z,SP13_REAR_OD/2,SP13_REAR_L)
sp13_plug=cyl_x(SP13_PANEL_X+SP13_FRONT_L,SP13_AXIS_Y,SP13_AXIS_Z,SP13_PLUG_OD/2,SP13_PLUG_L)
fixed_collision=fuse_all([yoke_pos,yoke_neg,bridge,cable_pod,sp13_front,sp13_rear,sp13_plug])

# fixed pivots + Z40 intentionally occupy the moving bearing/gear interfaces
pivot_pos=cyl_y_center(CAM_X,+32.0,CAM_Z,PIVOT_D/2,34.0)
pivot_neg=cyl_y_center(CAM_X,-32.0,CAM_Z,PIVOT_D/2,34.0)
tilt_wheel=ring_y_center(CAM_X,TILT_WHEEL_Y,CAM_Z,TILT_WHEEL_OD/2,PIVOT_D/2,TILT_WHEEL_FACE)

# side stack envelopes inside moving bosses
brg_pos=ring_y_center(CAM_X,HEAD_R+STACK_RETAINER+BEARING_W/2,CAM_Z,BEARING_OD/2,BEARING_ID/2,BEARING_W)
seal_pos=ring_y_center(CAM_X,BOSS_OUTER_Y-SEAL_W/2,CAM_Z,SEAL_OD/2,PIVOT_D/2,SEAL_W)
brg_neg=ring_y_center(CAM_X,-(HEAD_R+STACK_RETAINER+BEARING_W/2),CAM_Z,BEARING_OD/2,BEARING_ID/2,BEARING_W)
seal_neg=ring_y_center(CAM_X,-(BOSS_OUTER_Y-SEAL_W/2),CAM_Z,SEAL_OD/2,PIVOT_D/2,SEAL_W)

# internal ROLL/camera components
inner_cavity=cyl_x_center(CAM_X,0,CAM_Z,HEAD_IN_R,HEAD_L-2.0)
runcam=boxc(RUNCAM_X0+RUNCAM_L/2,0,CAM_Z,RUNCAM_L,RUNCAM_W,RUNCAM_H)
roll_brg1=ring_x_center(ROLL_BRG_X1,0,CAM_Z,ROLL_BRG_OD/2,ROLL_BRG_ID/2,ROLL_BRG_W)
roll_brg2=ring_x_center(ROLL_BRG_X2,0,CAM_Z,ROLL_BRG_OD/2,ROLL_BRG_ID/2,ROLL_BRG_W)
roll_gear=ring_x_center(ROLL_GEAR_X,0,CAM_Z,ROLL_GEAR_OD/2,ROLL_GEAR_ID/2,ROLL_GEAR_W)
m125=cyl_x(M125_X,0,CAM_Z,M125_OD/2,M125_L)
roll_motor=boxc(ROLL_MOTOR_X0+ROLL_MOTOR_L/2,ROLL_MOTOR_CY,ROLL_MOTOR_CZ,ROLL_MOTOR_L,ROLL_MOTOR_W,ROLL_MOTOR_H)
roll_pinion=cyl_x(ROLL_GEAR_X-ROLL_PINION_W/2,ROLL_MOTOR_CY,ROLL_MOTOR_CZ,ROLL_PINION_OD/2,ROLL_PINION_W)

# moving TILT worm/motor; integrated P3 pod, not cartridge/cassette
worm=cyl_x_center(CAM_X-5.0,TILT_WHEEL_Y,CAM_Z+WORM_CENTRE_DIST,WORM_OD/2,WORM_LEN)
tilt_motor=boxc(CAM_X+21.0,TILT_WHEEL_Y,CAM_Z+WORM_CENTRE_DIST,34.0,10.0,10.0)
tilt_pod_cavity=cyl_x_center(TILT_POD_CX,TILT_POD_CY,TILT_POD_CZ,TILT_POD_INNER_D/2,TILT_POD_X-3.0)

window=cyl_x(CAM_X-39.0,0,CAM_Z,WINDOW_D/2,WINDOW_T)
leds=[]
for i in range(6):
    a=math.radians(i*60)
    y=(LED_PCD/2)*math.cos(a)
    z=CAM_Z+(LED_PCD/2)*math.sin(a)
    leds.append(boxc(LED_X,y,z,LED_T,LED_BOARD,LED_BOARD))

# internal containment
main_internal={
    'RunCam':runcam,
    'RollBearing1':roll_brg1,
    'RollBearing2':roll_brg2,
    'RollGear':roll_gear,
    'M125':m125,
    'RollMotor':roll_motor,
    'RollPinion':roll_pinion,
    'Window':window,
}
main_out={k:outside_vol(v,inner_cavity) for k,v in main_internal.items() if k!='Window'}
pod_out={'Worm':outside_vol(worm,tilt_pod_cavity),'TiltMotor':outside_vol(tilt_motor,tilt_pod_cavity)}

internal_pairs=[]
items=[(k,v) for k,v in main_internal.items() if k!='Window']
for i,(ka,a) in enumerate(items):
    for kb,b in items[i+1:]:
        if {ka,kb}=={'RollGear','RollPinion'}:
            continue
        iv=intersect_vol(a,b)
        if iv>1e-4:
            internal_pairs.append([ka,kb,iv])

tilt_wheel_collisions=[]
for kb,b in items:
    iv=intersect_vol(tilt_wheel,b)
    if iv>1e-4:
        tilt_wheel_collisions.append(['TiltWheelZ40',kb,iv])

m125_radial_margin=ROLL_BRG_ID/2-M125_OD/2

# full 1 degree TILT sweep
angles=[TILT_MIN+i*1.0 for i in range(int((TILT_MAX-TILT_MIN)/1)+1)]
if angles[-1] != TILT_MAX: angles.append(TILT_MAX)
min_clear=1e9
worst_angle=None
max_fixed_collision=0.0
coll_angle=None
clearance_curve=[]
for deg in angles:
    m=rotate_y(moving_outer,deg)
    req=mesh_radial_required(m,0.55)
    clr=PIPE_R-req
    clearance_curve.append((deg,clr))
    if clr<min_clear:
        min_clear=clr; worst_angle=deg
    iv=intersect_vol(m,fixed_collision)
    if iv>max_fixed_collision:
        max_fixed_collision=iv; coll_angle=deg

def contiguous_ranges(curve, threshold):
    good=[(a,c) for a,c in curve if c>=threshold]
    if not good: return []
    ranges=[]
    start=prev=good[0][0]
    minc=good[0][1]
    for a,c in good[1:]:
        if abs(a-prev-1.0)<1e-9:
            prev=a; minc=min(minc,c)
        else:
            ranges.append([start,prev,minc])
            start=prev=a; minc=c
    ranges.append([start,prev,minc])
    return ranges

safe5_ranges=contiguous_ranges(clearance_curve,5.0)
safe3_ranges=contiguous_ranges(clearance_curve,3.0)
fixed_req=mesh_radial_required(fixed_collision,0.55)
fixed_clear=PIPE_R-fixed_req

stack_required=SEAL_W+STACK_SPACER+BEARING_W+STACK_RETAINER
stack_available=BOSS_LEN
stack_margin=stack_available-stack_required

architecture_ok=(len(wheels)==6 and WHEEL_X==(50.0,150.0,250.0))
internal_ok=(all(v<1e-4 for v in main_out.values()) and all(v<1e-4 for v in pod_out.values()) and not internal_pairs and not tilt_wheel_collisions and m125_radial_margin>=2.0)
sweep_ok=(min_clear>0.0 and fixed_clear>0.0 and max_fixed_collision<1e-4)
stack_ok=(stack_margin>=-1e-9)
status='PASS_SCREEN' if architecture_ok and internal_ok and sweep_ok and stack_ok else 'FAIL_SCREEN'

checks={
    'status':status,
    'architecture':{
        'axles_wheel_stations':3,
        'wheels_total':len(wheels),
        'wheel_x_mm':list(WHEEL_X),
        'drive_station_x_mm':250.0,
        'rule':'3 AXLES / 6 WHEELS HARD LOCK'
    },
    'camera':{
        'pivot_xyz_mm':[CAM_X,0,CAM_Z],
        'optical_shell_od_mm':HEAD_OD,
        'optical_shell_length_mm':HEAD_L,
        'tilt_range_deg':[TILT_MIN,TILT_MAX],
        'moving_tilt_drive_pod':'cylindrical OD%.1f x %.1f mm' % (TILT_POD_OD,TILT_POD_X),
        'min_ideal_DN150_moving_hard_clearance_mm':min_clear,
        'worst_sampled_tilt_deg':worst_angle,
        'sample_increment_deg':1.0,
        'fixed_yoke_SP13_min_ideal_DN150_clearance_mm':fixed_clear,
        'max_unintended_moving_fixed_collision_mm3':max_fixed_collision,
        'collision_worst_angle_deg':coll_angle,
        'DN150_safe_ranges_clearance_ge_5mm_deg':safe5_ranges,
        'DN150_ranges_clearance_ge_3mm_deg':safe3_ranges
    },
    'tilt_stack':{
        'pivot':'fixed yoke pivot, shell/boss rotates around it',
        'shaft_od_mm':PIVOT_D,
        'cable_bore_mm':PIVOT_BORE,
        'seal':'8x16x7 FKM target',
        'bearing':'618/8 8x16x4 open target',
        'boss_outer_y_mm':BOSS_OUTER_Y,
        'yoke_inner_face_abs_y_mm':YOKE_INNER_Y,
        'yoke_center_abs_y_mm':YOKE_CENTRE_Y,
        'stack_required_mm':stack_required,
        'stack_available_mm':stack_available,
        'stack_margin_mm':stack_margin,
        'boss_to_yoke_gap_mm':BOSS_GAP_TO_YOKE,
        'worm_wheel':{'module':TILT_WHEEL_M,'teeth':TILT_WHEEL_Z,'bore_mm':8.0,'OD_screen_mm':TILT_WHEEL_OD,'fixed_to_pivot':True},
        'worm_center_distance_screen_mm':WORM_CENTRE_DIST,
        'drive_interpretation':'moving worm/N20 on P3 shell walks around fixed Z40 wheel'
    },
    'roll_package':{
        'camera':'RunCam Phoenix 2 envelope 19x19x20',
        'bearings':'2x 6803 17x26x5',
        'gear':'m0.5 z51 OD26.5 screen',
        'slip_ring':'SenRing M125-06 OD12.5 x 13.5',
        'm125_radial_margin_inside_17mm_bearing_ID_mm':m125_radial_margin,
        'roll_motor':'N20 34x10x10 screen',
        'component_outside_main_cavity_mm3':main_out,
        'unintended_internal_collisions':internal_pairs,
        'tilt_wheel_internal_collisions':tilt_wheel_collisions
    },
    'tilt_drive_pod':{
        'component_outside_pod_cavity_mm3':pod_out,
        'note':'integrated shell bulge, not a cartridge/cassette'
    },
    'quick_connector':{
        'panel':'WEIPU SP1312/P6-C fixed on non-TILT rear bridge',
        'plug':'WEIPU SP1310/S6II-N operational envelope',
        'plug_axis':'rearward +X; fixed relative to yoke, not part of TILT sweep',
        'bridge_center_x_mm':BRIDGE_CX,
        'service_plug_end_x_mm':SP13_PANEL_X+SP13_FRONT_L+SP13_PLUG_L
    },
    'front':{
        'window_mm':[WINDOW_D,WINDOW_T],
        'led_boards':'6 x 8mm class on PCD40',
        'lighting_rule':'fixed to tilting optical shell but fixed relative to internal ROLL'
    },
    'release_holds':[
        'replace all component envelopes with measured purchased samples before machining release',
        'exact 618/8 brand/tolerance and exact 8x16x7 FKM article',
        'exact matched m0.5 Z40/8mm worm wheel + worm drawing and backlash test',
        'exact N20 output shaft, body and connector dimensions',
        'physical M125 CVBS rotating qualification',
        'SP13 installed +0.25 bar pressure and submerged test',
        'WB16 external LAPP harness R55 routing with real lift-arm clamps',
        'physical DN150 tube sweep with real parts and pipe ovality/debris allowance',
        'real fastener heads/stops/home sensor and thermal paths'
    ],
    'execution':{'engine':'CadQuery 2.8.0','model':'WB18','note':'envelope-level part integration, no machining release'}
}

assy=cq.Assembly(name='PX1_WB18_3AXLE_6W_CAMERA_MASTER')
for side,x,w in wheels:
    assy.add(w,name=f'Wheel_S{side:+d}_X{int(x)}')
assy.add(moving_outer,name='Camera_P3_Outer_Tilt0')
assy.add(yoke_pos,name='YokeCheek_CableSide')
assy.add(yoke_neg,name='YokeCheek_GearSide')
assy.add(bridge,name='RearYokeBridge')
assy.add(cable_pod,name='CableSideDryPod')
assy.add(sp13_front,name='SP1312_front_envelope')
assy.add(sp13_rear,name='SP1312_rear_envelope')
assy.add(sp13_plug,name='SP1310_S6II_plug_envelope')
assy.add(pivot_pos,name='FixedPivot_Cable_8x4_screen')
assy.add(pivot_neg,name='FixedPivot_Gear_8_screen')
assy.add(tilt_wheel,name='TiltWheel_Z40_fixed_screen')
assy.add(brg_pos,name='TiltBearing_Cable_618_8')
assy.add(seal_pos,name='TiltSeal_Cable_8x16x7')
assy.add(brg_neg,name='TiltBearing_Gear_618_8')
assy.add(seal_neg,name='TiltSeal_Gear_8x16x7')
assy.add(runcam,name='RunCam_Phoenix2')
assy.add(roll_brg1,name='RollBearing_6803_front')
assy.add(roll_brg2,name='RollBearing_6803_rear')
assy.add(roll_gear,name='RollGear_z51')
assy.add(m125,name='M125_06')
assy.add(roll_motor,name='Roll_N20')
assy.add(roll_pinion,name='RollPinion_z17_screen')
assy.add(worm,name='TiltWorm_m05_screen')
assy.add(tilt_motor,name='Tilt_N20')
assy.add(window,name='Window_28x3')
for i,led in enumerate(leds,1): assy.add(led,name=f'LED_MCPCB_{i}')

assy.save(os.path.join(OUT,'PX1_WB18_3AXLE_6W_CAMERA_MASTER.step'))
with open(os.path.join(OUT,'REV_B_WB18_VALIDATION.json'),'w') as f:
    json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if status!='PASS_SCREEN':
    raise SystemExit(2)
