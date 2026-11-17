"""PX1 A52: assumed straight bevel pitch-cone face section (NOT teeth)."""
import math, json
from pathlib import Path
P=Path(__file__).resolve().parent
M,Z1,Z2,B=1.5,16,40,8.0
R=math.hypot(M*Z1/2,M*Z2/2)
A=math.atan2(Z1,Z2)
assert 0<B<R/3
r1=(R-B)*math.sin(A); r2=(R-B)*math.cos(A)
assert r1>0 and r2>0
result={"status":"PASS_GEOMETRY_ONLY","assumed_module_mm":M,"pinion_teeth":Z1,"wheel_teeth":Z2,"assumed_face_mm":B,"cone_distance_mm":R,"outer_pitch_radii_mm":[12,30],"inner_pitch_radii_mm":[r1,r2],"pitch_angles_deg":[math.degrees(A),90-math.degrees(A)],"warning":"No tooth profile, CAD solid, contact analysis or manufacturing approval"}
(P/"a52_result.json").write_text(json.dumps(result,indent=2)+"\n")
s=6; ox=120; oy=350
def p(x,y):return f"{ox+s*x:.2f},{oy-s*y:.2f}"
x,y=R*math.cos(A),R*math.sin(A)
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="540" viewBox="0 0 860 540"><rect width="860" height="540" fill="#fafafa"/><text x="30" y="38" font-family="sans-serif" font-size="22">PX1 A52 - Z16/Z40 pitch cones</text><text x="30" y="63" font-family="sans-serif" font-size="14">ASSUMED m=1.5, face=8 mm; section only; NO TEETH</text><line x1="70" y1="350" x2="680" y2="350" stroke="#666" stroke-dasharray="6 5"/><line x1="120" y1="480" x2="120" y2="85" stroke="#666" stroke-dasharray="6 5"/><path d="M {p(0,0)} L {p(x,y)} L {p(x,-y)} Z" fill="#f6c57d" fill-opacity=".3" stroke="#c77c11" stroke-width="2"/><path d="M {p(0,0)} L {p(x,y)} L {p(-x,y)} Z" fill="#8bc6ef" fill-opacity=".3" stroke="#2377a6" stroke-width="2"/><line x1="{ox+s*(R-B)*math.cos(A):.2f}" y1="{oy-s*(R-B)*math.sin(A):.2f}" x2="{ox+s*x:.2f}" y2="{oy-s*y:.2f}" stroke="#d22" stroke-width="6"/><text x="380" y="175" font-size="16">Common pitch generator</text><text x="380" y="205" font-size="16">R = {R:.3f} mm</text><text x="380" y="235" font-size="16">Angles = {math.degrees(A):.3f} / {90-math.degrees(A):.3f} deg</text><text x="380" y="265" font-size="16">Inner pitch radii = {r1:.3f} / {r2:.3f} mm</text><text x="30" y="510" font-size="14" fill="#a22">NEEDS PHYSICAL CHECK: tooth form, bearings, clearance, contact and shaft positions.</text></svg>"""
(P/"a52_preview.svg").write_text(svg)
print(json.dumps(result,indent=2))
