"""Contact probes for the generated R14 named parts.

This is a geometric backing check only.  It is not a pressure, squeeze,
material, tolerance or IP test.
"""
from pathlib import Path
import hashlib, json, sys
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mechanical" / "cadquery"))
import PX1_R14_ServiceAndRetention as r14
from PX1_R12_SelectedParts import ann, ring, volume


def load_parts():
    folder = ROOT / "build_r14" / "named_parts"
    data = json.loads((folder / "index.json").read_text())
    parts = {name: cq.Workplane("XY").newObject(
             [cq.Shape.importBrep(str(folder / filename))])
             for name, filename in data["files"].items()}
    return parts


def main():
    parts = load_parts()
    body = parts["BODY_R14"]
    bottom_probe = ring(390, 84, 8, 2.8, .1, (206, 0, 25.55))
    report = {
        "revision": "R14", "physical_test": False,
        "source_sha256": hashlib.sha256(
            (ROOT / "mechanical/cadquery/PX1_R14_ServiceAndRetention.py").read_bytes()
        ).hexdigest(),
        "bottom_gland_probe_volume_mm3": volume(bottom_probe),
        "bottom_gland_unsupported_mm3": r14.outvol(bottom_probe, body),
        "side_static_ring_support": {}, "hub_washer_contact_mm": {},
        "bearing_cover_contact_mm": {},
        "scope": "Face/backing contact only; no pressure or tolerance qualification"
    }
    for side in (-1, 1):
        name = "L" if side == 1 else "R"
        side_probe = ann(35.05, 35.25, 2, (50, side * 49, 75), "y")
        cover = parts["Side_cover_" + name]
        report["side_static_ring_support"][name] = {
            "probe_volume_mm3": volume(side_probe),
            "unsupported_mm3": r14.outvol(side_probe, cover)
        }
        for x in (50., 150., 250.):
            tag = name + str(x)
            report["hub_washer_contact_mm"][tag] = parts["M8_washer_" + tag].val().distance(
                parts["Wheel_hub_" + tag].val())
            report["bearing_cover_contact_mm"][tag] = parts["61903_" + tag].val().distance(cover.val())
    ok = (report["bottom_gland_unsupported_mm3"] < .001 and
          all(x["unsupported_mm3"] < .001 for x in report["side_static_ring_support"].values()) and
          all(x < 1e-5 for x in report["hub_washer_contact_mm"].values()) and
          all(x < 1e-5 for x in report["bearing_cover_contact_mm"].values()))
    report["status"] = "PASS_SCOPED_CONTACT_PROBES" if ok else "FAIL_CONTACT_PROBES"
    out = ROOT / "validation" / "r14" / "contact_review.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
