import cadquery as cq
import math, json, os

OUT=os.path.abspath('build_wb17'); os.makedirs(OUT,exist_ok=True)
PIPE_R=75.0
PIPE_Z=52.0480547
WHEEL_X=(50.0,150.0,250.0)
WHEEL_Z=45.0
WHEEL_CENTER_Y=59.0
WHEEL_OD=90.0
WHEEL_W=16.0
CAM_X=83.557
CAM_Z=75.0
CAM_OD=52.0
CAM_L=78.0
TILT_RANGE=(-105.0,105.0)
YOKE_HALF_W=34.0
PIVOT_D=8.0
PIVOT_BORE=4.0
BEARING_D=16.0
BEARING_B=4.0
SEAL_D=16.0
SEAL_B=7.0
BOSS_OD=20.0
BOSS_L=13.0
CABLE_POD_OD=24.0
CABLE_POD_L=14.0

wp=lambda s: cq.Workplane('XY').newObject([s])
def cyl_y(x,y0,z,r,l,sgn=1):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cyl_y_center(x,y,z,r,l):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_x_center(x,y,z,r,l):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))

pipe=wp(cq.Solid.makeCylinder(PIPE_R,400,cq.Vector(-50,0,PIPE_Z),cq.Vector(1,0,0)))

# HARD LOCK: exactly 3 wheel stations per side / 6 wheels total.
wheels=[]
for side in (-1,1):
    for x in WHEEL_X:
        wheels.append((side,x,cyl_y_center(x,side*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)))

base_cam=cyl_x_center(CAM_X,0,CAM_Z,CAM_OD/2,CAM_L)
left_boss=cyl_y(CAM_X,0,CAM_Z,BOSS_OD/2,YOKE_HALF_W+BOSS_L,1)
right_boss=cyl_y(CAM_X,0,CAM_Z,BOSS_OD/2,YOKE_HALF_W+BOSS_L,-1)
pod=cyl_y(CAM_X,YOKE_HALF_W,CAM_Z,CABLE_POD_OD/2,CABLE_POD_L,1)

min_clear=1e9
worst=None
for deg in [TILT_RANGE[0]+i*(TILT_RANGE[1]-TILT_RANGE[0])/210 for i in range(211)]:
    maxrad=0.0
    a=math.radians(deg)
    for ti in range(41):
        t=-CAM_L/2+CAM_L*ti/40
        for pi in range(73):
            p=2*math.pi*pi/72
            y=(CAM_OD/2)*math.sin(p)
            z=CAM_Z+t*math.sin(a)+(CAM_OD/2)*math.cos(p)*math.cos(a)
            rr=math.hypot(y,z-PIPE_Z)
            maxrad=max(maxrad,rr)
    clr=PIPE_R-maxrad
    if clr<min_clear:
        min_clear=clr; worst=deg

def radial_margin(y,z,r):
    return PIPE_R-(math.hypot(y,z-PIPE_Z)+r)

wire_area=2*math.pi*(1.3/2)**2+4*math.pi*(1.0/2)**2
bore_area=math.pi*(PIVOT_BORE/2)**2
fill=wire_area/bore_area
OD=PIVOT_D; ID=PIVOT_BORE
I=math.pi/64*(OD**4-ID**4)
J=math.pi/32*(OD**4-ID**4)
Z=I/(OD/2)
m=0.25; g=9.81; ecc=0.03
M3=3*m*g*ecc; M5=5*m*g*ecc
sig3=M3*1000/Z; sig5=M5*1000/Z
tau221=(0.221*1000)*(OD/2)/J
seal_v=2*math.pi*(PIVOT_D/2/1000)*(30/360)
loop_arc=12*math.radians(210)

checks={
  'status':'PASS_SCREEN',
  'architecture':{
    'axles_wheel_stations':3,
    'wheels_total':len(wheels),
    'wheel_x_mm':list(WHEEL_X),
    'wheelbase_front_to_rear_mm':WHEEL_X[-1]-WHEEL_X[0],
    'rule':'3 AXLES / 6 WHEELS HARD LOCK'
  },
  'camera_low':{
    'axis_xyz_mm':[CAM_X,0,CAM_Z],
    'shell_od_mm':CAM_OD,
    'shell_length_mm':CAM_L,
    'tilt_range_deg':list(TILT_RANGE),
    'min_ideal_dn150_camera_shell_clearance_mm':min_clear,
    'worst_tilt_deg':worst
  },
  'wb17_pivots':{
    'shaft_od_mm':PIVOT_D,
    'cable_bore_mm':PIVOT_BORE,
    'bearing':'618/8 8x16x4',
    'seal_target':'FKM 8x16x7',
    'boss_od_mm':BOSS_OD,
    'boss_margin_ideal_dn150_mm':radial_margin(YOKE_HALF_W,CAM_Z,BOSS_OD/2),
    'cable_pod_od_mm':CABLE_POD_OD,
    'cable_pod_outer_center_y_mm':YOKE_HALF_W+CABLE_POD_L/2,
    'cable_pod_margin_ideal_dn150_mm':radial_margin(YOKE_HALF_W+CABLE_POD_L,CAM_Z,CABLE_POD_OD/2)
  },
  'cable':{
    'power_wires':'2 x ~1.3 mm OD',
    'signal_wires':'4 x ~1.0 mm OD',
    'bore_area_fill_ratio':fill,
    'free_loop_radius_mm':12.0,
    'arc_length_for_210deg_mm':loop_arc,
    'recommended_free_flex_length_mm':55.0
  },
  'shaft_screen':{
    'I_mm4':I,'J_mm4':J,'Z_mm3':Z,
    '3g_bending_stress_MPa':sig3,
    '5g_bending_stress_MPa':sig5,
    'torsion_0p221Nm_MPa':tau221
  },
  'seal_screen':{
    'circumferential_speed_at_30deg_s_mps':seal_v,
    'nominal_pressure_bar_g':0.25
  },
  'release_holds':[
    'exact 8x16x7 FKM seal article purchased and measured',
    'exact 618/8 bearing article purchased and measured',
    'real shaft seal-land finish and hardness',
    '500-cycle then endurance wire-flex test with powered CVBS/UART',
    'exact m0.5 Z40 8mm-bore worm wheel and matched worm',
    'full yoke fasteners/covers/SP13 integrated in master CAD',
    'physical DN150 tube sweep on six-wheel crawler'
  ]
}

if len(wheels)!=6 or min_clear<0 or checks['wb17_pivots']['boss_margin_ideal_dn150_mm']<0 or checks['wb17_pivots']['cable_pod_margin_ideal_dn150_mm']<0 or fill>0.55:
    checks['status']='FAIL_SCREEN'

assy=cq.Assembly(name='PX1_WB17_3AXLE_6W_CAMERA')
for side,x,w in wheels: assy.add(w,name=f'Wheel_S{side:+d}_X{int(x)}')
assy.add(base_cam,name='CameraShell_LOW')
assy.add(left_boss,name='TiltBoss_CableSide')
assy.add(right_boss,name='TiltBoss_GearSide')
assy.add(pod,name='CableSideDryPod')
assy.save(os.path.join(OUT,'PX1_WB17_3AXLE_6W_CAMERA.step'))
with open(os.path.join(OUT,'REV_B_WB17_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS_SCREEN': raise SystemExit(2)
