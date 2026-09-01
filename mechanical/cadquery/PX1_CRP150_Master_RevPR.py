import cadquery as cq
import math, json, os

# PX-1 Rev.PR — corrected CRP150-style master crawler skeleton
# Key correction: the rear wheel station X250 is the driven long-axle input.
# Rev.GL/GX X200 input geometry is superseded where it conflicts with the
# verified Proteus source architecture.
# Prototype engineering only; NOT machining release.

OUT=os.path.abspath('build_revpr'); os.makedirs(OUT,exist_ok=True)

# ----- global envelope / reference coordinates -----
PIPE_R=75.0
PIPE_Z=52.0480547
BODY_L=307.0
BODY_W=92.0
HALF_OUT=BODY_W/2
HALF_IN=34.0
Z0=8.0
ZTOP=90.0
FLOOR=6.0
WHEEL_Z=45.0
SIDE_COVER_Y=51.0

# Verified Proteus side-drive skeleton
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_X=(50.0,150.0,250.0)
DRIVE_X=250.0
SPUR_MODULE=1.0
SPUR_Z=50
SPUR_PD=SPUR_MODULE*SPUR_Z
SPUR_OD=SPUR_MODULE*(SPUR_Z+2)
SPUR_FACE=3.75
GEAR_Y=42.0

# Wheel is envelope only here; exact Rev.GF DN150 tread profile remains separate.
WHEEL_OD=90.0
WHEEL_WIDTH=16.0
WHEEL_CENTER_Y=59.0

# Rear motor / bevel envelope. Ratio is frozen, tooth geometry is not machining-released.
MOTOR_OD_MAX=35.0
MOTOR_LEN_MAX=100.0
MOTOR_Y=18.0
MOTOR_Z=45.0
MOTOR_CENTER_X=DRIVE_X + MOTOR_LEN_MAX/2.0
REAR_END=MOTOR_CENTER_X + MOTOR_LEN_MAX/2.0 + 8.0
BEVEL_RATIO=2.5
BEVEL_Z_SMALL=16
BEVEL_Z_LARGE=40
BEVEL_MODULE_SCREEN=1.25   # packaging screen only, NOT released gear geometry
BEVEL_LARGE_OD=BEVEL_MODULE_SCREEN*(BEVEL_Z_LARGE+2)
BEVEL_SMALL_OD=BEVEL_MODULE_SCREEN*(BEVEL_Z_SMALL+2)

# Lift / wet deck retained from Rev.GX, but drive handoff moved to X250.
DECK_HALF_W=38.0
ROOF_T=5.0
ROOF_PTS=[(0.0,38.0),(120.0,42.0),(200.0,77.0),(220.0,90.0)]
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=112.0
LIFT_AXLE_OD=12.0

# Generic electronics reserves; exact modules remain procurement gates.
PACK={
    'HV_TO_24V_CONVERTER_RESERVE': (62.0, 0.0, 24.0, 80.0, 58.0, 18.0),
    'DATA_VIDEO_INTERFACE_RESERVE': (130.0, 0.0, 25.0, 48.0, 20.0, 14.0),
    'TRACTION_DRIVER_L_RESERVE': (176.0, 16.0, 30.0, 34.0, 22.0, 14.0),
    'TRACTION_DRIVER_R_RESERVE': (176.0,-16.0, 30.0, 34.0, 22.0, 14.0),
    'INPUT_PROTECTION_RESERVE': (220.0, 0.0, 56.0, 24.0, 48.0, 18.0),
    'NUCLEO_F446RE_LOWPROFILE': (262.25, 0.0, 98.0, 82.5, 70.0, 12.0),
}

# ----- helpers -----
def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_y(x,y0,z,r,l,sgn=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cyl_x_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def outside(a,c): return a.val().cut(c.val()).Volume()
def prism_x(x0,pts_yz,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts_yz).close().extrude(length)
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]

# ----- pressure body / wet deck -----
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,Z0+FLOOR),(299.0,Z0+FLOOR),(299.0,85.0),(220.0,85.0),
            (200.0,72.0),(120.0,37.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN)
body=cut(body,inner)
# Open wet deck above the pressure roof.
deck_poly=ROOF_PTS+[(220.0,105.0),(0.0,105.0)]
deck_cut=cq.Workplane('XZ',origin=(0,DECK_HALF_W,0)).polyline(deck_poly).close().extrude(2*DECK_HALF_W)
body=cut(body,deck_cut)
# Dry side bays under removable covers.
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0))
body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))

# Correct driven long-axle openings at X250, not X200.
for sgn in (1,-1):
    body=cut(body,cyl_y(DRIVE_X,sgn*HALF_IN,WHEEL_Z,19.0,HALF_OUT-HALF_IN,sgn))
    for a in range(0,360,90):
        rr=23.0
        xx=DRIVE_X+rr*math.cos(math.radians(a))
        zz=WHEEL_Z+rr*math.sin(math.radians(a))
        body=cut(body,cyl_y(xx,sgn*HALF_IN,zz,2.1,HALF_OUT-HALF_IN,sgn))

# Rear motor pressure extension sized around two <=Ø35 x 100 mm gearmotors.
rear_x0=242.0
rear_outer=box0(rear_x0,-40,22,REAR_END-rear_x0,80,46)
body=fuse(body,rear_outer)
rear_cav=box0(246.0,-36,26,REAR_END-252.0,72,38)
body=cut(body,rear_cav)

# Streamlined controller saddle retained.
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]
pod_outer=prism_x(218,pod_outer_pts,min(89.0,BODY_L-218.0)); body=fuse(body,pod_outer)
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]
pod_cav=prism_x(221,pod_inner_pts,min(83.0,BODY_L-224.0)); body=cut(body,pod_cav)
throat=box0(224,-33,84,min(76.0,BODY_L-224.0),66,10); body=cut(body,throat)

# Integrated lift-pivot requirement retained as geometry references.
# Do not create a full-width pressure-body tube: the Proteus source uses local holding plates/bosses.
lift_pivots=[]
for zz in (PIVOT_Z_LOW,PIVOT_Z_HIGH):
    for side in (-1,1):
        yy=side*27.0
        lift_pivots.append((side,zz,cyl_y_center(BODY_PIVOT_X,yy,zz,LIFT_AXLE_OD/2,8.0)))

# Twin sealed wet scuppers retained from Rev.GX.
SCUPPER_X=120.0
for yy in (-26.0,26.0):
    outer=cyl_z(SCUPPER_X,yy,Z0,5.0,roof_top(SCUPPER_X)-Z0)
    body=fuse(body,outer)
    body=cut(body,cyl_z(SCUPPER_X,yy,Z0-1,3.0,roof_top(SCUPPER_X)-Z0+2))

# ----- drivetrain envelope assembly -----
spur_gears=[]
for side in (-1,1):
    gy=side*GEAR_Y
    for x in GEAR_X:
        spur_gears.append((side,x,cyl_y_center(x,gy,WHEEL_Z,SPUR_OD/2,SPUR_FACE)))

wheels=[]
for side in (-1,1):
    wy=side*WHEEL_CENTER_Y
    for x in WHEEL_X:
        wheels.append((side,x,cyl_y_center(x,wy,WHEEL_Z,WHEEL_OD/2,WHEEL_WIDTH)))

# Rear long axles and bevel gear screening envelopes.
axles=[]; bevels=[]; motors=[]
for side in (-1,1):
    sy=side*18.0
    axles.append((side,cyl_y_center(DRIVE_X,side*26.0,WHEEL_Z,6.0,42.0)))
    bevels.append((side,'Z40',cyl_y_center(DRIVE_X,sy,WHEEL_Z,BEVEL_LARGE_OD/2,12.0)))
    bevels.append((side,'Z16',cyl_x_center(DRIVE_X+2.0,sy,WHEEL_Z,BEVEL_SMALL_OD/2,14.0)))
    motors.append((side,cyl_x_center(MOTOR_CENTER_X,sy,MOTOR_Z,MOTOR_OD_MAX/2,MOTOR_LEN_MAX)))

# ----- electronics packaging envelopes -----
parts={name:boxc(*dims) for name,dims in PACK.items()}
parts['PRESSURE_SENSOR_RESERVE']=cyl_z(244.0,22.0,55.0,11.0,22.0)

# Dry cavity union for packaging screen.
cavity=wp(inner.val().fuse(rear_cav.val()).fuse(pod_cav.val()).fuse(throat.val()))

# ----- validation -----
pipe=wp(cq.Solid.makeCylinder(PIPE_R,REAR_END+20,cq.Vector(-10,0,PIPE_Z),cq.Vector(1,0,0)))
checks={
    'body_valid':body.val().isValid(),
    'body_outside_ideal_DN150_mm3':round(body.val().cut(pipe.val()).Volume(),6),
    'rear_input_station_x_mm':DRIVE_X,
    'wheel_stations_x_mm':list(WHEEL_X),
    'five_spur_positions_x_mm':list(GEAR_X),
    'spur_pitch_center_spacing_mm':[GEAR_X[i+1]-GEAR_X[i] for i in range(4)],
    'spur_module':SPUR_MODULE,
    'spur_teeth_each':SPUR_Z,
    'bevel_ratio':BEVEL_RATIO,
    'bevel_tooth_counts':[BEVEL_Z_SMALL,BEVEL_Z_LARGE],
    'bevel_module_status':'SCREENING_ONLY_NOT_RELEASED',
    'motor_envelope_max_mm':{'diameter':MOTOR_OD_MAX,'length':MOTOR_LEN_MAX},
    'component_outside_dry_volume_mm3':{},
    'component_intersections_mm3':{},
    'motor_body_intersections_mm3':{},
    'gear_train_center_spacing_error_mm':max(abs((GEAR_X[i+1]-GEAR_X[i])-SPUR_PD) for i in range(4)),
    'release_holds':[
        'exact traction motor article and shaft/mount drawing',
        'released Z16/Z40 bevel module/pressure angle/face width',
        'actual HV-to-24V converter article and thermal mounting',
        'exact side-cover/shaft-flange detail at X250 driven station',
        'full Rev.GF wheel profile integration and physical DN150 sweep',
        'full lift LOW/MID/HIGH sweep after X250 drive relocation',
        'pressure FEA/proof including rear extension and lift bosses',
    ]
}

for n,p in parts.items():
    checks['component_outside_dry_volume_mm3'][n]=round(outside(p,cavity),6)
keys=list(parts)
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        iv=inter(parts[a],parts[b])
        if iv>1e-5:
            checks['component_intersections_mm3'][a+'__'+b]=round(iv,6)
for side,m in motors:
    checks['motor_body_intersections_mm3'][str(side)]=round(inter(m,body),6)

# Body must remain in ideal DN150; wheel placeholders are simple cylinders and therefore
# are not used as a replacement for the verified tapered Rev.GF wheel profile sweep.
checks['status']='PASS' if (
    checks['body_valid'] and
    checks['body_outside_ideal_DN150_mm3'] < 1e-5 and
    checks['gear_train_center_spacing_error_mm'] < 1e-9 and
    all(v < 1e-5 for v in checks['component_outside_dry_volume_mm3'].values()) and
    not checks['component_intersections_mm3'] and
    all(v < 1e-5 for v in checks['motor_body_intersections_mm3'].values())
) else 'FAIL'

# ----- exports -----
cq.exporters.export(body,os.path.join(OUT,'PX1_CRP150_PressureBody_RevPR.step'))
assy=cq.Assembly(name='PX1_CRP150_Master_RevPR')
assy.add(body,name='PressureBody')
for side,x,g in spur_gears: assy.add(g,name=f'SpurZ50_S{side:+d}_X{int(x)}')
for side,x,w in wheels: assy.add(w,name=f'WheelEnvelope_S{side:+d}_X{int(x)}')
for side,a in axles: assy.add(a,name=f'RearLongAxle_S{side:+d}')
for side,n,b in bevels: assy.add(b,name=f'Bevel{n}_S{side:+d}')
for side,m in motors: assy.add(m,name=f'MotorEnvelope_S{side:+d}')
for side,zz,p in lift_pivots: assy.add(p,name=f'LiftPivotRef_S{side:+d}_Z{int(zz)}')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_CRP150_Master_RevPR.step'))
with open(os.path.join(OUT,'REV_PR_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS': raise SystemExit(2)
