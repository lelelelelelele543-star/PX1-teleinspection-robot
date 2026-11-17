"""A53 analytical bevel tooth-sector proxy. Not a conjugate bevel tooth profile."""
import math,json
from pathlib import Path
P=Path(__file__).resolve().parent
M,Z1,Z2,B=1.5,16,40,8.0
R=M*math.hypot(Z1,Z2)/2
assert 0<B<R/3
gears=[]
for z,other in ((Z1,Z2),(Z2,Z1)):
    d=math.atan2(z,other); outer=M*z/2; inner=(R-B)*math.sin(d)
    gears.append(dict(teeth=z,cone_angle_deg=math.degrees(d),outer_pitch_radius_mm=outer,inner_pitch_radius_mm=inner,angular_tooth_halfwidth_rad=math.pi/(2*z)))
assert abs(sum(math.atan2(a,b) for a,b in ((Z1,Z2),(Z2,Z1)))-math.pi/2)<1e-12
assert all(g["inner_pitch_radius_mm"]<g["outer_pitch_radius_mm"] for g in gears)
result=dict(status="PASS_ANALYTIC_PROXY",assumed_module_mm=M,assumed_face_mm=B,cone_distance_mm=R,ratio=Z2/Z1,gears=gears,limitations=["Radial tooth sectors only: NOT involute bevel teeth","No contact/backlash/strength/3D intersection validation"])
(P/"a53_result.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
