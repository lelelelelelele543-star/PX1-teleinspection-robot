#!/usr/bin/env python3
"""PX1 motor/centre-axle separation gate. Standard-library only.
Reads the canonical master; conservative radial clearance, NOT a BRep collision test.
"""
import ast
from pathlib import Path

MASTER = Path(__file__).with_name("PX1_Current_Master.py")
WANTED = {"MOTOR_OD", "MOTOR_LEN", "GEARHEAD_OD", "GEARHEAD_LEN",
          "MOTOR_FACE", "MOTOR_Y", "MIDDLE_INNER_Y", "WHEEL_X"}
tree = ast.parse(MASTER.read_text(encoding="utf-8"))
v = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in WANTED:
                try:
                    v[target.id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
assert WANTED <= v.keys(), f"Missing master constants: {WANTED - v.keys()}"
# Centre wheel shaft begins at |Y|=MIDDLE_INNER_Y. At X150 it faces
# the cylindrical motor body; gearhead begins farther rearward in X.
motor_start = v["MOTOR_FACE"] - v["GEARHEAD_LEN"] - v["MOTOR_LEN"]
motor_end = v["MOTOR_FACE"] - v["GEARHEAD_LEN"]
assert motor_end < 150 < v["MOTOR_FACE"], "Re-evaluate: centre station not inside gearhead X span"
assert v["WHEEL_X"][1] == 150
motor_body_outer_y = v["MOTOR_Y"] + v["GEARHEAD_OD"] / 2
clearance = v["MIDDLE_INNER_Y"] - motor_body_outer_y
print(f"Motor body X=[{motor_start:.2f},{motor_end:.2f}] mm; gearhead X=[{motor_end:.2f},{v['MOTOR_FACE']:.2f}]; centre axle X=150 mm")
print(f"Gearhead outer |Y|={motor_body_outer_y:.2f}; centre shaft inner |Y|={v['MIDDLE_INNER_Y']:.2f}")
print(f"Both sides: nominal gearhead-to-shaft radial gap={clearance:.2f} mm")
assert clearance > 0, "FAIL: gearhead envelope reaches centre axle inner end"
print("PASS: simplified gearhead and axle cylindrical envelopes do not overlap at centre station.")
print("NOT_RUN: exact BRep collisions, mounts, leads, dynamic clearance, tolerances.")
print("PHYSICAL_CHECK: purchased motor dimensions, bearings, shaft seals.")
