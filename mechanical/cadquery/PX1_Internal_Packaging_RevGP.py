import cadquery as cq
import math, json, os

OUT=os.path.abspath('build_revgp')
os.makedirs(OUT,exist_ok=True)

# Active Rev.GJ/GL pressure cavity.
MAIN_X0=8.0; MAIN_X1=307.0
MAIN_Y0=-34.0; MAIN_Y1=34.0
MAIN_Z0=14.0; MAIN_Z1=85.0
POD_X0=299.0; POD_X1=332.0
POD_Y0=-34.0; POD_Y1=34.0
POD_Z0=27.0; POD_Z1=63.0


def wp(s): return cq.Workplane('XY').newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def outside(comp,cavity): return comp.val().cut(cavity.val()).Volume()

main=box(MAIN_X0,MAIN_Y0,MAIN_Z0,MAIN_X1-MAIN_X0,MAIN_Y1-MAIN_Y0,MAIN_Z1-MAIN_Z0)
pod=box(POD_X0,POD_Y0,POD_Z0,POD_X1-POD_X0,POD_Y1-POD_Y0,POD_Z1-POD_Z0)
cavity=wp(main.val().fuse(pod.val()))

parts={}
# NUCLEO-F446RE 82.5 x 70 board; reserve 22 mm installed thickness/headers.
# Long dimension along X. In the 68 x 71 mm cavity cross-section the board is carried
# diagonally at 45 deg, giving a ~65 x 65 mm projected envelope.
nuc=(cq.Workplane('XY').box(82.5,22,70,centered=(False,True,True))
     .translate((15,0,49.5))
     .rotate((15,0,49.5),(97.5,0,49.5),45))
parts['NUCLEO_diagonal_45deg']=nuc

# Small front modules occupy the two corner voids around the diagonal Nucleo.
parts['TB6612_envelope']=box(25,-34,14,51,25,19)
parts['DATA_IO_reserve']=box(20,14,60,55,20,18)

# Full-size IBT-2/BTS7960 prototype modules mounted vertically in tandem.
parts['BTS7960_L']=box(105,-21.5,20,50,43,50)
parts['BTS7960_R']=box(160,-21.5,20,50,43,50)

# Input protection/current-sense reserve between drivers and motors.
parts['INPUT_PROTECTION']=box(212,-30,20,22,60,22)

# Current paired Ø32 x 92 rearward traction motors.
parts['MOTOR_L']=cyl_x(237,16.5,45,16,92)
parts['MOTOR_R']=cyl_x(237,-16.5,45,16,92)

# Compact 48->24 half-brick installed envelope above motor fronts, conduction-coupled upward.
parts['DC48_24_halfbrick']=box(220,-32.5,65,70,65,18)

# Four local internal floor bosses for blind ballast threads; 4 mm high in this envelope check.
for i,(x,y) in enumerate([(105,-18),(105,18),(245,-18),(245,18)],1):
    parts[f'BALLAST_BOSS_{i}']=wp(cq.Solid.makeCylinder(6.5,4.0,cq.Vector(x,y,14),cq.Vector(0,0,1)))

checks={}
checks['outside_cavity_mm3']={k:round(outside(v,cavity),6) for k,v in parts.items()}
checks['component_intersections_mm3']={}
keys=list(parts)
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        iv=inter(parts[a],parts[b])
        if iv>1e-5:
            checks['component_intersections_mm3'][f'{a}__{b}']=round(iv,6)

checks['motor_to_halfbrick_vertical_gap_mm']=65.0-(45.0+16.0)
checks['BTS_pair_axial_gap_mm']=160.0-(105.0+50.0)
checks['BTS_to_input_protection_gap_mm']=212.0-(160.0+50.0)
checks['input_protection_to_motor_gap_mm']=237.0-(212.0+22.0)
checks['front_ballast_boss_to_nucleo_axial_gap_mm']=105.0-97.5
checks['rear_ballast_boss_to_motor_lower_vertical_gap_mm']=(45.0-16.0)-(14.0+4.0)

pass_out=all(v<1e-5 for v in checks['outside_cavity_mm3'].values())
pass_inter=len(checks['component_intersections_mm3'])==0
checks['status']='PASS' if pass_out and pass_inter else 'FAIL'
checks['note']='Prototype bounding-envelope check; real connectors, harness bends, heat spreaders and service extraction remain gates.'

assy=cq.Assembly(name='PX1_Internal_Packaging_RevGP')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_Internal_Packaging_RevGP.step'))
with open(os.path.join(OUT,'REV_GP_PACKAGING.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if checks['status']!='PASS': raise SystemExit(2)
