"""PX1 M1: single-command FreeCAD integration runner, source-only until executed.
FreeCADCmd M1_run_integrated_chassis.py
Reuses existing chassis and keyed-interface generators; no invented STEP outputs.
"""
from pathlib import Path
import runpy, json, sys, traceback
ROOT=Path(__file__).resolve().parent
STAGES=[
 ("base","PX1_Integrated_6x6_M1_interface_repair.py",["PX1_Integrated_6x6_M1.FCStd","PX1_Integrated_6x6_M1.step"]),
 ("keyed","M1_integrated_keyed_interfaces.py",["PX1_Integrated_6x6_M1_keyed.FCStd","PX1_Integrated_6x6_M1_keyed.step"]),
]
report={"status":"NOT_RUN","stages":[],"design_assumptions":["10 mm shafts and bores","3x3 mm rectangular keys, NOT standard-qualified","m1 Z50 gear teeth","motor and seal packaging unqualified"],"physical_checks":["dynamic shaft sealing at 0.4-0.7 bar","key torque and retention","bearing fits","bevel contact"]}
for name,script,outputs in STAGES:
    stage={"name":name,"script":script,"status":"NOT_RUN","outputs":[]}
    report["stages"].append(stage)
    try:
        if not (ROOT/script).is_file(): raise FileNotFoundError(script)
        runpy.run_path(str(ROOT/script),run_name="__main__")
        for fn in outputs:
            f=ROOT/fn
            if not f.is_file() or f.stat().st_size<1024:
                raise RuntimeError("missing or empty output "+fn)
            stage["outputs"].append({"name":fn,"bytes":f.stat().st_size})
        stage["status"]="PASS"
    except Exception as exc:
        stage["status"]="FAIL"
        stage["error"]=str(exc)
        report["status"]="FAIL"
        traceback.print_exc()
        break
else:
    report["status"]="PASS"
report["not_run"]=["3D collision sweep","gear motion under load","pressure qualification","STEP keyed assembly roundtrip"]
(ROOT/"M1_run_integrated_chassis_result.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
if report["status"]!="PASS":sys.exit(2)
