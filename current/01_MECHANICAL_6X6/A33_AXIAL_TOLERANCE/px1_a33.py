"""PX1 A33 axial stack worst-case tolerance calculation. stdlib Python 3.
ALL numerical tolerances are assumed design targets, not DIN/catalog data.
Coordinates are axial mm. No production release or pressure qualification.
"""
from pathlib import Path
import csv
import xml.etree.ElementTree as ET

# nominal, symmetric half-tolerance (mm), count
PARTS = {"bearing": (8.0, 0.10, 2),
         "spacer": (2.0, 0.05, 2),
         "gear": (8.0, 0.10, 1)}
RETAINER_SPAN = (28.60, 0.15)  # between opposed retaining faces, ASSUMED
def calculate():
    stack = sum(n * count for n, tol, count in PARTS.values())
    stack_tol = sum(tol * count for n, tol, count in PARTS.values())
    span, span_tol = RETAINER_SPAN
    return {"stack_nom": stack, "stack_min": stack-stack_tol,
            "stack_max": stack+stack_tol, "span_nom": span,
            "span_min": span-span_tol, "span_max": span+span_tol,
            "clear_nom": span-stack,
            "clear_min": span-span_tol-stack-stack_tol,
            "clear_max": span+span_tol-stack+stack_tol}
def verify(d):
    assert abs(d["stack_nom"]-28.0)<1e-9
    assert abs(d["clear_nom"]-0.60)<1e-9
    assert abs(d["clear_min"]-0.05)<1e-9
    assert abs(d["clear_max"]-1.15)<1e-9
    assert d["clear_min"]>0  # avoids nominal negative axial clearance
def render(d):
    # Exact scale for nominal lengths. Vertical offset is illustrative only.
    scale=22; x0=75
    blocks=[("Bearing L",8,"#76a9bc"),("Spacer L",2,"#8bbf8a"),
            ("Z50 gear",8,"#e4b568"),("Spacer R",2,"#8bbf8a"),
            ("Bearing R",8,"#76a9bc")]
    x=x0; shapes=[]
    for label,w,color in blocks:
        shapes.append(f'<rect x="{x:.1f}" y="125" width="{w*scale:.1f}" height="78" fill="{color}" stroke="#233040"/>')
        shapes.append(f'<text x="{x+w*scale/2:.1f}" y="115" font-size="11" text-anchor="middle">{label}</text>')
        x+=w*scale
    end=x0+RETAINER_SPAN[0]*scale
    shapes += [f'<line x1="{x0}" y1="90" x2="{x0}" y2="232" stroke="#bd5b4e" stroke-width="3"/>',
               f'<line x1="{end:.1f}" y1="90" x2="{end:.1f}" y2="232" stroke="#bd5b4e" stroke-width="3"/>',
               f'<line x1="{x:.1f}" y1="220" x2="{end:.1f}" y2="220" stroke="#bd5b4e" stroke-width="2"/>',
               f'<text x="{(x+end)/2:.1f}" y="244" text-anchor="middle" font-size="11">0.60</text>']
    txt=f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="360" viewBox="0 0 860 360">
<rect width="860" height="360" fill="#fbfcfe"/>
<g font-family="Arial, sans-serif" fill="#172938">
<text x="28" y="32" font-size="21" font-weight="bold">PX1 A33 — X150 axial tolerance stack</text>
<text x="28" y="55" font-size="13">Parametric 2D dimension diagram; ALL dimensions assumed, mm</text>
{''.join(shapes)}
<text x="28" y="280" font-size="14">Stack: 28.00 ± 0.50 mm; retainer-face span: 28.60 ± 0.15 mm</text>
<text x="28" y="303" font-size="14" font-weight="bold">Worst-case axial clearance: 0.05 … 1.15 mm (nominal 0.60)</text>
<text x="28" y="327" font-size="12">Red faces represent idealized retainers, NOT DIN 471 groove geometry.</text>
<text x="28" y="345" font-size="12">Bearing inner-race contact, preload, clip deformation, gear backlash: NOT validated.</text>
</g></svg>"""
    ET.fromstring(txt)
    Path(__file__).with_name("px1_a33_preview.svg").write_text(txt,encoding="utf-8")
if __name__=="__main__":
    d=calculate();verify(d);render(d)
    print("PASS",d)
    print("NEEDS_PHYSICAL_CHECK: clip grooves, axial endplay, bearing fits, pressure sealing")
