"""A22 radial sensitivity. All dimensions assumed; mm. Python standard library."""
from pathlib import Path
R=13.4-.25
M=12.5+.25
def clearance(e=.2,tm=60):
    return R*(1+23e-6*(-30))-M*(1+12e-6*tm)-e
v=clearance()
assert abs(v-.1817465)<1e-8
assert abs(clearance(e=.2+v))<1e-8
assert clearance(e=.4)<0
print("PASS",v,"zero at e",.2+v,"negative at e=.4",clearance(e=.4))
print("SKIPPED 3D/FreeCAD; NEEDS_PHYSICAL_CHECK")
def svg():
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="540" viewBox="0 0 900 540"><rect width="900" height="540" fill="white"/><g font-family="Arial,sans-serif"><text x="40" y="40" font-size="23">PX1 A22: assumed radial clearance vs eccentricity</text><text x="40" y="68">Exact parametric 2D plot, not CAD or physical test</text>']
    for e in [i/10 for i in range(6)]:
        x=120+e*1200
        s.append(f'<line x1="{x}" y1="120" x2="{x}" y2="450" stroke="#ddd"/><text x="{x-10}" y="472">{e:.1f}</text>')
    for t in range(20,121,20):
        y=450-(t-20)*3
        s.append(f'<line x1="120" y1="{y}" x2="720" y2="{y}" stroke="#ddd"/><text x="80" y="{y+4}">{t}C</text>')
    for target,color in [(0,"#c22"),(.1,"#26c"),(.2,"#2a6")]:
        points=" ".join(f'{120+(clearance(e=0,tm=t)-target)*1200:.2f},{450-(t-20)*3:.2f}' for t in range(20,121,2))
        s.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
    s.extend(['<circle cx="360" cy="330" r="6" fill="black"/>','<text x="735" y="160" fill="#c22">0 mm</text><text x="735" y="190" fill="#26c">0.1 mm</text><text x="735" y="220" fill="#2a6">0.2 mm</text>',f'<text x="120" y="510">Baseline gap {v:.3f} mm; zero-gap eccentricity {(.2+v):.3f} mm at +60 C</text></g></svg>'])
    return "".join(s)
Path(__file__).with_name("px1_a22_preview.svg").write_text(svg(),encoding="utf-8")
