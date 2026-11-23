#!/usr/bin/env python3
"""Conservative AABB screening from the single current CAD master; not a CAD collision test."""
import ast, json, math, sys
from pathlib import Path

MASTER = Path(__file__).with_name("PX1_Current_Master.py")
KEYS = ("WHEEL_X","MOTOR_OD","MOTOR_LEN","MOTOR_FACE","MOTOR_Y","WHEEL_Z")
def read_datums(path=MASTER):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    values = {}
    for n in tree.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try: values[n.targets[0].id]=ast.literal_eval(n.value)
            except (TypeError,ValueError,KeyError): pass
    return {k:values[k] for k in KEYS}
def overlap(a,b):
    dims=[max(0,min(a[i][1],b[i][1])-max(a[i][0],b[i][0])) for i in range(3)]
    return dims,math.prod(dims)
def run(p):
    rows=[]
    r=p["MOTOR_OD"]/2
    for side in (-1,1):
        y=side*p["MOTOR_Y"]; z=p["WHEEL_Z"]
        # ASSUMPTION: motor extends from MOTOR_FACE - MOTOR_LEN to MOTOR_FACE.
        # Check transformed manufacturer STEP bbox before any release.
        motor=((p["MOTOR_FACE"]-p["MOTOR_LEN"],p["MOTOR_FACE"]),(y-r,y+r),(z-r,z+r))
        for x in p["WHEEL_X"]:
            shaft=((x-6,x+6),tuple(sorted((side*23,side*39))),(z-6,z+6))
            dimensions,volume=overlap(motor,shaft)
            rows.append(dict(side=side,x=x,aabb_intersection_mm=dimensions,
                             aabb_intersection_mm3=round(volume,3),
                             result="POTENTIAL_COLLISION" if volume>0 else "AABB_CLEAR"))
    return rows
def render(p,rows):
    sx=lambda x:70+2*x
    sy=lambda y:255-2*y
    shapes=[]
    for side in (-1,1):
        y=side*p["MOTOR_Y"]; r=p["MOTOR_OD"]/2
        shapes.append(f'<rect x="{sx(p["MOTOR_FACE"]-p["MOTOR_LEN"]):.1f}" y="{sy(y+r):.1f}" width="{2*p["MOTOR_LEN"]:.1f}" height="{4*r:.1f}" fill="#f59e0b" fill-opacity=".45" stroke="#b45309" stroke-width="2"/>')
        for x in p["WHEEL_X"]:
            lo,hi=sorted((side*23,side*39))
            shapes.append(f'<rect x="{sx(x-6):.1f}" y="{sy(hi):.1f}" width="24" height="{2*(hi-lo):.1f}" fill="#2563eb" fill-opacity=".38" stroke="#1d4ed8"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="850" height="500" viewBox="0 0 850 500">'
            '<rect width="850" height="500" fill="#fafafa"/>'
            '<text x="38" y="43" font-family="sans-serif" font-size="24" font-weight="bold">PX1 motor / axle envelope screen</text>'
            '<text x="38" y="70" font-family="sans-serif" font-size="14">Top view X/Y in mm. Amber: assumed motor box; blue: shaft boxes. NOT CAD collision.</text>'
            '<line x1="70" y1="255" x2="700" y2="255" stroke="#666" stroke-dasharray="5 5"/>'
            +''.join(shapes)+
            '<text x="38" y="405" font-family="sans-serif" font-size="15">Motor X141.7–195.5; wheel shafts X50 / X150 / X250</text>'
            '<text x="38" y="430" font-family="sans-serif" font-size="15">X150: bounding boxes overlap both sides; inspect actual STEP solids</text>'
            '<text x="38" y="456" font-family="sans-serif" font-size="13">DESIGN SCREEN · source current/CAD/PX1_Current_Master.py · shaft R6</text></svg>')
def main():
    p=read_datums();rows=run(p)
    assert len(rows)==6
    assert all(r["result"]=="POTENTIAL_COLLISION" for r in rows if r["x"]==150)
    assert all(r["result"]=="AABB_CLEAR" for r in rows if r["x"]!=150)
    target=Path(__file__).with_name("previews")/"px1_motor_axle_aabb.svg"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(render(p,rows),encoding="utf-8")
    print(json.dumps({"aabb":"PASS","true_solid_intersection":"NOT_RUN",
                      "motor_orientation":"ASSUMED","seal_pressure":"PHYSICAL_CHECK",
                      "results":rows},indent=2))
if __name__=="__main__":main()
