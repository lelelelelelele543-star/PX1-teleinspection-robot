"""PX1 A34 selective axial shim, assumed values only. Python 3 stdlib."""
from pathlib import Path
import csv
import xml.etree.ElementTree as ET
STACK=(28.0,0.40)  # nominal, half-range, assumed
SPAN=(28.8,0.15)   # changed from A33 to avoid impossible low-end clearance
SHIMS=[round(i/10,1) for i in range(14)]
TARGET=(0.10,0.30)
def select(stack,span):
    gap=span-stack
    options=[s for s in SHIMS if TARGET[0]-1e-8<=gap-s<=TARGET[1]+1e-8]
    return min(options,key=lambda s:abs(gap-s-0.2)) if options else None
def main():
    cases=[]
    for a in range(2760,2841):
        for b in range(2865,2896):
            stack=a/100;span=b/100
            shim=select(stack,span)
            assert shim is not None,(stack,span)
            play=round(span-stack-shim,6)
            assert 0.1-1e-8<=play<=0.3+1e-8
            cases.append(play)
    assert select(28,28.8)==0.6
    p=Path(__file__).parent
    scale=22;x=90
    blocks=[]
    for name,w,c in [('bearing L',8,'#76a9bc'),('spacer L',2,'#89b58d'),('Z50',8,'#e3b469'),('spacer R',2,'#89b58d'),('bearing R',8,'#76a9bc'),('shim',0.6,'#b68bd2')]:
        blocks.append(f'<rect x="{x:.2f}" y="116" width="{w*scale:.2f}" height="85" fill="{c}" stroke="#253443"/>')
        if w>=2:blocks.append(f'<text x="{x+w*scale/2:.2f}" y="110" font-size="11" text-anchor="middle">{name}</text>')
        x+=w*scale
    end=90+28.8*scale
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="355" viewBox="0 0 900 355"><rect width="900" height="355" fill="#fcfdff"/><g font-family="Arial,sans-serif" fill="#172938"><text x="30" y="35" font-size="22" font-weight="bold">PX1 A34 | X150 selectable axial shim</text><text x="30" y="59" font-size="13">PARAMETRIC 2D ENGINEERING DIAGRAM — ALL dimensions assumed, mm</text>{''.join(blocks)}<line x1="90" y1="90" x2="90" y2="210" stroke="#bb4b4b" stroke-width="3"/><line x1="{end:.2f}" y1="90" x2="{end:.2f}" y2="210" stroke="#bb4b4b" stroke-width="3"/><line x1="{x:.2f}" y1="194" x2="{end:.2f}" y2="194" stroke="#bb4b4b" stroke-width="2"/><text x="{(x+end)/2:.2f}" y="242" text-anchor="middle" font-size="12">endplay 0.20</text><text x="30" y="275" font-size="14">Nominal: stack 28.00 + shim 0.60 + endplay 0.20 = span 28.80</text><text x="30" y="302" font-size="14">Shim selection 0.0–1.3 mm / 0.1 mm step; measure actual assembly</text><text x="30" y="330" font-size="12">Retainers idealized. DIN 471 grooves, bearing contact and sealing NOT modeled.</text></g></svg>"""
    ET.fromstring(svg)
    (p/'px1_a34_preview.svg').write_text(svg,encoding='utf-8')
    print('PASS',len(cases),'cases; clearance',min(cases),max(cases))
if __name__=='__main__':main()
