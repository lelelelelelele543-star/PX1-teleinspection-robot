"""PX1 integrated motor and gear datum audit. Standard Python, no CadQuery import.
Reads only literal assignments from current/CAD/PX1_Current_Master.py.
Does not assert motor availability, fit, or electrical compatibility.
"""
import ast, math, json
from pathlib import Path

MASTER = Path(__file__).with_name("PX1_Current_Master.py")
NAMES = ("WHEEL_X","GEAR_X","WHEEL_Z","Z50_TEETH","Z50_MOD","Z50_PD",
         "MOTOR_OD","MOTOR_LEN","GEARHEAD_OD","GEARHEAD_LEN","MOTOR_FACE",
         "MOTOR_Y","MOTOR_SHAFT_D","MOTOR_SHAFT_L","BODY_L_SOURCE_SCREEN",
         "BODY_HALF_W_SCREEN","BODY_Z0","BODY_TOP","WHEEL_CENTRE_Y",
         "WHEEL_CROWN_R","PIPE_R")
def load():
    tree = ast.parse(MASTER.read_text(encoding="utf-8"))
    env = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id not in NAMES:
            continue
        try: env[target.id] = ast.literal_eval(node.value)
        except (ValueError, TypeError): pass
    missing = set(NAMES)-set(env)
    if missing: raise ValueError("Missing literal master constants: "+", ".join(sorted(missing)))
    return env
def audit(p):
    assert len(p["WHEEL_X"]) == 3 and len(p["GEAR_X"]) == 5
    assert tuple(p["WHEEL_X"]) == (50.,150.,250.)
    assert p["Z50_TEETH"] == 50 and p["Z50_MOD"] == 1.
    assert abs(p["Z50_PD"] - p["Z50_TEETH"]*p["Z50_MOD"]) < 1e-8
    # Motor screen only. Assumes longitudinal envelope ends at MOTOR_FACE.
    motor_length = p["MOTOR_LEN"] + p["GEARHEAD_LEN"]
    x0 = p["MOTOR_FACE"] - motor_length
    x1 = p["MOTOR_FACE"]
    body_min_x = (300.0-p["BODY_L_SOURCE_SCREEN"])/2
    body_max_x = body_min_x+p["BODY_L_SOURCE_SCREEN"]
    motor_body_screen = body_min_x <= x0 < x1 <= body_max_x
    # Radial cross-section screening at +/- MOTOR_Y, not full BREP interference.
    lateral_screen = abs(p["MOTOR_Y"])+max(p["MOTOR_OD"],p["GEARHEAD_OD"])/2 <= p["BODY_HALF_W_SCREEN"]
    motor_gap = 2*abs(p["MOTOR_Y"])-max(p["MOTOR_OD"],p["GEARHEAD_OD"])
    gear_pitch = [b-a for a,b in zip(p["GEAR_X"],p["GEAR_X"][1:])]
    gear_pitch_ok = all(abs(d-p["Z50_PD"]) < 1e-8 for d in gear_pitch)
    return {"source":"PX1_Current_Master.py","motor_x_screen_mm":[round(x0,2),round(x1,2)],
      "motor_pair_nominal_gap_mm":round(motor_gap,2),
      "motor_inside_body_bbox_screen":motor_body_screen,
      "motor_lateral_bbox_screen":lateral_screen,
      "gear_pitch_consistent":gear_pitch_ok,
      "wheels":6,"Z50":10,"motor_count":2,
      "motor_driver_match":"NOT_RUN: check exact motor datasheet (brushed/BLDC) versus driver",
      "full_brep_collision":"NOT_RUN","seal_pressure":"PHYSICAL_CHECK",
      "dimensions":"DESIGN SCREEN; not manufacturing release"}
if __name__=="__main__":
    result=audit(load())
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert result["motor_inside_body_bbox_screen"] and result["motor_lateral_bbox_screen"]
    assert result["gear_pitch_consistent"] and result["motor_pair_nominal_gap_mm"] >= 0
