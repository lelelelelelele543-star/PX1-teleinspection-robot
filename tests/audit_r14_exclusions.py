"""Independent regression audit of R14's overly broad collision exclusions.

Loads only the disputed cached shapes. This does not rerun R14's validator,
inherit its exemptions, or claim to validate every cached vendor component.
"""
from pathlib import Path
import hashlib
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "build_r14/named_parts"
    manifest = json.loads((folder / "index.json").read_text())
    pairs = [("Side_cover_R", "BODY_R14"), ("Side_cover_L", "BODY_R14"),
             ("Hanging_bearing_bridge", "BODY_R14"),
             ("HV_route_RESERVE", "BODY_R14"), ("LV_route_RESERVE", "BODY_R14")]
    names = {n for pair in pairs for n in pair} | {
        "RSD_thermal_angle", "BOTTOM_LID_R14", "Side_M3x8_R_00", "Bottom_M3x8_00"}
    parts = {n: cq.Shape.importBrep(str(folder / manifest["files"][n])) for n in names}
    overlaps = {a + "__" + b: sum(
        s.intersect(t).Volume() for s in parts[a].Solids() for t in parts[b].Solids())
        for a, b in pairs}
    report = {
        "audited_revision": "R14", "audit_date": "2026-09-09",
        "status": "R14_PASS_REJECTED_BY_INDEPENDENT_AUDIT",
        "cadquery": cq.__version__, "physical_test": False,
        "r14_source_sha256": hashlib.sha256((ROOT /
            "mechanical/cadquery/PX1_R14_ServiceAndRetention.py").read_bytes()).hexdigest(),
        "audited_brep_sha256": {n: hashlib.sha256(
            (folder / manifest["files"][n]).read_bytes()).hexdigest() for n in sorted(names)},
        "unexempted_overlap_mm3": overlaps,
        "thermal_angle_to_lid_gap_mm": parts["RSD_thermal_angle"].distance(parts["BOTTOM_LID_R14"]),
        "sample_fastener_solid_counts": {n: len(parts[n].Solids())
            for n in ("Side_M3x8_R_00", "Bottom_M3x8_00")},
        "findings": [
            "The cover/body and bridge/body overlaps are volumes, not face contacts.",
            "R14 omits housing from route collision checks.",
            "R14 omits all fasteners/references from static checks.",
            "R14 does not check moving lift parts against one another.",
            "R14's side withdrawal group omits gears, idlers and the rear bevel.",
            "This audit samples named BREP geometry, not the entire R14 export."
        ]
    }
    assert all(v > 0.001 for v in overlaps.values()), "R14 regression fixture changed"
    assert all(c == 2 for c in report["sample_fastener_solid_counts"].values())
    target = ROOT / "validation/r15/r14_independent_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
