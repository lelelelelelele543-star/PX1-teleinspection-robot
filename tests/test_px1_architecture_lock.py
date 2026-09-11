"""PX-1 hard architecture regression guard.

This test deliberately fails if the active crawler master is reduced to four wheels,
two axles, a centre input, or another side-gear topology without an explicit revision.
"""

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "mechanical" / "cadquery" / "PX1_CRP150_Master_RevPR.py"


def assigned_literal(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found in active master")


def test_px1_is_three_axle_six_wheel():
    tree = ast.parse(MASTER.read_text(encoding="utf-8"))

    wheel_x = tuple(assigned_literal(tree, "WHEEL_X"))
    gear_x = tuple(assigned_literal(tree, "GEAR_X"))
    drive_x = float(assigned_literal(tree, "DRIVE_X"))
    spur_module = float(assigned_literal(tree, "SPUR_MODULE"))
    spur_z = int(assigned_literal(tree, "SPUR_Z"))

    assert wheel_x == (50.0, 150.0, 250.0), (
        "PX-1 HARD LOCK VIOLATION: active crawler must retain exactly three "
        "wheel stations per side at X50/X150/X250."
    )
    assert len(wheel_x) == 3
    assert 2 * len(wheel_x) == 6

    assert gear_x == (50.0, 100.0, 150.0, 200.0, 250.0), (
        "PX-1 HARD LOCK VIOLATION: each side must retain five equal Z50 gears."
    )
    assert len(gear_x) == 5
    assert all(abs((gear_x[i + 1] - gear_x[i]) - 50.0) < 1e-12 for i in range(4))

    assert drive_x == 250.0, (
        "PX-1 HARD LOCK VIOLATION: rear long axle X250 must remain side-drive input."
    )
    assert spur_module == 1.0
    assert spur_z == 50


def test_px1_architecture_document_exists():
    lock = ROOT / "docs" / "PX1_HARD_ARCHITECTURE_LOCK_6W_3AXLE.md"
    assert lock.exists(), "Hard architecture lock document must remain in repository"
