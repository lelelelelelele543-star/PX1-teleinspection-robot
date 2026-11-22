#!/usr/bin/env python3
"""One-command PX1 CURRENT master build + CAD-derived preview; no surrogate CAD.

Run from any directory with: python current/CAD/run_integrated_build.py
Requires cadquery and checked-in vendor STEP dependencies. Does not alter main.
Exit nonzero if STEP/validation/preview cannot be produced.
"""
import os, sys, subprocess, json, hashlib, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
MASTER=HERE/"PX1_Current_Master.py"
POST=HERE/"PX1_postbuild_integration.py"
REPORT=ROOT/"PX1_integrated_build_run.json"
VENDOR=[
    HERE/"vendor"/"WeAct_F4_64Pin_V11_Manufacturer.step",
    HERE/"vendor"/"Pololu_G2_24v13_Manufacturer.step",
]
def finish(status, checks, started):
    report={"status":status,"master":str(MASTER.relative_to(ROOT)),
        "master_sha256":hashlib.sha256(MASTER.read_bytes()).hexdigest(),
        "duration_seconds":round(time.monotonic()-started,2),
        "checks":checks,
        "manufacturing_release":"NOT_APPROVED",
        "physical_pressure_test":"NEEDS_PHYSICAL_CHECK"}
    REPORT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0 if status=="CAD_EXPORT_COMPLETED_WITH_OPEN_QUALIFICATIONS" else 1

def main():
    started=time.monotonic()
    checks={}
    for p in (MASTER,POST,*VENDOR):
        checks[str(p.relative_to(ROOT))]="PASS" if p.is_file() and p.stat().st_size>0 else "FAIL_MISSING"
    if any(v!="PASS" for v in checks.values()):
        return finish("BLOCKED_MISSING_SOURCE_OR_VENDOR_STEP",checks,started)
    try:
        import cadquery
        checks["cadquery_import"]="PASS"
    except Exception as exc:
        checks["cadquery_import"]="FAIL: "+repr(exc)
        return finish("BLOCKED_CADQUERY_UNAVAILABLE",checks,started)
    env=dict(os.environ,PX1_OUT=str(ROOT),PYTHONUNBUFFERED="1")
    log=ROOT/"PX1_integrated_build.log"
    with log.open("w",encoding="utf-8") as f:
        proc=subprocess.run([sys.executable,str(MASTER)],cwd=str(HERE),env=env,
                            stdout=f,stderr=subprocess.STDOUT)
    checks["master_exit"]=proc.returncode
    if proc.returncode:
        return finish("FAIL_MASTER_BUILD_SEE_LOG",checks,started)
    step=HERE/"PX1_Current_Master.step"
    validation=ROOT/"PX1_Current_Validation.json"
    checks["master_step"]="PASS" if step.is_file() and step.stat().st_size>1000 else "FAIL"
    checks["validation"]="PASS" if validation.is_file() else "FAIL"
    if "FAIL" in checks.values():
        return finish("FAIL_MISSING_EXPORT",checks,started)
    with log.open("a",encoding="utf-8") as f:
        proc=subprocess.run([sys.executable,str(POST)],cwd=str(HERE),env=env,
                            stdout=f,stderr=subprocess.STDOUT)
    checks["postbuild_exit"]=proc.returncode
    preview=HERE/"previews"/"PX1_master_actual_export_plan.svg"
    checks["cad_derived_svg"]="PASS" if preview.is_file() and preview.stat().st_size>1000 else "FAIL"
    if proc.returncode or checks["cad_derived_svg"]!="PASS":
        return finish("FAIL_POSTBUILD_SEE_LOG",checks,started)
    return finish("CAD_EXPORT_COMPLETED_WITH_OPEN_QUALIFICATIONS",checks,started)

if __name__=="__main__":
    raise SystemExit(main())
