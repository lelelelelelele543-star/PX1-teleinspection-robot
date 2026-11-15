#!/usr/bin/env python3
"""PX1 A12: theoretical rack-generation undercut screening, not a tooth-contact test.
Assumed: standard full-depth 20-degree involute rack, ha*=1, module 1.5.
"""
import math
from pathlib import Path
M=1.5
ALPHA=math.radians(20)
Z_PINION,Z_WHEEL=16,40
def min_shift(z):
    return max(0.0,1.0-z*math.sin(ALPHA)**2/2.0)
def values():
    return {"pinion_z":Z_PINION,"wheel_z":Z_WHEEL,"module_mm":M,
      "standard_center_mm":M*(Z_PINION+Z_WHEEL)/2,
      "z_critical":2/math.sin(ALPHA)**2,
      "pinion_min_positive_shift":min_shift(Z_PINION),
      "wheel_min_positive_shift":min_shift(Z_WHEEL)}
def render_svg():
    d=values()
    w,h=760,450
    sx=lambda z: 85+(z-12)*25
    sy=lambda x: 370-x*950
    pts=" ".join(f"{sx(z):.2f},{sy(min_shift(z)):.2f}" for z in [12+i*.1 for i in range(281)])
    y0=sy(0)
    circles="".join(f'<circle cx="{sx(z)}" cy="{sy(min_shift(z)):.2f}" r="6" fill="{color}"/>' for z,color in [(16,"#d54b34"),(40,"#277c6d")])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" fill="#f7f9fc"/>
<text x="45" y="36" font-family="Arial" font-size="20" font-weight="bold">PX1 A12 — theoretical undercut screen, 20° full-depth rack</text>
<text x="45" y="59" font-family="Arial" font-size="13">ASSUMED geometry; not an actual tooth profile or production drawing</text>
<line x1="85" y1="90" x2="85" y2="370" stroke="#334155" stroke-width="2"/>
<line x1="85" y1="{y0}" x2="715" y2="{y0}" stroke="#334155" stroke-width="2"/>
<polyline points="{pts}" fill="none" stroke="#2463a5" stroke-width="3"/>
{circles}
<line x1="{sx(16)}" y1="90" x2="{sx(16)}" y2="370" stroke="#d54b34" stroke-dasharray="4,5"/>
<text x="{sx(16)+12}" y="120" font-size="14" fill="#a33220">Z16: x_min={d['pinion_min_positive_shift']:.4f}</text>
<text x="495" y="330" font-size="14" fill="#277c6d">Z40: x_min=0</text>
<text x="85" y="400" font-size="13">12 teeth</text><text x="625" y="400" font-size="13">40 teeth</text>
<text x="85" y="425" font-size="12">x_min=max(0, 1-z·sin²(20°)/2); rack-generation approximation</text>
<text x="80" y="85" font-size="12">min. positive shift x</text>
</svg>'''
def main():
    d=values()
    assert abs(d["standard_center_mm"]-42)<1e-10
    assert d["pinion_min_positive_shift"]>0
    assert d["wheel_min_positive_shift"]==0
    assert abs(d["z_critical"]-17.09726434)<1e-5
    Path(__file__).with_name("px1_a12_undercut_preview.svg").write_text(render_svg(),encoding="utf-8")
    for k,v in d.items(): print(f"{k}: {v:.7f}" if isinstance(v,float) else f"{k}: {v}")
    print("PASS: formula assertions; SKIPPED: gear generation, meshing, FreeCAD")
if __name__=="__main__": main()
