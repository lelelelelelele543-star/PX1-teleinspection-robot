"""A44: statically determinate X150 beam, hypothetical gear loads; not production data."""
import math, csv
from pathlib import Path
P=Path(__file__).parent
MODULE=1.5; TEETH=50; TORQUE_NM=10.; PRESSURE_ANGLE_DEG=20.
SUPPORTS=(-12.,12.)
# Design targets, not measured PX1 geometry. Total torque fractions sum to one.
STATIONS=[(-18.,.2),(-6.,.3),(6.,.3),(18.,.2)]
GROOVES=(-15.,15.)
assert abs(sum(f for _,f in STATIONS)-1)<1e-12
pitch_d=MODULE*TEETH
loads=[(x,2000*TORQUE_NM*f/pitch_d) for x,f in STATIONS]
def reactions(loads):
    a,b=SUPPORTS
    rb=sum(F*(x-a) for x,F in loads)/(b-a)
    return sum(F for _,F in loads)-rb,rb
def moment(x,loads):
    ra,rb=reactions(loads)
    a,b=SUPPORTS
    return (ra*max(0.,x-a)+rb*max(0.,x-b)-sum(F*max(0.,x-xf) for xf,F in loads))/1000
def shear(x,loads):
    ra,rb=reactions(loads);a,b=SUPPORTS
    return (ra if x>=a else 0)+(rb if x>=b else 0)-sum(F for xf,F in loads if x>=xf)
ra,rb=reactions(loads)
assert abs(ra+rb-sum(F for _,F in loads))<1e-9
assert abs(ra*SUPPORTS[0]+rb*SUPPORTS[1]-sum(x*F for x,F in loads))<1e-9
assert abs(moment(-21,loads))<1e-9 and abs(moment(21,loads))<1e-9
assert abs(ra-rb)<1e-9
# Independent superposition: moment of sum = sum of single-load moments.
for x in range(-21,22):
    assert abs(moment(x,loads)-sum(moment(x,[one]) for one in loads))<1e-10
# The radial tooth force is orthogonal; model it in a second plane.
radial=[(x,F*math.tan(math.radians(PRESSURE_ANGLE_DEG))) for x,F in loads]
def bending_resultant(x):
    return math.hypot(moment(x,loads),moment(x,radial))
def vm_at_groove(x,diameter=11.,kb=2.,kt=2.):
    M=bending_resultant(x)
    sigma=kb*32*M*1000/(math.pi*diameter**3)
    tau=kt*16*TORQUE_NM*1000/(math.pi*diameter**3)
    return math.hypot(sigma,math.sqrt(3)*tau)
with (P/'a44_results.csv').open('w',newline='') as fp:
    w=csv.writer(fp);w.writerow(['x_mm','M_tangential_Nm','M_radial_Nm','M_resultant_Nm','shear_tangential_N'])
    for x in range(-21,22):
        w.writerow([x,round(moment(x,loads),6),round(moment(x,radial),6),round(bending_resultant(x),6),round(shear(x,loads),6)])
print('PASS reactions N:',ra,rb,'groove moments Nm:',*[round(bending_resultant(x),6) for x in GROOVES])
print('PASS groove VM MPa:',*[round(vm_at_groove(x),4) for x in GROOVES])
print('SKIPPED FreeCAD; NEEDS_PHYSICAL_CHECK actual gear coordinates, force directions, torque, fatigue')
