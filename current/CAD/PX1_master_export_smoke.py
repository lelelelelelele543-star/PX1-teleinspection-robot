#!/usr/bin/env python3
"""Smoke-check REAL CadQuery exports from PX1_Current_Master.py.
This is not a manufacturing qualification. Nonzero exit on absent/invalid exports.
Run after PX1_OUT=/path python current/CAD/PX1_Current_Master.py.
"""
import os, json, pathlib, sys
import cadquery as cq
root=pathlib.Path(os.environ.get("PX1_OUT", pathlib.Path(__file__).resolve().parents[1]))
step=root/"CAD"/"PX1_Current_Master.step"
stls=list((root/"CAD"/"Print_STL").glob("*.stl"))
results={}
def report(k,ok,detail):
    results[k]={"status":"PASS" if ok else "FAIL","detail":detail}
report("assembly_step_exists",step.is_file() and step.stat().st_size>1000 if step.exists() else False,str(step))
if step.is_file():
    try:
        imported=cq.importers.importStep(str(step))
        solids=imported.solids().vals()
        report("step_roundtrip",bool(solids) and all(s.isValid() for s in solids),f"solids={len(solids)}")
    except Exception as e: report("step_roundtrip",False,repr(e))
else: report("step_roundtrip",False,"STEP absent")
report("prototype_stls_exist",len(stls)>=5,f"found={len(stls)}")
for p in stls:
    try:
        import trimesh
        m=trimesh.load_mesh(str(p),force="mesh")
        report("stl_"+p.name,len(m.faces)>0 and m.is_watertight,f"faces={len(m.faces)},watertight={m.is_watertight}")
    except Exception as e: report("stl_"+p.name,False,repr(e))
print(json.dumps(results,indent=2,ensure_ascii=False))
sys.exit(1 if any(x["status"]=="FAIL" for x in results.values()) else 0)
