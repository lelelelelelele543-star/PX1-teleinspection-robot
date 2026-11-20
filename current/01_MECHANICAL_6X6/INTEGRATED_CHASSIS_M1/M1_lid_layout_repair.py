"""PX1 M1 corrected lid fastener layout, pure Python 3.10+.
Design assumptions only. Produces exact plan SVG and JSON gate on execution.
Do not interpret 2D clearance PASS as pressure or manufacturing qualification.
"""
import json, math
from pathlib import Path

P = dict(lid_L=200., lid_W=90., opening_L=170., opening_W=60.,
         gasket_outer_L=176., gasket_outer_W=66.,
         bolt_head_d=5.6, hole_d=3.4, min_edge_land=3.,
         min_gasket_head_clearance=1., pressure_bar=0.7)
BOLTS = [(x,y) for x in (-94.,94.) for y in (-39.,39.)]
BOLTS += [(0.,-39.),(0.,39.),(-94.,0.),(94.,0.)]
def rectangle_distance(x,y,L,W):
    return math.hypot(max(abs(x)-L/2,0),max(abs(y)-W/2,0))
def evaluate(p=P, bolts=BOLTS):
    checks={}
    def gate(k, ok, mm):
        checks[k]={"status":"PASS" if ok else "FAIL","value_mm":round(mm,3)}
    radius=p["bolt_head_d"]/2
    for i,(x,y) in enumerate(bolts,1):
        gasket_gap=rectangle_distance(x,y,p["gasket_outer_L"],p["gasket_outer_W"])-radius
        edge_gap=min(p["lid_L"]/2-abs(x),p["lid_W"]/2-abs(y))-radius
        opening_gap=rectangle_distance(x,y,p["opening_L"],p["opening_W"])-p["hole_d"]/2
        gate(f"bolt_{i}_gasket_head_gap",gasket_gap>=p["min_gasket_head_clearance"],gasket_gap)
        gate(f"bolt_{i}_lid_edge_gap",edge_gap>=p["min_edge_land"],edge_gap)
        gate(f"bolt_{i}_opening_hole_gap",opening_gap>=0,opening_gap)
    gate("gasket_band_x",(p["gasket_outer_L"]-p["opening_L"])/2>=3,(p["gasket_outer_L"]-p["opening_L"])/2)
    gate("gasket_band_y",(p["gasket_outer_W"]-p["opening_W"])/2>=3,(p["gasket_outer_W"]-p["opening_W"])/2)
    return {"status":"PASS" if all(c["status"]=="PASS" for c in checks.values()) else "FAIL",
            "checks":checks,"bolts_mm":bolts,"assumptions":p,
            "pressure_force_N":round(p["pressure_bar"]*1e5*p["opening_L"]*p["opening_W"]*1e-6,2),
            "not_run":["FreeCAD solid Boolean","fastener preload and gasket compression","shaft seals at 0.7 bar","physical leak test"]}
def svg(p=P, bolts=BOLTS):
    # Scale 3 px/mm; centered geometry is derived directly from the same coordinates as gate.
    s=3; cx=360; cy=190
    def rect(L,W,fill,stroke,dash=""):
        return f'<rect x="{cx-L*s/2}" y="{cy-W*s/2}" width="{L*s}" height="{W*s}" fill="{fill}" stroke="{stroke}" stroke-width="2" {dash}/>'
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="430" viewBox="0 0 720 430">',
         '<rect width="720" height="430" fill="#fff"/>',
         '<text x="30" y="28" font-size="18" font-family="sans-serif">PX1 M1 | lid fastener correction | DESIGN ASSUMPTIONS</text>',
         '<text x="30" y="48" font-size="12" font-family="sans-serif">True parametric 2D plan; NOT FreeCAD CAD / not pressure-qualified</text>',
         rect(p["lid_L"],p["lid_W"],"#e5edf4","#334155"),
         rect(p["gasket_outer_L"],p["gasket_outer_W"],"#b6e4c7","#17803d"),
         rect(p["opening_L"],p["opening_W"],"#ffffff","#b45309")]
    for x,y in bolts:
        out.append(f'<circle cx="{cx+x*s}" cy="{cy-y*s}" r="{p["bolt_head_d"]*s/2}" fill="#e88e8e" fill-opacity=".7" stroke="#a32222" stroke-width="1.5"/>')
        out.append(f'<circle cx="{cx+x*s}" cy="{cy-y*s}" r="{p["hole_d"]*s/2}" fill="white" stroke="#a32222"/>')
    out += ['<text x="30" y="365" font-size="13" font-family="sans-serif">Lid 200 x 90 | gasket outer 176 x 66 | opening 170 x 60 mm</text>',
            '<text x="30" y="386" font-size="13" font-family="sans-serif">8 x M3 assumed, head dia 5.6 mm; bolt centers x = +/-94, 0; y = +/-39, 0</text>',
            '<text x="30" y="407" font-size="12" font-family="sans-serif">Green = gasket band; red = fastener head; white = aperture</text>','</svg>']
    return "\n".join(out)
if __name__=="__main__":
    root=Path(__file__).resolve().parent
    report=evaluate()
    (root/"M1_lid_layout_repair_result.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (root/"M1_lid_layout_repair.svg").write_text(svg(),encoding="utf-8")
    print(json.dumps({"status":report["status"],"checks":len(report["checks"]),"min_clearance_mm":min(c["value_mm"] for c in report["checks"].values())},indent=2))
    if report["status"]!="PASS": raise SystemExit(2)
