"""Independent M1 envelope/pressure regression; standard Python, no FreeCAD required.
Reads current FreeCAD generator AST, never duplicates its parameters silently.
These are analytic design-target checks, not solid collisions or pressure proof.
Run: python M1_integrated_envelope_regression.py
"""
import ast, json, math, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/"PX1_Integrated_6x6_M1_interface_repair.py"
tree=ast.parse(SRC.read_text(encoding="utf-8"))
pnode=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
P={kw.arg:ast.literal_eval(kw.value) for kw in pnode.keywords} if isinstance(pnode,ast.Call) and isinstance(pnode.func,ast.Name) and pnode.func.id=="dict" else ast.literal_eval(pnode)
checks={}
def gate(name,condition,details):
    checks[name]={"status":"PASS" if condition else "FAIL","details":details}
L,W,H=P["body_L"],P["body_W"],P["body_H"]
wheel_y=46+P["wheel_W"]
r=math.hypot(wheel_y,P["wheel_D"]/2)
gate("DN150_wheel_corner",r<=73,{"corner_radius_mm":round(r,4),"radial_clearance_mm":round(75-r,4),"minimum_target_mm":2})
gate("DN150_body_corner",math.hypot(W/2,H/2)<75,{"radius_mm":round(math.hypot(W/2,H/2),4)})
gate("six_wheels",len(P["stations"])==3 and P["stations"]==tuple(P["gear_x"][i] for i in (0,2,4)),{"stations":P["stations"]})
gate("ten_gears_pitch",len(P["gear_x"])==5 and all(abs(P["gear_x"][i+1]-P["gear_x"][i]-P["gear_m"]*50)<1e-9 for i in range(4)),{"pitch_mm":P["gear_m"]*50})
gate("motor_pair_clearance",2*P["motor_y"]-P["motor_D"]>=2,{"gap_mm":2*P["motor_y"]-P["motor_D"]})
gate("motor_to_spur",P["gear_y"]-P["gear_thick"]/2-(P["motor_y"]+P["motor_D"]/2)>=2,{"gap_mm":P["gear_y"]-P["gear_thick"]/2-(P["motor_y"]+P["motor_D"]/2)})
gate("wheel_axial_seal_package",46-(34+7)>=5,{"bearing_outer_y_mm":41,"seal_cartridge_end_y_mm":45,"wheel_inner_y_mm":46})
gate("gasket_nominal",0<P["lid_gasket_compression"]<P["lid_gasket_nominal"],{"nominal_mm":P["lid_gasket_nominal"],"compression_mm":P["lid_gasket_compression"]})
pressure_pa=P["pressure_bar_max"]*100000
force_n=pressure_pa*(170*60)*1e-6
gate("lid_pressure_force",force_n>0,{"opening_mm":[170,60],"pressure_bar":P["pressure_bar_max"],"separating_force_N":round(force_n,2),"per_bolt_average_N_not_preload":round(force_n/8,2)})
# IMPORTANT: no physical pressure rating is inferred from geometric fit.
for name in ("seal_pressure_rating","bearing_fits","idler_mount_strength","bevel_mesh","real_involute_teeth","full_3d_collisions","STEP_roundtrip"):
    checks[name]={"status":"NOT_RUN","details":"Requires supplier data, actual FreeCAD execution or physical validation"}
out={"source":str(SRC.name),"design_assumptions":True,"checks":checks,"pass_count":sum(x["status"]=="PASS" for x in checks.values()),"fail_count":sum(x["status"]=="FAIL" for x in checks.values())}
print(json.dumps(out,indent=2,ensure_ascii=False))
sys.exit(1 if out["fail_count"] else 0)
