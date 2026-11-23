"""PX1 master seal identity guard. Standard Python only; no CAD export claim.
Run: python current/CAD/PX1_seal_identity_guard.py
Separates the lobed side cover seal from the rectangular service-plug seal.
"""
import ast, math, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE/"PX1_Current_Master.py"
def load():
    tree=ast.parse(SOURCE.read_text(encoding="utf8"))
    wanted={"SIDE_ORING","SERVICE_ORING","SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D","SIDE_SEAL_R","SIDE_SEAL_CUSP","SIDE_SEAL_W","SIDE_SEAL_D"}
    result={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in wanted:
                    try: result[target.id]=ast.literal_eval(node.value)
                    except (ValueError,TypeError): pass
    missing=wanted-result.keys()
    if missing: raise ValueError("Missing master constants: "+", ".join(sorted(missing)))
    return result
def audit(p):
    # SERVICE_* is a radial rectangular plug; SIDE_* is a lobed side-cover track.
    L,W,r,c,d=(p[k] for k in ("SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D"))
    perimeter=2*((L-2*c-2*d)+(W-2*c-2*d))-(8-2*math.pi)*(r-c-d)
    id0,cs=p["SERVICE_ORING"]
    stretch=perimeter/(math.pi*id0)-1
    installed_cs=cs/math.sqrt(1+stretch)
    gland=c+d
    squeeze=1-gland/installed_cs
    # A substitution of 115x1.5 can only concern SERVICE_ORING, never SIDE_ORING.
    candidate_stretch=perimeter/(math.pi*115)-1
    checks={
      "separate_master_seal_ids":"PASS" if p["SIDE_ORING"]!=p["SERVICE_ORING"] else "FAIL",
      "service_current_stretch_screen":"PASS" if 0<=stretch<=.05 else "FAIL",
      "service_candidate_115_stretch_screen":"PASS" if 0<=candidate_stretch<=.05 else "FAIL",
      "side_lobed_groove_3d_fit":"NOT_RUN",
      "service_groove_3d_fit":"NOT_RUN",
      "seal_stock_material_and_pressure":"PHYSICAL_CHECK",
    }
    return {"master":SOURCE.name,"side_cover":{"oring_id_cs_mm":p["SIDE_ORING"],"track":"lobed","replacement_from_service_audit":"PROHIBITED"},"service_plug":{"oring_id_cs_mm":p["SERVICE_ORING"],"track":"rounded_rectangle","track_perimeter_mm":round(perimeter,3),"stretch_pct":round(100*stretch,3),"squeeze_pct":round(100*squeeze,3),"candidate_115_stretch_pct":round(100*candidate_stretch,3),"candidate_115_status":"DESIGN_ASSUMPTION_NOT_RELEASED"},"checks":checks}
def svg(r):
    a=r["side_cover"]; b=r["service_plug"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="440" viewBox="0 0 1100 440">
<rect width="1100" height="440" fill="#ffffff"/>
<g font-family="Arial,sans-serif" fill="#172b43">
<text x="35" y="40" font-size="24" font-weight="bold">PX1 — two distinct sealing interfaces</text>
<text x="35" y="67" font-size="15">Master-derived identity diagram, NOT a CAD render. Sizes of sketches not to scale.</text>
<rect x="35" y="90" width="490" height="280" rx="14" fill="#eef4f9" stroke="#7b92a8"/>
<rect x="575" y="90" width="490" height="280" rx="14" fill="#f5f1e9" stroke="#a69577"/>
<text x="60" y="123" font-size="19" font-weight="bold">SIDE COVER — lobed track</text>
<path d="M100 225 Q125 155 170 200 Q220 245 265 200 Q310 155 355 200 Q410 245 465 190" fill="none" stroke="#1764a0" stroke-width="7"/>
<text x="60" y="290" font-size="18">SIDE_ORING: {a["oring_id_cs_mm"][0]:g} x {a["oring_id_cs_mm"][1]:g} mm</text>
<text x="60" y="322" font-size="14">NOT_RUN: groove fit / pressure / continuity</text>
<text x="600" y="123" font-size="19" font-weight="bold">SERVICE PLUG — rounded rectangle</text>
<rect x="680" y="165" width="260" height="80" rx="22" fill="none" stroke="#b36a18" stroke-width="7"/>
<text x="600" y="290" font-size="18">SERVICE_ORING: {b["oring_id_cs_mm"][0]:g} x {b["oring_id_cs_mm"][1]:g} mm</text>
<text x="600" y="318" font-size="14">Current stretch: {b["stretch_pct"]:.2f}% | 115 candidate: {b["candidate_115_stretch_pct"]:.2f}%</text>
<text x="600" y="343" font-size="14">Candidate unverified, no master modification</text>
<text x="35" y="405" font-size="16" font-weight="bold">DO NOT apply 115 x 1.5 service candidate to the 190 x 1.5 lobed side-cover seal.</text>
</g></svg>'''
if __name__=="__main__":
    r=audit(load())
    out=HERE/"previews"
    out.mkdir(exist_ok=True)
    (out/"PX1_seal_identity_guard.svg").write_text(svg(r),encoding="utf8")
    (out/"PX1_seal_identity_guard.json").write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding="utf8")
    print(json.dumps(r,indent=2,ensure_ascii=False))
    assert r["checks"]["separate_master_seal_ids"]=="PASS"
