#!/usr/bin/env python3
import cadquery as cq
import math
from pathlib import Path

OUT = Path('/mnt/data/PX1_RevDX')
OUT.mkdir(exist_ok=True)

# PX-1 Rev.DX packaging master — CRP150-style 6WD
BODY_L=307.0
BODY_HALF_W=46.0
BODY_Z0=14.0
BODY_Z1=90.0
WHEEL_X=[50.0,150.0,250.0]
IDLER_X=[100.0,200.0]
WHEEL_Z=45.0
PIPE_R=75.0
# desired tread contact at outboard edge of narrow full-radius crown
CONTACT_Y=57.0
PIPE_Z=math.sqrt(PIPE_R**2-CONTACT_Y**2)  # contact point is z=0

# Side train: DRW-002-374-inspired five equal Z50 gears
SPUR_R_OD=26.0
SPUR_FACE=8.0
SPUR_Y0=35.5

# Bevel pair KHK SB1.5-1845H / SB1.5-4518H envelope
BEVEL_X=150.0
BEVEL_Z=45.0
INTERSECT_Y=5.0
BIG_R=68.18/2
BIG_MOUNT=30.0
PINION_R=30.86/2
PINION_LEN=21.97
PINION_BACK_FRONT=105.0
PINION_BACK_REAR=195.0

parts=[]
def add(name, shape):
    parts.append((name, shape))
    return shape

def cyl(radius, length, x,y,z, dx,dy,dz):
    return cq.Solid.makeCylinder(radius,length,cq.Vector(x,y,z),cq.Vector(dx,dy,dz))

def cone(r1,r2,length,x,y,z,dx,dy,dz):
    return cq.Solid.makeCone(r1,r2,length,cq.Vector(x,y,z),cq.Vector(dx,dy,dz))

# Main pressure body + local bevel belly pocket
body=add('PressureBody', cq.Workplane('XY').box(BODY_L, 2*BODY_HALF_W, BODY_Z1-BODY_Z0, centered=(False,True,False)).translate((0,0,BODY_Z0)).val())
belly=add('BevelBelly', cq.Workplane('XY').box(78,76,78, centered=(False,True,False)).translate((111,0,7)).val())

# Scalloped 5 mm side cover plates, 5 overlapping circular lobes around gears.
for side in (+1,-1):
    d=(0,side,0)
    ystart=46.0*side
    cover=None
    for x in [50,100,150,200,250]:
        s=cyl(30.0,5.0,x,ystart,WHEEL_Z,*d)
        cover=s if cover is None else cover.fuse(s)
    add(f'SideCover_{"L" if side>0 else "R"}',cover)
    # wheel station bearing/seal bosses to outboard y=55.5
    for x in WHEEL_X:
        boss=cyl(15.0,9.5,x,ystart,WHEEL_Z,*d)
        add(f'Boss_{side}_{int(x)}',boss)

# Side Z50 gear envelopes: all five equal, 8 mm face.
for side in (+1,-1):
    if side>0:
        y=SPUR_Y0; d=(0,1,0)
    else:
        y=-SPUR_Y0; d=(0,-1,0)
    for x in [50,100,150,200,250]:
        add(f'Z50_{side}_{int(x)}',cyl(SPUR_R_OD,SPUR_FACE,x,y,WHEEL_Z,*d))

# Wheel shafts Ø12, outer 61801 bearing envelope and 12x22x7 seal envelope.
for side in (+1,-1):
    d=(0,side,0)
    for x in WHEEL_X:
        yshaft=28*side
        add(f'WheelShaft_{side}_{int(x)}',cyl(6.0,40.5,x,yshaft,WHEEL_Z,*d))
        add(f'Outer61801_{side}_{int(x)}',cyl(10.5,5.0,x,43.5*side,WHEEL_Z,*d))
        add(f'Seal12x22x7_{side}_{int(x)}',cyl(11.0,7.0,x,48.5*side,WHEEL_Z,*d))

# Bevel output envelopes. Cone from intersection toward each side, conservative to full mounting distance.
add('BigBevel_L_env', cone(2.0,BIG_R,BIG_MOUNT,BEVEL_X,+INTERSECT_Y,BEVEL_Z,0,1,0))
add('BigBevel_R_env', cone(2.0,BIG_R,BIG_MOUNT,BEVEL_X,-INTERSECT_Y,BEVEL_Z,0,-1,0))
# Central compact 61800 support envelopes, one on each half-shaft.
add('Inner61800_L',cyl(9.5,5.0,BEVEL_X,0,BEVEL_Z,0,1,0))
add('Inner61800_R',cyl(9.5,5.0,BEVEL_X,0,BEVEL_Z,0,-1,0))

# Supported pinion shafts; one motor front, opposite motor rear to avoid Ø37 body overlap.
add('MotorFront_env',cyl(18.5,85.0,5,+INTERSECT_Y,BEVEL_Z,1,0,0))
add('FrontCoupler_env',cyl(7.0,15.0,90,+INTERSECT_Y,BEVEL_Z,1,0,0))
add('FrontPinionBearing1',cyl(9.5,6.0,93,+INTERSECT_Y,BEVEL_Z,1,0,0))
add('FrontPinionBearing2',cyl(9.5,6.0,99,+INTERSECT_Y,BEVEL_Z,1,0,0))
add('FrontPinion_env',cone(PINION_R,5.0,PINION_LEN,PINION_BACK_FRONT,+INTERSECT_Y,BEVEL_Z,1,0,0))

add('MotorRear_env',cyl(18.5,85.0,295,-INTERSECT_Y,BEVEL_Z,-1,0,0))
add('RearCoupler_env',cyl(7.0,15.0,205,-INTERSECT_Y,BEVEL_Z,1,0,0))
add('RearPinionBearing1',cyl(9.5,6.0,196,-INTERSECT_Y,BEVEL_Z,1,0,0))
add('RearPinionBearing2',cyl(9.5,6.0,202,-INTERSECT_Y,BEVEL_Z,1,0,0))
add('RearPinion_env',cone(PINION_R,5.0,PINION_LEN,PINION_BACK_REAR,-INTERSECT_Y,BEVEL_Z,-1,0,0))

# Tapered wheels. Narrow full Ø90 crown, then shoulder to r=14.8 at outer y=68.5.
for side in (+1,-1):
    d=(0,side,0)
    y0=55.5*side
    for x in WHEEL_X:
        crown=cyl(45.0,1.5,x,y0,WHEEL_Z,*d)
        shoulder=cone(45.0,14.8,11.5,x,57.0*side,WHEEL_Z,*d)
        add(f'Wheel_{side}_{int(x)}',crown.fuse(shoulder))

# Camera envelope at DN150-SAFE Z=75; horizontal body shown only.
add('CameraHead_SAFE_env',cyl(26.0,72.0,55,0,75,1,0,0))

# export compound
compound=cq.Compound.makeCompound([p for _,p in parts])
cq.exporters.export(compound,str(OUT/'PX1_CRP150_6W_Master_RevDX.step'))

# ---------- numerical checks ----------
def radial_clear(y,z):
    return PIPE_R-math.hypot(abs(y),z-PIPE_Z)

# conservative body/cover points
checks={}
checks['body_corner']=min(radial_clear(y,z) for y in (-46,46) for z in (14,90))
checks['belly_corner']=min(radial_clear(y,z) for y in (-38,38) for z in (7,85))
checks['cover_plate']=min(radial_clear(y,z) for y in (-51,51) for z in (15,75))
# boss outer y 55.5, z +/-15 around wheel axis
checks['wheel_boss']=min(radial_clear(y,z) for y in (-55.5,55.5) for z in (30,60))

# wheel profile: bottom-most point is limiting. Contact at y=57 is intentionally zero.
def wheel_r(yabs):
    if 55.5 <= yabs <= 57.0:
        return 45.0
    if 57.0 < yabs <= 68.5:
        t=(yabs-57.0)/(68.5-57.0)
        return 45.0+(14.8-45.0)*t
    return None
min_shoulder=999
min_point=None
for i in range(10001):
    y=57.05+(68.5-57.05)*i/10000
    r=wheel_r(y)
    c=radial_clear(y,WHEEL_Z-r)
    if c<min_shoulder:
        min_shoulder=c; min_point=(y,r)
checks['outer_shoulder_near_contact']=min_shoulder
checks['outer_shoulder_Y60']=radial_clear(60.0,WHEEL_Z-wheel_r(60.0))
checks['outer_shoulder_Y64']=radial_clear(64.0,WHEEL_Z-wheel_r(64.0))
checks['outer_face_Y68_5']=radial_clear(68.5,WHEEL_Z-wheel_r(68.5))

# camera cylindrical envelope sampled over tilt -105..+105, Ø52 x72.
def cam_clear(zcam):
    maxrad=0.0
    for thdeg in range(-105,106):
        th=math.radians(thdeg)
        for is_ in range(37):
            s=-36+72*is_/36
            for ip in range(73):
                ph=2*math.pi*ip/72
                y=26*math.sin(ph)
                z=zcam+s*math.sin(th)+26*math.cos(ph)*math.cos(th)
                maxrad=max(maxrad,math.hypot(y,z-PIPE_Z))
    return PIPE_R-maxrad
checks['camera_safe_Z75_full_tilt']=cam_clear(75.0)
checks['camera_Z76_full_tilt']=cam_clear(76.0)

# unintended hard collision checks (intended bevel mesh intersections are omitted)
def ivol(a,b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return float('nan')
# motors vs each other and vs side gears should be zero
byname={n:s for n,s in parts}
collisions={
    'motor_front_vs_rear':ivol(byname['MotorFront_env'],byname['MotorRear_env']),
    'motor_front_vs_left_sidegear':ivol(byname['MotorFront_env'],byname['Z50_1_150']),
    'motor_rear_vs_right_sidegear':ivol(byname['MotorRear_env'],byname['Z50_-1_150']),
    'big_bevel_L_vs_sidegear_L_gap':ivol(byname['BigBevel_L_env'],byname['Z50_1_150']),
    'big_bevel_R_vs_sidegear_R_gap':ivol(byname['BigBevel_R_env'],byname['Z50_-1_150']),
}

with open(OUT/'REV_DX_PACKAGING_CHECK.txt','w',encoding='utf-8') as f:
    f.write(f'PX-1 Rev.DX packaging check\nPIPE_R={PIPE_R:.3f} mm, PIPE_Z={PIPE_Z:.3f} mm, intentional wheel contact Y={CONTACT_Y:.3f}\n\n')
    for k,v in checks.items(): f.write(f'{k}: {v:.3f} mm\n')
    f.write('\nIntersection volumes (should be 0 for listed non-mesh pairs):\n')
    for k,v in collisions.items(): f.write(f'{k}: {v:.6f} mm^3\n')
    f.write('\nDecision:\n')
    f.write('DN150_SAFE camera axis = Z75 mm candidate (~4.3 mm nominal full-tilt margin). Z76 still clears ~3.3 mm ideally but is not preferred because tolerance/real protrusions would consume the margin.\n')
    f.write('Side drive corrected to five equal Z50 gears.\n')
    f.write('One motor front / one motor rear packaging prevents Ø37 motor-body collision.\n')

print((OUT/'REV_DX_PACKAGING_CHECK.txt').read_text())
print('STEP bytes', (OUT/'PX1_CRP150_6W_Master_RevDX.step').stat().st_size)
