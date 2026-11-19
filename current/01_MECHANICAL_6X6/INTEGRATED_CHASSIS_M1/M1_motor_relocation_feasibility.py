"""PX1 M1 motor relocation feasibility, independent of FreeCAD. Units mm.
Design study only: avoids idler bearing envelopes but does NOT solve motor-to-bevel torque coupling.
Run: python M1_motor_relocation_feasibility.py
"""
import math, json, pathlib
HERE=pathlib.Path(__file__).resolve().parent
# Motor axes x=-30..12 (42 mm), y=+/-14, z=10. Existing x=35..77 collides x=50 idlers.
MOTOR=(-30.,12.); MOTOR_R=11.; IDLER_X=(-50.,50.); IDLER_R=11.
MOTOR_Y=14.; MOTOR_Z=10.; IDLER_Y=19.; IDLER_Z=0.
# Cylinder with axis X vs bearing cylinder with axis Y: conservative sphere-like bounding criterion.
# For guaranteed clearance use nearest Euclidean distance between their finite axis segments.
def distance_x_y(x0,x1,y_motor,z_motor,x_idler,y0,y1,z_idler):
    dx=max(x0-x_idler,0.,x_idler-x1)
    dy=max(y0-y_motor,0.,y_motor-y1)
    return math.sqrt(dx*dx+dy*dy+(z_motor-z_idler)**2)
results={}
for side in (-1,1):
    for x in IDLER_X:
        # Idler bearing spans Y=19..26, X extent radius 11, motor spans x -30..12.
        # Axis-segment distance compared to sum of cylinder radii is conservative.
        d=distance_x_y(*MOTOR,side*MOTOR_Y,MOTOR_Z,x,*sorted((side*19.,side*26.)),IDLER_Z)
        results[f"side_{side}_idler_{int(x)}"]={"axis_distance":round(d,3),"conservative_clearance":round(d-22,3)}
# Rear drive shaft on existing motor axis intersects x=50 idler: prove no complete fix yet.
shaft_axis_gap=math.hypot(MOTOR_Y-IDLER_Y,MOTOR_Z-IDLER_Z)- (4+11)
results["straight_output_shaft_vs_idler"]={"radial_clearance":round(shaft_axis_gap,3),"status":"FAIL"}
# Motor outer roof and side-to-side spacing.
results["motor_roof_clearance"]=30-(MOTOR_Z+MOTOR_R)
results["motor_pair_clearance"]=2*MOTOR_Y-2*MOTOR_R
results["motor_to_spur_clearance"]=27-(MOTOR_Y+MOTOR_R)
# A long intermediate shaft at y=0,z=10 has 6.47 mm conservative clearance to bearing.
results["central_jackshaft_vs_idler"]={"radial_clearance":round(math.hypot(19,10)-(4+11),3),"status":"GEOMETRY_ONLY"}
results["decision"]="Motor relocation alone does not close the power path. Need additional gear/coupling stage, real FreeCAD booleans and support mounts."
assert all(v["conservative_clearance"]>0 for k,v in results.items() if k.startswith("side_"))
assert results["straight_output_shaft_vs_idler"]["radial_clearance"]<0
assert results["motor_roof_clearance"]>=0 and results["motor_pair_clearance"]>=2
HERE.joinpath("M1_motor_relocation_feasibility.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results,indent=2))
