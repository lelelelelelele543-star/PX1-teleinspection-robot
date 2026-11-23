#!/usr/bin/env python3
"""Source-derived subsystem uncertainty audit. Standard library only; no geometry validation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/"previews/render_manifest.json").read_text(encoding="utf-8"))
names=next(v["shown_components"] for v in m["views"] if v["file"].endswith("px1_isometric.png"))
groups=[
("pressure_shell_closures",("PRESSURE_BODY","SIDE_COVER","SIDE_ORING","ELECTRONICS_COVER","SERVICE_COVER")),
("shaft_seals_flanges",("XRING","FLANGE_ORING","AXLE_FLANGE","WHEEL_SHAFT","SHAFT_SEAL")),
("motor_bevel_input",("TRACTION_MOTOR","MOTOR_","Z16","Z40","COUPLING","PINION_BEARING")),
("gear_train_supports",("Z50","IDLE_PIN","IDLE_BUSH","61801_SIDE","MIDDLE_BUSH")),
("camera_lift_fittings",("CAMERA","LIFT","VALVE","FITTING","SKINTOP"))]
out={k:{"total":0,"uncertain":0,"examples":[]} for k,_ in groups}
out["other"]={"total":0,"uncertain":0,"examples":[]}
for n in names:
    key=next((key for key,tokens in groups if any(t in n for t in tokens)),"other")
    x=out[key];x["total"]+=1
    if "HOLD" in n or "ESTIMATED" in n:
        x["uncertain"]+=1
        if len(x["examples"])<8:x["examples"].append(n)
assert sum(x["total"] for x in out.values())==len(names)
assert m["manufacturing_release"] is False
report={"source_sha256":m["source_sha256"],"components":len(names),"subsystems":out,
"checks":{"manifest_partition":"PASS","geometric_intersections":"NOT_RUN","shaft_seal_pressure":"PHYSICAL_CHECK","motor_package":"PHYSICAL_CHECK"},
"next_step":"Resolve actual pressure boundary and shaft seal design in the single master, then CAD Boolean and physical pressure checks."}
p=ROOT/"previews/PX1_subsystem_uncertainty.json"
p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
