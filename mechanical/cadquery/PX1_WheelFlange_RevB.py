import cadquery as cq, math, json, os

OUT=os.path.abspath('build_revb_wb02')
os.makedirs(OUT, exist_ok=True)

# PX-1 Rev.B WB02 - wheel / axle flange / source-like M6 retention screen
# LEFT (+Y) wheel station at X250, Z45. NOT machining release.
X=250.0; Z=45.0
PIPE_R=75.0; PIPE_Z=52.0480547

PROFILE=[
    (51.25,45.00),(53.00,45.00),(55.00,43.80),(58.00,40.38),
    (61.00,36.45),(64.00,31.90),(67.00,26.50),(70.00,18.00),(71.00,15.50)
]
TIRE_T=4.0
BORE_R=8.5

COVER_INNER=46.0; COVER_OUTER=51.0
B61801=(12.0,21.0,5.0); B61801_Y=(46.15,51.15)
B61903=(17.0,30.0,7.0); B61903_Y=(51.35,58.35)
SEAL_LAND_D=19.0
XRING_GLAND_OD=23.61
XRING_Y=(58.55,61.95)
FLANGE_BODY_OD=34.0
FLANGE_CLAMP_OD=50.0
FLANGE_Y=(46.0,62.20)

FLANGE_POCKET_D=52.0
FLANGE_POCKET_Y=(51.0,62.45)
SHAFT_END_Y=67.00
KEY_Y0=62.15
KEY_Y1=66.90
KEY_L=KEY_Y1-KEY_Y0

SCREW_D=6.0
SCREW_LEN=14.0
SCREW_HEAD_D=10.5
SCREW_HEAD_H=3.3
SPRING_WASHER_ID=6.1
SPRING_WASHER_OD=11.8
SPRING_WASHER_T_COMP=1.6
WHEEL_DISK_OD=20.0
WHEEL_DISK_T=1.5

DISK_Y0=SHAFT_END_Y
DISK_Y1=SHAFT_END_Y+WHEEL_DISK_T
WASHER_Y0=DISK_Y1
WASHER_Y1=WASHER_Y0+SPRING_WASHER_T_COMP
HEAD_Y0=WASHER_Y1
HEAD_Y1=HEAD_Y0+SCREW_HEAD_H
SCREW_UNDERHEAD_Y=HEAD_Y0
SCREW_TIP_Y=SCREW_UNDERHEAD_Y-SCREW_LEN
THREAD_Y0=SCREW_TIP_Y
THREAD_Y1=SHAFT_END_Y
THREAD_ENGAGEMENT=THREAD_Y1-THREAD_Y0
RETENTION_POCKET_R=WHEEL_DISK_OD/2+0.25
RETENTION_POCKET_Y0=DISK_Y0-0.05
RETENTION_POCKET_Y1=DISK_Y1+0.10


def cyl_y(r,y0,y1):
    return cq.Workplane('XY').newObject([cq.Solid.makeCylinder(r,y1-y0,cq.Vector(X,y0,Z),cq.Vector(0,1,0))])

def ann_y(ro,ri,y0,y1):
    return cyl_y(ro,y0,y1).cut(cyl_y(ri,y0-0.02,y1+0.02))

def inter(a,b): return a.val().intersect(b.val()).Volume()
def outside(a,b): return a.val().cut(b.val()).Volume()
def pipe_allow_radius_at_y(y):
    return math.sqrt(max(0.0,PIPE_R**2-y**2))-(PIPE_Z-Z)

def make_revolved(profile):
    y0=profile[0][0]
    pts=[(y-y0,r) for y,r in profile]
    poly=pts+[(pts[-1][0],0),(pts[0][0],0)]
    s=cq.Workplane('XY').polyline(poly).close().revolve(360,(0,0),(1,0))
    return s.rotate((0,0,0),(0,0,1),90).translate((X,y0,Z))

outer=make_revolved(PROFILE)
inner_profile=[(y,max(BORE_R,r-TIRE_T)) for y,r in PROFILE]
inner_outer=make_revolved(inner_profile)
core=inner_outer.cut(cyl_y(BORE_R,50.5,71.5))
tire=outer.cut(inner_outer)

flange_pocket=cyl_y(FLANGE_POCKET_D/2,*FLANGE_POCKET_Y)
core=core.cut(flange_pocket)

key=(cq.Workplane('XY').box(4.0,KEY_L,3.0,centered=(True,False,False))
     .translate((X,KEY_Y0,Z+BORE_R-0.2)))
core=core.cut(key)

ret_pocket=cyl_y(RETENTION_POCKET_R,RETENTION_POCKET_Y0,RETENTION_POCKET_Y1)
core=core.cut(ret_pocket)

flange=cyl_y(FLANGE_BODY_OD/2,FLANGE_Y[0],FLANGE_Y[1]).union(cyl_y(FLANGE_CLAMP_OD/2,50.0,53.0))
flange=flange.cut(cyl_y(10.65,46.0,51.20))
flange=flange.cut(cyl_y(15.15,51.20,58.45))
flange=flange.cut(cyl_y(XRING_GLAND_OD/2,58.45,62.25))
for a in range(0,360,90):
    xx=X+20*math.cos(math.radians(a)); zz=Z+20*math.sin(math.radians(a))
    h=cq.Workplane('XY').newObject([cq.Solid.makeCylinder(1.7,16.5,cq.Vector(xx,45.8,zz),cq.Vector(0,1,0))])
    flange=flange.cut(h)

b61801=ann_y(B61801[1]/2,B61801[0]/2,*B61801_Y)
b61903=ann_y(B61903[1]/2,B61903[0]/2,*B61903_Y)
xring_env=ann_y(XRING_GLAND_OD/2,SEAL_LAND_D/2,*XRING_Y)
shaft_12=cyl_y(6.0,41.5,51.20)
shaft_17a=cyl_y(8.5,51.20,58.45)
shaft_19=cyl_y(9.5,58.45,62.05)
shaft_17b=cyl_y(8.5,62.05,SHAFT_END_Y)
shaft=shaft_12.union(shaft_17a).union(shaft_19).union(shaft_17b)
thread_env=cyl_y(3.0,THREAD_Y0,THREAD_Y1)
wheel_disk=ann_y(WHEEL_DISK_OD/2,3.2,DISK_Y0,DISK_Y1)
washer=ann_y(SPRING_WASHER_OD/2,SPRING_WASHER_ID/2,WASHER_Y0,WASHER_Y1)
screw_head=cyl_y(SCREW_HEAD_D/2,HEAD_Y0,HEAD_Y1)
screw_shank=cyl_y(SCREW_D/2,SCREW_TIP_Y,SCREW_UNDERHEAD_Y)

# 10x1.8 O-ring: local static face seal between shaft end and retaining disk.
ORING_ID=10.0; ORING_CS=1.8
ORING_GROOVE_DEPTH=1.35
ORING_GROOVE_WIDTH=2.40
ORING_MEAN_R=ORING_ID/2+ORING_CS/2
ORING_GROOVE_RI=ORING_MEAN_R-ORING_GROOVE_WIDTH/2
ORING_GROOVE_RO=ORING_MEAN_R+ORING_GROOVE_WIDTH/2
oring_groove=ann_y(ORING_GROOVE_RO,ORING_GROOVE_RI,SHAFT_END_Y-ORING_GROOVE_DEPTH,SHAFT_END_Y+0.02)
shaft=shaft.cut(oring_groove)
oring_env=ann_y((ORING_ID+2*ORING_CS)/2,ORING_ID/2,SHAFT_END_Y-ORING_GROOVE_DEPTH,SHAFT_END_Y)

pipe=cq.Workplane('XY').newObject([cq.Solid.makeCylinder(PIPE_R,120,cq.Vector(X-60,0,PIPE_Z),cq.Vector(1,0,0))])

checks={
    'key_effective_length_mm':KEY_L,
    'shaft_end_y_mm':SHAFT_END_Y,
    'm6_screw_underhead_length_mm':SCREW_LEN,
    'm6_thread_engagement_mm':THREAD_ENGAGEMENT,
    'm6_head_diameter_mm':SCREW_HEAD_D,
    'm6_head_height_mm':SCREW_HEAD_H,
    'compressed_spring_washer_thickness_mm':SPRING_WASHER_T_COMP,
    'retention_outer_y_mm':HEAD_Y1,
    'wheel_outer_end_y_mm':PROFILE[-1][0],
    'oring_10x1p8_face_groove_depth_mm':ORING_GROOVE_DEPTH,
    'oring_10x1p8_face_groove_width_mm':ORING_GROOVE_WIDTH,
    'oring_nominal_axial_squeeze_pct':round((1-ORING_GROOVE_DEPTH/ORING_CS)*100,2),
    'oring_groove_fill_pct':round((math.pi*(ORING_CS/2)**2)/(ORING_GROOVE_DEPTH*ORING_GROOVE_WIDTH)*100,2),
    'flange_pocket_radial_clearance_mm':FLANGE_POCKET_D/2-FLANGE_CLAMP_OD/2,
    'flange_pocket_axial_clearance_mm':FLANGE_POCKET_Y[1]-FLANGE_Y[1],
    'core_flange_intersection_mm3':round(inter(core,flange),6),
    'tire_flange_intersection_mm3':round(inter(tire,flange),6),
    'flange_b61801_intersection_mm3':round(inter(flange,b61801),6),
    'flange_b61903_intersection_mm3':round(inter(flange,b61903),6),
    'flange_xring_intersection_mm3':round(inter(flange,xring_env),6),
    'core_disk_intersection_mm3':round(inter(core,wheel_disk),6),
    'core_washer_intersection_mm3':round(inter(core,washer),6),
    'core_screw_head_intersection_mm3':round(inter(core,screw_head),6),
    'thread_envelope_outside_shaft_mm3':round(outside(thread_env,shaft),6),
    'oring_envelope_outside_shaft_end_mm3':round(outside(oring_env,cyl_y(8.5,SHAFT_END_Y-2.0,SHAFT_END_Y)),6),
}
for n,p in [('core',core),('tire',tire),('flange',flange),('wheel_disk',wheel_disk),('washer',washer),('screw_head',screw_head)]:
    checks[f'{n}_outside_DN150_mm3']=round(outside(p,pipe),6)

T=4000.0
checks['wheel_key_shear_MPa']=2*T/(17*4*KEY_L)
checks['wheel_key_bearing_MPa']=4*T/(17*4*KEY_L)
M6_MINOR=4.773
checks['min_radial_wall_at_d17_with_M6_minor_mm']=(17-M6_MINOR)/2
checks['min_wall_thread_to_keyway_root_mm']=(8.5-2.0)-M6_MINOR/2

margins=[]
for y,r in PROFILE:
    allow=pipe_allow_radius_at_y(y)
    margins.append((y,r,allow-r))
checks['wheel_profile_min_margin_mm']=min(v for _,_,v in margins)
checks['wheel_profile_margins_mm']=[{'y':y,'r':r,'margin':m} for y,r,m in margins]
core_margins=[]
for y,r in PROFILE:
    core_r=max(BORE_R,r-TIRE_T)
    core_margins.append(pipe_allow_radius_at_y(y)-core_r)
checks['hard_core_min_DN150_margin_mm']=min(core_margins)
checks['screw_head_tip_DN150_margin_mm']=pipe_allow_radius_at_y(HEAD_Y1)-SCREW_HEAD_D/2
checks['spring_washer_outer_DN150_margin_mm']=pipe_allow_radius_at_y(WASHER_Y1)-SPRING_WASHER_OD/2
checks['wheel_disk_outer_DN150_margin_mm']=pipe_allow_radius_at_y(DISK_Y1)-WHEEL_DISK_OD/2
checks['tread_interpretation']='ELASTOMER_CONTACT_SURFACE; near-zero ideal margin is intentional contact, hard-part margins govern fit'

pack_pass=(
    checks['flange_pocket_radial_clearance_mm']>=0.8 and
    checks['flange_pocket_axial_clearance_mm']>=0.2 and
    checks['core_flange_intersection_mm3']<1e-5 and
    checks['tire_flange_intersection_mm3']<1e-5 and
    checks['core_disk_intersection_mm3']<1e-5 and
    checks['core_washer_intersection_mm3']<1e-5 and
    checks['core_screw_head_intersection_mm3']<1e-5 and
    checks['thread_envelope_outside_shaft_mm3']<1e-5 and
    all(checks[f'{n}_outside_DN150_mm3']<1e-5 for n in ['core','tire','flange','wheel_disk','washer','screw_head'])
)
checks['packaging_status']='PASS_SCREEN' if pack_pass else 'HOLD'
checks['release_status']='HOLD'
checks['release_holds']=[
    'physical DN150 sweep with real elastic tread required; 0.12 mm tread value is intended rolling-contact geometry, not fixed hard-part clearance',
    'exact wheel disk thickness/material and O-ring 10x1.8 face-gland geometry',
    'exact A4 M6x14 screw and M6 spring washer article freeze',
    'M6 internal thread engagement and stripping check in selected shaft material',
    'full flange stress/deflection and bearing-fit tolerance release',
    'physical wheel removal/tool-access mock-up and submerged test'
]

assy=cq.Assembly(name='PX1_WheelFlange_RevB')
for n,p in [('WheelCore',core),('Tire',tire),('AxleFlange',flange),('B61801',b61801),('B61903',b61903),('XRingEnvelope',xring_env),('Shaft',shaft),('WheelDisk',wheel_disk),('SpringWasher',washer),('M6x14Head',screw_head),('M6Shank',screw_shank),('O_Ring_10x1p8_Envelope',oring_env)]:
    assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_WheelFlange_RevB.step'))
with open(os.path.join(OUT,'REV_B_WHEEL_FLANGE_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
