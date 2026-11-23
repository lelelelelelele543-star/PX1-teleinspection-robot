"""DN150 integrated YZ envelope: reads current master without executing CAD."""
import ast,math,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
KEYS={"PIPE_R","WHEEL_CENTRE_Y","WHEEL_Z","WHEEL_CROWN_R","WHEEL_PROFILE","BODY_HALF_W_SCREEN","BODY_Z0","BODY_TOP","WHEEL_X","GEAR_X"}
def read_master():
    tree=ast.parse((HERE/"PX1_Current_Master.py").read_text(encoding="utf-8"))
    out={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name) and t.id in KEYS:out[t.id]=ast.literal_eval(node.value)
    if KEYS-set(out):raise ValueError("Missing: "+str(KEYS-set(out)))
    return out
def run():
    p=read_master(); R=p["PIPE_R"]; yc=p["WHEEL_CENTRE_Y"]; wz=p["WHEEL_Z"]
    cz=wz-p["WHEEL_CROWN_R"]+math.sqrt(R*R-yc*yc)
    half=p["BODY_HALF_W_SCREEN"]
    corners=[R-math.hypot(y,z-cz) for y in (-half,half) for z in (p["BODY_Z0"],p["BODY_TOP"])]
    lower=[];upper=[]
    for side in (-1,1):
        for rad,dy in p["WHEEL_PROFILE"]:
            y=side*(yc+dy)
            if abs(y)>=R:raise ValueError("Wheel y outside pipe")
            q=math.sqrt(R*R-y*y)
            lower.append(wz-rad-(cz-q));upper.append(cz+q-(wz+rad))
    status="PASS_ANALYTIC" if min(corners)>0 and min(lower)>=-1e-7 and min(upper)>=-1e-7 else "FAIL_ANALYTIC"
    result={"status":status,"pipe_ID_mm":2*R,"body_corner_radial_gap_mm":min(corners),"wheel_lower_gap_mm":min(lower),"wheel_upper_gap_mm":min(upper),"wheel_count":2*len(p["WHEEL_X"]),"gear_stations":2*len(p["GEAR_X"]),"NOT_RUN":["3D collisions","dynamic bends","tire deformation","sealing pressure","tolerances"]}
    s=3; X=350;Y=315
    pt=lambda y,z:(X+s*y,Y-s*(z-cz))
    bx,by=pt(-half,p["BODY_TOP"]); ex,ey=pt(half,p["BODY_Z0"])
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 680"><rect width="700" height="680" fill="#fafafa"/>',
    '<text x="25" y="32" font-family="sans-serif" font-size="20">PX1 DN150 — integrated transverse section</text>',
    '<text x="25" y="55" font-family="sans-serif" font-size="13">ANALYTIC 2D, not CAD render. Body rectangular envelope, wheel profile samples.</text>',
    f'<circle cx="{X}" cy="{Y}" r="{s*R}" fill="#e8f5ff" stroke="#216e9a" stroke-width="3"/>',
    f'<rect x="{bx}" y="{by}" width="{ex-bx}" height="{ey-by}" fill="#b7c5ce" stroke="#263746" stroke-width="2"/>']
    for side in (-1,1):
        samples=[(side*(yc+dy),wz-r) for r,dy in p["WHEEL_PROFILE"]]
        samples += [(side*(yc+dy),wz+r) for r,dy in reversed(p["WHEEL_PROFILE"])]
        coords=" ".join("%.2f,%.2f"%pt(y,z) for y,z in samples)
        svg.append(f'<polygon points="{coords}" fill="#f2a45e" fill-opacity=".7" stroke="#a65315" stroke-width="2"/>')
    svg.extend([f'<text x="25" y="605" font-family="monospace" font-size="15">Body corner clearance: {min(corners):.2f} mm</text>',
      f'<text x="25" y="630" font-family="monospace" font-size="15">Wheel lower clearance: {min(lower):.2f} mm (contact)</text>',
      f'<text x="25" y="655" font-family="monospace" font-size="15">{status}; 3D and tolerances NOT_RUN</text>','</svg>'])
    out=HERE/"previews";out.mkdir(exist_ok=True)
    (out/"PX1_dn150_integrated_section.svg").write_text("\n".join(svg),encoding="utf-8")
    (out/"PX1_dn150_integrated_section.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    if status!="PASS_ANALYTIC":raise SystemExit(1)
if __name__=="__main__":run()
