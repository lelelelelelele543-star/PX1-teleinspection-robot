"""PX1 M1 drivetrain functional kinematics gate; Python standard library only.
Uses AGENTS.md 5x Z50 / side and existing M1 geometry; all numbers design assumptions.
Run: python M1_drivetrain_kinematics_gate.py
"""
from fractions import Fraction
from math import pi
import json
from pathlib import Path

P={"spur_teeth":50,"spur_stations_x_mm":[-100,-50,0,50,100],
   "wheel_stations_x_mm":[-100,0,100],"wheel_diameter_mm":78,
   "bevel_input_teeth":16,"bevel_output_teeth":40,
   "motor_rpm_assumed":66,"gear_module_mm_assumed":1.0,
   "wheel_outer_y_mm":60,"wheel_outer_z_mm":39,
   "pressure_target_bar":[0.4,0.7]}
checks={}
def gate(name,ok,details):
    checks[name]={"status":"PASS" if ok else "FAIL","details":details}
xs=P["spur_stations_x_mm"]
wheel_indices=[xs.index(x) for x in P["wheel_stations_x_mm"]]
gate("five_gears_per_side",len(xs)==5 and len(set(xs))==5,{"stations":xs})
gate("spur_pitch_centres",all(xs[i+1]-xs[i]==P["spur_teeth"]*P["gear_module_mm_assumed"] for i in range(4)),{"pitch_diameter_mm":50,"centre_distance_mm":50})
# External gear pairs reverse rotation; four meshes from rear to front.
signs=[(-1)**(4-i) for i in range(5)]
gate("three_wheel_same_rotation",len(set(signs[i] for i in wheel_indices))==1,{"gear_rotation_signs_front_to_rear":signs,"wheel_indices":wheel_indices})
ratio=Fraction(P["bevel_input_teeth"],P["bevel_output_teeth"])
wheel_rpm=P["motor_rpm_assumed"]*float(ratio)
speed_m_s=pi*(P["wheel_diameter_mm"]/1000)*wheel_rpm/60
gate("bevel_nominal_reduction",ratio==Fraction(2,5),{"ratio":str(ratio),"motor_rpm_ASSUMED":66,"wheel_rpm_no_load_ASSUMED":wheel_rpm,"ideal_ground_speed_m_s":round(speed_m_s,4)})
# This is a conservative rectangular corner, NOT a wheel/pipe traction simulation.
radial_clearance=75-(P["wheel_outer_y_mm"]**2+P["wheel_outer_z_mm"]**2)**0.5
gate("DN150_static_wheel_corner",radial_clearance>=2,{"radial_clearance_mm":round(radial_clearance,3),"minimum_design_mm":2})
# Critical missing functionality: source's motor shaft and bevel pitch proxies are not torque-qualified.
checks["motor_to_bevel_torque_joint"]={"status":"NOT_RUN","details":"Coaxial proxy overlap is not a keyed or otherwise torque-qualified coupling"}
checks["bevel_to_spur_torque_joint"]={"status":"NOT_RUN","details":"Z40/Z50 coaxial pitch proxies; actual hub/fastener load path unverified"}
checks["idler_bearing_rotation"]={"status":"NOT_RUN","details":"Bearing proxies do not demonstrate independent idler rotation under load"}
checks["pressure_shaft_seals"]={"status":"PHYSICAL_CHECK","details":"Six dynamic exits at 0.4-0.7 bar need rated seal design and bench test"}
result={"source":"AGENTS.md and PR83 integrated M1 source; NOT Proteus measurements",
        "assumptions":P,"checks":checks,
        "note":"Kinematic arithmetic PASS is not CAD collision, actual gear contact, or manufacturing approval"}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
assert all(v["status"]!="FAIL" for v in checks.values())
