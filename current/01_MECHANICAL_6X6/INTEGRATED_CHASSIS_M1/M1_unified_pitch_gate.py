#!/usr/bin/env python3
"""PX1 M1 unified X-stations: executable standard-library geometry gate.
DESIGN ASSUMPTION: preserve existing CAD centres (-110,-55,0,55,110).
Not a FreeCAD Boolean or tooth-contact test.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CAD_X=(-110,-55,0,55,110)
WHEEL_X=(-110,0,110)
GEAR_Z=50
MODULE=1.5
PITCH=GEAR_Z*MODULE
def verify():
    checks=[]
    def add(name,passed,detail):
        checks.append(dict(name=name,status="PASS" if passed else "FAIL",detail=detail))
    add("five stations per side",len(CAD_X)==5,str(CAD_X))
    add("six wheels at alternate stations",len(WHEEL_X)==3 and all(x in CAD_X for x in WHEEL_X),str(WHEEL_X))
    add("equal station pitch",len(set(b-a for a,b in zip(CAD_X,CAD_X[1:])))==1,"55 mm")
    add("spur Z50 pitch contact",all(abs(b-a-PITCH)<1e-6 for a,b in zip(CAD_X,CAD_X[1:])),
        "For m=1.5, Z50+Z50 centre distance = 75 mm; CAD station spacing = 55 mm")
    add("radial overlap check",all((b-a)>=PITCH for a,b in zip(CAD_X,CAD_X[1:])),
        "55 mm spacing vs 75 mm pitch distance: severe interference for m1.5 Z50")
    checks.append(dict(name="actual gear contact / CAD collision",status="NOT_RUN",detail="FreeCAD solid gear analysis required"))
    checks.append(dict(name="seals 0.4-0.7 bar",status="PHYSICAL_CHECK",detail="dynamic pressure rating unverified"))
    return dict(design_assumptions=dict(stations_mm=CAD_X,wheel_stations_mm=WHEEL_X,module=MODULE,teeth=GEAR_Z),
                checks=checks,next_action="Resolve Z50 module/tooth count or station pitch and package constraints together, before editing CAD")
if __name__=="__main__":
    report=verify()
    (ROOT/"M1_unified_pitch_gate.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
