"""PX1 integrated chassis audit: pure Python, no FreeCAD required.
Design assumptions read from current integrated CAD generator, not factory dimensions.
Produces SVG and JSON, runs with python3 M1_full_chassis_interface_audit.py.
"""
import ast, json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
CAD=ROOT/"PX1_Integrated_6x6_M1_interface_repair.py"
tree=ast.parse(CAD.read_text(encoding="utf-8"))
pnode=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
P={k.value:ast.literal_eval(v) for k,v in zip(pnode.keys,pnode.values)}
checks={}
def gate(name,condition,details):
    checks[name]={"status":"PASS" if condition else "FAIL","details":details}
x=P["gear_x"]; ws=P["stations"]; module=P["gear_m"]
gate("six_wheels",len(ws)==3 and ws==(x[0],x[2],x[4]),"3 stations x 2 sides")
gate("ten_gears",len(x)==5 and all(abs(x[i+1]-x[i]-50*module)<1e-9 for i in range(4)),"5 Z50 per side; m=1 design assumption")
wheel_y=46+P["wheel_W"]; wheel_r=P["wheel_D"]/2
radial=math.hypot(wheel_y,wheel_r)
gate("dn150_conservative",radial<=73,{"bounding_radius_mm":round(radial,3),"clearance_mm":round(75-radial,3)})
gate("bearing_seal_wheel_stack",46-(34+7)>=4+1,"bearing end Y41; seal Y41..45; wheel starts Y46")
gate("motor_pair",2*P["motor_y"]-P["motor_D"]>=2,"motor bodies clear across Y")
gate("motor_spur",P["gear_y"]-P["gear_thick"]/2-(P["motor_y"]+P["motor_D"]/2)>=2,"motor bodies clear spur pitch proxy in Y")
# Critical integration gap: lid opening top of shell at Z35, lid starts Z36.
# A gasket proxy occupies Z35..36, but it is not a pressure-qualified seal.
lid_pressure_N=0.7*0.1*(170*60) # 1 bar = 0.1 N/mm2
gate("lid_pressure_load_calculated",abs(lid_pressure_N-714)<1e-9,{"max_lid_load_N":lid_pressure_N,"status":"design load only; fasteners unverified"})
# Top cover is only an envelope: four-side pressure fasteners, gasket compression and grooves absent.
checks["lid_retention"]={"status":"PHYSICAL_CHECK","details":"714 N at 0.7 bar over 170x60 mm; fastener pattern, gasket compression, stiffness not defined"}
checks["shaft_pressure_seals"]={"status":"PHYSICAL_CHECK","details":"6 annular proxies, no verified dynamic pressure rating at 0.7 bar"}
checks["true_gear_teeth"]={"status":"NOT_RUN","details":"10 pitch-cylinder proxies in FreeCAD source; involute solid integration outstanding"}
checks["step_reopen"]={"status":"NOT_RUN","details":"FreeCADCmd and generated STEP required"}
checks["motor_bevel_contact"]={"status":"NOT_RUN","details":"Z16/Z40 are cylindrical proxies, not validated tooth contact"}
# Honest vector drawing: top view is schematic, not a 3D projection.
S=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="0 0 1100 650">',
'<rect width="1100" height="650" fill="#f7f9fb"/>',
'<text x="40" y="45" font-family="sans-serif" font-size="25" font-weight="bold">PX1 M1 — integrated 6x6 chassis interface (2D, ASSUMED)</text>',
'<text x="40" y="74" font-family="sans-serif" font-size="15">Plan view: wheels, body, Z50 pitch circles, motors, seal/bearing stack. NOT a CAD render.</text>']
sx=lambda a: 540+a*2.5
sy=lambda a: 290+a*2.5
S.append(f'<rect x="{sx(-153.5):.1f}" y="{sy(-39):.1f}" width="{307*2.5:.1f}" height="{78*2.5:.1f}" rx="12" fill="#e0e7ee" stroke="#475569" stroke-width="3"/>')
for side in (-1,1):
    for i,gx in enumerate(x):
        S.append(f'<circle cx="{sx(gx):.1f}" cy="{sy(side*30):.1f}" r="62.5" fill="none" stroke="#bd7b35" stroke-dasharray="5 4" stroke-width="2"/>')
        if i%2==0:
            S.append(f'<rect x="{sx(gx)-39:.1f}" y="{sy(side*53)-17.5:.1f}" width="78" height="35" rx="8" fill="#283c53" opacity=".88"/>')
            S.append(f'<circle cx="{sx(gx):.1f}" cy="{sy(side*41):.1f}" r="9" fill="#26a69a" stroke="#0f766e"/>')
    S.append(f'<rect x="{sx(35):.1f}" y="{sy(side*14)-27.5:.1f}" width="105" height="55" rx="25" fill="#93a9bc" stroke="#34495e"/>')
S+=['<text x="45" y="545" font-family="sans-serif" font-size="17">Z50: m1, pitch Ø50 (dashed) | 6 wheels Ø78 x 14 | 2 motor envelopes Ø22 x 42</text>',
'<text x="45" y="574" font-family="sans-serif" font-size="17">Pipe Ø150 conservative radial clearance: %.3f mm | lid load at 0.7 bar: 714 N</text>'%(75-radial),
'<text x="45" y="608" font-family="sans-serif" font-size="15" fill="#b45309">Unverified: involute solids, bevel mesh, shaft pressure seals, lid fasteners, full Boolean collisions</text>','</svg>']
svg=ROOT/"M1_full_chassis_interface_audit.svg"
svg.write_text("\n".join(S),encoding="utf-8")
report={"basis":"Existing integrated FreeCAD generator P dict; all dimensions assumed unless externally verified","parameters":P,"checks":checks,"svg":svg.name}
(ROOT/"M1_full_chassis_interface_audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps({k:v["status"] for k,v in checks.items()},indent=2))
assert all(v["status"]=="PASS" for v in checks.values() if v["status"] in ("PASS","FAIL"))
