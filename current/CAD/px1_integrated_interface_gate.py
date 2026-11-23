#!/usr/bin/env python3
"""PX1 integrated drivetrain clearance + bearing/pressure interface screen.
Reads current master datums via AST, never executes CadQuery.
Produces SVG and JSON. All proposals are ASSUMED, not CAD modifications.
"""
import ast, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=ast.parse((ROOT/"PX1_Current_Master.py").read_text(encoding="utf-8"))
names={"WHEEL_X","GEAR_X","MOTOR_Y","GEARHEAD_OD","GEARHEAD_LEN","MOTOR_FACE","MIDDLE_INNER_Y","MIDDLE_BUSH_W","WHEEL_CENTRE_Y","BODY_HALF_W_SCREEN","PIPE_R","WHEEL_CROWN_R","WHEEL_Z","PIPE_CENTER_Z"}
values={}
for n in src.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in names:
                try: values[t.id]=ast.literal_eval(n.value)
                except (TypeError,ValueError): pass
# Derived values are explicitly evaluated from the same primitive datums.
assert names-{"PIPE_CENTER_Z"} <= values.keys(), sorted(names-values.keys())
v=values
r=v["GEARHEAD_OD"]/2
motor_y=v["MOTOR_Y"]; shaft_y=v["MIDDLE_INNER_Y"]; bush=v["MIDDLE_BUSH_W"]
target=1.0 # ASSUMED nominal manufacturing clearance target, not tolerance-stack result
pair_gap=2*(motor_y-r)
shaft_gap=shaft_y-(motor_y+r)
proposed_y=motor_y+r+target
# A shortened shaft is not released: bush position, bearing seat and retention must be checked.
# Shaft trimming cannot be accepted without knowing which span MIDDLE_BUSH_W occupies.
x0=v["MOTOR_FACE"]-v["GEARHEAD_LEN"]; x1=v["MOTOR_FACE"]
assert x0<150<x1 and len(v["WHEEL_X"])==3 and len(v["GEAR_X"])==5
# Pressure force is p*A; do not treat radial shaft seals as pressure-rated without supplier evidence.
p=70000.0
cover_area=0.262*0.060 # nominal rectangular bounding area; actual lobed area unknown
cover_force_upper=p*cover_area
status={"datum_topology":"PASS","motor_pair_nominal":"PASS" if pair_gap>0 else "FAIL",
"motor_shaft_nominal":"PASS" if shaft_gap>0 else "FAIL",
"target_1mm":"PASS" if min(pair_gap,shaft_gap)>=target else "FAIL",
"shaft_shortening_support":"NOT_RUN","exact_3d_interference":"NOT_RUN",
"pressure_seal_rating":"PHYSICAL_CHECK","cover_pressure_load":"ESTIMATED"}
result={"source":"current/CAD/PX1_Current_Master.py","units":"mm","status":status,
"dimensions":{"motor_x":[x0,x1],"motor_center_y_abs":motor_y,"gearhead_radius":r,
"middle_shaft_inner_y_abs":shaft_y,"middle_bush_width":bush,
"motor_pair_gap":pair_gap,"shaft_gap":shaft_gap,"assumed_min_gap":target,
"proposed_middle_shaft_inner_y_abs":proposed_y,
"proposed_shaft_end_retraction":proposed_y-shaft_y,
"cover_bounding_pressure_force_N_at_0p7bar":cover_force_upper},
"assumptions":[{"name":"minimum_nominal_gap","value_mm":target,"basis":"design target, no tolerance stack","verification":"3D BRep and tolerances"},
{"name":"shaft_retraction","value_mm":proposed_y-shaft_y,"basis":"geometric clearance only","verification":"bearing seats, bush, circlip, key and sealing stack"},
{"name":"cover_area","value_m2":cover_area,"basis":"262x60 bounding rectangle, not actual loaded contour","verification":"CAD projected pressure area"}],
"next":"Inspect actual BRep shaft and motor solids; resolve bearing/bush and shaft seal stack before changing master."}
out=ROOT/"previews";out.mkdir(exist_ok=True)
(out/"px1_integrated_interface_gate.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
# Scale-preserving top view: X horizontal, Y vertical, motor rectangles, center shaft lines.
def X(x):return 90+x*2.0
def Y(y):return 230-y*3.5
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="560" viewBox="0 0 920 560">',
'<rect width="920" height="560" fill="#fff"/>',
'<text x="35" y="32" font-family="sans-serif" font-size="21">PX1 | integrated drivetrain interface (XY plan)</text>',
'<text x="35" y="55" font-family="sans-serif" font-size="13">Master-derived datums; simplified envelopes, NOT BRep or OEM dimensions</text>']
for xx in v["WHEEL_X"]:
    svg.append(f'<line x1="{X(xx)}" y1="90" x2="{X(xx)}" y2="375" stroke="#aaa" stroke-dasharray="5 5"/>')
    svg.append(f'<text x="{X(xx)-15}" y="400" font-size="13">X{xx:g}</text>')
svg.append(f'<rect x="{X(18)}" y="{Y(34)}" width="{(278)*2}" height="{68*3.5}" fill="#edf2f7" stroke="#64748b" stroke-width="2"/>')
for side in (-1,1):
    yy=side*motor_y
    svg.append(f'<rect x="{X(x0)}" y="{Y(yy+r)}" width="{(x1-x0)*2}" height="{2*r*3.5}" fill="#93c5fd" stroke="#1d4ed8" stroke-width="2"/>')
    svg.append(f'<line x1="{X(150)}" y1="{Y(side*shaft_y)}" x2="{X(150)}" y2="{Y(side*61)}" stroke="#dc2626" stroke-width="9"/>')
    svg.append(f'<line x1="{X(150)+10}" y1="{Y(side*proposed_y)}" x2="{X(150)+10}" y2="{Y(side*61)}" stroke="#16a34a" stroke-width="3" stroke-dasharray="6 4"/>')
svg += [f'<text x="35" y="436" font-size="15">Motor pair nominal gap: {pair_gap:.2f} mm | motor-to-middle-shaft: {shaft_gap:.2f} mm</text>',
f'<text x="35" y="460" font-size="15">ASSUMED 1.0 mm target FAIL; proposed shaft inner end |Y|={proposed_y:.1f} mm (NOT implemented)</text>',
f'<text x="35" y="484" font-size="15">0.7 bar x 262x60 mm bounding area = {cover_force_upper:.0f} N (screen only)</text>',
'<text x="35" y="510" font-size="14">Blue: motor envelope | Red: current shaft | Green dashed: proposed retraction</text>',
'<text x="35" y="535" font-size="13">NOT_RUN: BRep, bearings, sealing, tolerances. PHYSICAL_CHECK: pressure-rated dynamic seals.</text>',
'</svg>']
(out/"px1_integrated_interface_gate.svg").write_text("\n".join(svg),encoding="utf-8")
print(json.dumps(status,ensure_ascii=False))
