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
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="490" viewBox="0 0 1100 490">','<rect width="1100" height="490" fill="#f8fafc"/>','<style>text{font:15px sans-serif;fill:#172033}.h{font:bold 23px sans-serif}.note{font:13px sans-serif;fill:#526077}.gear{fill:#ffe4b5;stroke:#9a5c0a;stroke-width:2}.wheel{fill:#d1fae5;stroke:#176b4b;stroke-width:2}.motor{fill:#dbeafe;stroke:#2563eb;stroke-width:2}line{stroke:#334155;stroke-width:3}</style>','<text x="30" y="37" class="h">PX1 M1 | Six-wheel torque-path diagram (assumed)</text>','<text x="30" y="60" class="note">Connectivity and nominal ratio only. NOT a mechanical drawing, CAD render or proof of meshing.</text>']
 for row,side in enumerate(("L","R")):
  y=135+row*205
  s.append(f'<text x="30" y="{y+8}">{side} side</text>')
  xs=[155,285,415,545,675,805,935]
  for i in range(6):s.append(f'<line x1="{xs[i]+30}" y1="{y}" x2="{xs[i+1]-30}" y2="{y}"/>')
  labels=["Motor","Z16","Z40","Z50@250","Z50@200","Z50@150","Z50@100"]
  for i,(x,label) in enumerate(zip(xs,labels)):
   cls="motor" if i==0 else "gear"
   s.append(f'<rect class="{cls}" x="{x-48}" y="{y-23}" width="96" height="46" rx="9"/><text x="{x}" y="{y+5}" text-anchor="middle">{label}</text>')
  s.append(f'<text x="325" y="{y-40}" class="note">bevel mesh</text><text x="600" y="{y-40}" class="note">rigid hub + spur meshes (assumed)</text>')
  for x,station in [(545,250),(805,150),(935,50)]:
   s.append(f'<line x1="{x}" y1="{y+24}" x2="{x}" y2="{y+64}"/><rect class="wheel" x="{x-47}" y="{y+64}" width="94" height="32" rx="8"/><text x="{x}" y="{y+85}" text-anchor="middle">Wheel {station}</text>')
  s.append(f'<text x="960" y="{y+6}" class="note">Z50@50</text>')
 s.append('<text x="30" y="475" class="note">ASSUMPTIONS: 2 motors; 5 Z50/side; 16:40 input = 2.5:1; no pressure or tooth contact validation.</text></svg>')
 return "\n".join(s)
if __name__=="__main__":
 result=audit()
 (ROOT/"M1_six_wheel_powerpath.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
 (ROOT/"M1_six_wheel_powerpath.svg").write_text(svg(),encoding="utf-8")
 print(json.dumps({r["status"]:sum(x["status"]==r["status"] for x in result["results"]) for r in result["results"]},indent=2))
 assert sum(r["status"]=="FAIL" for r in result["results"])==0
