"""PX1 drivetrain integrated analytical gate; Python 3 stdlib.
Run: python current/CAD/px1_drivetrain_gate.py
Reads existing PX1_Current_Master.py without importing CadQuery or exporting solids.
"""
import ast, math, json
from pathlib import Path
def parameters(path):
    result={}
    for node in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(node,ast.Assign):
            try: value=ast.literal_eval(node.value)
            except (ValueError,TypeError): continue
            for t in node.targets:
                if isinstance(t,ast.Name): result[t.id]=value
    return result
def gate(path):
    p=parameters(path)
    wx=p["WHEEL_X"]; gx=p["GEAR_X"]; pitch=p["Z50_TEETH"]*p["Z50_MOD"]
    gap=[round(b-a,5) for a,b in zip(gx,gx[1:])]
    signs=[(-1)**i for i in range(len(gx))]
    checks={
      "six_wheels":len(wx)==3,
      "ten_Z50":len(gx)==5,
      "wheel_station_gears":all(x in gx for x in wx),
      "four_pitch_center_distances":all(abs(v-pitch)<1e-6 for v in gap),
      "all_wheels_same_direction_per_side":all(signs[gx.index(x)]==signs[0] for x in wx),
      "input_ratio_2_5":p["Z40_TEETH"]/p["Z16_TEETH"]==2.5,
    }
    motor=(p["MOTOR_FACE"]-p["MOTOR_LEN"],p["MOTOR_FACE"])
    return {"status":"PASS_ANALYTICAL" if all(checks.values()) else "FAIL_ANALYTICAL",
       "checks":checks,"gear_centers_mm":gx,"wheel_centers_mm":wx,
       "mesh_center_distances_mm":gap,"gear_rotation_signs":signs,
       "motor_X_range_mm":motor,"motor_crosses_X150_projection":motor[0]<=150<=motor[1],
       "assumptions":{"gear_centers_and_module":"MASTER, not verified OEM",
                      "motor_envelope":"MASTER estimated; 3D Y/Z unresolved"},
       "CAD_collisions":"NOT_RUN","tooth_contact":"NOT_RUN",
       "dynamic_shaft_sealing":"PHYSICAL_CHECK","manufacturing_release":False}
if __name__=="__main__":
    result=gate(Path(__file__).with_name("PX1_Current_Master.py"))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert result["status"]=="PASS_ANALYTICAL"
