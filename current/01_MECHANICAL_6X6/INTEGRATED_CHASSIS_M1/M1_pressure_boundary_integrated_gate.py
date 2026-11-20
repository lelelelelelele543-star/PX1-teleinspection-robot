"""PX1 M1 pressure-boundary + drivetrain integration audit.
Run with stock Python 3: python M1_pressure_boundary_integrated_gate.py
Reads the EXISTING FreeCAD generator's literal P dictionary; no duplicate CAD constants.
Outputs deterministic SVG and JSON next to this file. Does not claim pressure certification.
"""
import ast, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE/"PX1_Integrated_6x6_M1_interface_repair.py"
def parameters():
    tree=ast.parse(SOURCE.read_text(encoding="utf-8"))
    assign=next(n for n in tree.body if isinstance(n,ast.Assign) and
                any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
    return ast.literal_eval(assign.value)
def audit(p):
    checks=[]
    def record(name,ok,detail,kind="geometry"):
        checks.append(dict(name=name,status="PASS" if ok else "FAIL",detail=detail,kind=kind))
    gear_x=p["gear_x"]; stations=p["stations"]
    record("6 wheel stations",len(stations)==3 and stations==(gear_x[0],gear_x[2],gear_x[4]),str(stations))
    record("10 gear positions",len(gear_x)==5 and all(abs(gear_x[i+1]-gear_x[i]-50)<1e-9 for i in range(4)),str(gear_x))
    clearance=75-math.hypot(46+p["wheel_W"],p["wheel_D"]/2)
    record("DN150 conservative wheel corner >=2mm",clearance>=2, f"{clearance:.3f} mm; conservative rectangular wheel envelope")
    shell=p["body_W"]/2; inner=shell-p["wall"]
    record("bearing counterbore penetrates shell",34<=inner and 34+5>=shell,f"shell y={inner:.1f}..{shell:.1f}, bore y=34..39")
    axial=46-(34+7)
    record("seal packaging 4mm +1mm",axial>=5,f"{axial:.1f} mm")
    gasket=p["lid_gasket_compression"]/p["lid_gasket_nominal"]
    record("nominal gasket overlap",0<gasket<1,f"{gasket:.0%}; material/fasteners NOT validated")
    force=.7*1e5*(.170*.060)
    # Existing model cuts ten sidewall bearing openings, but only SIX seal proxy rings.
    # Four idler bearing openings still connect dry body to atmosphere.
    record("all sidewall passages have modeled pressure seals",False,
           "10 Ø22 full-wall bores vs 6 external shaft-seal proxy rings; 4 idler positions unsealed", "pressure_boundary")
    record("pressure-qualified dynamic seals",False,
           "six annular proxy rings are not validated pressure-rated seals", "pressure_boundary")
    record("lid mechanical fastening",False,
           f"lid opening 170x60 mm, force {force:.0f} N at 0.7 bar; bolts/groove absent", "pressure_boundary")
    record("gear involute tooth geometry",False,
           "10 Z50 pitch cylinders are proxies, not involute teeth", "drivetrain")
    return checks,clearance,force
def svg(p,checks,clearance,force):
    # Deterministic 2D drawing from the same source parameters; NOT a CAD render.
    esc=lambda s: str(s).replace("&","&amp;").replace("<","&lt;")
    x0=90; scale=1.5; mid=285
    body_x=x0+(307-200)*scale/2
    body_w=200*scale
    circles=[]
    for x in p["gear_x"]:
        cx=mid+x*scale
        for cy in (135,355):
            circles.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="16.5" fill="#fce7d8" stroke="#b45309" stroke-width="2"/>')
            circles.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="5" fill="#fff" stroke="#92400e"/>')
    for x in p["stations"]:
        cx=mid+x*scale
        for cy in (94,396):
            circles.append(f'<rect x="{cx-10.5:.1f}" y="{cy-18}" width="21" height="36" rx="5" fill="#334155" stroke="#0f172a"/>')
    bad=[-50,50]
    for x in bad:
        cx=mid+x*scale
        for cy in (135,355):
            circles.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="23" fill="none" stroke="#dc2626" stroke-width="3" stroke-dasharray="6 4"/>')
    lines=[
      '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="640" viewBox="0 0 900 640">',
      '<rect width="900" height="640" fill="#fff"/>',
      '<text x="36" y="42" font-family="sans-serif" font-size="25" font-weight="bold">PX1 M1 — pressure boundary / 6×6 integration</text>',
      '<text x="36" y="67" font-family="sans-serif" font-size="15" fill="#475569">2D parameter drawing; NOT FreeCAD render. All dimensions design assumptions.</text>',
      '<rect x="54" y="112" width="462" height="276" rx="9" fill="#e2e8f0" stroke="#475569" stroke-width="3"/>',
      '<rect x="158" y="163" width="254" height="174" rx="5" fill="#f8fafc" stroke="#64748b" stroke-dasharray="7 5"/>',
      *circles,
      '<text x="558" y="126" font-family="sans-serif" font-size="17" font-weight="bold">10 sidewall bores Ø22</text>',
      '<text x="558" y="158" font-family="sans-serif" font-size="15">6 wheel seals: PROXY</text>',
      '<text x="558" y="189" font-family="sans-serif" font-size="15" fill="#b91c1c">4 idler bores: NO SEAL</text>',
      '<text x="558" y="220" font-family="sans-serif" font-size="15">2 motors; 10 Z50 pitch proxies</text>',
      f'<text x="558" y="251" font-family="sans-serif" font-size="15">DN150 margin: {clearance:.3f} mm</text>',
      f'<text x="558" y="282" font-family="sans-serif" font-size="15">Lid force @0.7 bar: {force:.0f} N</text>',
      '<text x="558" y="320" font-family="sans-serif" font-size="14" fill="#b91c1c">Red dashed: unsealed idler</text>',
      '<text x="558" y="342" font-family="sans-serif" font-size="14" fill="#b91c1c">bearing openings, both sides</text>',
      '<line x1="60" y1="450" x2="840" y2="450" stroke="#cbd5e1"/>',
      '<text x="60" y="485" font-family="sans-serif" font-size="19" font-weight="bold">FAIL — pressure boundary is open at four idler bearings</text>',
      '<text x="60" y="520" font-family="sans-serif" font-size="16">Recommended redesign: blind internal idler supports, no through-wall idler bores.</text>',
      '<text x="60" y="551" font-family="sans-serif" font-size="16">Then integrate six rated wheel-shaft seals and bolted lid with controlled gasket groove.</text>',
      '<text x="60" y="605" font-family="sans-serif" font-size="13" fill="#64748b">Static checks only. FreeCAD / STEP / motion / pressure test: NOT_RUN / PHYSICAL_CHECK.</text>',
      '</svg>'
    ]
    return "\n".join(lines)+"\n"
def main():
    p=parameters(); checks,clearance,force=audit(p)
    report={"source":SOURCE.name,"classification":"DESIGN_ASSUMPTIONS","checks":checks,
            "summary":{k:sum(c["status"]==k for c in checks) for k in ("PASS","FAIL")},
            "freecad":"NOT_RUN","step":"NOT_RUN","pressure_test":"PHYSICAL_CHECK"}
    (HERE/"M1_pressure_boundary_integrated_gate.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (HERE/"M1_pressure_boundary_integrated_gate.svg").write_text(svg(p,checks,clearance,force),encoding="utf-8")
    for c in checks: print(c["status"],c["name"],":",c["detail"])
    print("PASS audit executed; FAIL pressure boundary / drivetrain manufacturing readiness")
    return 0 # diagnostics are expected, keep CI able to collect artifacts
if __name__=="__main__": raise SystemExit(main())
