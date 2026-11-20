"""Audit corrected 200x90 lid against the ACTUAL existing 307x78 chassis source.
Pure stdlib. Reads source AST, never silently claims FreeCAD/pressure qualification.
Run: python M1_lid_to_body_integration_gate.py
"""
import ast, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def assignments(path):
    tree=ast.parse(path.read_text(encoding="utf-8"))
    return tree
def get_P(tree):
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in node.targets):
            return {k.arg:ast.literal_eval(k.value) for k in node.value.keywords}
    raise ValueError("No parameter dict P")
base=ROOT/"PX1_Integrated_6x6_M1_interface_repair.py"
lid=ROOT/"M1_lid_layout_repair.py"
body=get_P(assignments(base))
fix=get_P(assignments(lid))
# Existing shell: body_W=78, outer lateral extent +/-39. Corrected lid +/-45.
# A fastener center outside the shell cannot be threaded into its top wall.
bolts=[(x,y) for x in (-94.,94.) for y in (-39.,39.)]
bolts += [(0.,-39.),(0.,39.),(-94.,0.),(94.,0.)]
half_w=body["body_W"]/2
half_l=body["body_L"]/2
hole_r=fix["hole_d"]/2
head_r=fix["bolt_head_d"]/2
edge_margin=3.0  # ESTIMATED: minimum blind-hole wall land, not verified M3 engagement
checks={}
def gate(name,ok,detail):
    checks[name]={"status":"PASS" if ok else "FAIL","detail":detail}
gate("lid_overhang_y",fix["lid_W"]<=body["body_W"],
     f"lid width {fix['lid_W']} mm > shell width {body['body_W']} mm")
gate("lid_overhang_x",fix["lid_L"]<=body["body_L"],
     "lid fits in shell length")
for i,(x,y) in enumerate(bolts,1):
    land_y=half_w-abs(y)-hole_r
    land_x=half_l-abs(x)-hole_r
    gate(f"blind_M3_{i}_shell_land",land_y>=edge_margin and land_x>=edge_margin,
         f"shell edge land x={land_x:.2f} y={land_y:.2f} mm; target >= {edge_margin:.1f} mm")
gate("original_fastener_pattern_reused",False,
     "base source still uses x +/-90 and y +/-35.5; lid repair uses x +/-94 and y +/-39")
gate("original_lid_geometry_reused",False,
     "base FreeCAD still builds 190x78 lid; corrected design is 200x90")
gate("original_gasket_footprint",True,
     "both variants use nominal 176x66 outer / 170x60 inner ring; not pressure-qualified")
gate("DN150_body_cross_section",math.hypot(body["body_W"]/2,body["body_H"]/2)<75,
     "bare rectangular body envelope only, excludes new lid and hardware")
# For lid at z=35.7..39.7, outermost y=45, radial corner > body estimate.
lid_radius=math.hypot(fix["lid_W"]/2,body["body_H"]/2+body["lid_gasket_nominal"]-body["lid_gasket_compression"]+4)
gate("DN150_lid_corner_nominal",lid_radius<=75-2,
     f"lid corner radius {lid_radius:.2f} mm; no allowance for screws/lift")
report={"status":"PASS" if all(v["status"]=="PASS" for v in checks.values()) else "FAIL",
"checks":checks,"design_assumptions":{"blind_hole_edge_land_mm":edge_margin,
"hole_d_mm":fix["hole_d"],"lid_W_mm":fix["lid_W"],"body_W_mm":body["body_W"]},
"not_run":["FreeCAD Boolean","STEP export","lid pressure deformation","thread engagement"],
"physical_check":["gasket compression","M3 preload","0.4-0.7 bar seal test"],
"next_step":"Redesign actual chassis top flange or relocate all 8 holes within a verified continuous land; regenerate FreeCAD solid and repeat gate."}
(ROOT/"M1_lid_to_body_integration_gate.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"status":report["status"],"PASS":sum(x["status"]=="PASS" for x in checks.values()),"FAIL":sum(x["status"]=="FAIL" for x in checks.values())},indent=2))
raise SystemExit(0 if report["status"]=="PASS" else 2)
