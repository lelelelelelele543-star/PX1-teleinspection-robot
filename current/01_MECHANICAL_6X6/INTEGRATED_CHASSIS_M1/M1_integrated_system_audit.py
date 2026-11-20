"""PX1 M1 integrated consistency audit. Pure Python 3, no FreeCAD required.
Design assumptions, NOT factory measurements or manufacturing release.
Usage: python3 M1_integrated_system_audit.py
Writes SVG + JSON alongside this file. Explicit FAIL is intentional.
"""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parent
P=dict(body_L=307,body_W=78,body_H=70,wall=5,wheel_D=78,wheel_W=18,
       wheel_stations=(-110,0,110),gear_stations=(-110,-55,0,55,110),
       gear_pitch_D=55,gear_center_Y=30,gear_thick=6,gear_center_Z=0,
       wheel_inner_Y=43,bearing_start_Y=34,bearing_width=7,
       motor_D=22,motor_center_Y=14,motor_start_X=35,motor_L=42,
       bevel_Z40_R=30,bevel_Z40_X=110,bevel_Z40_inner_Y=19,
       bevel_Z40_width=8,spur_rear_X=110,spur_rear_inner_Y=27,
       spur_rear_width=6,pressure_target_bar=(0.4,0.7))
checks=[]
def check(name,actual,limit,mode="min",note=""):
    passed=(actual>=limit if mode=="min" else actual<=limit)
    checks.append(dict(name=name,status="PASS" if passed else "FAIL",
                       actual_mm=round(actual,3),limit_mm=limit,note=note))
    return passed
wheel_radial=math.hypot(P["wheel_inner_Y"]+P["wheel_W"],P["wheel_D"]/2)
check("DN150 wheel bounding envelope",wheel_radial,75,"max",
      "Conservative rectangular rim envelope; not a rolling clearance test")
check("body outer shell vs wheel",P["wheel_inner_Y"]-P["body_W"]/2,1)
check("bearing vs wheel axial",P["wheel_inner_Y"]-(P["bearing_start_Y"]+P["bearing_width"]),2)
check("spur vs inner side wall",P["body_W"]/2-P["wall"]-(P["gear_center_Y"]+P["gear_thick"]/2),1)
check("motor vs spur lateral",P["gear_center_Y"]-P["gear_thick"]/2-(P["motor_center_Y"]+P["motor_D"]/2),2)
check("motor pair center gap",2*P["motor_center_Y"]-P["motor_D"],2)
check("motor rear vs bevel X proxy",80-(P["motor_start_X"]+P["motor_L"]),3)
# IMPORTANT: axial contact of nominal pitch cylinders does NOT prove tooth mesh.
# The Z40 is a bevel proxy with axis Y and the rear Z50 is a spur proxy also axis Y.
# They cannot form a bevel mesh simply by touching at an axial face.
axial_gap=P["spur_rear_inner_Y"]-(P["bevel_Z40_inner_Y"]+P["bevel_Z40_width"])
check("Z40 to Z50 proxy axial non-overlap",axial_gap,0)
# The gear centers coincide at X110, Z0: their pitch cylinders share a common axis.
# This is not a viable torque-transfer mesh for two independent gears.
same_axis=(P["bevel_Z40_X"]==P["spur_rear_X"])
checks.append(dict(name="Z40-to-Z50 distinct-axis mesh",status="FAIL" if same_axis else "NOT_RUN",
                   note="Z40 and rear Z50 are coaxial proxy solids. Need defined common-shaft coupling or distinct-axis gear geometry; no validated bevel mesh."))
checks.append(dict(name="Pressure seal 0.4-0.7 bar",status="PHYSICAL_CHECK",
                   note="No pressure-rated shaft seal or groove validation in M1"))
checks.append(dict(name="FreeCAD STEP reopen + Boolean collisions",status="NOT_RUN",
                   note="Requires FreeCAD environment and geometry-aware intended-contact exclusions"))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="620" viewBox="0 0 1100 620">',
'<rect width="1100" height="620" fill="#101a2a"/>',
'<text x="40" y="45" fill="#fff" font-size="25" font-family="sans-serif">PX1 M1 | integrated chassis audit | ASSUMED mm</text>',
'<text x="40" y="75" fill="#aabbd1" font-size="16" font-family="sans-serif">Top XY projection; pitch disks are NOT actual involute teeth. Not FreeCAD render.</text>']
# top projection: x axis along chassis, y lateral. scale=2.2 px/mm
s=2.2; X=lambda x:410+s*x; Y=lambda y:295-s*y
svg.append(f'<rect x="{X(-153.5):.1f}" y="{Y(39):.1f}" width="{307*s:.1f}" height="{78*s:.1f}" fill="#35475c" stroke="#8fa2b7" stroke-width="2"/>')
for side in (-1,1):
    for x in P["wheel_stations"]:
        yi=side*43; yo=side*61
        svg.append(f'<rect x="{X(x-39):.1f}" y="{min(Y(yi),Y(yo)):.1f}" width="{78*s:.1f}" height="{18*s:.1f}" fill="#263a45" stroke="#64c6cb" stroke-width="2"/>')
    for x in P["gear_stations"]:
        yy=side*30
        svg.append(f'<circle cx="{X(x):.1f}" cy="{Y(yy):.1f}" r="{27.5*s:.1f}" fill="#d58a27" fill-opacity=".13" stroke="#e6a84b" stroke-dasharray="5 5"/>')
    svg.append(f'<rect x="{X(35):.1f}" y="{Y(side*14)-11*s:.1f}" width="{42*s:.1f}" height="{22*s:.1f}" fill="#46b69a" fill-opacity=".65" stroke="#7ee4cb"/>')
    svg.append(f'<circle cx="{X(110):.1f}" cy="{Y(side*23):.1f}" r="{30*s:.1f}" fill="none" stroke="#f76b71" stroke-width="3"/>')
svg.extend(['<text x="45" y="520" fill="#e6a84b" font-size="17" font-family="sans-serif">Orange dashed: Z50 pitch envelopes (10)</text>',
'<text x="45" y="547" fill="#7ee4cb" font-size="17" font-family="sans-serif">Green: two assumed motor envelopes</text>',
'<text x="45" y="574" fill="#f76b71" font-size="17" font-family="sans-serif">Red: Z40 rear proxy; coaxial interface NOT verified</text>',
'<text x="620" y="520" fill="#e7edf6" font-size="17" font-family="sans-serif">6 wheels | 2 motors | 10 Z50 | 2 Z40</text>',
'<text x="620" y="550" fill="#f76b71" font-size="17" font-family="sans-serif">FAIL: no defined Z40 to Z50 torque coupling</text>',
'</svg>'])
(ROOT/"M1_integrated_system_audit.svg").write_text("\n".join(svg),encoding="utf-8")
result=dict(assumptions=P,checks=checks,summary={s:sum(c["status"]==s for c in checks) for s in ("PASS","FAIL","NOT_RUN","PHYSICAL_CHECK")})
(ROOT/"M1_integrated_system_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
for c in checks: print(c["status"],c["name"],c.get("actual_mm",""),c.get("note",""))
print("SUMMARY",result["summary"])
