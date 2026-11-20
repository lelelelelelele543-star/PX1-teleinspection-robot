"""PX1 M1: full-tooth-pitch 2D Z50/Z50 mesh sweep; run with Python + shapely.
Uses the SAME involute_m1.profile() as the FreeCAD assembly. No FreeCAD needed.
Design assumption: module=1, Z=50, 50 mm center distance, alternate 3.6 deg phase.
"""
import json
from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
from involute_m1 import profile

gear=Polygon(profile(z=50,module=1.0))
assert gear.is_valid, "FAIL invalid involute outline"
angles=[i*7.2/72 for i in range(73)]
overlap=[]
for angle in angles:
    first=rotate(gear,angle,origin=(0,0))
    second=translate(rotate(gear,3.6-angle,origin=(0,0)),xoff=50.0)
    overlap.append(first.intersection(second).area)
peak=max(overlap)
result={"status":"PASS" if peak<1e-5 else "FAIL",
        "test":"Z50/Z50 external mesh 2D one tooth pitch",
        "samples":len(angles),"max_overlap_mm2":peak,
        "phase_deg":3.6,"module_mm":1.0,"center_distance_mm":50.0,
        "limitations":"2D outlines only; no 3D Boolean, backlash, root fillet, bearing play, strength or torque"}
print(json.dumps(result,indent=2))
assert result["status"]=="PASS", result
