"""PX1 DN150 wheel-profile clearance audit against current CAD master.
Run: python current/CAD/PX1_dn150_wheel_clearance.py
Only analytic YZ section at wheel stations, NOT 3D collision clearance.
"""
import ast, math, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
MASTER=HERE/"PX1_Current_Master.py"
KEYS={"PIPE_R","WHEEL_CENTRE_Y","WHEEL_Z","WHEEL_CROWN_R","WHEEL_PROFILE","WHEEL_X"}
def read_parameters():
    tree=ast.parse(MASTER.read_text(encoding="utf-8"))
    out={}
    for n in tree.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            k=n.targets[0].id
            if k in KEYS:
                out[k]=ast.literal_eval(n.value)
    missing=KEYS-out.keys()
    if missing: raise ValueError("Missing master parameters: "+str(sorted(missing)))
    return out
def check():
    p=read_parameters()
    R=p["PIPE_R"]; yc=p["WHEEL_CENTRE_Y"]; zw=p["WHEEL_Z"]
    crown=p["WHEEL_CROWN_R"]
    zpipe=zw-crown+math.sqrt(R*R-yc*yc)
    rows=[]
    for r,dy in p["WHEEL_PROFILE"]:
        yy=yc+dy
        if abs(yy)>=R: raise AssertionError("Wheel outside pipe horizontal section")
        floor=zpipe-math.sqrt(R*R-yy*yy)
        roof=zpipe+math.sqrt(R*R-yy*yy)
        bottom=(zw-r)-floor
        top=roof-(zw+r)
        rows.append({"radius_mm":r,"offset_y_mm":dy,
                     "lower_clearance_mm":round(bottom,4),
                     "upper_clearance_mm":round(top,4)})
    assert len(p["WHEEL_X"])==3
    assert any(abs(x["offset_y_mm"])<1e-8 and abs(x["radius_mm"]-crown)<1e-8 for x in rows)
    assert min(x["lower_clearance_mm"] for x in rows)>=-0.01
    assert min(x["upper_clearance_mm"] for x in rows)>=-0.01
    result={"status":"PASS_ANALYTIC_ONLY","pipe_diameter_mm":2*R,
            "wheel_stations_per_side":len(p["WHEEL_X"]),
            "minimum_lower_clearance_mm":min(x["lower_clearance_mm"] for x in rows),
            "minimum_upper_clearance_mm":min(x["upper_clearance_mm"] for x in rows),
            "rows":rows,
            "not_run":["3D collision","tire deformation","dynamic pipe bends","manufacturing tolerances"]}
    print(json.dumps(result,indent=2))
    return result
if __name__=="__main__":check()
