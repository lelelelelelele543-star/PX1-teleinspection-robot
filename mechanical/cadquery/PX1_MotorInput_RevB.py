import cadquery as cq
import math, json, os

# PX-1 Rev.B WB04 — motor / supported Z16 input packaging screen
# NOT a machining release. Exact bevel mounting distance and motor sample remain gates.

OUT=os.path.abspath('build_revb_wb04'); os.makedirs(OUT, exist_ok=True)
PIPE_R=75.0
PIPE_Z=52.0480547
DRIVE_X=250.0
AXIS_Y=18.0
AXIS_Z=45.0

# Candidate rear pressure extension, widened only to create service/thermal clearance.
REAR_X0=242.0
REAR_X1=384.0
REAR_Y_HALF=46.0
REAR_Z0=19.0
REAR_Z1=71.0
CAV_X0=246.0
CAV_X1=378.0
CAV_Y_HALF=40.0
CAV_Z0=24.0
CAV_Z1=66.0

# Leading motor candidate ISL PGM-32P-24-100-60-02.
MOTOR_OD=32.0
MOTOR_TOTAL=92.0       # shaft tip to rear end product dimension
MOTOR_SHAFT_D=6.0
MOTOR_SHAFT_LEN=12.0   # IG-32PGM family drawing screen; exact purchased sample gate
MOTOR_FACE_X=293.0     # adjustable candidate; final bevel mounting-distance gate
MOTOR_REAR_X=MOTOR_FACE_X + (MOTOR_TOTAL-MOTOR_SHAFT_LEN)
MOTOR_SHAFT_TIP_X=MOTOR_FACE_X-MOTOR_SHAFT_LEN

# NBK MLR-20C-6-6 rigid clamp coupling.
COUPLING_OD=20.0
COUPLING_LEN=24.0
COUPLING_RATED_NM=2.5
# Keep coupling in front of a 5 mm motor-holder face. The motor shaft passes through the holder.
COUPLING_X1=MOTOR_FACE_X-5.0
COUPLING_X0=COUPLING_X1-COUPLING_LEN
MOTOR_INSERTION=COUPLING_X1-MOTOR_SHAFT_TIP_X

# Source-like dedicated pinion bearing.
BEARING_ID=12.0
BEARING_OD=21.0
BEARING_W=5.0
BEARING_X1=COUPLING_X0-1.5
BEARING_X0=BEARING_X1-BEARING_W

# Packaging-only Z16 tooth envelope. Exact axial position/mounting distance TBD by final matched gear drawing.
PINION_OD_SCREEN=18.6
PINION_LEN_SCREEN=7.5
PINION_X1=BEARING_X0-0.5
PINION_X0=PINION_X1-PINION_LEN_SCREEN

# Holder face local boss envelope (not the final structural holder).
HOLDER_FACE_T=5.0
HOLDER_BOSS_OD=36.0
HOLDER_X0=MOTOR_FACE_X-HOLDER_FACE_T
HOLDER_X1=MOTOR_FACE_X


def cyl_x(x0,y,z,r,l):
    return cq.Workplane('XY').newObject([cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0))])

def box0(x0,y0,z0,dx,dy,dz):
    return cq.Workplane('XY').newObject([cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0))])

def volume_outside(a,b):
    return a.val().cut(b.val()).Volume()

def intersect_vol(a,b):
    return a.val().intersect(b.val()).Volume()

rear_outer=box0(REAR_X0,-REAR_Y_HALF,REAR_Z0,REAR_X1-REAR_X0,2*REAR_Y_HALF,REAR_Z1-REAR_Z0)
rear_cavity=box0(CAV_X0,-CAV_Y_HALF,CAV_Z0,CAV_X1-CAV_X0,2*CAV_Y_HALF,CAV_Z1-CAV_Z0)
pipe=cq.Workplane('XY').newObject([cq.Solid.makeCylinder(PIPE_R,REAR_X1-REAR_X0+20,cq.Vector(REAR_X0-10,0,PIPE_Z),cq.Vector(1,0,0))])

parts=[]
for side in (-1,1):
    y=side*AXIS_Y
    motor=cyl_x(MOTOR_FACE_X,y,AXIS_Z,MOTOR_OD/2,MOTOR_REAR_X-MOTOR_FACE_X)
    shaft=cyl_x(MOTOR_SHAFT_TIP_X,y,AXIS_Z,MOTOR_SHAFT_D/2,MOTOR_SHAFT_LEN)
    coupling=cyl_x(COUPLING_X0,y,AXIS_Z,COUPLING_OD/2,COUPLING_LEN)
    bearing=cyl_x(BEARING_X0,y,AXIS_Z,BEARING_OD/2,BEARING_W)
    pinion=cyl_x(PINION_X0,y,AXIS_Z,PINION_OD_SCREEN/2,PINION_LEN_SCREEN)
    holder_boss=cyl_x(HOLDER_X0,y,AXIS_Z,HOLDER_BOSS_OD/2,HOLDER_FACE_T)
    # Central shaft clearance through the holder face.
    holder_boss=cq.Workplane('XY').newObject([holder_boss.val().cut(cyl_x(HOLDER_X0-0.1,y,AXIS_Z,4.5,HOLDER_FACE_T+0.2).val())])
    parts.append((side,'motor',motor))
    parts.append((side,'motor_shaft',shaft))
    parts.append((side,'coupling',coupling))
    parts.append((side,'bearing',bearing))
    parts.append((side,'pinion_screen',pinion))
    parts.append((side,'holder_face_boss',holder_boss))

# Intentional overlaps: motor shaft inside coupling and motor/holder mounting face.
collision_pairs=[]
for i,(s1,n1,p1) in enumerate(parts):
    for s2,n2,p2 in parts[i+1:]:
        if s1==s2 and ({n1,n2} in [
            {'motor_shaft','coupling'}, {'motor_shaft','holder_face_boss'},
            {'motor','holder_face_boss'}
        ]):
            continue
        v=intersect_vol(p1,p2)
        if v>1e-5:
            collision_pairs.append((s1,n1,s2,n2,round(v,4)))

outside_cavity={}
outside_pipe={}
for side,name,p in parts:
    outside_cavity[f'{side}:{name}']=round(volume_outside(p,rear_cavity),6)
    outside_pipe[f'{side}:{name}']=round(volume_outside(p,pipe),6)

motor_center_gap=2*AXIS_Y-MOTOR_OD
motor_to_side_cavity=CAV_Y_HALF-(AXIS_Y+MOTOR_OD/2)
motor_vertical_cavity=min((AXIS_Z-MOTOR_OD/2)-CAV_Z0,CAV_Z1-(AXIS_Z+MOTOR_OD/2))
motor_rear_service=CAV_X1-MOTOR_REAR_X
rear_outer_margin=PIPE_R-max(math.hypot(REAR_Y_HALF,REAR_Z0-PIPE_Z),math.hypot(REAR_Y_HALF,REAR_Z1-PIPE_Z))


def tau_mpa(torque_nm,dmm=6.0):
    return 16*torque_nm*1000/(math.pi*dmm**3)

# Bearing screen using conservative SKF 61801 C=1740 N and WB03 tooth-force values.
# A 1.5 multiplier is used here only as an overhang/reaction screening allowance.
C_N=1740.0
loads={}
for T,Ft,Fr,Fa in [(0.6,88,30,12),(0.8,118,40,16),(1.0,147,50,20),(2.0,294,99,40)]:
    Pr=math.hypot(Ft,Fr)*1.5
    L10_mrev=(C_N/Pr)**3
    hours=L10_mrev*1e6/(60*60) # 60 rpm screen
    loads[str(T)]={'screen_equiv_radial_N':Pr,'L10_million_rev':L10_mrev,'L10_hours_at_60rpm':hours,'axial_N':Fa}

metrics={
    'status':'PASS_SCREEN' if (
        all(v<1e-5 for v in outside_cavity.values()) and
        all(v<1e-5 for v in outside_pipe.values()) and
        not collision_pairs and MOTOR_INSERTION>=6.0 and
        motor_center_gap>=4.0 and motor_to_side_cavity>=4.0 and motor_vertical_cavity>=3.0 and motor_rear_service>=4.0
    ) else 'FAIL_SCREEN',
    'drive_axis':{'x_intersection_nominal':DRIVE_X,'y_centers':[-AXIS_Y,AXIS_Y],'z':AXIS_Z},
    'rear_extension_candidate':{'x':[REAR_X0,REAR_X1],'width_mm':2*REAR_Y_HALF,'z':[REAR_Z0,REAR_Z1],
                                'cavity_x':[CAV_X0,CAV_X1],'cavity_width_mm':2*CAV_Y_HALF,'cavity_z':[CAV_Z0,CAV_Z1]},
    'motor':{'part':'ISL PGM-32P-24-100-60-02','OD_mm':MOTOR_OD,'total_tip_to_rear_mm':MOTOR_TOTAL,
             'shaft_d_mm':MOTOR_SHAFT_D,'shaft_len_screen_mm':MOTOR_SHAFT_LEN,'mount_face_x':MOTOR_FACE_X,
             'rear_x':MOTOR_REAR_X},
    'coupling':{'part':'NBK MLR-20C-6-6','OD_mm':COUPLING_OD,'overall_length_mm':COUPLING_LEN,
                'rated_torque_Nm':COUPLING_RATED_NM,'x':[COUPLING_X0,COUPLING_X1],
                'motor_shaft_insertion_mm':MOTOR_INSERTION},
    'pinion_bearing':{'family':'61801-2RS','id_mm':BEARING_ID,'od_mm':BEARING_OD,'width_mm':BEARING_W,
                      'x':[BEARING_X0,BEARING_X1]},
    'pinion_screen_x':[PINION_X0,PINION_X1],
    'hard_clearances_mm':{'between_motor_bodies':motor_center_gap,'motor_to_side_cavity':motor_to_side_cavity,
                          'motor_vertical_to_cavity':motor_vertical_cavity,'motor_rear_service':motor_rear_service,
                          'rear_outer_to_ideal_DN150_min':rear_outer_margin},
    'shaft_6mm_nominal_torsional_shear_MPa':{str(T):tau_mpa(T) for T in (0.6,0.8,1.0,2.0,3.923)},
    '61801_bearing_screen':loads,
    'outside_cavity_mm3':outside_cavity,
    'outside_pipe_mm3':outside_pipe,
    'unintended_collisions':collision_pairs,
    'release_holds':[
        'exact purchased ISL motor front register and shaft geometry',
        'final matched Z16/Z40 mounting distance and pinion hub/bore interface',
        'actual NBK coupling procurement and D-shaft clamp/slip test',
        'final holder structural ribs and bearing outer-ring retainer',
        'holder/motor thermal conduction test in sealed P0',
        'rear pressure-extension FEA/proof and tail connector integration'
    ]
}

assy=cq.Assembly(name='PX1_MotorInput_RevB_WB04')
assy.add(rear_outer,name='RearOuterEnvelope')
for side,name,p in parts:
    assy.add(p,name=f'S{side:+d}_{name}')
assy.save(os.path.join(OUT,'PX1_MotorInput_RevB_WB04.step'))
with open(os.path.join(OUT,'REV_B_WB04_VALIDATION.json'),'w') as f:
    json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))
if metrics['status']!='PASS_SCREEN': raise SystemExit(2)
