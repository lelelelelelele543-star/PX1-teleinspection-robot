"""PX1 master-derived service-cover radial O-ring design audit.
Does not execute CadQuery. Design candidate 115x1.5 is NOT procurement verified.
"""
import ast, math, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
MASTER=HERE/"PX1_Current_Master.py"
def constants():
    tree=ast.parse(MASTER.read_text(encoding="utf-8"))
    names={"SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D","SERVICE_RGLAND_D","SERVICE_ORING"}
    result={}
    for n in tree.body:
        if isinstance(n,ast.Assign):
            for t in n.targets:
                if isinstance(t,ast.Name) and t.id in names:
                    try: result[t.id]=ast.literal_eval(n.value)
                    except (ValueError,TypeError): pass
    # SERVICE_RGLAND_D is an expression in the master, calculate from constituents.
    missing=(names-{"SERVICE_RGLAND_D"})-result.keys()
    if missing: raise ValueError("Master constants missing: "+str(missing))
    return result
def audit():
    p=constants()
    L=p["SERVICE_PLUG_L"]; W=p["SERVICE_OPEN_W"]; r=p["SERVICE_PLUG_R"]
    c=p["SERVICE_PLUG_CLR"]; d=p["SERVICE_RGROOVE_D"]
    root=2*((L-2*c-2*d)+(W-2*c-2*d))-(8-2*math.pi)*(r-c-d)
    gland=d+c
    rows=[]
    for label,ID,cs,source in [("current",*p["SERVICE_ORING"],"master part-list"),("candidate",115.0,1.5,"DESIGN ASSUMPTION; stock unverified")]:
        stretch=root/(math.pi*ID)-1
        cs_inst=cs/math.sqrt(1+stretch) if stretch>-1 else float("nan")
        squeeze=1-gland/cs_inst
        rows.append(dict(name=label,ID_mm=ID,CS_mm=cs,stretch_pct=round(100*stretch,3),
                         squeeze_pct=round(100*squeeze,3),status="PASS_ANALYTIC" if 0<=stretch<=0.05 and 0.15<=squeeze<=0.30 else "FAIL_ANALYTIC",source=source))
    result=dict(master=str(MASTER.name),root_perimeter_mm=round(root,3),radial_gland_mm=gland,
                candidates=rows,checks={"current":rows[0]["status"],"candidate":rows[1]["status"],
                "pressure":"PHYSICAL_CHECK","groove_fill":"NOT_RUN","seal_material":"NOT_RUN",
                "availability_115x1_5":"NOT_RUN","3D_cover_clearance":"NOT_RUN"})
    assert rows[0]["status"]=="FAIL_ANALYTIC"
    assert rows[1]["status"]=="PASS_ANALYTIC"
    return result
if __name__=="__main__":
    out=audit()
    path=HERE/"previews"/"PX1_service_radial_seal_audit.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
