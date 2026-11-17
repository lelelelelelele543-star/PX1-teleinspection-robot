"""A55: straight bevel gear formative tooth count (Tredgold approximation).
Corrects A54's helical-gear cos(delta)^3 formula. Analytical only.
"""
import math, json
from pathlib import Path
P=Path(__file__).resolve().parent
M=1.5
Z1,Z2=16,40
ALPHA=math.radians(20)
R=M*math.hypot(Z1,Z2)/2
B=8.0
def gear(z,other):
    delta=math.atan2(z,other)
    formative=z/math.cos(delta) # straight bevel: NOT helical z/cos^3(delta)
    pitch=M*formative/2
    base=pitch*math.cos(ALPHA)
    tip=pitch+M
    return dict(z=z,delta_deg=math.degrees(delta),
                formative_teeth= formative,virtual_pitch_radius_mm=pitch,
                virtual_base_radius_mm=base,virtual_tip_radius_mm=tip,
                outer_pitch_radius_mm=M*z/2,
                inner_pitch_radius_mm=(R-B)*math.sin(delta))
g1,g2=gear(Z1,Z2),gear(Z2,Z1)
assert abs(g1["delta_deg"]+g2["delta_deg"]-90)<1e-10
assert abs(g1["formative_teeth"]-Z1/math.cos(math.atan2(Z1,Z2)))<1e-10
assert 0<B<=R/3
assert all(g["virtual_base_radius_mm"]<g["virtual_pitch_radius_mm"]<g["virtual_tip_radius_mm"] for g in (g1,g2))
result={"status":"PASS_ANALYTIC_ONLY","warning":"Formative equivalent spur approximation; no conjugate 3D bevel teeth, contact, backlash or strength verified","module_mm_assumed":M,"face_width_mm_assumed":B,"pressure_angle_deg_assumed":20,"cone_distance_mm":R,"gears":[g1,g2],"a54_correction":"For straight bevel virtual teeth z_v=z/cos(delta), not z/cos(delta)^3 (helical approximation)."}
(P/"a55_result.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
