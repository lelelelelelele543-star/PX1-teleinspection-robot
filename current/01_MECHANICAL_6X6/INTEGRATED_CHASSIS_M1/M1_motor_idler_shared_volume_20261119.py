"""PX1 M1 integrated motor/idler collision witness. Standard Python 3 only.
Coordinates read from the existing M1 FreeCAD generator design assumptions.
This test deliberately FAILS while a real shared-volume collision exists.
"""
import ast, math, pathlib, re, sys
src=pathlib.Path(__file__).with_name("PX1_Integrated_6x6_M1_interface_repair.py").read_text(encoding="utf-8")
tree=ast.parse(src)
pnode=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
# Parse the original dict() declaration; only numerical literals/tuples are needed.
P={kw.arg:ast.literal_eval(kw.value) for kw in pnode.value.keywords}
assert P["motor_D"]==22 and P["motor_L"]==42 and P["motor_y"]==14 and P["motor_z"]==10
# The current generator uses motor X=35..77 and idler stub X=+50, Y=19..34.
# Witness point (50,+/-21,3) is strictly INSIDE BOTH motor and idler stub.
for side in (-1,1):
    x,y,z=50.0,side*21.0,3.0
    motor_inside=(35<x<35+P["motor_L"] and (y-side*P["motor_y"])**2+(z-P["motor_z"])**2 < (P["motor_D"]/2)**2)
    stub_inside=(19<side*y<34 and (x-50)**2+(z-P["gear_z"])**2 < (P["axle_D"]/2)**2)
    assert motor_inside and stub_inside, "Witness invalid; re-evaluate current geometry"
    print("FAIL MOTOR_IDLER_SHARED_VOLUME side",side,"witness_mm",(x,y,z))
print("FAIL: Both motor envelopes intersect internal idler stubs at X=+50.")
print("NOT_RUN: FreeCAD Boolean volume and motor/idler-bearing collision sweep.")
print("DESIGN ASSUMPTIONS: motor and stub are nominal cylinders; actual mounting not validated.")
sys.exit(1)
