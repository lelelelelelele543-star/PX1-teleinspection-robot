"""PX1 M1 integrated source audit: stdlib only, does not claim FreeCAD validation.
Run: python M1_integrated_assembly_gate_20261120.py
"""
import ast, pathlib, math
source=pathlib.Path(__file__).with_name("PX1_Integrated_6x6_M1_interface_repair.py").read_text(encoding="utf-8")
tree=ast.parse(source)
assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
P={kw.arg: ast.literal_eval(kw.value) for kw in assign.value.keywords} if isinstance(assign.value,ast.Call) and isinstance(assign.value.func,ast.Name) and assign.value.func.id=="dict" else ast.literal_eval(assign.value)
checks=[]
def check(name,ok,detail):
    checks.append((name,"PASS" if ok else "FAIL",detail))
    print(checks[-1][1],name,detail)
check("6x6 wheel stations",len(P["stations"])==3 and len(P["gear_x"])==5,"3 per side; 5 spur stations per side")
check("spur pitch spacing",all(abs(P["gear_x"][i+1]-P["gear_x"][i]-50*P["gear_m"])<1e-8 for i in range(4)),"Z50, m=1 ASSUMED")
check("motor count and package",P["motor_D"]==22 and P["motor_L"]==42,"2 motors, envelope ASSUMED")
check("motor versus idler X",P["motor_x"]>=-38 and P["motor_x"]+P["motor_L"]<=38,"idler station X=+-50, radius 11 +1 allowance")
check("shaft versus idler YZ",math.hypot(P["motor_y"]-19,P["motor_z"]-P["gear_z"])>=16,"shaft radius 4, bearing radius 11, clearance >=1")
check("wheel pipe clearance",75-math.hypot(46+P["wheel_W"],P["wheel_D"]/2)>=2,"DN150 circular envelope, >=2 mm ASSUMED")
check("gasket opening matches", "Part.makeBox(176,66,1" in source and "Part.makeBox(170,60,1" in source,"ring nominal 3 mm")
check("motor Z16 hub overlap",P["motor_x"]+P["motor_L"]+93>=105 and 105-101>=4,"nominal 4 mm, NOT torque-rated")
check("pressure load reported",abs(170*60*0.07-714)<1e-9,"714 N at 0.7 bar across opening, 89.25 N/8 nominal, not bolt design")
# Crucial negative gates: pitch-cylinder proxies do not represent real toothed gears.
check("real involute spur gear geometry",not ("Z50_pitch_PROXY_" in source),"must replace 10 pitch cylinders with teeth")
check("real bevel contact",not ("Bevel_Z16_PROXY_" in source or "Bevel_Z40_PROXY_" in source),"must replace bevel proxies and validate mesh")
check("pressure-qualified shaft seals",not ("Shaft_seal_CARTRIDGE_PROXY_" in source),"0.4-0.7 bar rating unverified")
check("motor mounting and torque connection",not ("Motor_" in source and "_ENVELOPE" in source),"motor brackets, coupling and axial supports required")
print("SUMMARY",sum(s=="PASS" for _,s,_ in checks),"PASS",sum(s=="FAIL" for _,s,_ in checks),"FAIL")
print("NOT_RUN FreeCAD solids, Boolean sweep, STEP roundtrip, dynamic mesh, pressure test")
print("PHYSICAL_CHECK shaft seals, fastener preload, motor fit, manufacturing tolerances")
if any(s=="FAIL" for _,s,_ in checks):
    raise SystemExit(2)
