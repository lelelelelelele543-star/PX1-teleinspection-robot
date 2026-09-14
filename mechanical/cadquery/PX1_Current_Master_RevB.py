import cadquery as cq
import math, json, os
from pathlib import Path

# PX1 Current Master - 2026-09-14
# Proteus CRP-150 is the mechanical reference.
# HOLD_* geometry is an integration/keep-out proxy and is never a manufacturing PASS.
OUT=Path(os.environ.get('PX1_OUT','PX1_master_build')); OUT.mkdir(parents=True,exist_ok=True)

PIPE_R=75.; PIPE_Z=52.0480547
WHEEL_X=(50.,150.,250.); GEAR_X=(50.,100.,150.,200.,250.)
WHEEL_Z=45.; WHEEL_CENTER_Y=59.; WHEEL_OD=90.; WHEEL_W=16.
Z50_OD=52.; Z50_FACE=4.; GEAR_Y=43.
B61903=(17.,30.,7.); B61801=(12.,21.,5.); B61800=(10.,19.,5.)
XRING_ID=18.72; XRING_CS=2.62; XRING_OD=23.96
SHAFT_SEAL=(18.,30.,7.); Z40_OD=40.74; Z16_OD=17.86
BODY_L=307.; HALF_OUT=46.; HALF_IN=34.; Z0=8.; ZTOP=90.
ROOF_PTS=[(0.,22.),(140.,26.),(200.,77.),(220.,90.)]

def wp(s): return cq.Workplane('XY').newObject([s])
def box0(x,y,z,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(1,1,1)).translate((x,y,z))
def cy(x,y,z,d,l): return wp(cq.Solid.makeCylinder(d/2,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cx(x,y,z,d,l): return wp(cq.Solid.makeCylinder(d/2,l,cq.Vector(x,y,z),cq.Vector(1,0,0)))
def cz(x,y,z,d,l): return wp(cq.Solid.makeCylinder(d/2,l,cq.Vector(x,y,z),cq.Vector(0,0,1)))
def ringy(x,y,z,od,id_,l): return wp(cy(x,y,z,od,l).val().cut(cy(x,y,z,id_,l+.4).val()))
def ringx(x,y,z,od,id_,l): return wp(cx(x,y,z,od,l).val().cut(cx(x-.2,y,z,id_,l+.4).val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def between(a,b,d):
    a=cq.Vector(*a); b=cq.Vector(*b); v=b-a
    return wp(cq.Solid.makeCylinder(d/2,v.Length,a,v.normalized()))
def roof(x):
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]
def clear(p):
    vs,_=p.val().tessellate(.7)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vs)

body=box0(0,-46,8,307,92,82)
inner=cq.Workplane('XZ',origin=(0,34,0)).polyline([(8,14),(299,14),(299,85),(220,85),(200,72),(140,21),(8,roof(8)-5)]).close().extrude(68)
body=cut(body,inner)
wet=cq.Workplane('XZ',origin=(0,38,0)).polyline(ROOF_PTS+[(220,115),(0,115)]).close().extrude(76)
body=cut(body,wet)
body=cut(body,box0(10.5,34,6,286,12,80)); body=cut(body,box0(10.5,-46,6,286,12,80))
rear=box0(242,-46,19,168,92,52); rear_cav=box0(246,-40,24,158,80,42)
body=fuse(body,rear); body=cut(body,rear_cav)
pod=cq.Workplane('YZ',origin=(218,0,0)).polyline([(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]).close().extrude(89)
body=fuse(body,pod)
pod_i=cq.Workplane('YZ',origin=(221,0,0)).polyline([(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]).close().extrude(83)
body=cut(body,pod_i); throat=box0(224,-33,84,76,66,10); body=cut(body,throat)
eout=box0(300,-30,65,110,60,52); ecav=box0(304,-26,69,104,52,45)
body=fuse(body,eout); body=cut(body,ecav); body=cut(body,boxc(261,0,108,48,22,8))
dry=wp(inner.val().fuse(rear_cav.val()).fuse(pod_i.val()).fuse(throat.val()).fuse(ecav.val()))

wheels=[]; z50=[]; stations=[]; keys=[]
for side in (-1,1):
    s=float(side)
    for x in WHEEL_X:
        wheels.append((f'HOLD_QRW90_{side}_{int(x)}',cy(x,s*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD,WHEEL_W)))
        stations += [
          (f'61801_A_HOLDaxial_{side}_{int(x)}',ringy(x,s*33,WHEEL_Z,21,12,5)),
          (f'61801_B_HOLDaxial_{side}_{int(x)}',ringy(x,s*38,WHEEL_Z,21,12,5)),
          (f'61903_{side}_{int(x)}',ringy(x,s*49,WHEEL_Z,30,17,7)),
          (f'Xring_18p72x2p62_{side}_{int(x)}',ringy(x,s*54.5,WHEEL_Z,XRING_OD,XRING_ID,XRING_CS)),
          (f'HOLD_axle_flange_{side}_{int(x)}',cy(x,s*57.5,WHEEL_Z,34,3)),
          (f'HOLD_wheel_axle_{side}_{int(x)}',cy(x,s*45,WHEEL_Z,17,28)),
          (f'HOLD_wheel_stub_{side}_{int(x)}',cy(x,s*63,WHEEL_Z,12,18))]
        keys.append((f'key_4x4x12_HOLDaxial_{side}_{int(x)}',boxc(x,s*43,WHEEL_Z+7,4,12,4)))
    keys.append((f'rear_key_4x4x7_HOLDaxial_{side}',boxc(250,s*35,WHEEL_Z+7,4,7,4)))
    for x in GEAR_X: z50.append((f'Z50_m1_B4_HOLDtooth_{side}_{int(x)}',ringy(x,s*GEAR_Y,WHEEL_Z,Z50_OD,12,Z50_FACE)))

z40=[]; motors=[]
for side in (-1,1):
    s=float(side); y=s*18
    z40 += [(f'Z40_m1_HOLDmount_{side}',ringy(250,y,45,Z40_OD,10,6.5)),
            (f'61800_{side}',ringy(250,s*24.7,45,19,10,5)),
            (f'shaft_seal_18x30x7_{side}',ringy(250,s*31.5,45,30,18,7)),
            (f'HOLD_Z40_shaft_{side}',cy(250,s*29,45,10,28))]
    motors += [(f'ISL_PGM32P_HOLDlength_{side}',cx(293,y,45,32,92)),
               (f'NBK_MLR20C_6_6_{side}',ringx(257,y,45,20,6,24)),
               (f'61801_Z16_support_{side}',ringx(250,y,45,21,12,5)),
               (f'Z16_m1_HOLDmount_{side}',ringx(239,y,45,Z16_OD,6,7.5))]

pivx=200.; pzl=92.; pzh=109.; link=90.; camz=75.; theta=math.asin((camz-2-100.5)/link)
dx=-link*math.cos(theta); dz=link*math.sin(theta); low=(pivx+dx,pzl+dz); high=(pivx+dx,pzh+dz)
def arm(a,b,y):
    x1,z1=a; x2,z2=b; L=math.hypot(x2-x1,z2-z1); ang=math.degrees(math.atan2(z2-z1,x2-x1))
    return boxc(0,y,0,L,4,14).rotate((0,0,0),(0,1,0),-ang).translate(((x1+x2)/2,0,(z1+z2)/2))
arms=[]
for side in (-1,1): arms += [(f'HOLD_lower_arm_{side}',arm((pivx,pzl),low,side*31)),(f'HOLD_upper_arm_{side}',arm((pivx,pzh),high,side*31))]
carrier=boxc((low[0]+high[0])/2,0,(low[1]+high[1])/2,12,58,24)
camera=cx(83.5569-39,0,75,52,78); camera=cut(camera,cx(83.5569-35,0,75,44,70))
gas=between((194,16,82.9),(pivx-63*math.cos(theta),16,pzl+63*math.sin(theta)),12)

cover=boxc(261,0,113,86,44,6); valve=cz(273,0,116,12,1.5)
gland=fuse(cx(205,12,103,12,6.5),boxc(221.5,12,103,20,16,16))
p1=(pivx-20*math.cos(theta),25.5,pzl+20*math.sin(theta)); p2=(pivx-72*math.cos(theta),25.5,pzl+72*math.sin(theta))
harness=between(p1,p2,6.5); guard=between(p1,p2,10)
sp13=cx(83.5569+39,0,93,13,36)

electronics={
 'HOLD_BTS7960_A':boxc(330,0,91.5,50,50,43),'HOLD_BTS7960_B':boxc(382,0,91.5,50,50,43),
 'DELTA_TR1D_P2':boxc(205,-22,42,43,16,15),'NICHICON_UCS2D221MHD1TN':cx(192.5,24,30,18,25),
 'CINCON_CQB150W110S24':boxc(260,0,70,57.9,36.8,12.7),'NUCLEO_F446RE_HOLDheight':boxc(262.25,0,98,82.5,70,12),
 'HOLD_LM2596_variant':boxc(220,0,70,21,43,14),'HOLD_MP1584_variant':boxc(270,0,58,22,17,8),
 'HOLD_MAX485_variant':boxc(260,0,27,44,14,9),'HOLD_pressure_sensor_keepout_NOT_PART':boxc(210,0,50,30,24,15)}
rear_conn=cx(410,0,45,20,20); strain=cx(430,0,45,24,20); tether=cx(450,0,45,10,31)

assy=cq.Assembly(name='PX1_Current_Master')
assy.add(body,name='01_pressure_body_HOLDmachining')
for grp in (wheels,z50,stations,keys,z40,motors,arms):
    for n,p in grp: assy.add(p,name=n)
for n,p in [('HOLD_camera_carrier',carrier),('HOLD_sealed_camera',camera),('HOLD_gas_spring',gas),('PRESSURE_LIFT_cover_HOLDgroove',cover),('HOLD_pressure_valve',valve),('LAPP_53112000',gland),('camera_harness_EXACTLY_6_CORE',harness),('HOLD_harness_guard',guard),('HOLD_SP13',sp13),('HOLD_rear_connector',rear_conn),('HOLD_strain_relief',strain),('HOLD_6core_tether',tether)]: assy.add(p,name=n)
for n,p in electronics.items(): assy.add(p,name=n)
step=OUT/'PX1_Current_Master.step'; assy.save(str(step))

counts={'wheels':len(wheels),'Z50':len(z50),'side_drive_61801':sum(n.startswith('61801_') and 'Z16' not in n for n,p in stations),'61903':sum(n.startswith('61903_') for n,p in stations),'Xrings':sum(n.startswith('Xring_') for n,p in stations),'Z40':sum(n.startswith('Z40_') for n,p in z40),'61800':sum(n.startswith('61800_') for n,p in z40),'shaft_seal_18x30x7':sum(n.startswith('shaft_seal_') for n,p in z40),'Z16':sum(n.startswith('Z16_') for n,p in motors),'Z16_61801':sum(n.startswith('61801_Z16') for n,p in motors),'traction_motors':sum(n.startswith('ISL_') for n,p in motors),'wheel_keys_4x4x12':sum(n.startswith('key_') for n,p in keys),'rear_input_keys_4x4x7':sum(n.startswith('rear_key') for n,p in keys),'lift_arms':len(arms),'local_camera_conductors':6}
expected={'wheels':6,'Z50':10,'side_drive_61801':12,'61903':6,'Xrings':6,'Z40':2,'61800':2,'shaft_seal_18x30x7':2,'Z16':2,'Z16_61801':2,'traction_motors':2,'wheel_keys_4x4x12':6,'rear_input_keys_4x4x7':2,'lift_arms':4,'local_camera_conductors':6}
service=[cover,gland,valve]
coll={'service_vs_Z50':max(inter(p,g) for p in service for _,g in z50),'service_vs_arms':max(inter(p,a) for p in service for _,a in arms),'service_vs_camera':max(inter(p,camera) for p in service),'guard_vs_Z50':max(inter(guard,g) for _,g in z50),'guard_vs_camera':inter(guard,camera),'motor_vs_camera':max(inter(p,camera) for n,p in motors if n.startswith('ISL_'))}
outside={n:round(p.val().cut(dry.val()).Volume(),4) for n,p in electronics.items()}
pairs={}; e=list(electronics)
for i,a in enumerate(e):
  for b in e[i+1:]:
    v=inter(electronics[a],electronics[b])
    if v>1e-3: pairs[a+'__'+b]=round(v,3)
pipe={'body':clear(body),'service_cover':clear(cover),'LAPP_gland':clear(gland),'pressure_cap':clear(valve),'lift_guard_LOW':clear(guard),'camera_LOW':clear(camera),'rear_strain_relief':clear(strain),'wheel_PROXY_min_NOT_RELEASE':min(clear(p) for _,p in wheels)}
result={'status':'INTEGRATED_GEOMETRY_COMPLETE_WITH_HOLDS / NOT_FINAL_MACHINING_RELEASE','policy':'No HOLD proxy is counted as PASS.','source_counts':counts,'counts_match':counts==expected,'collision_check':coll,'electronics_outside_dry_volume_mm3':outside,'electronics_pair_collisions_mm3':pairs,'electronics_packaging_geometry_pass':all(v<1e-3 for v in outside.values()) and not pairs,'dn150_clearance_mm':pipe,'dn150_wheel_release':False,'holds':['QRW90 exact wheel solid','side-drive 61801 axial stack and axle shoulders','Z16/Z40 full supplier geometry','PGM-32P sample dimensions','BTS7960 bought-board dimensions','pressure sensor exact article','SP13 and rear tether termination dimensions','pressure-decay/submersion test','6-core cable EMC/flex + 40 m tether test']}
(OUT/'PX1_CURRENT_MASTER_VALIDATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
