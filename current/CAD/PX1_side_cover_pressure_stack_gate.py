#!/usr/bin/env python3
"""Source-driven side-cover pressure/seal/fastener screening. Standard Python 3.
No geometry modification, no pressure qualification, no CAD Boolean claim.
"""
import ast, json, math
from pathlib import Path
root=Path(__file__).parent
src=root/"PX1_Current_Master.py"
tree=ast.parse(src.read_text(encoding="utf-8"))
keys={"SIDE_COVER_L","SIDE_COVER_H","SIDE_COVER_T","SIDE_ORING","SIDE_SEAL_W","SIDE_SEAL_D","COVER_SCREW_DX","COVER_SCREW_DZ","COVER_SCREW_CBORE"}
p={}
for n in tree.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in keys:
                p[t.id]=ast.literal_eval(n.value)
assert keys <= p.keys(), f"Missing master parameters: {keys-p.keys()}"
L,H,T=p["SIDE_COVER_L"],p["SIDE_COVER_H"],p["SIDE_COVER_T"]
cord,section=p["SIDE_ORING"]
depth=p["SIDE_SEAL_D"]
head_r,cb_depth=p["COVER_SCREW_CBORE"]
edge=min(L/2-max(map(abs,p["COVER_SCREW_DX"])),H/2-max(map(abs,p["COVER_SCREW_DZ"])))-head_r
squeeze=(section-depth)/section
remaining=T-cb_depth
area=L*H
force=area*0.07  # N, 0.7 bar = 0.07 N/mm2; rectangular conservative screening area
results={
 "fastener_count_both_sides": {"value":2*len(p["COVER_SCREW_DX"])*len(p["COVER_SCREW_DZ"]),"status":"PASS" if 2*len(p["COVER_SCREW_DX"])*len(p["COVER_SCREW_DZ"])==24 else "FAIL"},
 "head_edge_clearance_mm":{"value":round(edge,3),"status":"PASS" if edge>=0 else "FAIL"},
 "nominal_seal_squeeze_pct":{"value":round(squeeze*100,2),"status":"PASS" if 0.15<=squeeze<=0.30 else "FAIL"},
 "metal_below_counterbore_mm":{"value":round(remaining,3),"status":"PASS" if remaining>0 else "FAIL"},
 "upper_bound_cover_pressure_force_N":{"value":round(force,2),"status":"SCREEN_ONLY"},
 "nominal_force_per_screw_N":{"value":round(force/12,2),"status":"SCREEN_ONLY"}
}
report={"source":"current/CAD/PX1_Current_Master.py","scope":"two side covers; nominal dimensions only","results":results,
"assumptions":[{"name":"0.7 bar differential","status":"DESIGN_TARGET","verification":"controlled pressure qualification"},
{"name":"full cover projected area for load","status":"CONSERVATIVE_SCREEN","verification":"derive actual sealed projected area from 3D lobe track"},
{"name":"seal compression from section minus groove depth","status":"NOMINAL_ONLY","verification":"groove width, ring stretch, tolerances and compression set"}],
"not_run":["3D Boolean","seal-to-screw collision","thread engagement","plate bending","bolt preload","physical pressure test"]}
(root/"PX1_side_cover_pressure_stack_gate.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
raise SystemExit(1 if any(x["status"]=="FAIL" for x in results.values()) else 0)
