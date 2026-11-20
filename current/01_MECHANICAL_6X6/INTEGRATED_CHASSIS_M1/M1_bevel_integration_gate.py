"""PX1 M1 rear bevel interface gate. Standard Python 3; geometric proxies, mm.
Checks lateral overlaps on BOTH sides. Not a gear-contact or FreeCAD validation.
"""
import json, math
from pathlib import Path
out=Path(__file__).with_suffix(".json")
checks=[]
for side in (-1,1):
    tag="L" if side<0 else "R"
    # From PX1_Integrated_6x6_M1_interface_repair.py
    def interval(a,b): return sorted((a,b))
    z50=interval(side*30-3,side*30+3)
    bevel=interval(side*24,side*32)
    bearing=interval(side*31,side*38)
    axle=interval(side*29,side*58)
    for name,other,radius in (("Z50",z50,27.5),("bearing",bearing,11),("axle",axle,5)):
        overlap=max(0,min(bevel[1],other[1])-max(bevel[0],other[0]))
        # All rear components have same x=110 and z=0. Bearing/axle are
        # solid proxies; a final shaft/bearing bore is still required.
        vol=round(math.pi*radius**2*overlap,2)
        checks.append(dict(side=tag,bevel_vs=name,overlap_y_mm=overlap,
                           proxy_overlap_mm3=vol,status="FAIL" if overlap>0 else "PASS"))
report=dict(status="FAIL" if any(x["status"]=="FAIL" for x in checks) else "PASS",
            checks=checks,freecad="NOT_RUN",step="NOT_RUN",
            note="Solid proxy overlap; bevel/Z50 requires a redesigned input stage. Axle and bearing need actual bores and fits.")
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
