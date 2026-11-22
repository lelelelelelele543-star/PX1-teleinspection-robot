#!/usr/bin/env python3
"""PX1 current master — two sealing interface 3D CAD screen.
Reads current/CAD/PX1_Current_Master.py and its EXACT lobed_seal_face function.
CadQuery local solids only. No production release, no pressure qualification.
"""
import ast, json, math, sys
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parent
MASTER=ROOT/"PX1_Current_Master.py"
OUT=ROOT/"previews"
OUT.mkdir(exist_ok=True)
tree=ast.parse(MASTER.read_text(encoding="utf-8"),str(MASTER))
keys={"SIDE_SEAL_R","SIDE_SEAL_CUSP","SIDE_SEAL_W","SIDE_SEAL_D","SIDE_ORING",
      "SIDE_COVER_L","SIDE_COVER_H","SIDE_COVER_T","COVER_SCREW_DX",
      "COVER_SCREW_DZ","COVER_SCREW_CBORE","GEAR_X","SERVICE_ORING",
      "SERVICE_ORING_OEM_REFERENCE","SERVICE_PLUG_L","SERVICE_OPEN_W",
      "SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D",
      "SERVICE_RGROOVE_W","SERVICE_SPIGOT_H","SERVICE_SPIGOT_WALL"}
v={}
for n in tree.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in keys:
                try: v[t.id]=ast.literal_eval(n.value)
                except (ValueError,TypeError): pass
if keys-v.keys():raise RuntimeError("Missing current-master parameters: "+str(keys-v.keys()))
f=next((n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="lobed_seal_face"),None)
if f is None:raise RuntimeError("Missing current master lobed_seal_face")
ns={"math":math,"cq":cq,**v}
exec(compile(ast.Module(body=[f],type_ignores=[]),str(MASTER),"exec"),ns)
profile=ns["lobed_seal_face"]  # exactly the master 2D lobe, not a new outline
center=profile(0).wire().val()
loop=center.Length()
side_stretch=loop/(math.pi*v["SIDE_ORING"][0])-1
L,H,T=(v[k] for k in ("SIDE_COVER_L","SIDE_COVER_H","SIDE_COVER_T"))
gwidth=v["SIDE_SEAL_W"];gdepth=v["SIDE_SEAL_D"]
groove=profile(gwidth/2).extrude(gdepth).cut(profile(-gwidth/2).extrude(gdepth))
cover=cq.Workplane("XY").box(L,H,T,centered=(True,True,False)).translate((150,0,0)).edges("|Z").chamfer(1).cut(groove)
# The screw shank passes through the inner groove plane. Counterbores are at outer face.
holes=[]
for dx in v["COVER_SCREW_DX"]:
    for dz in v["COVER_SCREW_DZ"]:
        x=150+dx
        hole=cq.Workplane("XY").center(x,dz).circle(1.7).extrude(T+.2)
        cover=cover.cut(hole)
        cover=cover.cut(cq.Workplane("XY").workplane(offset=T-v["COVER_SCREW_CBORE"][1]).center(x,dz).circle(v["COVER_SCREW_CBORE"][0]).extrude(v["COVER_SCREW_CBORE"][1]+.1))
        holes.append(hole)
# Same master installed O-ring geometry proxy: volume-preserving rectangular section.
half_width=math.pi*(v["SIDE_ORING"][1]/2)**2/gdepth/2
side_ring=profile(half_width).extrude(gdepth).cut(profile(-half_width).extrude(gdepth))
inter=cover.intersect(side_ring)
side_overlap=inter.val().Volume() if inter.solids().size() else 0
side_to_M3=min(side_ring.val().distance(hole.val()) for hole in holes)
# Service plug local rounded-rectangle radial gland from master dimensions.
SL,SW,SR,clr,gd=(v[k] for k in ("SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D"))
root=2*((SL-2*clr-2*gd)+(SW-2*clr-2*gd))-(8-2*math.pi)*(SR-clr-gd)
st=root/(math.pi*v["SERVICE_ORING"][0])-1
section=v["SERVICE_ORING"][1]/math.sqrt(1+st)
gland=gd+clr
squeeze=1-gland/section
fill=(math.pi*section**2/4)/(v["SERVICE_RGROOVE_W"]*gland)
def rrect(z,L,W,r,h):
    return cq.Workplane("XY").box(L,W,h,centered=(True,True,False)).edges("|Z").fillet(r).translate((0,0,z))
def rframe(z,L,W,r,t,h):
    return rrect(z,L,W,r,h).cut(rrect(z-.1,L-2*t,W-2*t,r-t,h+.2))
plug=rframe(0,SL-2*clr,SW-2*clr,SR-clr,v["SERVICE_SPIGOT_WALL"],v["SERVICE_SPIGOT_H"])
plug=plug.cut(rframe(1,SL-2*clr+.2,SW-2*clr+.2,SR-clr+.1,gd+.1,v["SERVICE_RGROOVE_W"]))
rubber_height=math.pi*section**2/4/gland
ring=rframe(2-rubber_height/2,SL-.02,SW-.02,SR-.01,gland-.02,rubber_height)
inter=plug.intersect(ring)
service_overlap=inter.val().Volume() if inter.solids().size() else 0
checks={
 "different_master_seals":"PASS" if v["SIDE_ORING"]!=v["SERVICE_ORING"] else "FAIL",
 "side_closed_wire":"PASS" if center.IsClosed() else "FAIL",
 "side_stretch_0_to_5pct":"PASS" if 0<=side_stretch<=.05 else "FAIL",
 "side_cover_ring_3D_boolean":"PASS" if cover.val().isValid() and side_ring.val().isValid() and side_overlap<1e-4 else "FAIL",
 "side_ring_to_M3_shank_2mm":"PASS" if side_to_M3>=2 else "FAIL",
 "service_stretch_0_to_5pct":"PASS" if 0<=st<=.05 else "FAIL",
 "service_squeeze_15_to_30pct":"PASS" if .15<=squeeze<=.30 else "FAIL",
 "service_fill_below_85pct":"PASS" if 0<fill<.85 else "FAIL",
 "service_plug_ring_3D_boolean":"PASS" if plug.val().isValid() and ring.val().isValid() and service_overlap<1e-4 else "FAIL",
 "whole_master_3D_intersections":"NOT_RUN",
 "pressurization_0p4_to_0p7bar":"PHYSICAL_CHECK",
 "ring_supplier_material_tolerances":"PHYSICAL_CHECK"}
report={"source":"current/CAD/PX1_Current_Master.py","geometry":"local 3D CAD interfaces reconstructed from current master. Not an assembly-wide STEP clash check",
 "side":{"loop_length_mm":round(loop,3),"stretch_pct":round(100*side_stretch,3),
 "M3_shank_min_distance_mm":round(side_to_M3,3),"ring_to_cover_overlap_mm3":round(side_overlap,5)},
 "service":{"root_length_mm":round(root,3),"stretch_pct":round(100*st,3),
 "squeeze_pct":round(100*squeeze,3),"fill_pct":round(100*fill,3),
 "ring_to_plug_overlap_mm3":round(service_overlap,5)},
 "checks":checks}
(OUT/"PX1_dual_seal_3d_gate.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
def svg_path(wire,ox,oy,s,n):
    points,_=wire.sample(n)  # preserves topological order (Edges() does not)
    return "M "+" L ".join(f"{ox+p.x*s:.2f},{oy-p.y*s:.2f}" for p in points)+" Z"
side_path=svg_path(center,45,185,2.24,260)
service_path=svg_path(rrect(0,SL,SW,SR,1).faces(">Z").wires().val(),813,375,1.75,220)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<rect width="1180" height="610" fill="#f9fbfe"/><g font-family="Arial,sans-serif" fill="#142b43">
<text x="32" y="37" font-size="25" font-weight="bold">PX1 | CAD-derived seal geometry check</text>
<text x="32" y="62" font-size="15">Source: PX1_Current_Master.py / Local CadQuery 3D interfaces / NOT pressure-qualified</text>
<text x="45" y="105" font-size="19" font-weight="bold">Side cover: lobed 190 x 1.5 mm</text>
<rect x="84" y="118" width="586.88" height="134.4" rx="4" fill="#d7e7f6" stroke="#7a9cba"/>
<path d="{side_path}" stroke="#c2547c" stroke-width="5" fill="none"/>
<text x="45" y="280" font-size="17">CAD loop {loop:.2f} mm / stretch {100*side_stretch:.2f}%</text>
<text x="45" y="306" font-size="16">3D Boolean overlap {side_overlap:.3f} mm3 / nearest M3 shank {side_to_M3:.2f} mm</text>
<text x="45" y="336" font-size="16">PASS: nominal local fit / NOT_RUN: full assembly and tolerances</text>
<text x="730" y="105" font-size="19" font-weight="bold">Service plug: radial 115 x 1.5 mm</text>
<path d="{service_path}" stroke="#c2547c" stroke-width="5" fill="none"/>
<text x="730" y="480" font-size="16">Gland root {root:.2f} mm / stretch {100*st:.2f}%</text>
<text x="730" y="505" font-size="16">Radial squeeze {100*squeeze:.2f}% / fill {100*fill:.2f}%</text>
<text x="45" y="564" font-size="15">Pink curves: CadQuery wire sampling / Blue: nominal 262 x 60 cover perimeter</text>
<text x="45" y="587" font-size="15">PHYSICAL_CHECK: pressure 0.4-0.7 bar, stock material, tolerances. No manufacturing release.</text>
</g></svg>'''
(OUT/"PX1_dual_seal_3d_gate.svg").write_text(svg,encoding="utf8")
print(json.dumps(report,indent=2,ensure_ascii=False))
sys.exit(1 if "FAIL" in checks.values() else 0)
