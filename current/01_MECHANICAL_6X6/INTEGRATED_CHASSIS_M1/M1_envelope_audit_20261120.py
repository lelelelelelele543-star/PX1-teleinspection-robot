"""PX1 M1 independent envelope audit. Python stdlib; design assumptions, not factory measurements.
Run: python M1_envelope_audit_20261120.py
"""
import math,json
from pathlib import Path
p=Path(__file__).resolve().parent
checks={}
def check(name,actual,minimum):
 checks[name]={"clearance_mm":round(actual,3),"minimum_mm":minimum,"status":"PASS" if actual>=minimum else "FAIL"}
check("DN150 wheel corner",75-math.hypot(60,39),2)
check("DN150 body corner",75-math.hypot(39,35),0)
check("wheel to shell side",46-39,1)
check("Z50 to inner wall",34-33,1)
check("Z50 tip to inner floor (estimated OD52)",30-26,1)
check("motor to roof",30-(18+11),1)
check("motor to motor",28-22,2)
check("motor to spur axial Y",27-(14+11),2)
check("shaft to idler bearing radial",math.hypot(18,14-19)-(4+11),1)
check("motor to left idler X",-30-(-50+11),1)
check("motor to right idler X",(50-11)-(-30+42),1)
check("wheel axle engagement",59-46,12)
check("nominal gasket compression",36-35.7,0.2)
result={"source":"M1 existing generator coordinates; ESTIMATED not Proteus dimensions",
"checks":checks,"pressure_lid_force_N_at_0_7bar":round(.7*.1*170*60,1),
"pressure_note":"Force on 170x60 aperture, NOT a bolt preload or stress qualification",
"not_run":["FreeCAD Boolean 3D collision","bevel and spur kinematics","dynamic shaft seals","key torque","pressure test","motor driver electrical compatibility"],
"physical_check":["0.4-0.7 bar shaft seals","lid gasket preload","bearing fits","wheel retention"]}
(p/"M1_envelope_audit_20261120.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
assert all(v["status"]=="PASS" for v in checks.values())
