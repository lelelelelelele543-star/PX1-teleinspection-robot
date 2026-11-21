#!/usr/bin/env python3
"""Audit actual CAD render manifest; labels are uncertainty markers, not failures.
Run: python current/CAD/PX1_manifest_readiness_audit.py
No CadQuery dependency. Does NOT validate tolerances, sealing or STEP solids.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "previews/render_manifest.json").read_text(encoding="utf-8"))
views = {Path(v["file"]).name: v["shown_components"] for v in manifest["views"]}
full = views["px1_isometric.png"]
assert len(full) == len(set(full)), "Duplicate component names in full view"
assert len(full) >= 200, "Unexpectedly small assembly"
assert all(set(v).issubset(set(full)) for v in views.values()), "View has unknown components"
assert manifest["manufacturing_release"] is False, "Do not interpret render as manufacturing release"
checks = {
    "six_wheels": sum("HOLD_QRW90SR150_WHEEL_" in n for n in full) == 6,
    "two_traction_motors": sum(n.startswith("TRACTION_MOTOR_") for n in full) == 2,
    "ten_z50_gears": sum(n.startswith("HOLD_Z50_") for n in full) == 10,
    "two_side_covers": sum(n.startswith("HOLD_SIDE_COVER_") for n in full) == 2,
    "two_cover_orings": sum(n.startswith("HOLD_SIDE_ORING_") for n in full) == 2,
}
report = {
    "source": "current/CAD/previews/render_manifest.json",
    "source_sha256": manifest["source_sha256"],
    "mesh_sha256": manifest["mesh_sha256"],
    "full_view_components": len(full),
    "full_view_hold_prefixed": sum(n.startswith("HOLD_") for n in full),
    "full_view_hold_or_estimated": sum("HOLD" in n or "ESTIMATED" in n for n in full),
    "drivetrain_view_components": len(views["px1_drivetrain.png"]),
    "checks": {k: "PASS" if v else "FAIL" for k, v in checks.items()},
    "geometry_collision_check": "NOT_RUN",
    "manufacturing_release": "PHYSICAL_CHECK",
    "note": "HOLD labels mark unresolved geometry/parts; a passing render is not a physical design validation.",
}
out = HERE / "previews/PX1_manifest_readiness_audit.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
