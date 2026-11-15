#!/usr/bin/env python3
"""PX1 A13: analytical shifted spur pair, design-only. Python 3 standard library."""
import math, csv, pathlib
M=1.5; ALPHA=math.radians(20); Z1=16; Z2=40; X1=.20; X2=-.20
def gear(z,x):
    r=M*z/2; rb=r*math.cos(ALPHA)
    ra=M*(z/2+1+x); rf=M*(z/2-1.25+x)
    thickness=M*(math.pi/2+2*x*math.tan(ALPHA))
    return dict(z=z,x=x,r=r,rb=rb,ra=ra,rf=rf,s=thickness)
g1,g2=gear(Z1,X1),gear(Z2,X2)
a=M*(Z1+Z2)/2
base_pitch=math.pi*M*math.cos(ALPHA)
path=math.sqrt(g1["ra"]**2-g1["rb"]**2)+math.sqrt(g2["ra"]**2-g2["rb"]**2)-a*math.sin(ALPHA)
epsilon=path/base_pitch
clearance1=a-g1["ra"]-g2["rf"]
clearance2=a-g2["ra"]-g1["rf"]
# Theoretical rack undercut screen, not a proof of generated tooth-root geometry.
xmin=1-Z1*math.sin(ALPHA)**2/2
assert X1>xmin
assert abs(X1+X2)<1e-12
assert min(clearance1,clearance2)>.3
assert epsilon>1.2
assert abs(a-42)<1e-10
print(f"PASS: a={a:.3f} mm, epsilon={epsilon:.5f}, root clearances={clearance1:.3f}/{clearance2:.3f} mm")
print(f"PASS: Z16 shift={X1:+.2f} > undercut-screen minimum {xmin:.5f}")
print("SKIPPED: conjugate mesh simulation, trochoidal fillets, backlash, strength, FreeCAD")
print("NEEDS_PHYSICAL_CHECK: pressure, shaft fit, cutting process and actual gear quality")
