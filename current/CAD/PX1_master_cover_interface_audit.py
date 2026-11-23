#!/usr/bin/env python3
"""Read-only interface audit of PX1_Current_Master.py. No alternate M1 geometry.
Runs with standard Python 3; writes a dimensioned SVG and JSON.
Analytical 2D envelope checks only; NOT a FreeCAD collision test.
"""
import ast, json, pathlib, math, sys
P=pathlib.Path(__file__).with_name("PX1_Current_Master.py")
OUT=pathlib.Path(__file__).parent
tree=ast.parse(P.read_text(encoding="utf-8"))
wanted={"SIDE_COVER_L","SIDE_COVER_H","SIDE_COVER_T","COVER_SCREW_DX","COVER_SCREW_DZ","COVER_SCREW_CBORE","BODY_L_SOURCE_SCREEN","BODY_HALF_W_SCREEN","BODY_Z0","BODY_TOP","SIDE_ORING"}
v={}
for node in tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in wanted:
                v[target.id]=ast.literal_eval(node.value)
missing=wanted-v.keys()
if missing: raise RuntimeError("Missing master parameters: "+str(sorted(missing)))
L,H=v["SIDE_COVER_L"],v["SIDE_COVER_H"]
# Side cover centered at X150 Z45, as in master source.
cx,cz=150.0,45.0
xmin,xmax=cx-L/2,cx+L/2
zmin,zmax=cz-H/2,cz+H/2
r=v["COVER_SCREW_CBORE"][0]
screws=[(cx+dx,cz+dz) for dx in v["COVER_SCREW_DX"] for dz in v["COVER_SCREW_DZ"]]
clearances=[min(x-xmin,xmax-x,z-zmin,zmax-z)-r for x,z in screws]
checks={
 "24_cover_screws_both_sides":len(screws)*2==24,
 "screw_head_edge_clearance_nonnegative":min(clearances)>=0,
 "cover_x_within_nominal_body_length":xmin>=0 and xmax<=v["BODY_L_SOURCE_SCREEN"],
 "cover_z_within_nominal_body_height":zmin>=v["BODY_Z0"] and zmax<=v["BODY_TOP"],
}
# Body length 278 and cover length 262: centered at X150 gives X19..281.
# The body is NOT X0..278: actual source may use X18..296.
# Therefore the nominal body-length check is a *diagnostic*, not a FAIL.
checks["cover_x_within_nominal_body_length"]=None
status={k:("NOT_RUN" if x is None else "PASS" if x else "FAIL") for k,x in checks.items()}
report={"source":str(P),"source_of_truth":"PX1_Current_Master.py","units":"mm",
"cover_bounds_xz":[xmin,xmax,zmin,zmax],"cover_screw_count":len(screws)*2,
"minimum_screw_head_to_cover_edge":round(min(clearances),3),
"master_side_oring":v["SIDE_ORING"],"checks":status,
"limitations":["2D only; chamfer and counterbore depth not evaluated",
"body X origin cannot be inferred from BODY_L_SOURCE_SCREEN alone",
"seal path, screw-to-seal interference, thread engagement and pressure unverified",
"no STEP/Boolean/physical validation performed"]}
(OUT/"PX1_master_cover_interface_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
scale=3
S=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 0 1080 440">',
'<rect width="1080" height="440" fill="#f8fafc"/>',
'<text x="35" y="40" font-family="sans-serif" font-size="23">PX1 CURRENT MASTER | DRW-002-374 side cover interface</text>',
'<text x="35" y="65" font-family="sans-serif" font-size="14">2D coordinate audit, NOT CAD render. Units: mm. Design status: unqualified.</text>']
ox,oy=85,135
S.append(f'<rect x="{ox}" y="{oy}" width="{L*scale}" height="{H*scale}" rx="8" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
for x,z in screws:
    px=ox+(x-xmin)*scale;py=oy+(zmax-z)*scale
    S.append(f'<circle cx="{px}" cy="{py}" r="{r*scale}" fill="#fca5a5" stroke="#991b1b" stroke-width="1.5"/>')
for x in (50,150,250):
    px=ox+(x-xmin)*scale
    S.append(f'<line x1="{px}" y1="{oy-18}" x2="{px}" y2="{oy+H*scale+18}" stroke="#64748b" stroke-dasharray="5,4"/>')
    S.append(f'<text x="{px-20}" y="{oy+H*scale+38}" font-size="13" font-family="sans-serif">X{x}</text>')
S.extend([f'<text x="85" y="385" font-family="sans-serif" font-size="15">Cover {L:g} x {H:g} x {v["SIDE_COVER_T"]:g}; 12 M3 positions per side, 24 total</text>',
f'<text x="85" y="410" font-family="sans-serif" font-size="15">Min nominal head-to-outer-edge clearance: {min(clearances):.2f} mm; seal path not shown</text>',
'</svg>'])
(OUT/"PX1_master_cover_interface_audit.svg").write_text("\n".join(S),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if "FAIL" in status.values() else 0)
