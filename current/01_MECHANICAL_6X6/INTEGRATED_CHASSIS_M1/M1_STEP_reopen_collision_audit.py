"""PX1 M1 FreeCAD validation runner. Run with FreeCADCmd in the same directory.
Reads the existing integrated generator output, never invents a STEP success.
"""
import os, json, sys
import FreeCAD as App
import Part
ROOT=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(ROOT,"PX1_Integrated_6x6_M1_interface_repair.py")
step=os.path.join(ROOT,"PX1_Integrated_6x6_M1.step")
report=os.path.join(ROOT,"M1_STEP_reopen_collision_audit.json")
results={"source":src,"step":step,"checks":{},"limitations":["Proxy pitch cylinders are NOT involute teeth","Pressure seals and bearing fits need physical verification"]}
def check(name,status,details):
    results["checks"][name]={"status":status,"details":details}
try:
    if not os.path.isfile(step):
        check("step_exists","FAIL","Run integrated generator in FreeCADCmd first")
    else:
        shape=Part.read(step)
        solids=shape.Solids
        check("step_reopen","PASS" if len(solids)>0 and not shape.isNull() else "FAIL",{"solid_count":len(solids),"volume_mm3":shape.Volume})
        check("step_shape_valid","PASS" if shape.isValid() else "FAIL","OpenCascade isValid")
        # Part.export does not preserve individual object names reliably; audit source FCStd instead.
        fc=os.path.join(ROOT,"PX1_Integrated_6x6_M1.FCStd")
        if os.path.isfile(fc):
            doc=App.openDocument(fc)
            items=[o for o in doc.Objects if hasattr(o,"Shape") and not o.Shape.isNull()]
            check("component_count","PASS" if len(items)>=35 else "FAIL",{"objects":len(items)})
            # Only test disjoint parts that should never touch: left and right motors.
            motors=[o for o in items if o.Name.startswith("Motor_") and o.Name.endswith("_ENVELOPE")]
            if len(motors)==2:
                overlap=motors[0].Shape.common(motors[1].Shape).Volume
                check("motor_pair_boolean","PASS" if overlap<1e-6 else "FAIL",{"intersection_mm3":overlap})
            else:
                check("motor_pair_boolean","FAIL","Two motor envelopes not found")
            # Deliberate contact: gear/axle/bearing and wheel/axle, excluded from naive all-pairs tests.
            # Identify potential *unintended* overlap of motor bodies and gear proxies.
            gears=[o for o in items if "Z50_pitch_PROXY" in o.Name]
            maxoverlap=0.0
            for motor in motors:
                for gear in gears:
                    maxoverlap=max(maxoverlap,motor.Shape.common(gear.Shape).Volume)
            check("motor_Z50_boolean","PASS" if maxoverlap<1e-6 else "FAIL",{"max_intersection_mm3":maxoverlap})
            check("complete_collision_audit","NOT_RUN","Requires connection-aware exclusion map and real gear tooth solids")
            App.closeDocument(doc.Name)
        else:
            check("fcstd_exists","FAIL","FreeCAD document missing")
except Exception as exc:
    check("runner","FAIL",repr(exc))
with open(report,"w",encoding="utf-8") as f: json.dump(results,f,indent=2,ensure_ascii=False)
print(json.dumps(results,indent=2,ensure_ascii=False))
sys.exit(1 if any(c["status"]=="FAIL" for c in results["checks"].values()) else 0)
