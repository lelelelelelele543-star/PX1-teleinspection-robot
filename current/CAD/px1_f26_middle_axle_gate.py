#!/usr/bin/env python3
"""F26 regression gate. Reads the active master without importing CadQuery."""
import ast, json
from pathlib import Path
p=Path(__file__).with_name("PX1_Current_Master.py")
tree=ast.parse(p.read_text(encoding="utf-8"))
names={"MIDDLE_INNER_Y","MIDDLE_BUSH_W","MOTOR_Y","GEARHEAD_OD","MOTOR_FACE","GEARHEAD_LEN"}
v={}
for n in tree.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in names:
                v[t.id]=ast.literal_eval(n.value)
assert names<=v.keys()
gap=v["MIDDLE_INNER_Y"]-(v["MOTOR_Y"]+v["GEARHEAD_OD"]/2)
sleeve_end=v["MIDDLE_INNER_Y"]+v["MIDDLE_BUSH_W"]
motor_x0=v["MOTOR_FACE"]-v["GEARHEAD_LEN"]
status={"nominal_middle_clearance":"PASS" if gap>=0.999 else "FAIL",
        "sleeve_follows_shaft":"PASS" if sleeve_end>v["MIDDLE_INNER_Y"] else "FAIL",
        "actual_brep":"NOT_RUN","shaft_seal_pressure":"PHYSICAL_CHECK"}
result={"source":str(p.name),"assumption":"nominal clearance target 1.0mm; no tolerance stack",
        "gap_mm":gap,"sleeve_y_range_mm":[v["MIDDLE_INNER_Y"],sleeve_end],
        "gearhead_x_range_mm":[motor_x0,v["MOTOR_FACE"]],"status":status}
print(json.dumps(result,indent=2))
assert status["nominal_middle_clearance"]=="PASS"
