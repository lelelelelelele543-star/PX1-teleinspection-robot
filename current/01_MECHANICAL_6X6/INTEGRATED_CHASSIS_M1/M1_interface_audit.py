"""PX1 M1 integrated interface audit. CPython 3, no CAD dependency.
All numbers are DESIGN ASSUMPTIONS taken from M1 PR81, not measured Proteus data.
Outputs SVG with geometric envelopes and machine-readable JSON. No STEP claim.
"""
import json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
P=dict(body_L=307.,body_W=80.,body_H=70.,wheel_D=78.,wheel_W=18.,
       stations=(-110.,0.,110.),gear_x=(-110.,-55.,0.,55.,110.),
       gear_m=1.1,gear_y=32.,gear_thick=6.,motor_D=22.,
       motor_y=16.,motor_x=(35.,97.),motor_z=10.,wheel_z=-5.)
checks=[]
def check(name,actual,limit,op="ge",detail=""):
    ok=actual>=limit if op=="ge" else actual<=limit
    checks.append(dict(name=name,status="PASS" if ok else "FAIL",actual_mm=round(actual,3),limit_mm=limit,detail=detail))
    return ok
wheel_radial=math.hypot(58,44)
check("DN150 wheel bounding envelope",wheel_radial,75,"le","Nominal 150mm internal diameter ASSUMED")
check("Adjacent wheel clearance",110-78,0)
check("Z50 pitch spacing",55-50*1.1,0)
# Existing M1 creates motor cylinder with literal radius 12 although P motor_D=22.
check("Motor radius matches parameter",abs(12-P["motor_D"]/2),0,"le","M1 code uses cyl(12,62), not P['motor_D']/2")
# M1 creates a bearing cylinder from y=36 to 43, and wheel from y=40 to 58.
check("Bearing vs wheel axial separation",40-43,0,"ge","3mm axial penetration of simplified solids, not an allowed mating")
# Wheel axle passes through side wall y=35..40, but M1 body shell has no axle bores.
check("Body axle passage",0,1,"ge","Six axle passages absent from body boolean")
# Gear proxy centered at y=32 and thickness 6 -> y=29..35; motor radius actual 12 centered y=16 -> reaches 28.
check("Motor to Z50 actual Y envelope",29-(16+12),2,"ge","Actual clearance 1mm, previous claimed 2mm used parameter Ø22")
# Body cavity top z30; motor top z22 (actual r12) so roof clearance 8mm
check("Motor roof clearance",30-(10+12),0)
data=dict(title="PX1 integrated M1 interface audit",confidence="ASSUMED",checks=checks,
          statuses=dict(PASS=sum(c["status"]=="PASS" for c in checks),FAIL=sum(c["status"]=="FAIL" for c in checks)),
          NOT_RUN=["FreeCAD Boolean intersection", "STEP reopen", "real gear tooth contact", "seal pressure qualification"],
          PHYSICAL_CHECK=["bearing fit", "0.4-0.7 bar dynamic shaft sealing", "pipe ovality/debris"])
(ROOT/"M1_interface_audit.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
# True parametric orthographic section, not a render. x is horizontal, y vertical in SVG.
scale=3
def rect(x,y,w,h,color,opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="{opacity}" stroke="#273341" stroke-width="1"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="650" viewBox="0 0 1050 650">',
'<rect width="1050" height="650" fill="#f7f9fc"/>',
'<text x="35" y="38" font-size="24" font-family="sans-serif">PX1 M1 — integrated geometry interface audit</text>',
'<text x="35" y="65" font-size="15" font-family="sans-serif">PARAMETRIC 2D / ASSUMED / not FreeCAD or production drawing</text>',
'<text x="35" y="108" font-size="18" font-family="sans-serif">Side elevation: six wheels and body (mm)</text>']
# side view X,Z: body from x=-153.5..153.5, z=-35..35
cx=520; cz=275
s.append(rect(cx-307*1.2/2,cz-70*1.2/2,307*1.2,70*1.2,"#8aa9c4",.65))
for x in P["stations"]:
    for side in (-1,1):
        s.append(f'<circle cx="{cx+x*1.2}" cy="{cz+5*1.2}" r="{39*1.2}" fill="{"#ce8c55" if side==1 else "#a85d38"}" fill-opacity=".35" stroke="#7d4426"/>')
s += ['<text x="35" y="390" font-size="18" font-family="sans-serif">Transverse section: motor / Z50 / wheel and bearing interfaces</text>']
# transverse: horizontal y, vertical z
cy=520; z0=520
s.append(f'<circle cx="{cy}" cy="{z0}" r="{75*1.2}" fill="none" stroke="#3186ca" stroke-width="3"/>')
s.append(rect(cy-40*1.2,z0-35*1.2,80*1.2,70*1.2,"#8aa9c4",.4))
for sign in (-1,1):
    y=sign*16
    s.append(f'<circle cx="{cy+y*1.2}" cy="{z0-10*1.2}" r="{12*1.2}" fill="#4d9970" fill-opacity=".75" stroke="#246344"/>')
    y=sign*32
    s.append(rect(cy+(y-3 if sign==1 else y-3)*1.2,z0-27.5*1.2,6*1.2,55*1.2,"#dd9650",.8))
    yy=sign*49
    s.append(rect(cy+(40 if sign==1 else -58)*1.2,z0-(39-5)*1.2,18*1.2,78*1.2,"#343b46",.65))
s += ['<text x="750" y="462" font-size="15" font-family="sans-serif">FAIL: motor radius hardcoded 12</text>',
'<text x="750" y="489" font-size="15" font-family="sans-serif">FAIL: bearing / wheel overlap 3 mm</text>',
'<text x="750" y="516" font-size="15" font-family="sans-serif">FAIL: axle bores absent in shell</text>',
'<text x="750" y="543" font-size="15" font-family="sans-serif">FAIL: motor / gear gap 1 mm vs 2 target</text>',
'<text x="35" y="630" font-size="13" font-family="sans-serif">Blue: body and DN150 boundary; green: motors; orange: Z50 envelopes; dark: wheel envelopes. Simplified, not tooth geometry.</text>','</svg>']
(ROOT/"M1_interface_audit.svg").write_text("\n".join(s),encoding="utf-8")
print(json.dumps(data["statuses"]))
if __name__=="__main__" and data["statuses"]["FAIL"]: print("AUDIT FAIL: integration requires correction; no manufacturing release")
