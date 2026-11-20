"""PX1 M1: actual FreeCAD Boolean clearance gate for disjoint component groups.
Run after M1_run_integrated_chassis.py using FreeCADCmd.
Does not test tooth meshing, press-fit interfaces or seal pressure rating.
"""
from pathlib import Path
import FreeCAD as App
import json, math, sys, traceback
ROOT=Path(__file__).resolve().parent
FC=ROOT/"PX1_Integrated_6x6_M1_bridged.FCStd"
OUT=ROOT/"M1_disjoint_boolean_gate_result.json"
report={"source":str(FC),"status":"NOT_RUN","checks":[],"limitations":[
"Intentional contacts (gears, hubs, bearings and supports) are excluded",
"Static Boolean intersections do not validate rotating swept volumes",
"Pressure, tooth stress, preload, tolerances and manufacturing NOT_RUN"]}
def check(a,b,kind="disjoint"):
    sa=a.Shape; sb=b.Shape
    if sa.isNull() or sb.isNull(): raise ValueError("null shape")
    # Fast bounding box rejection avoids unnecessary OCC Boolean operations.
    bb=sa.BoundBox; bc=sb.BoundBox
    if not bb.intersect(bc):
        v=0.0
    else:
        v=sa.common(sb).Volume
    status="PASS" if v<0.01 else "FAIL"
    report["checks"].append({"a":a.Name,"b":b.Name,"type":kind,
      "overlap_mm3":round(v,5),"status":status})
def run():
    if not FC.is_file(): raise FileNotFoundError("Run integrated generator first: "+str(FC))
    d=App.openDocument(str(FC))
    obj={o.Name:o for o in d.Objects if hasattr(o,"Shape")}
    def get(name):
        if name not in obj: raise KeyError("Missing required component: "+name)
        return obj[name]
    body=get("Body_hollow_ASSUMED")
    for side in ("L","R"):
        motor=get("Motor_"+side+"_ENVELOPE")
        # A drive motor must not cut into a wheel, gear or idler bearing.
        for j in range(1,6):
            check(motor,get("Z50_pitch_PROXY_"+side+"_"+str(j)))
        for j in (1,3):
            check(motor,get("Idler_bearing_PROXY_"+side+"_"+str(j)))
        for j in range(1,4):
            check(motor,get("Wheel_"+side+"_"+str(j)))
            # Wheel and pressure vessel must be disjoint.
            check(body,get("Wheel_"+side+"_"+str(j)))
        # Long motor shaft must clear idler bearings and their carriers.
        shaft=get("Motor_shaft_"+side)
        for j in (1,3):
            check(shaft,get("Idler_bearing_PROXY_"+side+"_"+str(j)))
            check(shaft,get("Idler_carrier_PROXY_"+side+"_"+str(j)))
    check(get("Motor_L_ENVELOPE"),get("Motor_R_ENVELOPE"))
    report["status"]="PASS" if all(x["status"]=="PASS" for x in report["checks"]) else "FAIL"
    report["tested_pairs"]=len(report["checks"])
try: run()
except Exception as exc:
    report["status"]="FAIL"
    report["error"]=repr(exc)
    report["traceback"]=traceback.format_exc()
finally:
    OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
if report["status"]!="PASS": sys.exit(2)
