#!/usr/bin/env python3
"""PX1 M1: coordinate-frame and power-path integration gate. Stdlib only.
Checks the existing FreeCAD generator and the existing power-path source;
does not claim gear contact, collision-free solids or pressure qualification.
"""
import ast,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
def assigned(source,name):
    tree=ast.parse(source)
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise ValueError("missing literal "+name)
def read_cad():
    s=(P/"PX1_Integrated_6x6_M1_interface_repair.py").read_text()
    m=re.search(r"P=dict\((.*?)\)\s*\nparts=",s,re.S)
    if not m: raise ValueError("CAD parameter block missing")
    # Parse keyword arguments without executing FreeCAD.
    call=ast.parse("dict("+m.group(1)+")",mode="eval").body
    return {k.arg:ast.literal_eval(k.value) for k in call.keywords}
def main():
    cad=read_cad()
    src=(P/"M1_six_wheel_powerpath.py").read_text()
    assumptions=assigned(src,"ASSUMPTIONS")
    checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,status="PASS" if ok else "FAIL",detail=detail))
    wheel=sorted(cad["stations"])
    gear=sorted(cad["gear_x"])
    graph_wheel=sorted(assumptions["axles_x_mm"])
    graph_gear=sorted(assumptions["gear_x_mm"])
    offsets={b-a for a,b in zip(wheel,graph_wheel)}
    gear_offsets={b-a for a,b in zip(gear,graph_gear)}
    check("wheel count",len(wheel)==3 and assumptions["wheel_count"]==6,str(wheel))
    check("five gears per side",len(gear)==5 and assumptions["spur_station_count"]==10,str(gear))
    check("wheel station frame",len(offsets)==1,"graph minus CAD offsets="+str(sorted(offsets)))
    check("gear station frame",len(gear_offsets)==1 and offsets==gear_offsets,
          "gear offsets="+str(sorted(gear_offsets))+"; wheel offsets="+str(sorted(offsets)))
    check("wheel/gear shared stations",set(wheel).issubset(set(gear)),str(wheel))
    pitch=cad["gear_m"]*50
    intervals=[b-a for a,b in zip(gear,gear[1:])]
    check("Z50 pitch center distances",all(abs(d-pitch)<1e-7 for d in intervals),
          "pitch="+str(pitch)+"; centers="+str(intervals))
    check("motor count",assumptions["motor_count"]==2,"one motor per side")
    check("wheel radial DN150",((43+cad["wheel_W"])**2+(cad["wheel_D"]/2)**2)**0.5<=75,
          "conservative corner radius mm")
    report=dict(model="PX1 M1 CAD/kinematic frame integration",assumptions={
      "coordinate_transform":"graph X = CAD X + 160 mm (candidate, not applied)",
      "gear_surfaces":"pitch cylinders, not manufactured involute gears",
      "seals":"dynamic seals not qualified for 0.4-0.7 bar",
      "motor":"22x42 mm assumed, catalog unverified"},checks=checks,
      not_run=["FreeCAD STEP reopen","Boolean collisions","bevel tooth contact","pressure testing"])
    (P/"M1_frame_integration_gate.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__=="__main__":
    r=main()
    for c in r["checks"]:print(c["status"],c["name"],c["detail"])
    raise SystemExit(1 if any(c["status"]=="FAIL" for c in r["checks"]) else 0)
