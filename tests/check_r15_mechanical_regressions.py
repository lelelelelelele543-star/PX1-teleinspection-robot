"""Independent checks for the real defects found in R14 and new wheel keys.

Uses the exported named solids and their hash manifest. Deliberately moving a
key by1degree must cause hub interference: this proves modeled engagement,
not its strength, manufacturing fit or allowable transmitted torque.
"""
from pathlib import Path
import hashlib
import json
import sys
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mechanical/cadquery"))
import PX1_R15_CheckedAssembly as r15


def main():
    directory = ROOT / "build_r15/named_parts"
    data = json.loads((directory / "index.json").read_text())
    parts = {}
    for name, filename in data["files"].items():
        path = directory / filename
        assert hashlib.sha256(path.read_bytes()).hexdigest() == data["brep_sha256"][name], name
        # Vendor compounds participate in the full validator; no need to
        # duplicate their expensive geometry loading for these local regressions.
        if not name.startswith("Pololu4695_"):
            parts[name] = cq.Workplane("XY").newObject([cq.Shape.importBrep(str(path))])
    checks = [("Side_cover_R", "BODY_R15"), ("Side_cover_L", "BODY_R15"),
        ("Hanging_bearing_bridge", "BODY_R15"), ("HV_route_RESERVE", "BODY_R15"),
        ("LV_route_RESERVE", "BODY_R15")]
    report = {"revision": "R15", "physical_test": False,
        "geometry_source_sha256": data["r15_source_sha256"],
        "test_source_sha256": r15.sha(__file__),
        "regression_overlap_mm3": {a + "__" + b: r15.overlap(parts[a], parts[b]) for a, b in checks},
        "thermal_angle_gap_mm": parts["RSD_thermal_angle"].val().distance(parts["BOTTOM_LID_R15"].val()),
        "screws": {}, "wheel_keys": {}, "nut_corner_diameter_mm": 13 / (3 ** .5 / 2)}
    for name, shape in parts.items():
        if name.startswith(("Side_M3x8_", "Bottom_M3x8_")):
            host = "BOTTOM_LID_R15" if name.startswith("Bottom") else "Side_cover_" + name.split("_")[2]
            report["screws"][name] = {"solid_count": len(shape.solids().vals()),
                "cover_intersection_mm3": r15.overlap(shape, parts[host])}
    for side in ("L", "R"):
        for x in (50., 150., 250.):
            tag = side + str(x)
            key, axle, hub = (parts[prefix + tag] for prefix in ("Wheel_key_5x5x10_", "Axle_", "Wheel_hub_"))
            turned = key.rotate((x, 0, 75), (x, 1, 75), 1)
            report["wheel_keys"][tag] = {"key_axle_mm3": r15.overlap(key, axle),
                "key_hub_mm3": r15.overlap(key, hub),
                "shaft_seat_contact_mm": key.val().distance(axle.val()),
                "hub_interference_after_1deg_relative_rotation_mm3": r15.overlap(turned, hub)}
    ok = (len(report["screws"]) == 50
        and all(v <= .001 for v in report["regression_overlap_mm3"].values())
        and report["thermal_angle_gap_mm"] <= 1e-5
        and all(p["solid_count"] == 1 and p["cover_intersection_mm3"] <= .001 for p in report["screws"].values())
        and all(p["key_axle_mm3"] <= .001 and p["key_hub_mm3"] <= .001 and
                p["shaft_seat_contact_mm"] <= 1e-5 and
                p["hub_interference_after_1deg_relative_rotation_mm3"] > .001 for p in report["wheel_keys"].values()))
    report["status"] = "PASS_R15_LOCAL_MECHANICAL_REGRESSIONS" if ok else "FAIL_R15_LOCAL_MECHANICAL_REGRESSIONS"
    target = ROOT / "validation/r15/mechanical_regressions.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "screws"}, indent=2), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
