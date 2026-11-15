"""PX1 A21: radial motor-relief tolerance + thermal budget, mm. All inputs ASSUMED.
Run: python px1_a21.py ; writes px1_a21_preview.svg; standard library only.
Not a 3D collision or strength validation.
"""
import math
from pathlib import Path
P = dict(outer=29.5, outer_tol=.2, axis=13.5, axis_tol=.3,
         relief=13.4, relief_tol=.25, motor=12.5, motor_tol=.25,
         eccentricity=.2, dT_motor=60., dT_plate=-30.,
         alpha_motor=12e-6, alpha_plate=23e-6)
def budget(p):
    relief_min=p["relief"]-p["relief_tol"]
    motor_max=p["motor"]+p["motor_tol"]
    cold_relief=relief_min*(1+p["alpha_plate"]*p["dT_plate"])
    hot_motor=motor_max*(1+p["alpha_motor"]*p["dT_motor"])
    nominal=p["relief"]-p["motor"]
    tolerance=relief_min-motor_max
    thermal=cold_relief-hot_motor
    assembled=thermal-p["eccentricity"]
    web=p["outer"]-p["outer_tol"]-(p["axis"]+p["axis_tol"])-(p["relief"]+p["relief_tol"])
    return dict(nominal=nominal,tolerance=tolerance,thermal=thermal,assembled=assembled,web=web)
v=budget(P)
assert abs(v["nominal"]-.9)<1e-10
assert abs(v["tolerance"]-.4)<1e-10
assert .18<v["assembled"]<.19
assert abs(v["web"]-1.85)<1e-10
assert v["assembled"]>0
print("PASS nominal/tolerance/thermal/assembled/web:",v)
print("SKIPPED: 3D interference, finite element strength; NEEDS_PHYSICAL_CHECK: temperature, eccentricity, motor dimensions")
def svg(v):
    # Coordinates directly generated from the same numeric budget (100 px per mm).
    x0=110; scale=100; y=160; h=100
    segments=[("Worst-case tolerance",v["tolerance"],"#2563eb"),
              ("Thermal + eccentricity",v["assembled"],"#16a34a")]
    shapes=[]
    for i,(label,gap,color) in enumerate(segments):
        yy=y+i*140
        shapes.append(f'<text x="110" y="{yy-20}" font-size="18">{label}: {gap:.3f} mm</text>')
        shapes.append(f'<rect x="{x0}" y="{yy}" width="280" height="{h}" fill="#cbd5e1" stroke="#334155"/>')
        shapes.append(f'<rect x="{x0+280}" y="{yy}" width="{gap*scale:.3f}" height="{h}" fill="{color}"/>')
        shapes.append(f'<rect x="{x0+280+gap*scale:.3f}" y="{yy}" width="170" height="{h}" fill="#fbbf24" stroke="#92400e"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="850" height="540" viewBox="0 0 850 540">'
      '<rect width="850" height="540" fill="white"/><g font-family="Arial, sans-serif">'
      '<text x="35" y="40" font-size="24" font-weight="bold">PX1 A21 — motor relief radial clearance budget</text>'
      '<text x="35" y="70" font-size="15">ASSUMED inputs | exact parametric 1D radial stack | NOT CAD or physical test</text>'
      +''.join(shapes)+f'<text x="110" y="465" font-size="18">Minimum web (A20): {v["web"]:.2f} mm</text>'
      '<text x="110" y="495" font-size="15">Grey: relief reference | colored: calculated gap | yellow: motor envelope</text>'
      '</g></svg>')
Path(__file__).with_name("px1_a21_preview.svg").write_text(svg(v),encoding="utf-8")
