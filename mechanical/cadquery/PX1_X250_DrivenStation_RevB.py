import cadquery as cq, math, json, os

OUT=os.path.abspath('build_revb_x250')
os.makedirs(OUT, exist_ok=True)

# PX-1 Rev.B Work Block 01
# Coordinate system follows active Rev.PR style:
# X longitudinal, Y transverse, Z vertical.
# This file models the LEFT/+Y X250 station only.
# NOT a manufacturing release.
X=250.0
Z=45.0
PIPE_R=75.0
PIPE_Z=52.0480547

# Active body/side-bay references
P0_WALL_Y=34.0
COVER_INNER_Y=46.0
COVER_OUTER_Y=51.0
SIDE_BAY_DEPTH=COVER_INNER_Y-P0_WALL_Y

# P0 output shaft / seal path
P0_SEAL_Y0=27.0
P0_SEAL_Y1=34.0
P0_SEAL_SHAFT_D=18.0
OUTPUT_STUB_D=10.0
OUTPUT_STUB_Y0=34.0
OUTPUT_STUB_Y1=41.2

# Overlapped coupling hub + bearing
HUB_Y0=34.0
HUB_Y1=41.5
HUB_OD=20.0
HUB_BORE=10.10  # diametral packaging-clearance screen only
B6704_D=20.0
B6704_OD=27.0
B6704_B=4.0
B6704_Y0=37.5
B6704_Y1=41.5

# Z50 gear envelope
GEAR_M=1.0
GEAR_Z=50
GEAR_OD=GEAR_M*(GEAR_Z+2)
GEAR_FACE=4.0
GEAR_Y0=41.65
GEAR_Y1=45.65
GEAR_BORE=12.0

# Cover / outboard support
B61801=(12.0,21.0,5.0)
B61801_Y0=46.15
B61801_Y1=51.15
B61903=(17.0,30.0,7.0)
B61903_Y0=51.35
B61903_Y1=58.35
XRING_Y0=58.55
XRING_Y1=61.95
XRING_GLAND_OD=23.61
WHEEL_SEAT_Y0=62.15
WHEEL_SEAT_Y1=69.15

# Rev.GF tapered/dished wheel envelope points, global Y and radial envelope.
WHEEL_PROFILE=[
    (51.25,45.00),
    (53.00,45.00),
    (55.00,43.80),
    (58.00,40.38),
    (61.00,36.45),
    (64.00,31.90),
    (67.00,26.50),
    (70.00,18.00),
    (71.00,15.50),
]


def cyl_y(r, y0, y1):
    return cq.Workplane('XY').newObject([
        cq.Solid.makeCylinder(r, y1-y0, cq.Vector(X,y0,Z), cq.Vector(0,1,0))
    ])


def ann_y(ro, ri, y0, y1):
    return cyl_y(ro,y0,y1).cut(cyl_y(ri,y0-0.01,y1+0.01))


def vol_inter(a,b):
    return a.val().intersect(b.val()).Volume()


def vol_outside(a,b):
    return a.val().cut(b.val()).Volume()


# P0 shaft: inner Ø10 + Ø18 seal land + Ø10 male stub.
shaft_inner=cyl_y(5.0,18.0,P0_SEAL_Y0)
shaft_seal=cyl_y(P0_SEAL_SHAFT_D/2,P0_SEAL_Y0,P0_SEAL_Y1)
shaft_stub=cyl_y(OUTPUT_STUB_D/2,OUTPUT_STUB_Y0,OUTPUT_STUB_Y1)
output_shaft=shaft_inner.union(shaft_seal).union(shaft_stub)

# Female coupling hub integrated with long axle.
hub=ann_y(HUB_OD/2,HUB_BORE/2,HUB_Y0,HUB_Y1)

# Rear long axle stepped outer shaft.
shaft_12=cyl_y(6.0,HUB_Y1,51.2)
shaft_17=cyl_y(8.5,51.2,58.45)
shaft_19=cyl_y(9.5,58.45,62.05)
shaft_wheel=cyl_y(8.5,62.05,WHEEL_SEAT_Y1)
long_axle=hub.union(shaft_12).union(shaft_17).union(shaft_19).union(shaft_wheel)

# Bearing envelopes.
b6704=ann_y(B6704_OD/2,B6704_D/2,B6704_Y0,B6704_Y1)
b61801=ann_y(B61801[1]/2,B61801[0]/2,B61801_Y0,B61801_Y1)
b61903=ann_y(B61903[1]/2,B61903[0]/2,B61903_Y0,B61903_Y1)

# Gear envelope ring.
gear=ann_y(GEAR_OD/2,GEAR_BORE/2,GEAR_Y0,GEAR_Y1)

# Side-cover local station patch only, not the full plate.
cover=ann_y(25.0,17.0,COVER_INNER_Y,COVER_OUTER_Y)

# Provisional Rev.B axle-flange envelope.
flange_outer=cyl_y(25.0,COVER_INNER_Y,62.2)
flange=flange_outer
flange=flange.cut(cyl_y(10.7,COVER_INNER_Y,51.25))
flange=flange.cut(cyl_y(15.2,51.25,58.50))
flange=flange.cut(cyl_y(XRING_GLAND_OD/2,58.50,62.20))

# X-ring gland clearance envelope, not elastomer solid.
xring_env=ann_y(XRING_GLAND_OD/2,19.0/2,XRING_Y0,XRING_Y1)

# Rev.GF wheel outer envelope as cylinders/frustums.
wheel=None
for (y0,r0),(y1,r1) in zip(WHEEL_PROFILE,WHEEL_PROFILE[1:]):
    if abs(r1-r0) < 1e-9:
        seg=cyl_y(r0,y0,y1)
    else:
        seg=cq.Workplane('XY').newObject([
            cq.Solid.makeCone(r0,r1,y1-y0,cq.Vector(X,y0,Z),cq.Vector(0,1,0))
        ])
    wheel=seg if wheel is None else wheel.union(seg)
wheel=wheel.union(cyl_y(WHEEL_PROFILE[0][1],WHEEL_PROFILE[0][0],WHEEL_PROFILE[0][0]+0.05))
wheel=wheel.union(cyl_y(WHEEL_PROFILE[-1][1],WHEEL_PROFILE[-1][0]-0.05,WHEEL_PROFILE[-1][0]))
wheel=wheel.cut(cyl_y(12.0,51.0,71.2))

# Ideal DN150 pipe envelope along X.
pipe=cq.Workplane('XY').newObject([
    cq.Solid.makeCylinder(PIPE_R,120.0,cq.Vector(X-60,0,PIPE_Z),cq.Vector(1,0,0))
])

checks={}
checks['side_bay_depth_mm']=SIDE_BAY_DEPTH
checks['coupling_stub_radial_clearance_mm']=(HUB_BORE-OUTPUT_STUB_D)/2
checks['bearing_to_gear_axial_clearance_mm']=GEAR_Y0-B6704_Y1
checks['gear_to_cover_axial_clearance_mm']=COVER_INNER_Y-GEAR_Y1
checks['hub_length_mm']=HUB_Y1-HUB_Y0
checks['stub_engagement_mm']=OUTPUT_STUB_Y1-OUTPUT_STUB_Y0
checks['stub_end_clearance_mm']=HUB_Y1-OUTPUT_STUB_Y1

# Collision checks.
checks['stub_hub_material_intersection_mm3']=round(vol_inter(shaft_stub,hub),6)
checks['hub_b6704_intersection_mm3']=round(vol_inter(hub,b6704),6)
checks['long_axle_gear_intersection_mm3']=round(vol_inter(long_axle,gear),6)
checks['gear_cover_intersection_mm3']=round(vol_inter(gear,cover),6)
checks['b61801_cover_material_intersection_mm3']=round(vol_inter(b61801,cover),6)
checks['b61903_flange_material_intersection_mm3']=round(vol_inter(b61903,flange),6)
checks['xring_flange_material_intersection_mm3']=round(vol_inter(xring_env,flange),6)

# Pipe containment screens.
for name,part in [('gear',gear),('cover',cover),('flange',flange),('wheel',wheel),('long_axle',long_axle),('b6704',b6704)]:
    checks[f'{name}_outside_DN150_mm3']=round(vol_outside(part,pipe),6)

# Analytical wheel-profile margin at lower pipe side.
profile_margins=[]
for y,r in WHEEL_PROFILE:
    allow=math.sqrt(max(0.0,PIPE_R**2-y**2))-(PIPE_Z-Z)
    profile_margins.append((y,r,allow,allow-r))
checks['wheel_profile_min_margin_mm']=min(p[3] for p in profile_margins)
checks['wheel_profile_margins_mm']=[
    {'y':p[0],'r':p[1],'allow':p[2],'margin':p[3]} for p in profile_margins
]

# Torque screen.
T=4.0
Tmm=T*1000.0
checks['key_3x3x7_shear_MPa']=2*Tmm/(10.0*3.0*7.0)
checks['key_3x3x7_bearing_MPa']=4*Tmm/(10.0*3.0*7.0)
checks['shaft_d12_torsion_MPa']=16*Tmm/(math.pi*12.0**3)
Ft=Tmm/25.0
Fr=Ft*math.tan(math.radians(20.0))
checks['z50_mesh_Ft_N']=Ft
checks['z50_mesh_Fr_N']=Fr
checks['z50_mesh_resultant_N']=math.hypot(Ft,Fr)

pack_pass=(
    checks['coupling_stub_radial_clearance_mm']>0 and
    checks['bearing_to_gear_axial_clearance_mm']>=0.10 and
    checks['gear_to_cover_axial_clearance_mm']>=0.30 and
    checks['stub_hub_material_intersection_mm3']<1e-5 and
    checks['gear_cover_intersection_mm3']<1e-5
)
checks['packaging_status']='PASS_SCREEN' if pack_pass else 'HOLD'
checks['release_status']='HOLD'
checks['release_holds']=[
    'exact 6704 purchased brand, tolerance and fit',
    'real keyed blind-bore coupling geometry and retention',
    'real Z50 gear hub/key/retention geometry',
    'production axle-flange bearing pockets and X-ring gland',
    'full assembly path and tool access',
    'complete DN150 crawler sweep with body, lift, camera and hardware',
    'first-article torque / leak-decay / submerged rotation test',
]

assy=cq.Assembly(name='PX1_X250_DrivenStation_RevB')
for name,part in [
    ('P0_OutputShaft',output_shaft),('LongAxle',long_axle),('Bearing6704',b6704),
    ('GearZ50_B4',gear),('SideCoverPatch',cover),('Bearing61801',b61801),
    ('Bearing61903',b61903),('AxleFlangeEnvelope',flange),('XRingGlandEnvelope',xring_env),
    ('Wheel_RevGF_Envelope',wheel),('DN150_Pipe',pipe)
]:
    assy.add(part,name=name)
assy.save(os.path.join(OUT,'PX1_X250_DrivenStation_RevB.step'))
with open(os.path.join(OUT,'REV_B_X250_CAD_VALIDATION.json'),'w') as f:
    json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
