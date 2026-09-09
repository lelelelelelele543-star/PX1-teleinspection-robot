#!/usr/bin/env python3
"""Fast nominal regression checks for the R16 CRP-150-style rebuild."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mechanical" / "cadquery"))
import PX1_R16_ProteusRebuild as r16  # noqa: E402


def main() -> int:
    profile = json.loads((ROOT / "firmware" / "crawler" / "r16" /
                          "hardware_profile.json").read_text())
    assert profile["revision"] == "R16"
    assert profile["status"] == "PIN_ALLOCATION_ONLY_NOT_FLASHABLE"
    driver_names = {"traction_left", "traction_right", "camera_pan", "camera_tilt"}
    assert set(profile["driver"]["channels"]) == driver_names
    driver_pins = [pin for name in driver_names for pin in profile["pins"][name]]
    assert len(driver_pins) == 8 and len(set(driver_pins)) == 8
    parts, groups = r16.build_parts()
    out = ROOT / "build_r16_regression"
    report = r16.validate(parts, groups, out)
    assert report["status"] == "PASS_R16_NOMINAL_PACKAGING_STUDY", report["status"]
    assert not report["invalid_parts"], report["invalid_parts"]
    assert not report["pipe_outside_mm3"], report["pipe_outside_mm3"]
    assert len(report["wheel_ground_contact"]) == 6
    assert all(x["touches_ground"] for x in report["wheel_ground_contact"].values())
    env = report["envelopes"]
    assert abs(env["body_plus_six_wheels_mm"]["xlen"] - 307.0) < 0.01
    assert abs(env["body_plus_six_wheels_mm"]["ylen"] - 133.0) < 0.01
    assert abs(env["body_plus_six_wheels_mm"]["zmin"]) < 0.01
    assert abs(env["body_plus_six_wheels_mm"]["zmax"] - 90.0) < 0.02
    assert all(row["wrench_required"] is False for row in report["quick_release"].values())
    assert all(row["pin_is_hand_accessible"] for row in report["quick_release"].values())
    assert report["camera_fit"]["low_pod_pipe_outside_mm3"] == 0.0
    assert report["camera_fit"]["camera_window_recessed"]
    assert report["camera_fit"]["front_guard_present"]
    assert not report["internal_packaging"]["outside_dry_envelope_mm3"]
    assert not report["internal_packaging"]["reserve_collisions_mm3"]
    assert report["rear_snag"]["parts_below_wheel_contact_plane"] == []
    assert abs(report["lift_kinematics"]["low_lengths_mm"][0] - 80.0) < 0.02
    assert abs(report["lift_kinematics"]["low_lengths_mm"][1] - 80.0) < 0.02
    assert len([n for n in parts if n.startswith("Z50m1_L_")]) == 5
    assert len([n for n in parts if n.startswith("Z50m1_R_")]) == 5
    print(json.dumps({"status": report["status"],
                      "body_plus_six_wheels_mm": env["body_plus_six_wheels_mm"],
                      "quick_release_count": len(report["quick_release"]),
                      "body_reserve_count": report["internal_packaging"]["body_reserve_count"],
                      "camera_low_pipe_outside_mm3": report["camera_fit"]["low_pod_pipe_outside_mm3"]},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
