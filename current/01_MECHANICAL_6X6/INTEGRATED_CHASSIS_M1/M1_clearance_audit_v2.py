"""M1 integrated interface audit, pure Python 3 (no FreeCAD required).
All dimensions are DESIGN ASSUMPTIONS. Run: python3 M1_clearance_audit_v2.py
Writes M1_clearance_audit_v2.svg and M1_clearance_audit_v2.json.
"""
import json, math, pathlib
P={"body_width":80.0,"body_height":70.0,"body_length":307.0,
   "wheel_diameter":78.0,"wheel_width":18.0,"wheel_inner_y":40.0,
   "wheel_center_z":-5.0,"wheel_stations":[-110.0,0.0,110.0],
   "gear_stations":[-110.0,-55.0,0.0,55.0,110.0],
   "gear_module":1.1,"gear_teeth":50,"gear_y_inner":29.0,
   "gear_y_outer":35.0,"inner_wall_y":35.0,
   "motor_radius":11.0,"motor_center_y":16.0,
   "bearing_outer_y":38.0,"tube_radius":75.0}
tests=[]
def check(name,condition,actual,required,category="geometry"):
    tests.append({"name":name,"status":"PASS" if condition else "FAIL",
                  "actual_mm":round(actual,4),"required":required,"category":category})
wheel_outer=P["wheel_inner_y"]+P["wheel_width"]
r=math.hypot(wheel_outer,abs(P["wheel_center_z"])+P["wheel_diameter"]/2)
check("DN150 wheel conservative radial envelope",r<=75,r,"<=75")
check("wheel station clearance",110-78>0,110-78,">0")
check("spur pitch station",abs(55-1.1*50)<1e-8,55-1.1*50,"=0")
check("motor-to-spur lateral clearance",29-(16+11)>=2,29-(16+11),">=2")
check("wheel-to-body axial clearance",40-40>=1,40-40,">=1 DESIGN TARGET")
check("spur-to-inner-wall axial clearance",35-35>=1,35-35,">=1 DESIGN TARGET")
check("bearing-to-wheel axial clearance",40-38>=2,40-38,">=2")
for name in ("Full 3D Boolean collisions","Real involute teeth and gear backlash",
             "Bevel input contact and shaft coupling","Dynamic shaft sealing at 0.7 bar",
             "STEP export and STEP reopen","Manufacturing bearing fit"):
    tests.append({"name":name,"status":"NOT_RUN","reason":"requires FreeCAD or verified hardware data"})
# A wheel cylinder aligned to Y appears as a rectangle in YZ; bounding corners are conservative.
# This is deliberately a conservative screening check, not a pipe-traversal simulation.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="660" viewBox="0 0 1120 660">',
'<rect width="1120" height="660" fill="#f7f9fc"/>',
'<text x="40" y="48" font-size="25" font-family="sans-serif" fill="#13243a">PX1 M1 — interface audit / design assumptions</text>',
'<text x="40" y="76" font-size="15" font-family="sans-serif">2D geometry derived from current FreeCAD generator; NOT a CAD render</text>',
'<text x="40" y="113" font-size="19" font-family="sans-serif">YZ cross-section / tube Ø150</text>',
'<circle cx="280" cy="340" r="195" fill="none" stroke="#2479ad" stroke-width="4"/>',
'<rect x="176" y="249" width="208" height="182" fill="#bbc5d1" fill-opacity=".5" stroke="#53677e" stroke-width="2"/>',
'<text x="222" y="342" font-size="16" font-family="sans-serif">BODY</text>']
# scale 2.6 px/mm; Y horizontal and Z vertical. Wheels are circular in YZ.
scale=2.6
for side in (-1,1):
    yc=side*(40+9)
    cx=280+yc*scale
    cy=340-(-5)*scale
    svg.append(f'<rect x="{cx-9*scale:.2f}" y="{cy-39*scale:.2f}" width="{18*scale:.2f}" height="{78*scale:.2f}" fill="#2f3a4c" fill-opacity=".2" stroke="#202e42" stroke-width="2"/>')
    svg.append(f'<rect x="{280+side*35*scale-3 if side>0 else 280-35*scale-3:.1f}" y="326" width="6" height="28" fill="#df7d24"/>')
svg+=['<text x="40" y="585" font-size="15" font-family="sans-serif">Wheel Y envelope ±58 mm, Z center −5 mm; conservative radius %.2f mm</text>'%r,
'<text x="620" y="113" font-size="19" font-family="sans-serif">Critical axial interfaces</text>',
'<text x="620" y="151" font-size="16" font-family="sans-serif">Motor → spur: 2 mm (PASS target)</text>',
'<text x="620" y="184" font-size="16" font-family="sans-serif" fill="#b42318">Wheel → body: 0 mm (FAIL target 1 mm)</text>',
'<text x="620" y="217" font-size="16" font-family="sans-serif" fill="#b42318">Spur → inner wall: 0 mm (FAIL target 1 mm)</text>',
'<text x="620" y="250" font-size="16" font-family="sans-serif">Bearing → wheel: 2 mm (PASS target)</text>',
'<text x="620" y="299" font-size="17" font-family="sans-serif">NOT_RUN: 3D booleans, teeth, bevel, seals, STEP</text>',
'<text x="620" y="343" font-size="15" font-family="sans-serif">Suggested next integrated revision:</text>',
'<text x="620" y="372" font-size="15" font-family="sans-serif">Move wheel outward 1–2 mm, then recalc DN150.</text>',
'<text x="620" y="401" font-size="15" font-family="sans-serif">Move gear inward or add wall recess and verify.</text>',
'<text x="620" y="430" font-size="15" font-family="sans-serif">Recheck bearing/axle engagement and pressure seal.</text>',
'<text x="40" y="630" font-size="14" font-family="sans-serif" fill="#5a6777">Source: PX1_Integrated_6x6_M1_interface_repair.py; analytical audit, not manufacturing approval.</text>','</svg>']
root=pathlib.Path(__file__).resolve().parent
(root/"M1_clearance_audit_v2.svg").write_text("\n".join(svg),encoding="utf-8")
(root/"M1_clearance_audit_v2.json").write_text(json.dumps({"assumptions":P,"checks":tests},indent=2),encoding="utf-8")
print(json.dumps({"pass":sum(x["status"]=="PASS" for x in tests),
                  "fail":sum(x["status"]=="FAIL" for x in tests),
                  "not_run":sum(x["status"]=="NOT_RUN" for x in tests),
                  "failed":[x["name"] for x in tests if x["status"]=="FAIL"]},indent=2))
