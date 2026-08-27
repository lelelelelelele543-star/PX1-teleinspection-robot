import cadquery as cq
import math, json, os

# PX-1 Rev.FN — manual CRP-style parallelogram lift + digital camera/yoke
# Prototype geometry only. Own PX-1 dimensions, architecture informed by uploaded Proteus drawings.

PIPE_R=75.0
PIPE_Z=52.0480547
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=112.0
LINK_L=120.0
ARM_Y=26.0
ARM_T=5.0
ARM_H=18.0
PIVOT_D=8.0
CAM_AXIS_OFFSET_Z=2.0
CAM_OD=52.0
CAM_LEN=72.0
CAM_ZS={'LOW':75.0,'MID':130.0,'HIGH':205.0}
YOKE_HALF_W=34.0
YOKE_T=5.0
YOKE_H=60.0
YOKE_X=22.0
GAS_FORCE=150.0
GAS_BASE=(220.0,35.0)
GAS_ATTACH_FROM_LOWER_PIVOT=80.0


def theta_for_cam_z(z):
    mid=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
    s=(z-CAM_AXIS_OFFSET_Z-mid)/LINK_L
    return math.asin(s)


def qpoints(z):
    th=theta_for_cam_z(z)
    dx=-LINK_L*math.cos(th)
    dz=LINK_L*math.sin(th)
    q1=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz)
    q2=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
    camx=(q1[0]+q2[0])/2.0
    return th,q1,q2,camx


def link_plate(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    ang=math.degrees(math.atan2(dz,dx))
    length=math.hypot(dx,dz)
    plate=(cq.Workplane('XZ').workplane(offset=y-ARM_T/2)
           .slot2D(length,ARM_H,0).extrude(ARM_T))
    plate=plate.rotate((0,0,0),(0,1,0),-ang)
    plate=plate.translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))
    return plate


def gas_metrics(z):
    th,q1,q2,camx=qpoints(z)
    ux=-math.cos(th); uz=math.sin(th)
    ax=BODY_PIVOT_X+ux*GAS_ATTACH_FROM_LOWER_PIVOT
    az=PIVOT_Z_LOW+uz*GAS_ATTACH_FROM_LOWER_PIVOT
    bx,bz=GAS_BASE
    length=math.hypot(ax-bx,az-bz)
    fx=GAS_FORCE*(bx-ax)/length
    fz=GAS_FORCE*(bz-az)/length
    rx=ax-BODY_PIVOT_X; rz=az-PIVOT_Z_LOW
    torque=(rx*fz-rz*fx)/1000.0
    return dict(length_mm=length,assist_torque_Nm=torque,attach=(ax,az))

th,q1,q2,camx=qpoints(CAM_ZS['LOW'])
assy=cq.Assembly(name='PX1_LiftCamera_RevFN')

for side_y in (-ARM_Y,ARM_Y):
    a1=link_plate((BODY_PIVOT_X,PIVOT_Z_LOW),q1,side_y)
    a2=link_plate((BODY_PIVOT_X,PIVOT_Z_HIGH),q2,side_y)
    assy.add(a1,name=f'LowerArm_{"R" if side_y<0 else "L"}')
    assy.add(a2,name=f'UpperArm_{"R" if side_y<0 else "L"}')

for s in (-1,1):
    y=s*(YOKE_HALF_W-YOKE_T/2)
    cheek=(cq.Workplane('XZ').workplane(offset=y-YOKE_T/2)
           .box(YOKE_X,YOKE_H,YOKE_T,centered=(True,True,False)))
    cheek=cheek.faces('>Y' if s>0 else '<Y').workplane().hole(PIVOT_D)
    cheek=cheek.translate((camx,0,CAM_ZS['LOW']))
    assy.add(cheek,name=f'YokeCheek_{"L" if s>0 else "R"}')

bridge=(cq.Workplane('XY').box(12.0,2*YOKE_HALF_W,5.0,centered=(True,True,True))
        .translate((camx+CAM_LEN/2+4.0,0,CAM_ZS['LOW'])))
assy.add(bridge,name='YokeBridge')

shell_outer=(cq.Workplane('YZ').circle(CAM_OD/2).extrude(CAM_LEN/2,both=True)
             .translate((camx,0,CAM_ZS['LOW'])))
shell_inner=(cq.Workplane('YZ').circle((CAM_OD-5.0)/2).extrude((CAM_LEN-10.0)/2,both=True)
             .translate((camx,0,CAM_ZS['LOW'])))
shell=shell_outer.cut(shell_inner)
assy.add(shell,name='DigitalCameraOuterShell')

frontx=camx-CAM_LEN/2
ret=(cq.Workplane('YZ').circle(CAM_OD/2).circle(15.0).extrude(5.0)
     .translate((frontx-5.0,0,CAM_ZS['LOW'])))
assy.add(ret,name='FrontWindowRetainer')

m=gas_metrics(CAM_ZS['LOW']); ax,az=m['attach']; bx,bz=GAS_BASE
dx=ax-bx; dz=az-bz; gl=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
gas=(cq.Workplane('YZ').circle(7.5).extrude(gl)
     .rotate((0,0,0),(0,1,0),-ang)
     .translate((bx,0,bz)))
assy.add(gas,name='GasSpring150N_Envelope')

out=os.path.abspath('build_revfn')
os.makedirs(out,exist_ok=True)
assy.save(os.path.join(out,'PX1_LiftCamera_RevFN.step'))

metrics={'positions':{},'pipe':{'R':PIPE_R,'axis_Z':PIPE_Z}}
for name,z in CAM_ZS.items():
    th,q1,q2,cx=qpoints(z)
    gm=gas_metrics(z)
    metrics['positions'][name]={
        'camera_axis_Z_mm':z,
        'arm_angle_deg':math.degrees(th),
        'camera_axis_X_mm':cx,
        'lower_camera_pivot_XZ':q1,
        'upper_camera_pivot_XZ':q2,
        'gas_spring_length_mm':gm['length_mm'],
        'gas_assist_torque_Nm':gm['assist_torque_Nm']
    }

mins=[]
for d in [x/2 for x in range(-210,211)]:
    a=math.radians(d)
    maxrad=0.0
    for t_i in range(73):
        t=-CAM_LEN/2+CAM_LEN*t_i/72
        for p_i in range(91):
            p=2*math.pi*p_i/90
            y=(CAM_OD/2)*math.sin(p)
            z=CAM_ZS['LOW'] + t*math.sin(a) + (CAM_OD/2)*math.cos(p)*math.cos(a)
            rr=math.hypot(y,z-PIPE_Z)
            maxrad=max(maxrad,rr)
    mins.append((PIPE_R-maxrad,d))
metrics['dn150_low_camera_full_tilt_min_clearance_mm']=min(mins)[0]
metrics['dn150_low_camera_worst_tilt_deg']=min(mins)[1]
metrics['dn150_upper_pivot_nominal_clearance_mm']=PIPE_R-math.hypot(31.0,PIVOT_Z_HIGH-PIPE_Z)
metrics['gas_stroke_required_mm']=max(v['gas_spring_length_mm'] for v in metrics['positions'].values())-min(v['gas_spring_length_mm'] for v in metrics['positions'].values())
metrics['status']='prototype geometry; actual gas spring, fastener heads and physical DN150 tube gate remain'
with open(os.path.join(out,'REV_FN_VALIDATION.json'),'w') as f:
    json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))