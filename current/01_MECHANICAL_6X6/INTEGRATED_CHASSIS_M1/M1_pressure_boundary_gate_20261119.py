#!/usr/bin/env python3
"""PX1 integrated pressure-boundary and cover interface gate. Stdlib only.
Static source audit: no FreeCAD execution or physical qualification implied.
"""
import ast, pathlib, json, math
root=pathlib.Path(__file__).resolve().parent
src=(root/"PX1_Integrated_6x6_M1_interface_repair.py").read_text(encoding="utf8")
tree=ast.parse(src)
p=next({kw.arg:ast.literal_eval(kw.value) for kw in n.value.keywords} for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
checks=[]
def check(label,ok,detail):
    checks.append(dict(name=label,status="PASS" if ok else "FAIL",detail=detail))
check("wheel count",len(p["stations"])*2==6,"6 wheels across 2 sides")
check("gear count",len(p["gear_x"])*2==10,"10 pitch positions across 2 sides")
r=math.hypot(46+p["wheel_W"],p["wheel_D"]/2)
check("DN150 conservative clearance",r<=73,"radial clearance %.3f mm, target >=2 mm"%(75-r))
check("bearing holes", 'for xx in P["gear_x"]' in src and "cyl(11,5,(xx,sign*34,0)" in src,"ten Ø22 through-wall counterbores")
check("pressure boundary continuity",False,"10 through-wall Ø22 holes with bearing proxies; no qualified shaft seal geometry or pressure boundary")
check("lid compression",False,"lid starts z=36, gasket ends z=36: zero nominal squeeze; no screw clamp geometry")
check("lid load",abs(0.7*1e5*0.170*0.060-714)<1e-6,"714 N at 0.7 bar on 170x60 mm aperture")
checks.extend([dict(name="FreeCAD Boolean/STEP reopen",status="NOT_RUN",detail="Requires executing CAD generator and export/reimport"),dict(name="pressure qualification",status="PHYSICAL_CHECK",detail="Seal rating, runout, cover fasteners and controlled safe leak test")])
out={"scope":"static audit of existing integrated generator; NOT CAD execution","assumptions":{"pressure_bar":0.7,"cover_opening_mm":[170,60],"pipe_ID_mm":150},"checks":checks}
(root/"M1_pressure_boundary_gate_20261119.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
for c in checks: print(c["status"],c["name"],c["detail"])
raise SystemExit(2 if any(c["status"]=="FAIL" for c in checks) else 0)
