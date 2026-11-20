"""PX1 M1 integrated FreeCAD runner: validates fresh CAD and STEP roundtrip.
Run: FreeCADCmd M1_run_integrated_chassis.py
No manufacturing qualification; geometry and hardware assumptions remain unverified.
"""
from pathlib import Path
import runpy, json, sys, traceback, time
ROOT=Path(__file__).resolve().parent
STAGES=[
 ("base","PX1_Integrated_6x6_M1_interface_repair.py",
  ["PX1_Integrated_6x6_M1.FCStd","PX1_Integrated_6x6_M1.step"]),
 ("keyed","M1_integrated_keyed_interfaces.py",
  ["PX1_Integrated_6x6_M1_keyed.FCStd","PX1_Integrated_6x6_M1_keyed.step"]),
 ("bridged","M1_torque_interface_bridge.py",\n  ["PX1_Integrated_6x6_M1_bridged.FCStd","PX1_Integrated_6x6_M1_bridged.step"]),\n]
report={"status":"NOT_RUN","stages":[],"design_assumptions":[
 "10 mm shaft/bores","3x3 mm rectangular keys (not standard-qualified)",
 "module 1 Z50 involute design","motor, bearing and pressure-seal packaging unqualified"],
 "physical_checks":["0.4-0.7 bar dynamic shaft seals","key torque and retention",
 "bearing fits and loads","bevel tooth contact and lubrication"],
 "not_run":["full motion collision sweep","load-bearing tooth stress",
 "pressure qualification"]}
def verify_step(path):
 import Part
 shape=Part.read(str(path))
 if shape.isNull() or not shape.Solids:
  raise ValueError("STEP reimport produced null shape or zero solids")
 solids=shape.Solids
 invalid=[i for i,s in enumerate(solids) if not s.isValid() or s.Volume<=0]
 if invalid: raise ValueError("Invalid/nonpositive STEP solids: "+str(invalid[:12]))
 return {"solids":len(solids),"volume_mm3":round(sum(s.Volume for s in solids),3)}
for name,script,outputs in STAGES:
 stage={"name":name,"script":script,"status":"NOT_RUN","outputs":[]}
 report["stages"].append(stage)
 try:
  if not (ROOT/script).is_file(): raise FileNotFoundError(script)
  # Never mistake stale artifacts from an earlier successful run for new results.
  for fn in outputs:
   p=ROOT/fn
   if p.exists(): p.unlink()
  started=time.time()
  runpy.run_path(str(ROOT/script),run_name="__main__")
  for fn in outputs:
   p=ROOT/fn
   if not p.is_file() or p.stat().st_size<1024:
    raise RuntimeError("Missing/empty output: "+fn)
   if p.stat().st_mtime < started-2:
    raise RuntimeError("Output predates this run: "+fn)
   item={"name":fn,"bytes":p.stat().st_size}
   if fn.lower().endswith(".step"): item["roundtrip"]=verify_step(p)
   stage["outputs"].append(item)
  stage["status"]="PASS"
 except Exception as exc:
  stage["status"]="FAIL"
  stage["error"]=str(exc)
  report["status"]="FAIL"
  traceback.print_exc()
  break
else:
 report["status"]="PASS"
report["limitations"]=[
 "STEP validity does not prove mating fits, zero collisions or correct gear kinematics",
 "A bridged STEP is not qualified for fabrication without mechanical and pressure checks",\n "Bridge hubs are geometric proxies; motor-to-wheel torque path is not functionally proven"]
(ROOT/"M1_run_integrated_chassis_result.json").write_text(
 json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
if report["status"]!="PASS": sys.exit(2)
