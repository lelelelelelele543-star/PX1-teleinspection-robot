"""A47 two motor staggered envelope; dimensions assumed, plan view only."""
from pathlib import Path
import csv
P=Path(__file__).parent
radius=12.5; plate_inner=22.5; axis_y=8.5
motors=[("L",55,120,-axis_y),("R",150,215,axis_y)]
lateral=plate_inner-axis_y-radius
axial=motors[1][1]-motors[0][2]
assert abs(lateral-1.5)<1e-9 and axial==30
assert all(0<=a<b<=278 for _,a,b,_ in motors)
with (P/"results.csv").open("w",newline="") as f:
 w=csv.writer(f);w.writerow(["metric","mm","confidence"])
 w.writerows([["motor_diameter",25,"ASSUMED"],["motor_length",65,"ASSUMED"],["plate_inner_y",22.5,"A15_BASELINE"],["axis_abs_y",axis_y,"DESIGN_TARGET"],["lateral_clearance",lateral,"PASS_2D"],["axial_gap",axial,"PASS_2D"]])
s=4; X=lambda a:80+a*s; Y=lambda a:235-a*s
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="580" viewBox="0 0 1320 580">','<rect width="1320" height="580" fill="#f8fafc"/>','<text x="60" y="42" font-size="24" font-family="sans-serif">PX1 A47 — staggered motors: TOP VIEW / ASSUMED</text>']
svg.append(f'<rect x="{X(0)}" y="{Y(40)}" width="{278*s}" height="{80*s}" fill="#e2e8f0" stroke="#64748b"/>')
for sign in (-1,1):
 yy=Y(sign*plate_inner);svg.append(f'<line x1="{X(0)}" y1="{yy}" x2="{X(278)}" y2="{yy}" stroke="#64748b" stroke-width="4" stroke-dasharray="9 5"/>')
for name,a,b,cy in motors:
 svg.append(f'<rect x="{X(a)}" y="{Y(cy+radius)}" width="{(b-a)*s}" height="{25*s}" rx="45" fill="#38bdf8" fill-opacity=".7" stroke="#0f172a" stroke-width="2"/>')
 svg.append(f'<text x="{X((a+b)/2)}" y="{Y(cy)}" font-family="sans-serif" text-anchor="middle">{name}: Ø25 × 65</text>')
svg.append(f'<text x="80" y="485" font-size="19" font-family="sans-serif">Nominal plate gap: {lateral} mm each side; longitudinal motor gap: {axial} mm</text>')
svg.append('<text x="80" y="520" font-size="16" font-family="sans-serif" fill="#9a3412">NOT MODELED: X250 input, gearbox, mounting, pressure shell, DN150, 3D collisions</text></svg>')
(P/"a47_preview.svg").write_text("\n".join(svg))
print("PASS 2D only; SKIPPED 3D CAD; NEEDS_PHYSICAL_CHECK")
