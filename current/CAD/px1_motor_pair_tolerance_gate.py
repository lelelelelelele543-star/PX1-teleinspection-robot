#!/usr/bin/env python3
"""Integrated motor pair / middle shaft tolerance gate (stdlib only).
Reads datums from PX1_Current_Master.py without executing CadQuery.
This is an envelope screen, NOT a solid collision or manufacturing approval.
"""
import ast
from pathlib import Path
P=Path(__file__).with_name("PX1_Current_Master.py")
tree=ast.parse(P.read_text(encoding="utf-8"))
keys={"MOTOR_Y","GEARHEAD_OD","MOTOR_OD","MIDDLE_INNER_Y","MOTOR_FACE","GEARHEAD_LEN","WHEEL_X"}
v={}
for n in tree.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in keys:
                try: v[t.id]=ast.literal_eval(n.value)
                except (ValueError,TypeError): pass
assert keys <= v.keys(),f"Missing {keys-v.keys()}"
assert v["WHEEL_X"][1]==150
assert v["MOTOR_FACE"]-v["GEARHEAD_LEN"] < 150 < v["MOTOR_FACE"]
r=v["GEARHEAD_OD"]/2
y=v["MOTOR_Y"]
shaft=v["MIDDLE_INNER_Y"]
pair_gap=2*(y-r)
shaft_gap=shaft-(y+r)
TARGET=1.0 # DESIGN ASSUMPTION: initial minimum nominal envelope clearance in mm
required_shaft_inner=y+r+TARGET
required_y_for_shaft=shaft-r-TARGET
required_y_for_pair=r+TARGET/2
print(f"Gearhead pair gap: {pair_gap:.3f} mm")
print(f"Gearhead-to-middle-shaft gap, each side: {shaft_gap:.3f} mm")
print(f"Design target: {TARGET:.3f} mm each interface (ASSUMED; not tolerance stack)")
print(f"Motor Y required for pair: >= {required_y_for_pair:.3f} mm")
print(f"Motor Y required for shaft: <= {required_y_for_shaft:.3f} mm")
print(f"Proposed shaft inner |Y| >= {required_shaft_inner:.3f} mm if motor Y unchanged")
assert pair_gap>0 and shaft_gap>0,"FAIL: nominal envelope overlap"
print("PASS: nominal pair and middle-shaft envelope separation")
if pair_gap<TARGET or shaft_gap<TARGET:
    print("FAIL: assumed 1 mm target not achieved by current datums")
if required_y_for_pair>required_y_for_shaft:
    print("FAIL: moving both motors in Y alone cannot meet both 1 mm targets")
else:
    print("PASS: feasible Y interval for both target gaps")
print("NOT_RUN: BRep collisions, bearings after shaft shortening, motor fasteners, tolerances")
print("PHYSICAL_CHECK: purchased gearhead OD and shaft retention/pressure seals")
