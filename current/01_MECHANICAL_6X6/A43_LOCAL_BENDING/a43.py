"""PX1 A43: local beam bending; all dimensions and forces are ASSUMED."""
import math,csv
from pathlib import Path
p=Path(__file__).parent
T=10.;m=1.5;z=50;d=11.;alpha=math.radians(20)
Ft=2000*T/(m*z);Fr=Ft*math.tan(alpha);F=math.hypot(Ft,Fr);R=F/2
def M(x):return R*max(0.,12.-abs(x))/1000
def vm(x):
    sigma=2*32*M(x)*1000/(math.pi*d**3)
    tau=2*16*T*1000/(math.pi*d**3)
    return math.hypot(sigma,math.sqrt(3)*tau)
assert abs(M(0)-1.7026844)<1e-5
assert M(-15)==M(15)==0
assert abs(vm(15)-132.5509)<.001
with (p/'a43_results.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['x_mm','bending_Nm','von_mises_MPa_assumed'])
    for x in range(-21,22):w.writerow([x,round(M(x),6),round(vm(x),4)])
pts=' '.join(f'{120+(x+21)*16:.1f},{300-M(x)*105:.1f}' for x in range(-21,22))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="480"><rect width="960" height="480" fill="#f8fafc"/><text x="30" y="43" font-size="25">PX1 A43 — X150 bending at grooves</text><text x="30" y="75" font-size="16">ASSUMED: bearings ±12 mm; gear 0; grooves ±15 mm; T=10 Nm</text><line x1="120" y1="150" x2="792" y2="150" stroke="#334155" stroke-width="12"/><circle cx="456" cy="150" r="35" fill="none" stroke="#64748b" stroke-width="7"/><path d="M264 175 l-15 23 h30 z M648 175 l-15 23 h30 z" fill="#0f766e"/><path d="M216 140 v20 M696 140 v20" stroke="#dc2626" stroke-width="5"/><text x="205" y="120" font-size="16">grooves</text><text x="427" y="108" font-size="16">Z50</text><line x1="120" y1="300" x2="792" y2="300" stroke="#64748b" stroke-width="2"/><polyline points="{pts}" fill="none" stroke="#2563eb" stroke-width="4"/><text x="30" y="280" font-size="16">M(x), Nm</text><text x="30" y="380" font-size="18">Mmax at gear: {M(0):.3f} Nm; M at grooves: 0 Nm (ideal model)</text><text x="30" y="412" font-size="18">Groove von Mises Kt=2: {vm(15):.2f} MPa (torsion only)</text><text x="30" y="450" font-size="15">Other gear forces, wheel loads and misalignment excluded. Not manufacturing-ready.</text></svg>'''
(p/'a43_preview.svg').write_text(svg)
print('PASS',F,R,M(0),vm(15))
