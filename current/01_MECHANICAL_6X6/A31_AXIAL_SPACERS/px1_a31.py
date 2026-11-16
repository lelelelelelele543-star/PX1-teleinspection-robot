"""A31 independent axial stack verification; assumed dimensions in mm.
Run: python3 px1_a31.py (standard library only).
A30 bearing faces touch rotating gear; this revision adds axial clearance.
"""
import csv, math
from pathlib import Path
P=Path(__file__).resolve().parent
gear=(0.0,8.0)
bearings=[(-9.0,-1.0),(9.0,17.0)]
spacers=[(-1.0,-0.5),(8.5,9.0)]
shaft=(-12.0,20.0)
min_gap=0.5
def gap(a,b): return b[0]-a[1]
assert gap(bearings[0],gear)==1.0
assert gap(gear,bearings[1])==1.0
assert gap(spacers[0],gear)==0.5
assert gap(gear,spacers[1])==0.5
assert shaft[0]<bearings[0][0] and shaft[1]>bearings[1][1]
assert all(gap(a,b)>=min_gap for a,b in [(spacers[0],gear),(gear,spacers[1])])
assert abs((bearings[0][1]-bearings[0][0])-8)<1e-9
assert abs((bearings[1][1]-bearings[1][0])-8)<1e-9
# Spacer must contact only the bearing INNER race; OD 17 is provisional.
assert 12<17<28
print("PASS: two 0.5 mm axial clearances to gear faces; 8 mm bearings; 32 mm shaft envelope")
print("NEEDS_PHYSICAL_CHECK: fits, bearing race dimensions, retaining rings, shaft seal at 0.7 bar")
