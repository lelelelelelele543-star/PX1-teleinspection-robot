#!/usr/bin/env python3
"""PX1 M1 six-wheel power-path graph audit. Standard-library only.
Conceptual kinematics, NOT tooth contact, structural or FreeCAD validation.
Run: python M1_six_wheel_powerpath.py
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ASSUMPTIONS={
 "motor_count":2,"wheel_count":6,"spur_station_count":10,
 "spur_teeth":50,"input_pinion_teeth":16,"input_bevel_teeth":40,
 "axles_x_mm":[50,150,250],
 "gear_x_mm":[50,100,150,200,250],
 "coupling":"Z40 rigidly keyed to rear Z50 (design assumption)",
 "spur_intermediates":"5 Z50 per side in a continuous train (design assumption)",
 "pressure_bar":[0.4,0.7],
}
def audit():
 results=[]
 def check(name,ok,detail):
  results.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
 nodes=set(); edges=[]
 for side in ("L","R"):
  m=f"{side}:MOTOR"; p=f"{side}:Z16"; b=f"{side}:Z40"
  nodes.update((m,p,b));edges.extend([(m,p,"shaft"),(p,b,"bevel_mesh")])
  gears=[f"{side}:Z50@{x}" for x in ASSUMPTIONS["gear_x_mm"]]
  nodes.update(gears);edges.append((b,gears[-1],"rigid_hub_assumed"))
  for a,c in zip(gears,gears[1:]):edges.append((a,c,"spur_mesh_assumed"))
  for x in ASSUMPTIONS["axles_x_mm"]:
   w=f"{side}:WHEEL@{x}";nodes.add(w)
   edges.append((f"{side}:Z50@{x}",w,"keyed_axle_assumed"))
  seen={m}; frontier=[m]
  while frontier:
   u=frontier.pop()
   for a,c,_ in edges:
    if a==u and c not in seen:seen.add(c);frontier.append(c)
    if c==u and a not in seen:seen.add(a);frontier.append(a)
  check(f"{side} all three wheels connected",all(f"{side}:WHEEL@{x}" in seen for x in ASSUMPTIONS["axles_x_mm"]),str(sorted(seen)))
 check("2 independent motors",len([n for n in nodes if n.endswith(":MOTOR")])==2,"one per side")
 check("6 wheel nodes",len([n for n in nodes if ":WHEEL@" in n])==6,"3 per side")
 check("10 Z50 nodes",len([n for n in nodes if ":Z50@" in n])==10,"5 per side")
 check("nominal input ratio",ASSUMPTIONS["input_bevel_teeth"]/ASSUMPTIONS["input_pinion_teeth"]==2.5,"40/16=2.5; spur Z50 idlers 1:1")
 check("pressure seal qualified",False,"NOT a validated pressure seal; select/test rated dynamic seal")
 results[-1]["status"]="PHYSICAL_CHECK"
 results.extend([
 {"check":"bevel tooth geometry/contact","status":"NOT_RUN","detail":"true bevel tooth surfaces and axis orientation unverified"},
 {"check":"intermediate gear shaft/bearing support","status":"NOT_RUN","detail":"solid supports and axial retention not yet audited"},
 {"check":"CAD Boolean intersections and STEP reopen","status":"NOT_RUN","detail":"requires FreeCAD execution"},
 {"check":"hub torque and key stress","status":"NOT_RUN","detail":"requires measured motor stall torque and selected key dimensions"},
 ])
 return {"model":"PX1 M1 conceptual power-path", "assumptions":ASSUMPTIONS,"nodes":sorted(nodes),"edges":[{"a":a,"b":b,"interface":k} for a,b,k in edges],"results":results}
def svg():
 """Two complete directed torque paths. Every Z50 station and wheel is drawn."""
 import html
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="1360" height="570" viewBox="0 0 1360 570">',
 '<rect width="1360" height="570" fill="#f8fafc"/>',
 '<style>text{font:15px sans-serif;fill:#172033}.h{font:bold 23px sans-serif}.note{font:13px sans-serif;fill:#526077}.gear{fill:#ffe4b5;stroke:#9a5c0a;stroke-width:2}.wheel{fill:#d1fae5;stroke:#176b4b;stroke-width:2}.motor{fill:#dbeafe;stroke:#2563eb;stroke-width:2}line{stroke:#334155;stroke-width:3}</style>',
 '<text x="30" y="38" class="h">PX1 M1 | Full 6-wheel conceptual torque path</text>',
 '<text x="30" y="62" class="note">Topology only, not spatial CAD: 5 Z50 per side, 3 wheels per side. All couplings assumed, tooth contact NOT_RUN.</text>']
 for row,side in enumerate(("L","R")):
  y=145+row*230
  xs=[120,250,380,530,680,830,980,1130]
  labels=["Motor","Z16","Z40","Z50@250","Z50@200","Z50@150","Z50@100","Z50@50"]
  s.append(f'<text x="25" y="{y-43}" class="h">{side} side</text>')
  for a,b in zip(xs,xs[1:]):
   s.append(f'<line x1="{a+47}" y1="{y}" x2="{b-47}" y2="{y}"/>')
  for i,(x,label) in enumerate(zip(xs,labels)):
   cls="motor" if i==0 else "gear"
   s.append(f'<rect class="{cls}" x="{x-49}" y="{y-24}" width="98" height="48" rx="8"/>')
   s.append(f'<text x="{x}" y="{y+5}" text-anchor="middle">{html.escape(label)}</text>')
  for x,station in ((530,250),(830,150),(1130,50)):
   s.append(f'<line x1="{x}" y1="{y+24}" x2="{x}" y2="{y+72}"/>')
   s.append(f'<rect class="wheel" x="{x-50}" y="{y+72}" width="100" height="34" rx="8"/>')
   s.append(f'<text x="{x}" y="{y+94}" text-anchor="middle">Wheel {station}</text>')
  s.append(f'<text class="note" x="250" y="{y-39}">Z16/Z40 bevel assumed</text>')
  s.append(f'<text class="note" x="595" y="{y-39}">Z40/Z50 rigid hub + 4 spur meshes assumed</text>')
 s.append('<text x="30" y="550" class="note">DESIGN ASSUMPTIONS: X stations 50/100/150/200/250 mm; 16:40 = 2.5:1; NOT_RUN: actual gears, bearings, pressure seals, 3D interference.</text>')
 s.append('</svg>')
 return "\\n".join(s)
def test_svg():
 """Fail if diagram omits, duplicates or mislabels any power-path station."""
 import xml.etree.ElementTree as ET
 root=ET.fromstring(svg())
 texts=[(node.text or "") for node in root.iter() if node.tag.endswith("text")]
 for label in ("Z50@250","Z50@200","Z50@150","Z50@100","Z50@50",
               "Wheel 250","Wheel 150","Wheel 50","Z16","Z40","Motor"):
  assert texts.count(label)==2, (label,texts.count(label))
 assert len([node for node in root.iter() if node.attrib.get("class")=="wheel"])==6
 assert len([node for node in root.iter() if node.attrib.get("class")=="gear"])==14
 return True
if __name__=="__main__":
 result=audit()
 assert test_svg(), "SVG power-path layout mismatch"
 (ROOT/"M1_six_wheel_powerpath.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
 (ROOT/"M1_six_wheel_powerpath.svg").write_text(svg(),encoding="utf-8")
 print(json.dumps({r["status"]:sum(x["status"]==r["status"] for x in result["results"]) for r in result["results"]},indent=2))
 assert sum(r["status"]=="FAIL" for r in result["results"])==0
