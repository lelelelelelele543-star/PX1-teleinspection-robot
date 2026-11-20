"""PX1 M1 involute flank feasibility and synchronized drivetrain station check.
Standard-library only: python M1_involute_contact_gate.py
2D analytical geometry; not a FreeCAD gear or a production-ready part.
"""
import math, json, pathlib
m,z,alpha=1.0,50,math.radians(20)
rp=m*z/2; rb=rp*math.cos(alpha); ra=rp+m; rf=rp-1.25*m
x=(-100,-50,0,50,100)
contact=(2*math.sqrt(ra**2-rb**2)-2*rp*math.sin(alpha))/(math.pi*m*math.cos(alpha))
checks={
 "gear_stations_10":len(x)*2==10,
 "wheel_stations_6":len(x[::2])*2==6,
 "center_distance":all(abs(x[i+1]-x[i]-m*z)<1e-8 for i in range(4)),
 "radii":0<rb<rf<rp<ra,
 "contact_ratio_ideal":contact>1,
 "body_length":max(x)+ra<307/2,
 "DN150_rectangular_wheel_bound":math.hypot(43+18,78/2)<=75,
}
result={"design_assumptions":{"module":m,"teeth":z,"pressure_angle_deg":20,"stations_mm":x,
"pitch_diameter_mm":2*rp,"base_diameter_mm":2*rb,"tip_diameter_mm":2*ra,
"root_diameter_mm":2*rf,"ideal_contact_ratio":contact},
"checks":{k:("PASS" if v else "FAIL") for k,v in checks.items()},
"NOT_RUN":["FreeCAD solids and STEP reopen","3D collision","gear strength/backlash",
"Z16-Z40 bevel mesh","shaft seal pressure","idler bearing seats"],
"PHYSICAL_CHECK":["pressure 0.4-0.7 bar","gear manufacturing tolerances"]}
pathlib.Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2),encoding="utf-8")
for k,v in result["checks"].items():print(v,k)
print("Ideal transverse contact ratio",round(contact,4))
assert all(checks.values())
