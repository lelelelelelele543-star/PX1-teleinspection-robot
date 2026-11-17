"""PX1 A51: preliminary 90-degree straight bevel input pitch geometry.
ASSUMED m=1.5 mm, z1=16, z2=40, shaft angle=90 degrees.
Pitch cones only; no generated teeth, no validated bearing/motor packaging.
"""
import math, json
from pathlib import Path
Z1,Z2,M=16,40,1.5
r1,r2=M*Z1/2,M*Z2/2
R=math.hypot(r1,r2)
d1,d2=math.atan2(Z1,Z2),math.atan2(Z2,Z1)
assert abs(d1+d2-math.pi/2)<1e-12
assert abs(R*math.sin(d1)-r1)<1e-10
assert abs(R*math.sin(d2)-r2)<1e-10
assert abs(math.hypot(r1,r2)-R)<1e-10
result={"status":"PASS_PITCH_CONES_ONLY","m_mm":M,"pinion_teeth":Z1,"wheel_teeth":Z2,"shaft_angle_deg":90,"pitch_radii_mm":[r1,r2],"cone_distance_mm":R,"pitch_angles_deg":[math.degrees(d1),math.degrees(d2)],"ratio":Z2/Z1}
Path(__file__).with_name("a51_result.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
