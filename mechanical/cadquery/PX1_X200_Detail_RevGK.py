import cadquery as cq
import math, json, os

# PX-1 Rev.GK — detailed supported X200 shaft/pinion retention and bearing-reaction validation
# Prototype engineering only. Not machining release.

OUT=os.path.abspath('build_revgk')
os.makedirs(OUT, exist_ok=True)

# Active GJ geometry
X200=200.0
Z=45.0
MOTOR_Y=16.5
M=1.25
ZP=16
ZG=40
FACE=8.0
PHI=math.radians(20.0)
DELTA_P=math.atan(ZP/ZG)
DELTA_G=math.atan(ZG/ZP)
R_CONE=0.5*M*math.sqrt(ZP**2+ZG**2)
PINION_APEX_OUT=R_CONE*math.cos(DELTA_P)
GEAR_APEX_OUT=R_CONE*math.cos(DELTA_G)
PINION_X1=X200+PINION_APEX_OUT
PINION_X0=PINION_X1-FACE

# Torque ceiling retained from Rev.GJ until actual motor and gear tests
T_MOTOR=1.0 # N*m
ETA_BEVEL=0.85
T_SIDE=T_MOTOR*(ZG/ZP)*ETA_BEVEL

# Bearings used in the supported pinion cartridge
B6801_ID=12.0; B6801_OD=21.0; B6801_W=5.0
B6701_ID=12.0; B6701_OD=18.0; B6701_W=4.0
PINION_B1_X0=225.5; PINION_B1_X1=230.5
PINION_B2_X0=231.0; PINION_B2_X1=235.0
PINION_B1_C=(PINION_B1_X0+PINION_B1_X1)/2
PINION_B2_C=(PINION_B2_X0+PINION_B2_X1)/2
PINION_FORCE_X=(PINION_X0+PINION_X1)/2
MOTOR_FACE_X=237.0

# Candidate motor D-shaft interface; exact purchased motor overrides these dimensions
MOTOR_SHAFT_D=6.0
MOTOR_D_FLAT_AF=5.4
D_BORE_DEPTH=10.0

# Pinion gear-seat/key/end retention
PINION_SEAT_D=8.0
PINION_KEY_W=2.0; PINION_KEY_H=2.0; PINION_KEY_L=7.0
PINION_KEY_T1=1.2
PINION_END_THREAD_D=4.0
PINION_END_THREAD_DEPTH=8.0

# X200 side shaft stack, one side local Y-axis coordinates (left side)
B6800_ID=10.0; B6800_OD=19.0; B6800_W=5.0
SEAL_ID=18.0; SEAL_OD=30.0; SEAL_W=7.0
SIDE_JOURNAL_D=12.0
SIDE_B1_Y0=29.5; SIDE_B1_Y1=34.5; SIDE_B1_C=32.0
SEAL_Y0=34.5; SEAL_Y1=41.5
SLINGER_Y0=41.5; SLINGER_W=0.5
Z50_FACE_Y0=42.0; Z50_FACE_W=3.5; Z50_FACE_Y1=Z50_FACE_Y0+Z50_FACE_W
THRUST_SHIM_Y0=45.5; THRUST_SHIM_W=0.3
SIDE_B2_Y0=49.0; SIDE_B2_Y1=53.0; SIDE_B2_C=51.0
SIDE_GEAR_FORCE_Y=(Z50_FACE_Y0+Z50_FACE_Y1)/2
BEVEL_FORCE_Y=MOTOR_Y+GEAR_APEX_OUT-FACE/2

# Parallel keys and circlip
BEVEL_KEY_W=3.0; BEVEL_KEY_H=3.0; BEVEL_KEY_L=10.0; BEVEL_KEY_T1=1.8
Z50_KEY_W=4.0; Z50_KEY_H=4.0; Z50_KEY_L=3.5; Z50_KEY_T1=2.5
CIRCLIP_D_NOM=12.0; CIRCLIP_GROOVE_D=11.5; CIRCLIP_GROOVE_W=1.1
CIRCLIP_Y0=45.9
LOCAL_BOSS_OD=26.0; LOCAL_BOSS_Y0=46.0; LOCAL_BOSS_Y1=54.0


def wp(s): return cq.Workplane('XY').newObject([s])
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,1,0)))
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()

# ---- Supported pinion shaft ----
pinion_shaft=cyl_x(PINION_X0-1.0, MOTOR_Y, Z, PINION_SEAT_D/2, (PINION_B1_X0-(PINION_X0-1.0)))
pinion_shaft=fuse(pinion_shaft,cyl_x(PINION_B1_X0,MOTOR_Y,Z,6.0,PINION_B2_X1-PINION_B1_X0))
pinion_shaft=fuse(pinion_shaft,cyl_x(PINION_B2_X1,MOTOR_Y,Z,7.0,MOTOR_FACE_X-PINION_B2_X1))
thread_tool=cyl_x(PINION_X0-1.2,MOTOR_Y,Z,PINION_END_THREAD_D/2,PINION_END_THREAD_DEPTH)
pinion_shaft=cut(pinion_shaft,thread_tool)
keyway_pin=box(PINION_X0, MOTOR_Y-PINION_KEY_W/2, Z+PINION_SEAT_D/2-PINION_KEY_T1,
               PINION_KEY_L, PINION_KEY_W, PINION_KEY_T1+0.4)
pinion_shaft=cut(pinion_shaft,keyway_pin)
dtool=cyl_x(MOTOR_FACE_X-D_BORE_DEPTH,MOTOR_Y,Z,MOTOR_SHAFT_D/2,D_BORE_DEPTH+0.2)
flat_z = Z - MOTOR_SHAFT_D/2 + MOTOR_D_FLAT_AF
cap=box(MOTOR_FACE_X-D_BORE_DEPTH-0.1,MOTOR_Y-4,flat_z, D_BORE_DEPTH+0.4,8,4)
dtool=cut(dtool,cap)
pinion_shaft=cut(pinion_shaft,dtool)

pinion_env=cq.Workplane('YZ').center(MOTOR_Y,Z).circle((M*ZP/2+M)).extrude(FACE).translate((PINION_X0,0,0))
pinion_key=box(PINION_X0,MOTOR_Y-PINION_KEY_W/2,Z+PINION_SEAT_D/2-PINION_KEY_T1,
               PINION_KEY_L,PINION_KEY_W,PINION_KEY_H)
b6801=cyl_x(PINION_B1_X0,MOTOR_Y,Z,B6801_OD/2,B6801_W)
b6701_p=cyl_x(PINION_B2_X0,MOTOR_Y,Z,B6701_OD/2,B6701_W)

# ---- Detailed left X200 side shaft ----
side_shaft=cyl_y(X200,18.0,Z,5.0,16.5)
side_shaft=fuse(side_shaft,cyl_y(X200,34.5,Z,9.0,7.0))
side_shaft=fuse(side_shaft,cyl_y(X200,41.5,Z,6.0,11.5))
side_shaft=cut(side_shaft,cyl_y(X200,18.0,Z,2.0,8.0))
bevel_keyway=box(X200-BEVEL_KEY_W/2,18.5,Z+5.0-BEVEL_KEY_T1,BEVEL_KEY_W,BEVEL_KEY_L,BEVEL_KEY_T1+0.4)
side_shaft=cut(side_shaft,bevel_keyway)
z50_keyway=box(X200-Z50_KEY_W/2,Z50_FACE_Y0,Z+SIDE_JOURNAL_D/2-Z50_KEY_T1,Z50_KEY_W,Z50_KEY_L,Z50_KEY_T1+0.4)
side_shaft=cut(side_shaft,z50_keyway)
groove_outer=cyl_y(X200,CIRCLIP_Y0,Z,CIRCLIP_D_NOM/2,CIRCLIP_GROOVE_W)
groove_inner=cyl_y(X200,CIRCLIP_Y0,Z,CIRCLIP_GROOVE_D/2,CIRCLIP_GROOVE_W)
side_shaft=cut(side_shaft,wp(groove_outer.val().cut(groove_inner.val())))

b6800=cyl_y(X200,SIDE_B1_Y0,Z,B6800_OD/2,B6800_W)
seal=cyl_y(X200,SEAL_Y0,Z,SEAL_OD/2,SEAL_W)
slinger=cyl_y(X200,SLINGER_Y0,Z,10.0,SLINGER_W)
z50=cyl_y(X200,Z50_FACE_Y0,Z,26.0,Z50_FACE_W)
z50_key=box(X200-Z50_KEY_W/2,Z50_FACE_Y0,Z+SIDE_JOURNAL_D/2-Z50_KEY_T1,Z50_KEY_W,Z50_KEY_L,Z50_KEY_H)
shim=cyl_y(X200,THRUST_SHIM_Y0,Z,9.0,THRUST_SHIM_W)
b6701_s=cyl_y(X200,SIDE_B2_Y0,Z,B6701_OD/2,B6701_W)
local_cover_boss=cyl_y(X200,LOCAL_BOSS_Y0,Z,LOCAL_BOSS_OD/2,LOCAL_BOSS_Y1-LOCAL_BOSS_Y0)
large_bevel=cyl_y(X200,18.0,Z,(M*ZG/2+M),8.0)
bevel_key=box(X200-BEVEL_KEY_W/2,18.5,Z+5.0-BEVEL_KEY_T1,BEVEL_KEY_W,BEVEL_KEY_L,BEVEL_KEY_H)

# ---- Load/reaction calculations ----
Ft_p=T_MOTOR*1000.0/(M*ZP/2.0)
Fr_p=Ft_p*math.tan(PHI)*math.cos(DELTA_P)
Fa_p=Ft_p*math.tan(PHI)*math.sin(DELTA_P)
Pr=math.hypot(Ft_p,Fr_p)
span_p=PINION_B2_C-PINION_B1_C
R1p=Pr*(PINION_B2_C-PINION_FORCE_X)/span_p
R2p=Pr*(PINION_FORCE_X-PINION_B1_C)/span_p

Ft_g=Ft_p
Fr_g=Ft_g*math.tan(PHI)*math.cos(DELTA_G)
Fa_g=Ft_g*math.tan(PHI)*math.sin(DELTA_G)
Ft_z50=T_SIDE*1000.0/(50.0/2.0)
Fr_z50=Ft_z50*math.tan(PHI)
span_s=SIDE_B2_C-SIDE_B1_C

def reactions_overhung(P, x, a, b):
    Ra=P*(b-x)/(b-a)
    Rb=P*(x-a)/(b-a)
    return Ra,Rb

A_Ft_g,B_Ft_g=reactions_overhung(Ft_g,BEVEL_FORCE_Y,SIDE_B1_C,SIDE_B2_C)
A_Fr_g,B_Fr_g=reactions_overhung(Fr_g,BEVEL_FORCE_Y,SIDE_B1_C,SIDE_B2_C)
A_Ft_z,B_Ft_z=reactions_overhung(Ft_z50,SIDE_GEAR_FORCE_Y,SIDE_B1_C,SIDE_B2_C)
A_Fr_z,B_Fr_z=reactions_overhung(Fr_z50,SIDE_GEAR_FORCE_Y,SIDE_B1_C,SIDE_B2_C)
A_tan_abs=abs(A_Ft_g)+abs(A_Ft_z)
B_tan_abs=abs(B_Ft_g)+abs(B_Ft_z)
A_rad_abs=abs(A_Fr_g)+abs(A_Fr_z)
B_rad_abs=abs(B_Fr_g)+abs(B_Fr_z)
A_result=math.hypot(A_tan_abs,A_rad_abs)
B_result=math.hypot(B_tan_abs,B_rad_abs)

def tau_shaft(T_Nm,d_mm): return 16*T_Nm*1000.0/(math.pi*d_mm**3)
def key_shear(T_Nm,d,b,l): return 2*T_Nm*1000.0/(d*b*l)
def key_bearing(T_Nm,d,h,l): return 4*T_Nm*1000.0/(d*h*l)

checks={
 'pinion_force_N': {'Ft':Ft_p,'Fr':Fr_p,'Fa':Fa_p,'radial_resultant':Pr},
 'pinion_support_centers_x_mm':[PINION_B1_C,PINION_B2_C],
 'pinion_force_station_x_mm':PINION_FORCE_X,
 'pinion_support_reactions_signed_N':[R1p,R2p],
 'pinion_support_reactions_abs_N':[abs(R1p),abs(R2p)],
 'pinion_support_reactions_2x_abs_N':[2*abs(R1p),2*abs(R2p)],
 'side_bevel_force_N': {'Ft':Ft_g,'Fr':Fr_g,'Fa':Fa_g},
 'side_z50_force_N': {'Ft':Ft_z50,'Fr':Fr_z50},
 'side_support_centers_y_mm':[SIDE_B1_C,SIDE_B2_C],
 'side_force_stations_y_mm': {'bevel':BEVEL_FORCE_Y,'z50':SIDE_GEAR_FORCE_Y},
 'side_support_conservative_resultant_N':[A_result,B_result],
 'side_support_conservative_2x_N':[2*A_result,2*B_result],
 'bearing_static_ratings_N': {'6801_61801':1050.0,'6701':530.0,'6800_61800':840.0},
 'pinion_bearing_2x_static_safety': [1050.0/(2*abs(R1p)),530.0/(2*abs(R2p))],
 'side_bearing_2x_static_safety': [840.0/(2*A_result),530.0/(2*B_result)],
 'shaft_torsion_MPa': {'pinion_d8':tau_shaft(T_MOTOR,8.0),'x200_d10':tau_shaft(T_SIDE,10.0),'outer_d12':tau_shaft(T_SIDE,12.0)},
 'key_stress_MPa': {
    'pinion_2x2x7': {'shear':key_shear(T_MOTOR,8.0,2.0,PINION_KEY_L),'bearing':key_bearing(T_MOTOR,8.0,2.0,PINION_KEY_L)},
    'bevel_3x3x10': {'shear':key_shear(T_SIDE,10.0,3.0,BEVEL_KEY_L),'bearing':key_bearing(T_SIDE,10.0,3.0,BEVEL_KEY_L)},
    'z50_4x4x3p5': {'shear':key_shear(T_SIDE,12.0,4.0,Z50_KEY_L),'bearing':key_bearing(T_SIDE,12.0,4.0,Z50_KEY_L)},
 },
 'z50_axial_stack_mm': {'slinger':[SLINGER_Y0,SLINGER_Y0+SLINGER_W],'gear':[Z50_FACE_Y0,Z50_FACE_Y1],'shim':[THRUST_SHIM_Y0,THRUST_SHIM_Y0+THRUST_SHIM_W],'circlip_groove':[CIRCLIP_Y0,CIRCLIP_Y0+CIRCLIP_GROOVE_W],'bearing':[SIDE_B2_Y0,SIDE_B2_Y1],'local_cover_boss':[LOCAL_BOSS_Y0,LOCAL_BOSS_Y1]},
 'motor_D_bore_candidate': {'diameter_mm':MOTOR_SHAFT_D,'AF_mm':MOTOR_D_FLAT_AF,'depth_mm':D_BORE_DEPTH,'status':'HOLD until purchased motor is measured'},
 'circlip_candidate': {'shaft_nominal_mm':12.0,'groove_d_mm':CIRCLIP_GROOVE_D,'groove_w_mm':CIRCLIP_GROOVE_W,'status':'candidate; verify exact DIN471 supplier ring'},
}

solids={'pinion_shaft':pinion_shaft,'pinion_env':pinion_env,'pinion_key':pinion_key,'b6801':b6801,'b6701_p':b6701_p,
        'side_shaft':side_shaft,'b6800':b6800,'seal':seal,'slinger':slinger,'z50':z50,'z50_key':z50_key,'shim':shim,'b6701_s':b6701_s,'local_cover_boss':local_cover_boss,
        'large_bevel':large_bevel,'bevel_key':bevel_key}
checks['solid_validity']={n:s.val().isValid() for n,s in solids.items()}
checks['unintended_intersections_mm3']={
  'pinion_key_vs_b6801':inter(pinion_key,b6801),
  'pinion_key_vs_b6701':inter(pinion_key,b6701_p),
  'z50_vs_6701':inter(z50,b6701_s),
  'z50_vs_seal':inter(z50,seal),
  'z50_key_vs_seal':inter(z50_key,seal),
  'slinger_vs_seal':inter(slinger,seal),
  'slinger_vs_z50':inter(slinger,z50),
  'shim_vs_z50':inter(shim,z50),
  'shim_vs_6701':inter(shim,b6701_s),
  'z50_vs_local_cover_boss':inter(z50,local_cover_boss),
  'bevel_key_vs_b6800':inter(bevel_key,b6800),
}
checks['pass_geometry']=all(checks['solid_validity'].values()) and all(v<1e-6 for v in checks['unintended_intersections_mm3'].values())
checks['pass_bearing_screen']=(min(checks['pinion_bearing_2x_static_safety'])>=1.25 and min(checks['side_bearing_2x_static_safety'])>=1.25)
checks['pass_key_screen']=all(d['shear']<80 and d['bearing']<160 for d in checks['key_stress_MPa'].values())
checks['status']='PASS' if checks['pass_geometry'] and checks['pass_bearing_screen'] and checks['pass_key_screen'] else 'FAIL'

assy=cq.Assembly(name='PX1_X200_Detail_RevGK')
for n,s in solids.items(): assy.add(s,name=n)
assy.save(os.path.join(OUT,'PX1_X200_Detail_RevGK.step'))
for n in ['pinion_shaft','side_shaft']:
    cq.exporters.export(solids[n],os.path.join(OUT,n+'_RevGK.step'))
with open(os.path.join(OUT,'REV_GK_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS': raise SystemExit(2)
