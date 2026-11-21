#!/usr/bin/env python3
"""Integrated source-driven side-cover interface screen. No FreeCAD Boolean claim."""
import ast, json, math
from pathlib import Path
master=Path(__file__).with_name("PX1_Current_Master.py")
tree=ast.parse(master.read_text(encoding="utf-8"))
p={}
for node in tree.body:
    if isinstance(node,ast.Assign):
        for t in node.targets:
            if isinstance(t,ast.Name):
                try:p[t.id]=ast.literal_eval(node.value)
                except (ValueError,TypeError,KeyError):pass
required=("WHEEL_X","GEAR_X","WHEEL_Z","SIDE_COVER_L","SIDE_COVER_H","COVER_SCREW_DX","COVER_SCREW_DZ","COVER_SCREW_CBORE","SIDE_SEAL_R","SIDE_SEAL_W","SIDE_SEAL_D","SIDE_ORING","Z50_OD")
assert all(k in p for k in required), "Missing master parameters: "+str([k for k in required if k not in p])
L,H=p["SIDE_COVER_L"],p["SIDE_COVER_H"]
sx,sz=p["COVER_SCREW_DX"],p["COVER_SCREW_DZ"]
head=p["COVER_SCREW_CBORE"][0]
screws=[(150+x,p["WHEEL_Z"]+z) for x in sx for z in sz]
edge=min(L/2-max(map(abs,sx)),H/2-max(map(abs,sz)))-head
lobe=min(math.hypot(x-g,p["WHEEL_Z"]-z)-p["SIDE_SEAL_R"]-p["SIDE_SEAL_W"]/2-head for x,z in screws for g in p["GEAR_X"])
gear_overlap=p["Z50_OD"]-min(b-a for a,b in zip(p["GEAR_X"],p["GEAR_X"][1:]))
results={"screws_both_covers":{"value":2*len(screws),"status":"PASS" if len(screws)==12 else "FAIL"},
"head_edge_mm":{"value":round(edge,3),"status":"PASS" if edge>0 else "FAIL"},
"head_to_circular_seal_lobe_mm":{"value":round(lobe,3),"status":"SCREEN_ONLY" if lobe>=0 else "FAIL"},
"Z50_outer_overlap_mm":{"value":round(gear_overlap,3),"status":"INTENTIONAL_MESH_NOT_BOOLEAN_PASS"},
"seal_squeeze_pct":{"value":round(100*(p["SIDE_ORING"][1]-p["SIDE_SEAL_D"])/p["SIDE_ORING"][1],2),"status":"SCREEN_ONLY"},
"cover_pressure_force_N_at_0p7bar":{"value":round(L*H*.07,2),"status":"SCREEN_ONLY"}}
report={"source":"PX1_Current_Master.py","results":results,"assumptions":["Seal lobes approximated as circles; connecting seal spline not tested","Full cover rectangle used for conservative pressure screen"],"not_run":["FreeCAD Boolean","actual seal groove-to-screw intersection","shaft seal pressure qualification","STEP"]}
Path(__file__).with_suffix(".json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
raise SystemExit(int(any(v["status"]=="FAIL" for v in results.values())))
