"""PX1 integrated interface gate: read CURRENT master, no duplicate CAD geometry.
Run: python current/CAD/PX1_integrated_interface_gate.py
Outputs current/CAD/previews/PX1_integrated_interface_gate.svg
Only static interface screening; not a CAD collision/pressure test.
"""
import ast, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MASTER=ROOT/"PX1_Current_Master.py"
def values():
    tree=ast.parse(MASTER.read_text(encoding="utf-8"))
    wanted={"WHEEL_X","GEAR_X","WHEEL_Z","PIPE_R","WHEEL_CENTRE_Y","WHEEL_CROWN_R",
            "BODY_TOP","BODY_Z0","MOTOR_OD","MOTOR_LEN","MOTOR_FACE",
            "SERVICE_ORING","SERVICE_ORING_STRETCH","SERVICE_RGLAND_D",
            "SERVICE_ORING_CS_INST","LIFT_A_Z","SIDE_COVER_L","SIDE_COVER_H"}
    out={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name not in wanted: continue
            try:
                out[name]=eval(compile(ast.Expression(node.value),str(MASTER),"eval"),
                               {"__builtins__":{},"math":math},out)
            except (NameError,TypeError,ValueError,AttributeError):
                pass
    return out
def run():
    p=values()
    required=("WHEEL_X","GEAR_X","WHEEL_Z","PIPE_R","WHEEL_CENTRE_Y",
              "WHEEL_CROWN_R","BODY_TOP","BODY_Z0","MOTOR_OD","MOTOR_LEN",
              "MOTOR_FACE","SERVICE_ORING","SERVICE_ORING_STRETCH",
              "SERVICE_RGLAND_D","SERVICE_ORING_CS_INST","LIFT_A_Z")
    missing=[k for k in required if k not in p]
    if missing: raise RuntimeError("Master changed, missing: "+", ".join(missing))
    assert len(p["WHEEL_X"])==3 and len(p["GEAR_X"])==5
    assert all(x in p["GEAR_X"] for x in p["WHEEL_X"])
    assert p["SERVICE_RGLAND_D"]>0
    R=p["PIPE_R"]; yc=p["WHEEL_CENTRE_Y"]; z=p["WHEEL_Z"]
    cz=z-p["WHEEL_CROWN_R"]+math.sqrt(R*R-yc*yc)
    crown=math.hypot(yc,cz-z)+p["WHEEL_CROWN_R"] # diagnostic only; not pipe clearance
    # The wheel contact point is along radial direction from pipe centre; radial wheel centre distance + crown R
    wheel_center_dist=math.hypot(yc,z-cz)
    contact_residual=wheel_center_dist+p["WHEEL_CROWN_R"]-R
    # A circle fully inside pipe must have distance-to-centre + radius <= pipe radius.
    checks={
      "3 wheels per side":len(p["WHEEL_X"])==3,
      "5 gear stations per side":len(p["GEAR_X"])==5,
      "wheel stations subset gear stations":all(x in p["GEAR_X"] for x in p["WHEEL_X"]),
      "wheel/pipe crown tangency":abs(contact_residual)<1e-6,
      "motor diameter below body height":p["MOTOR_OD"]<(p["BODY_TOP"]-p["BODY_Z0"]),
      "service O-ring stretch <=5% screen":p["SERVICE_ORING_STRETCH"]<=.05,
    }
    # SVG is a datum drawing, NOT a render of physical shapes
    X=lambda x:90+x*2.1
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 520">',
      '<rect width="920" height="520" fill="#fff"/>',
      '<g font-family="Arial,sans-serif" fill="#182536">',
      '<text x="45" y="37" font-size="22" font-weight="bold">PX1 — current master interface gate</text>',
      '<text x="45" y="62" font-size="13">Parametric datum view, NOT a 3D CAD render. Unverified dimensions remain design assumptions.</text>',
      '<text x="45" y="102" font-size="16">Top view: wheel and Z50 station axes (mm)</text>',
      '<rect x="128" y="145" width="584" height="136" rx="9" fill="#edf2f6" stroke="#34495e" stroke-width="2"/>']
    for x in p["GEAR_X"]:
        svg.append(f'<line x1="{X(x):.1f}" y1="130" x2="{X(x):.1f}" y2="295" stroke="#8394a5" stroke-dasharray="5 5"/>')
        svg.append(f'<text x="{X(x)-12:.1f}" y="121" font-size="12">X{x:g}</text>')
    for x in p["WHEEL_X"]:
        for y in (145,281):
            svg.append(f'<circle cx="{X(x):.1f}" cy="{y}" r="27" fill="#cad5df" stroke="#304960" stroke-width="2"/>')
            svg.append(f'<circle cx="{X(x):.1f}" cy="{y}" r="6" fill="#304960"/>')
    svg+=['<text x="46" y="331" font-size="13">6 wheels / 10 Z50 gear positions / 2 motors: datum-level representation only</text>',
      '<text x="46" y="369" font-size="16">Interface screens</text>']
    yy=397
    for name,ok in checks.items():
        svg.append(f'<text x="56" y="{yy}" font-size="13" fill="{"#12683b" if ok else "#b42318"}">{"PASS" if ok else "FAIL"} — {name}</text>')
        yy+=20
    svg.append(f'<text x="535" y="392" font-size="13">O-ring stretch: {100*p["SERVICE_ORING_STRETCH"]:.2f}% (screen limit 5%)</text>')
    svg.append(f'<text x="535" y="413" font-size="13">Radial gland: {p["SERVICE_RGLAND_D"]:.2f} mm; installed CS: {p["SERVICE_ORING_CS_INST"]:.2f} mm</text>')
    svg.append('<text x="535" y="438" font-size="13">NOT_RUN: solid collisions, STEP, pressure, motor fit</text>')
    svg.append('<text x="535" y="459" font-size="13">PHYSICAL_CHECK: seal compression &amp; leakage</text>')
    svg.append('</g></svg>')
    out=ROOT/"previews"/"PX1_integrated_interface_gate.svg"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(svg),encoding="utf-8")
    for name,ok in checks.items(): print(("PASS" if ok else "FAIL"),name)
    print("SVG",out)
    return checks
if __name__=="__main__": run()
