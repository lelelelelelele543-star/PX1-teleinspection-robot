"""PX1 M1: independently runnable integration audit, Python 3 standard library.
Reads current FreeCAD generator as source of truth; creates SVG preview and JSON report.
FAIL is intentional for any uncut idler-stub/shell overlap. No STEP or CAD claim.
"""
from pathlib import Path
import ast, json, math
HERE=Path(__file__).resolve().parent
SOURCE=HERE/"PX1_Integrated_6x6_M1_interface_repair.py"
tree=ast.parse(SOURCE.read_text(encoding="utf-8"))
params=None
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in node.targets):
        params={kw.arg:ast.literal_eval(kw.value) for kw in node.value.keywords}
        break
if params is None: raise RuntimeError("Missing P dict in existing generator")
W=params["body_W"]; wall=params["wall"]; inner=W/2-wall; outer=W/2
idler_start=25.; idler_length=13.; idler_radius=5.
# Idler stub cylinders occupy lateral 25..38, penetrating solid sidewall 34..39.
overlap=max(0.,min(outer,idler_start+idler_length)-max(inner,idler_start))
# Existing generator cuts shell only for wheel stations, not idlers at x +/-50.
wheel_x=set(params["stations"]); idler_x=set(params["gear_x"])-wheel_x
checks={
 "wheel_count":{"status":"PASS" if len(wheel_x)*2==6 else "FAIL","value":len(wheel_x)*2},
 "gear_station_count":{"status":"PASS" if len(params["gear_x"])*2==10 else "FAIL","value":len(params["gear_x"])*2},
 "idler_stub_shell_intersection":{"status":"FAIL" if overlap>0 else "PASS","overlap_mm":overlap,"idler_positions_mm":sorted(idler_x),"affected_stubs":2*len(idler_x)},
 "idler_bearing_and_seat":{"status":"FAIL","reason":"No bearing, counterbore or housing is created for four idler stubs"},
 "actual_freecad_boolean":{"status":"NOT_RUN"},
 "step_reopen":{"status":"NOT_RUN"},
 "seal_pressure_0p7bar":{"status":"PHYSICAL_CHECK"}
}
# Top view diagram in millimeters, deliberately showing only calculated interfaces.
scale=2.5
sx=lambda x: 460+x*scale
sy=lambda y: 210-y*scale
lines=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="450" viewBox="0 0 920 450">',
'<rect width="920" height="450" fill="#f8fafc"/>',
'<text x="30" y="36" font-family="sans-serif" font-size="21">PX1 M1 — IDLER / SHELL INTERFACE (2D PARAMETRIC)</text>',
'<text x="30" y="60" font-family="sans-serif" font-size="13">DESIGN ASSUMPTIONS; NOT CAD RENDER; units mm. Four idler stub penetrations uncut.</text>']
lines.append(f'<rect x="{sx(-params["body_L"]/2)}" y="{sy(outer)}" width="{params["body_L"]*scale}" height="{W*scale}" fill="#dbe4ee" stroke="#334155" stroke-width="2"/>')
for x in params["gear_x"]:
    for side in (-1,1):
        y=side*30
        color="#dc2626" if x in idler_x else "#15803d"
        lines.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="10" fill="{color}" opacity=".85"/>')
        if x in idler_x:
            lines.append(f'<circle cx="{sx(x)}" cy="{sy(side*36)}" r="6" fill="none" stroke="#dc2626" stroke-width="2"/>')
lines.extend(['<text x="30" y="395" font-family="sans-serif" font-size="15" fill="#b91c1c">FAIL: 4 idler stubs overlap uncut shell by 4 mm laterally (Y=34..38).</text>',
'<text x="30" y="421" font-family="sans-serif" font-size="14">Next: idler bearing seats + wall bores + independent gear support; then 3D Boolean check.</text>','</svg>'])
svg=HERE/"M1_idler_wall_integration_audit.svg"
svg.write_text("\n".join(lines),encoding="utf-8")
report=HERE/"M1_idler_wall_integration_audit.json"
report.write_text(json.dumps({"source":SOURCE.name,"checks":checks,"note":"Analytical check only; do not manufacture"},indent=2),encoding="utf-8")
print(json.dumps(checks,indent=2))
assert overlap==4., "Unexpected source geometry; review assumptions"
