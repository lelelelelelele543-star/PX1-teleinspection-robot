import cadquery as cq
import math, json, os

# PX-1 Rev.GX — integrated sealed wet-deck, twin scuppers and streamlined electronics saddle
# Prototype engineering only; NOT machining release.

OUT=os.path.abspath('build_revgx'); os.makedirs(OUT,exist_ok=True)
L=307.0; W=92.0; Z0=8.0; ZTOP=90.0; PIPE_R=75.0; PIPE_Z=52.0480547
HALF_OUT=46.0; HALF_IN=34.0; FLOOR=6.0; WHEEL_Z=45.0
BAY_X0=10.5; BAY_L=286.0; BAY_Z0=6.0; BAY_H=80.0; BAY_DEPTH=8.0; BAY_INNER_Y=38.0
DECK_HALF_W=38.0; ROOF_T=5.0
ROOF_PTS=[(0.0,38.0),(120.0,42.0),(200.0,77.0),(220.0,90.0)]
CAM_OD=52.0; CAM_LEN=72.0; CAM_Z=75.0
BODY_PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=112.0; LINK_L=120.0
ARM_Y=26.0; ARM_T=5.0; ARM_H=18.0


def wp(s): return cq.Workplane('XY').newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l,sgn=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cyl_z(x,y,z0,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def outside(a,c): return a.val().cut(c.val()).Volume()
def prism_x(x0,pts_yz,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts_yz).close().extrude(length)
def bcenter(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cylx_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]

# ---- pressure body ----
body=box(0,-HALF_OUT,Z0,L,W,ZTOP-Z0)
inner_pts=[(8.0,Z0+FLOOR),(299.0,Z0+FLOOR),(299.0,85.0),(220.0,85.0),
           (200.0,72.0),(120.0,37.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
deck_poly=ROOF_PTS+[(220.0,105.0),(0.0,105.0)]
deck_cut=cq.Workplane('XZ',origin=(0,DECK_HALF_W,0)).polyline(deck_poly).close().extrude(2*DECK_HALF_W)
body=cut(body,deck_cut)
left_pocket=box(BAY_X0,BAY_INNER_Y,BAY_Z0,BAY_L,BAY_DEPTH,BAY_H)
right_pocket=box(BAY_X0,-HALF_OUT,BAY_Z0,BAY_L,BAY_DEPTH,BAY_H)
body=cut(cut(body,left_pocket),right_pocket)
for sgn in (1,-1):
    body=cut(body,cyl_y(200,sgn*HALF_IN,WHEEL_Z,19.0,HALF_OUT-HALF_IN,sgn))
    for a in range(0,360,90):
        rr=23.0; xx=200+rr*math.cos(math.radians(a)); zz=WHEEL_Z+rr*math.sin(math.radians(a))
        body=cut(body,cyl_y(xx,sgn*HALF_IN,zz,2.1,HALF_OUT-HALF_IN,sgn))

# Rear motor pressure extension.
rear_outer=box(299,-40,23,41,80,44); body=fuse(body,rear_outer)
rear_cav=box(299,-34,27,33,68,36); body=cut(body,rear_cav)

# Streamlined top electronics saddle: full width at board height, tapering inward near DN150 roof.
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]
pod_outer=prism_x(218,pod_outer_pts,89); body=fuse(body,pod_outer)
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]
pod_cav=prism_x(221,pod_inner_pts,83); body=cut(body,pod_cav)
throat=box(224,-33,84,76,66,10); body=cut(body,throat)

# Twin sealed wet scuppers at the front-slope/ramp local-low transition.
# Fuse pressure-boundary tube first, then cut only the wet bore.
SCUPPER_X=120.0; SCUPPER_YS=(-26.0,26.0); SCUPPER_OD=10.0; SCUPPER_ID=6.0
scupper_solids=[]
for yy in SCUPPER_YS:
    outer=cyl_z(SCUPPER_X,yy,Z0,SCUPPER_OD/2,roof_top(SCUPPER_X)-Z0)
    body=fuse(body,outer); scupper_solids.append(outer)
    bore=cyl_z(SCUPPER_X,yy,Z0-1,SCUPPER_ID/2,roof_top(SCUPPER_X)-Z0+2)
    body=cut(body,bore)

cavity=wp(inner.val().fuse(rear_cav.val()).fuse(pod_cav.val()).fuse(throat.val()))

# ---- LOW camera/lift collision geometry ----
def theta_for_cam_z(z):
    mid=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0
    return math.asin((z-2.0-mid)/LINK_L)
def qpoints(z):
    th=theta_for_cam_z(z); dx=-LINK_L*math.cos(th); dz=LINK_L*math.sin(th)
    q1=(BODY_PIVOT_X+dx,PIVOT_Z_LOW+dz); q2=(BODY_PIVOT_X+dx,PIVOT_Z_HIGH+dz)
    return th,q1,q2,(q1[0]+q2[0])/2.0
def link_plate(p1,p2,y):
    dx=p2[0]-p1[0]; dz=p2[1]-p1[1]
    ang=math.degrees(math.atan2(dz,dx)); length=math.hypot(dx,dz)
    s=cq.Workplane('XZ').workplane(offset=y-ARM_T/2).slot2D(length,ARM_H,0).extrude(ARM_T)
    s=s.rotate((0,0,0),(0,1,0),-ang)
    return s.translate(((p1[0]+p2[0])/2,0,(p1[1]+p2[1])/2))
th,q1,q2,camx=qpoints(CAM_Z)
camera=cq.Workplane('YZ').circle(CAM_OD/2).extrude(CAM_LEN/2,both=True).translate((camx,0,CAM_Z))
arms=[]
for y in (-ARM_Y,ARM_Y):
    arms += [link_plate((BODY_PIVOT_X,PIVOT_Z_LOW),q1,y),link_plate((BODY_PIVOT_X,PIVOT_Z_HIGH),q2,y)]

# ---- revised packaging after scupper insertion ----
parts={
 'DC48_24_halfbrick':bcenter(55,0,24,70,65,18),
 'AVD_video_TX':bcenter(122.5,0,25,55,20,12),
 'TB6612_camera_axes':bcenter(175,0,28,50,25,19),
 'INPUT_PROTECTION_reserve':bcenter(190,0,50,22,60,22),
 'DUAL_MC33926_candidate':bcenter(219,-10,50,28,46,12),
 'NUCLEO_F446RE_lowprofile':bcenter(262.25,0,98,82.5,70,12),
 'MOTOR_L_32x92':cylx_center(283,16.5,45,16,92),
 'MOTOR_R_32x92':cylx_center(283,-16.5,45,16,92),
 'PRESSURE_SENSOR_24p4x25':cyl_z(237,20.5,61.5,12.2,25),
}

# ---- validation ----
pipe=wp(cq.Solid.makeCylinder(PIPE_R,380,cq.Vector(-10,0,PIPE_Z),cq.Vector(1,0,0)))
checks={
 'body_valid':body.val().isValid(),
 'body_outside_ideal_DN150_mm3':round(body.val().cut(pipe.val()).Volume(),6),
 'camera_body_intersection_mm3':round(inter(camera,body),6),
 'arm_body_intersection_mm3':[round(inter(a,body),6) for a in arms],
 'component_outside_dry_volume_mm3':{k:round(outside(v,cavity),6) for k,v in parts.items()},
 'component_intersections_mm3':{},
 'scupper_component_intersections_mm3':{},
}
keys=list(parts)
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        iv=inter(parts[a],parts[b])
        if iv>1e-5: checks['component_intersections_mm3'][a+'__'+b]=round(iv,6)
for n,p in parts.items():
    for si,s in enumerate(scupper_solids):
        iv=inter(p,s)
        if iv>1e-5: checks['scupper_component_intersections_mm3'][n+'__SCUPPER'+str(si+1)]=round(iv,6)

lens_x=camx-CAM_LEN/2
checks['wet_deck_roof_profile_xz_mm']=ROOF_PTS
checks['camera_side_clearance_each_mm']=round(DECK_HALF_W-CAM_OD/2,3)
checks['camera_under_gap_front_center_rear_mm']=[round(CAM_Z-CAM_OD/2-roof_top(x),3) for x in (lens_x,camx,camx+CAM_LEN/2)]
checks['forward_opening_horizontal_cone_deg_screen']=round(2*math.degrees(math.atan2(DECK_HALF_W,lens_x)),3)
mingap=1e9
for i in range(201):
    xx=q1[0]+(BODY_PIVOT_X-q1[0])*i/200
    zc=q1[1]+(PIVOT_Z_LOW-q1[1])*(xx-q1[0])/(BODY_PIVOT_X-q1[0])
    mingap=min(mingap,(zc-ARM_H/2)-roof_top(xx))
checks['minimum_lower_arm_to_roof_gap_mm']=round(mingap,3)
checks['scuppers']={'x_mm':SCUPPER_X,'y_mm':list(SCUPPER_YS),'OD_mm':SCUPPER_OD,'ID_mm':SCUPPER_ID,'radial_wall_mm':(SCUPPER_OD-SCUPPER_ID)/2}
checks['front_deck_body_slope_deg']=round(math.degrees(math.atan2(42-38,120)),3)
checks['rear_ramp_body_slope_deg']=round(math.degrees(math.atan2(77-42,200-120)),3)
checks['streamlined_saddle_DN150_margin_mm']={'side_transition_y39_z104':round(PIPE_R-math.hypot(39,104-PIPE_Z),3),'top_y34_z110':round(PIPE_R-math.hypot(34,110-PIPE_Z),3)}
checks['status']='PASS' if (checks['body_valid'] and checks['body_outside_ideal_DN150_mm3']<1e-5 and checks['camera_body_intersection_mm3']<1e-5 and all(v<1e-5 for v in checks['arm_body_intersection_mm3']) and all(v<1e-5 for v in checks['component_outside_dry_volume_mm3'].values()) and not checks['component_intersections_mm3'] and not checks['scupper_component_intersections_mm3']) else 'FAIL'
checks['release_holds']=['manufacturing fillets/radii','full LOW/MID/HIGH dynamic lift sweep','scupper pressure FEA/proof','water/sludge incline test','actual NUCLEO installed height','exact compact traction driver article/thermal test','actual camera lens FOV']

cq.exporters.export(body,os.path.join(OUT,'PX1_PressureBody_WetDeck_RevGX.step'))
assy=cq.Assembly(name='PX1_RevGX_Packaging')
assy.add(body,name='PressureBody_WetDeck_Scuppers')
assy.add(camera,name='Camera_LOW')
for i,a in enumerate(arms): assy.add(a,name=f'LiftArm_{i+1}')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_RevGX_Packaging.step'))
with open(os.path.join(OUT,'REV_GX_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS': raise SystemExit(2)
