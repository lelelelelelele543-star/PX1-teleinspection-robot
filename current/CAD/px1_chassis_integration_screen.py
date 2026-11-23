"""PX1 integrated drivetrain datum/pressure screening; no CadQuery dependency.
Run: python current/CAD/px1_chassis_integration_screen.py
Reads constants from the ONE existing CAD master without executing its export.
DESIGN SCREEN ONLY: motor placement, seal pressure and collision remain unqualified.
"""
import ast, math, json
from pathlib import Path
MASTER=Path(__file__).with_name("PX1_Current_Master.py")
def constants(path):
    tree=ast.parse(path.read_text(encoding="utf-8"))
    names={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            try:
                value=ast.literal_eval(node.value)
            except (ValueError,TypeError,KeyError):
                continue
            for target in node.targets:
                if isinstance(target,ast.Name): names[target.id]=value
    return names
def check():
    p=constants(MASTER)
    wheels=p["WHEEL_X"]; gears=p["GEAR_X"]
    assert wheels==(50.,150.,250.),"wheel datum drift"
    assert gears==(50.,100.,150.,200.,250.),"gear datum drift"
    assert set(wheels).issubset(set(gears))
    assert p["MOTOR_LEN"]>0 and p["MOTOR_OD"]>0
    motor_x=(p["MOTOR_FACE"]-p["MOTOR_LEN"],p["MOTOR_FACE"])
    axle_x=150.
    overlap=motor_x[0]<=axle_x<=motor_x[1]
    # Overlap in X projection is NOT a 3D collision: motor/shaft Z and Y required.
    assert overlap,"motor envelope moved; reassess X150 interference screen"
    pressure=0.7*0.1 # N/mm2 at 0.7 bar
    side_area=12145.804 # prior PR84 numerical screen, NOT OEM / not master solid
    side_force=pressure*side_area
    assert 840<side_force<860
    return {"status":"PASS_DATUM_ONLY","wheel_count":2*len(wheels),
        "Z50_count":2*len(gears),"motor_count_target":2,
        "motor_x_screen_mm":motor_x,"X150_in_motor_X_projection":overlap,
        "motor_center_axle_3D":"NOT_RUN: requires solids and 3D interference test",
        "side_cover_force_N_at_0_7bar_screen":round(side_force,2),
        "side_cover_area_source":"PR84 derived analytical screen; not OEM",
        "shaft_seal_0_7bar":"PHYSICAL_CHECK",
        "manufacturing_release":False}
if __name__=="__main__":
    print(json.dumps(check(),ensure_ascii=False,indent=2))
