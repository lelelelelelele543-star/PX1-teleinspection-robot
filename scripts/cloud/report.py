#!/usr/bin/env python3
"""Create an honest CAD-derived outline and a machine-readable build summary.
The SVG uses bounding boxes computed from actual CadQuery solids, not generative art.
A build PASS is NOT a manufacturing, pressure, gear-mesh or endurance PASS.
"""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

out = Path(sys.argv[1]).resolve()
validation_path = out / "PX1_Current_Validation.json"
registry_path = out / "component_registry.json"
step_path = out / "CAD" / "PX1_Current_Master.step"
validation = json.loads(validation_path.read_text(encoding="utf-8"))
registry = json.loads(registry_path.read_text(encoding="utf-8"))
counts = validation["counts"]
expected = validation["expected_counts"]
missing = [name for name, num in expected.items() if counts.get(name) != num]
invalid = validation.get("invalid_shapes", [])
step_ok = step_path.is_file() and step_path.stat().st_size > 1024
geometry_ok = step_ok and not missing and not invalid
clashes = validation.get("interferences", [])
rigid = [c for c in clashes if c.get("classification") == "RIGID_INTERFERENCE"]

# X/Z side projection from exact component solid bounds, with generous drawing margins.
svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620">',
    '<rect width="1200" height="620" fill="#101827"/>',
    '<text x="38" y="50" fill="#f1f5f9" font-size="28" font-family="sans-serif">PX1 — current CAD assembly, side-envelope projection</text>',
    '<text x="38" y="82" fill="#a8c4d8" font-size="17" font-family="sans-serif">Geometry sourced from the assembled solids’ bounding boxes. Not a FreeCAD viewport or manufacturing drawing.</text>',
    '<g transform="translate(120 510) scale(2.55 -2.55)">',
]
def bbox(item):
    a = item["bbox_mm"]
    return a[0], a[2], a[3] - a[0], a[5] - a[2]
def box_shape(item, fill, alpha="0.35", stroke="#64748b"):
    x,z,w,h = bbox(item)
    return f'<rect x="{x:.3f}" y="{z:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" fill-opacity="{alpha}" stroke="{stroke}" stroke-width="0.8"/>'
def circle_shape(item, fill):
    x,z,w,h = bbox(item)
    return f'<ellipse cx="{x+w/2:.3f}" cy="{z+h/2:.3f}" rx="{w/2:.3f}" ry="{h/2:.3f}" stroke="{fill}" stroke-width="1.3" fill="{fill}" fill-opacity="0.3"/>'
# Layer only a few classes; the full 146-component assembly remains in STEP.
for item in registry:
    if "PRESSURE_BODY" in item["id"]:
        svg.append(box_shape(item,"#567b96","0.5","#87b8d7"))
for item in registry:
    if "Z50_" in item["id"] or "Z40_BEVEL" in item["id"] or "Z16_BEVEL" in item["id"]:
        svg.append(circle_shape(item,"#f4b95c"))
for item in registry:
    if "MOTOR_" in item["id"] and "MANUFACTURER" in item["id"]:
        svg.append(box_shape(item,"#58c3b4","0.45","#58c3b4"))
for item in registry:
    if "_QRW90SR150_WHEEL_" in item["id"]:
        svg.append(circle_shape(item,"#d7e0e7"))
svg.append('</g>')
svg.append('<text x="38" y="560" fill="#f1f5f9" font-size="19" font-family="sans-serif">Six wheels · 2 motors · 10 × Z50 · Z16/Z40 inputs · CRP150-inspired proportions</text>')
svg.append(f'<text x="38" y="590" fill="#ffcd85" font-size="16" font-family="sans-serif">PROTOTYPE ONLY — {len(rigid)} rigid CAD interferences logged; physical validation not performed.</text>')
svg.append("</svg>")
(out / "px1_side_envelope.svg").write_text("\n".join(svg), encoding="utf-8")

summary = {
    "source": "current/CAD/PX1_Current_Master.py",
    "build_status": "PASS_EXPORT_AND_COUNTS" if geometry_ok else "FAIL_EXPORT_OR_COUNTS",
    "manufacturing_release": False,
    "actual_components": validation.get("component_count"),
    "counts": counts,
    "expected_counts": expected,
    "missing_counts": missing,
    "invalid_shapes": invalid,
    "rigid_interference_count": len(rigid),
    "geometry_validation_status": validation.get("status"),
    "pressure_test": "NOT_RUN",
    "freecad_fcstd_conversion": "NOT_RUN",
    "step_bytes": step_path.stat().st_size if step_path.is_file() else 0,
}
(out / "cloud_build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
if not geometry_ok:
    sys.exit("PX1 CAD master export/counts failed; see logs and validation")
