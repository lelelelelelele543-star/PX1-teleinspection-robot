"""A48 motor-to-rear-axle reach; assumed coordinates inherited from A47."""
from pathlib import Path
import csv
P=Path(__file__).parent
rear_x=250.0
motors={"L":(55.0,120.0),"R":(150.0,215.0)}
m,z1,z2=1.5,16,40
pitch_distance=m*(z1+z2)/2
reaches={side:rear_x-end for side,(_,end) in motors.items()}
assert pitch_distance==42.0
assert reaches=={"L":130.0,"R":35.0}
assert all(0<=start<end<rear_x<278 for start,end in motors.values())
with (P/"results.csv").open("w",newline="") as f:
 w=csv.writer(f);w.writerow(["parameter","value_mm","confidence"])
 w.writerow(["rear_axle_x",rear_x,"ASSUMED"])
 w.writerow(["Z16_Z40_spur_pitch_distance",pitch_distance,"DERIVED_IF_SPUR_m1.5"])
 for side,reach in reaches.items():w.writerow([side+"_motor_end_to_X250",reach,"DERIVED_A47"])
x=lambda a:90+a*3.5
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500">','<rect width="1200" height="500" fill="#f8fafc"/>','<text x="55" y="42" font-size="23" font-family="sans-serif">PX1 A48 — assumed motor-to-X250 axial reach</text>',f'<rect x="{x(0)}" y="100" width="{278*3.5}" height="250" fill="#e2e8f0" stroke="#64748b"/>',f'<line x1="{x(rear_x)}" y1="90" x2="{x(rear_x)}" y2="365" stroke="#dc2626" stroke-width="3" stroke-dasharray="8 5"/>',f'<text x="{x(rear_x)-10}" y="85" text-anchor="end" font-size="17">X250 assumed</text>']
for side,(start,end),y,color in [('L',motors['L'],145,'#0284c7'),('R',motors['R'],255,'#0d9488')]:
 svg.extend([f'<rect x="{x(start)}" y="{y}" width="{(end-start)*3.5}" height="45" rx="10" fill="{color}"/>',f'<text x="{x((start+end)/2)}" y="{y+28}" text-anchor="middle" font-size="17" fill="white">Motor {side}</text>',f'<line x1="{x(end)}" y1="{y+58}" x2="{x(rear_x)}" y2="{y+58}" stroke="#ea580c" stroke-width="3"/>',f'<text x="{x((end+rear_x)/2)}" y="{y+82}" text-anchor="middle" font-size="17">{reaches[side]:g} mm</text>'])
svg.extend(['<text x="60" y="404" font-size="18">Z16/Z40 spur pitch-center distance = 42 mm; NOT an axial coupling length</text>','<text x="60" y="440" font-size="16" fill="#9a3412">NOT MODELED: shaft couplings, bevel geometry, bearing fits, pressure shell, 3D collisions</text>','<text x="60" y="469" font-size="15">Assumptions only; not Proteus measurements or manufacturing CAD.</text></svg>'])
(P/"a48_preview.svg").write_text("\n".join(svg),encoding="utf-8")
print("PASS arithmetic; SKIPPED FreeCAD; NEEDS_PHYSICAL_CHECK")
