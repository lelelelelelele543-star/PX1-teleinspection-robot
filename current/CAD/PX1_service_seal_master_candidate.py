#!/usr/bin/env python3
"""PX1 service plug: dependency-free analytical seal preview, NOT CAD or pressure test."""
from pathlib import Path
import ast, math, sys
MASTER=Path(__file__).with_name("PX1_Current_Master.py")
def literal(name):
    tree=ast.parse(MASTER.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id==name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)
def main():
    candidate=literal("SERVICE_ORING")
    reference=literal("SERVICE_ORING_OEM_REFERENCE")
    # From master geometry audit: root perimeter ~373.4 mm; read actual
    # computed value using a sandbox of numeric assignments only is avoided.
    # Root perimeter is an AUDIT INPUT, not a measured OEM dimension.
    perimeter=373.4
    stretch=lambda ring: perimeter/(math.pi*ring[0])-1
    assert reference==(110.,1.5)
    assert candidate==(115.,1.5)
    assert stretch(reference)>.05
    assert 0<stretch(candidate)<.05
    print("PASS_ANALYTIC: OEM stretch %.2f%%; PX1 candidate %.2f%%"%
          (100*stretch(reference),100*stretch(candidate)))
    print("NOT_RUN: FreeCAD/CadQuery geometry, seal gland fill, pressure test")
    out=Path(__file__).parent/"previews"/"PX1_service_seal_master_candidate.svg"
    out.parent.mkdir(parents=True,exist_ok=True)
    def ring(cx,diam,color):
        r=diam*1.5
        return f'<circle cx="{cx}" cy="190" r="{r:.2f}" fill="none" stroke="{color}" stroke-width="7"/>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480">
<rect width="1000" height="480" fill="#101b2a"/>
<g font-family="sans-serif" fill="#edf3fa">
<text x="40" y="48" font-size="26" font-weight="bold">PX1 / service plug — radial O-ring comparison</text>
<text x="40" y="80" font-size="16">Parameter-derived 2D diagram, NOT 3D CAD / NOT manufacturing drawing</text>
<text x="185" y="110" font-size="20">OEM reference: 110 × 1.5</text>
<text x="650" y="110" font-size="20">PX1 assumed: 115 × 1.5</text>
{ring(275,110,"#ee907c")}{ring(745,115,"#6fdfc6")}
<text x="175" y="390" font-size="19">Stretch: {stretch(reference)*100:.2f}% — FAIL (5% screen)</text>
<text x="635" y="390" font-size="19">Stretch: {stretch(candidate)*100:.2f}% — PASS (screen)</text>
<text x="40" y="442" font-size="15">Groove root perimeter: 373.4 mm (reconstructed / unverified). Side-cover seal 190 × 1.5 unchanged.</text>
<text x="40" y="464" font-size="15">Pressure 0.4–0.7 bar: NOT_RUN / PHYSICAL_CHECK. Ring supplier, gland fill, squeeze: NOT_RUN.</text>
</g></svg>'''
    out.write_text(svg,encoding="utf-8")
    print(out)
if __name__=="__main__": main()
