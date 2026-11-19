"""PX1 integrated motor/shaft envelope gate. No FreeCAD required; design assumptions only."""
import math,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
MOTOR=(-25.,17.); MR=11.; MY=14.; MZ=10.
def distance(x0,x1,y,z,ix,iy0,iy1,iz):
    dx=max(x0-ix,0,ix-x1)
    dy=max(iy0-y,0,y-iy1)
    return math.sqrt(dx*dx+dy*dy+(z-iz)**2)
checks={}
for side in (-1,1):
    for ix in (-50.,50.):
        iy0,iy1=sorted((side*19.,side*26.))
        c=distance(*MOTOR,side*MY,MZ,ix,iy0,iy1,0.)-22.
        checks[f"motor_{side}_idler_{ix:g}"]={"clearance_mm":round(c,3),"status":"PASS" if c>=2 else "FAIL"}
for ix in (-50.,50.):
    c=distance(17.,100.,0.,10.,ix,19.,26.,0.)-15.
    checks[f"central_shaft_idler_{ix:g}"]={"clearance_mm":round(c,3),"status":"PASS" if c>=2 else "FAIL"}
checks["motor_to_central_shaft"]={"status":"NOT_RUN","reason":"Missing transfer gears and bearings"}
checks["central_shaft_to_rear_bevel"]={"status":"NOT_RUN","reason":"Rear Z16 axis is y=+/-14, not y=0"}
checks["pressure_seals"]={"status":"PHYSICAL_CHECK","reason":"0.4-0.7 bar dynamic shaft seal not qualified"}
assert all(v["status"]=="PASS" for v in checks.values() if "clearance_mm" in v),checks
report={"assumptions":{"motor_x_mm":MOTOR,"motor_diameter_mm":22,"motor_y_abs_mm":MY,"motor_z_mm":MZ,"idler_radius_mm":11,"central_shaft_x_mm":[17,100],"central_shaft_y_mm":0,"central_shaft_z_mm":10,"central_shaft_diameter_mm":8,"clearance_target_mm":2},"checks":checks,"conclusion":"Envelope-only PASS; torque path NOT CLOSED; no 3D Boolean, gearing or pressure proof"}
(HERE/"M1_drive_path_gate.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
S=2.2; X=lambda x:360+S*x; Y=lambda y:175-S*y
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="440" viewBox="0 0 900 440">','<rect width="900" height="440" fill="#f8fafc"/>','<text x="35" y="36" font-family="sans-serif" font-size="20">PX1 M1 — integrated drivetrain XY feasibility</text>','<text x="35" y="58" font-family="sans-serif" font-size="13">DESIGN ASSUMPTIONS / schematic XY / NOT CAD or STEP</text>',f'<rect x="{X(-153.5)}" y="{Y(39)}" width="{307*S}" height="{78*S}" rx="12" fill="none" stroke="#64748b" stroke-width="2"/>']
for side in (-1,1):
 for x in (-100,0,100):
  svg.append(f'<circle cx="{X(x)}" cy="{Y(side*53)}" r="{39*S}" fill="#94a3b8" fill-opacity=".12" stroke="#64748b" stroke-dasharray="5 5"/>')
 for x in (-50,50):
  svg.append(f'<circle cx="{X(x)}" cy="{Y(side*22.5)}" r="{11*S}" fill="#f59e0b" fill-opacity=".5" stroke="#b45309"/>')
 svg.append(f'<rect x="{X(-25)}" y="{Y(side*14+11)}" width="{42*S}" height="{22*S}" fill="#2563eb" fill-opacity=".6" stroke="#1d4ed8"/>')
svg.append(f'<rect x="{X(17)}" y="{Y(4)}" width="{83*S}" height="{8*S}" fill="#16a34a" fill-opacity=".6" stroke="#15803d"/>')
svg+=['<text x="35" y="367" font-family="sans-serif" font-size="14">Blue: 2 motors Ø22×42, X -25..17; orange: internal idler bearing envelopes Ø22</text>','<text x="35" y="390" font-family="sans-serif" font-size="14">Green: central shaft Ø8, X 17..100; grey: wheel envelopes Ø78</text>','<text x="35" y="415" font-family="sans-serif" font-size="14" fill="#b91c1c">NOT BUILT: motor-to-shaft and shaft-to-rear-bevel torque transfer</text>','</svg>']
(HERE/"M1_drive_path_gate.svg").write_text("\n".join(svg),encoding="utf8")
print(json.dumps(report,ensure_ascii=False,indent=2))
