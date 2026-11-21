#!/usr/bin/env python3
"""PX1 integrated master regression: source datums + exact 2D plan; no STEP claims.
Run: python current/CAD/PX1_master_integration_regression.py
Reads only the current master; never imports it (import would execute CAD exports).
"""
import ast, pathlib, math, sys
P=pathlib.Path(__file__).with_name("PX1_Current_Master.py")
tree=ast.parse(P.read_text(encoding="utf-8"))
nodes={t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
def literal(k):
    try:return ast.literal_eval(nodes[k])
    except (KeyError,ValueError,TypeError) as e:raise RuntimeError("Cannot extract literal "+k) from e
wheel=literal("WHEEL_X"); gears=literal("GEAR_X")
errors=[]
def check(name,ok):print(("PASS" if ok else "FAIL"),name);errors.append(name) if not ok else None
check("3 wheel stations",wheel==(50.0,150.0,250.0))
check("5 gears per side",gears==(50.0,100.0,150.0,200.0,250.0))
check("wheel stations are gear stations",set(wheel).issubset(gears))
check("equal 50 mm gear pitch",all(abs(b-a-50)<1e-8 for a,b in zip(gears,gears[1:])))
check("side covers fit source body length",literal("SIDE_COVER_L")<=literal("BODY_L_SOURCE_SCREEN"))
check("side cover height 60",literal("SIDE_COVER_H")==60)
check("cover screw pitch six columns",literal("COVER_SCREW_DX")==(-125.,-75.,-25.,25.,75.,125.))
check("cover screw pitch two rows",literal("COVER_SCREW_DZ")==(-24.,24.))
check("nominal 24 side-cover fasteners",len(literal("COVER_SCREW_DX"))*len(literal("COVER_SCREW_DZ"))*2==24)
check("6x6 and 2 motors architecture source markers", "MOTOR_FACE=" in P.read_text() and "WHEEL_X=" in P.read_text())
print("SOURCE-ONLY: no Boolean/STEP, no manufacturing validation.")
sys.exit(bool(errors))
