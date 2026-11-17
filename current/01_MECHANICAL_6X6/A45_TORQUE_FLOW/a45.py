"""A45: torsion-flow model, not a verified PX1 drivetrain layout."""
from math import pi, sqrt
from pathlib import Path
import csv
T_INPUT=10.0 # N*m, ASSUMED, input from negative X
D_ROOT=11.0 # mm, ASSUMED groove root
KT=2.0 # ASSUMED stress concentration multiplier
STATIONS=[(-18.0,0.20),(-6.0,0.30),(6.0,0.30),(18.0,0.20)]
GROOVES=[-15.0,15.0]
def torque(x):
    return T_INPUT*(1-sum(frac for station,frac in STATIONS if station<=x))
def tau_mpa(x):
    return KT*16*torque(x)*1000/(pi*D_ROOT**3)
assert abs(sum(f for _,f in STATIONS)-1)<1e-12
assert abs(torque(-20)-10)<1e-12
assert abs(torque(-15)-8)<1e-12
assert abs(torque(15)-2)<1e-12
assert abs(torque(20))<1e-12
assert all(torque(x)>=-1e-10 for x in range(-21,22))
assert abs(sum(T_INPUT*f for _,f in STATIONS)-T_INPUT)<1e-12
out=Path(__file__).parent
with (out/'a45_results.csv').open('w',newline='') as fh:
    w=csv.writer(fh);w.writerow(['x_mm','torque_Nm','nominal_shear_MPa','assumed_Kt_shear_MPa'])
    for x in range(-21,22):
        t=torque(x)
        w.writerow([x,round(t,6),round(16*t*1000/(pi*D_ROOT**3),6),round(tau_mpa(x),6)])
print('PASS torque equilibrium; groove torques',*[torque(x) for x in GROOVES])
print('PASS groove Kt shear MPa',*[round(tau_mpa(x),3) for x in GROOVES])
print('NEEDS_PHYSICAL_CHECK torque input location and direction; actual gears and bearings')
print('SKIPPED FreeCAD and physical tests')
