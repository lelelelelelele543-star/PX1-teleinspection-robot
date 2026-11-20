"""PX1 M1 integration gate: independent standard-library audit of existing FreeCAD parameters.
Run: python M1_integrated_geometry_gate.py
Does not claim a FreeCAD execution or manufacturing clearance.
"""
import json, math, pathlib, re, ast
ROOT=pathlib.Path(__file__).resolve().parent
src=(ROOT/"PX1_Integrated_6x6_M1_interface_repair.py").read_text(encoding="utf-8")
tree=ast.parse(src)
params=None
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in node.targets):
        params={kw.arg:ast.literal_eval(kw.value) for kw in node.value.keywords} if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='dict' else ast.literal_eval(node.value)
        break
assert params is not None
P=params
checks={}
def check(name,ok,detail):
    checks[name]={"status":"PASS" if ok else "FAIL","detail":detail}
check("wheel_count",len(P["stations"])*2==6,"6 wheels, 3 per side")
check("gear_count",len(P["gear_x"])*2==10,"10 Z50 pitch proxies")
check("station_alignment",tuple(P["gear_x"][::2])==tuple(P["stations"]),"wheel axes coincide with gear positions 1/3/5")
pitch=P["gear_m"]*50
check("spur_pitch",all(abs(b-a-pitch)<1e-8 for a,b in zip(P["gear_x"],P["gear_x"][1:])),"pitch distance %.1f mm"%pitch)
wheel_radial=math.hypot(43+P["wheel_W"],P["wheel_D"]/2)
check("DN150_wheel_envelope",wheel_radial<=75,"bounding radius %.3f mm; idealized straight DN150"%wheel_radial)
body_radial=math.hypot(P["body_W"]/2,P["body_H"]/2)
check("DN150_body_envelope",body_radial<=75,"bounding radius %.3f mm"%body_radial)
check("motor_pair",2*P["motor_y"]-P["motor_D"]>=2,"nominal motor-to-motor gap %.1f mm"%(2*P["motor_y"]-P["motor_D"]))
check("motor_spur",P["gear_y"]-P["gear_thick"]/2-P["motor_y"]-P["motor_D"]/2>=2,"nominal Y gap %.1f mm"%(P["gear_y"]-P["gear_thick"]/2-P["motor_y"]-P["motor_D"]/2))
# Hard blockers: existing gear bodies are smooth cylinders, not teeth; 2 intermediate stubs per side have no bearing.
check("real_spur_teeth",False,"Z50 is Part.makeCylinder pitch proxy, no involute teeth")
check("idler_bearing_support",False,"4 idler stubs lack dedicated bearing objects and housing")
check("dynamic_shaft_seals",False,"6 axle passages have no dynamic pressure seal geometry")
check("bevel_contact",False,"Z16/Z40 are cylinders; bevel mesh and torque coupling unvalidated")
# Important new check: bearing Ø22 counterbore starts at y=35, shell extends y=39;
# 3 mm depth reaches y=38 leaving 1 mm external shell lip; not a 7 mm bearing seat.
check("bearing_seat_depth",False,"3 mm counterbore versus 7 mm bearing proxy; retention not designed")
checks["freecad_boolean"]={"status":"NOT_RUN","detail":"requires FreeCAD runtime"}
checks["step_reopen"]={"status":"NOT_RUN","detail":"requires FreeCAD STEP export and independent re-import"}
checks["pressure_test"]={"status":"PHYSICAL_CHECK","detail":"0.4-0.7 bar pressurized dry body, seal validation required"}
out={"source":"PX1_Integrated_6x6_M1_interface_repair.py","design_assumptions":{"gear_module":P["gear_m"],"wheel_diameter_mm":P["wheel_D"],"body_width_mm":P["body_W"],"pressure_bar":[P["pressure_bar_min"],P["pressure_bar_max"]]},"checks":checks}
(ROOT/"M1_integrated_geometry_gate.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
for name,item in checks.items():print(item["status"],name,item["detail"])
assert all(v["status"]=="PASS" for k,v in checks.items() if k in ("wheel_count","gear_count","station_alignment","spur_pitch","DN150_wheel_envelope","DN150_body_envelope","motor_pair","motor_spur"))
print("PASS parameter audit; FAIL functional design gates remain")
