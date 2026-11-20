"""PX1 M1 rear drive interface audit. Source-derived dimensions, NOT a FreeCAD solid test."""
import ast, json, math, pathlib
root=pathlib.Path(__file__).resolve().parent
src=(root/"PX1_Integrated_6x6_M1_interface_repair.py").read_text(encoding="utf-8")
tree=ast.parse(src)
pnode=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets))
P=dict(zip([k.arg for k in pnode.keywords],[ast.literal_eval(k.value) for k in pnode.keywords]))
motor_end=P["motor_x"]+P["motor_L"]
shaft_end=motor_end+88.
bevel_start=101.
bevel_end=109.
rear_x=P["gear_x"][-1]
# Projected axial envelopes: a bevel wheel is not a cylinder; this audit checks only the CAD proxies.
gap=bevel_start-shaft_end
# Z40 proxy spans Y=19..27; rear Z50 proxy spans Y=27..33 (right side).
# Actual geometry from source: Z50 at Y=30-3..30+3, Z40 at Y=19..27.
z40_y=(19.,27.)
z50_y=(P["gear_y"]-3.,P["gear_y"]+3.)
z40_z_radius=30.
z50_z_radius=P["gear_m"]*50/2
motor_z=P["motor_z"]
# Rear Z40 cylindrical proxy crosses shaft axis (X=100,Z=0), but Z16 has axis X and is centered at Z=18.
# Their tooth contact and center distance remain undefined.
checks={
 "motor_shaft_to_Z16_axial_gap_mm":round(gap,3),
 "motor_shaft_Z16_connection":"FAIL" if gap>0 else "PHYSICAL_CHECK",
 "rear_Z40_Z50_nominal_face_gap_mm":round(z50_y[0]-z40_y[1],3),
 "rear_Z40_Z50_torque_joint":"FAIL",
 "bevel_teeth_mesh":"NOT_RUN",
 "FreeCAD_boolean":"NOT_RUN",
 "STEP_roundtrip":"NOT_RUN",
 "pressure_seals":"PHYSICAL_CHECK"
}
assert abs(rear_x-100)<1e-9
assert gap==1.0, "Upstream geometry changed: reassess shaft coupling"
assert z40_y[1]==z50_y[0]
(root/"M1_rear_interface_audit_20261120.json").write_text(json.dumps({"design_assumptions":True,"checks":checks},indent=2),encoding="utf-8")
print(json.dumps(checks,indent=2))
