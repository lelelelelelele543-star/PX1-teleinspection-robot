#!/usr/bin/env python3
"""Independent PX1 verification report: always fail-closed on manufacturing.

Normal exit 0 means checker INTEGRITY passed, NOT that PX1 is fit to machine.
--require-release exits 2 while any release blocker exists.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engineering"))
from simulation import evaluate_model_suite  # noqa: E402

LOCKED_COUNTS = {"wheel": 6, "Z50": 10, "Z40": 2, "Z16": 2, "traction_motor": 2}


def gate(name: str, state: str, summary: str, evidence: list[str]) -> dict:
    return {"gate": name, "state": state, "summary": summary, "evidence": evidence}


def classify_evidence(validation: dict, hold_register: list, bom_rows: list[dict]) -> tuple[list[dict], list[str]]:
    checks, errors = [], []
    actual = validation.get("counts", {})
    bad_counts = {k: {"expected": v, "actual": actual.get(k)} for k, v in LOCKED_COUNTS.items()
                  if actual.get(k) != v}
    if bad_counts or validation.get("counts_match") is not True:
        errors.append("The 6-wheel / 10 Z50 / dual-motor architecture is not verified")
        checks.append(gate("architecture", "FAIL", json.dumps(bad_counts), ["PX1_Current_Validation.json"]))
    else:
        checks.append(gate("architecture", "PASS_STATIC",
                           "Required 6-wheel architecture counts match the current model.",
                           ["PX1_Current_Validation.json"]))
    invalid_shapes = validation.get("invalid_shapes", [])
    rigid = [x for x in validation.get("interferences", [])
             if x.get("classification") == "RIGID_INTERFERENCE"]
    remaining = [x for x in hold_register if x.get("id")]
    checks.append(gate(
        "cad_geometry",
        "BLOCKED" if rigid or invalid_shapes or remaining else "SCREEN_ONLY",
        f"{len(rigid)} RIGID_INTERFERENCE overlaps; {len(invalid_shapes)} invalid shapes; "
        f"{len(remaining)} unresolved hold items. Bounding/boolean checks are not production drawings.",
        ["current/PX1_Current_Validation.json", "current/HOLD_REGISTER.json"],
    ))
    tentative = [r for r in bom_rows if any("HOLD" in (r.get(k) or "").upper()
                for k in ("article", "dimensions", "cad_state", "release"))]
    missing_articles = [r for r in bom_rows if not (r.get("article") or "").strip()]
    checks.append(gate(
        "procurement",
        "BLOCKED",
        f"{len(bom_rows)} BOM entries, {len(tentative)} with explicit HOLD, "
        f"{len(missing_articles)} without article. No current vendor-stock audit.",
        ["current/PX1_Current_BOM.csv"],
    ))
    checks.append(gate(
        "camera_reel_console_firmware",
        "NOT_QUALIFIED",
        "Component envelopes, drawings, pinouts and compiled firmware need "
        "individual evidence and cross-system hardware tests.",
        ["current/REV_A_FAST_TRACK.md", "current/07_TESTS/README.md"],
    ))
    checks.append(gate(
        "physical_validation",
        "NOT_TESTED",
        "A0 through A5 physical test sheets require actual measurements and "
        "human-confirmed evidence; simulation never signs these off.",
        ["current/07_TESTS/README.md"],
    ))
    false_release = validation.get("metal_release") is True and (
        bool(rigid) or bool(invalid_shapes) or bool(remaining) or bool(tentative)
    )
    if false_release:
        errors.append("Manufacturing release flag contradicts unresolved critical evidence")
    return checks, errors


def audit(root: Path = ROOT) -> dict:
    needed = [
        "AGENTS.md", "current/README.md", "current/PX1_Current_Validation.json",
        "current/HOLD_REGISTER.json", "current/PX1_Current_BOM.csv",
        "current/CAD/PX1_Current_Master.py",
        "current/03_FIRMWARE/protocol/PX1_PROTOCOL_V1.md",
    ]
    missing = [p for p in needed if not (root / p).is_file()]
    if missing:
        return {"verdict": "FAIL_CHECKER", "integrity_errors": ["Missing inputs: " + ", ".join(missing)],
                "release_permitted": False, "gates": [], "models": None}
    val = json.loads((root / "current/PX1_Current_Validation.json").read_text(encoding="utf-8"))
    holds = json.loads((root / "current/HOLD_REGISTER.json").read_text(encoding="utf-8"))
    with (root / "current/PX1_Current_BOM.csv").open(encoding="utf-8-sig", newline="") as f:
        bom = list(csv.DictReader(f, delimiter=";"))
    gates, errors = classify_evidence(val, holds, bom)
    bench_text = (root / "current/01_MECHANICAL_6X6/A0_DRIVETRAIN_BENCH.md").read_text(encoding="utf-8")
    motor_rows = [r for r in bom if (r.get("item") or "").strip() == "P01"]
    motor_article = " ".join((r.get("article") or "") for r in motor_rows)
    # A real master/BOM mismatch: active A0 source-match motor is FAULHABER,
    # while the current Rev.C assembly/BOM still uses Pololu 5707 envelopes.
    faulhaber_active = "active mechanical baseline is now the source-envelope-matched FAULHABER" in bench_text
    pololu_still_in_bom = "5707" in motor_article or "pololu" in motor_article.lower()
    motor_conflict = faulhaber_active and pololu_still_in_bom
    gates.append(gate(
        "mechanics_to_procurement_motor_fit",
        "BASELINE_CONFLICT" if motor_conflict else "NEEDS_CROSSCHECK",
        "A0 bench describes FAULHABER as the active motor but current BOM P01 is: "
        + (motor_article or "MISSING") + ". Need a single verified motor envelope in CAD/BOM.",
        ["current/01_MECHANICAL_6X6/A0_DRIVETRAIN_BENCH.md", "current/PX1_Current_BOM.csv"],
    ))
    src = (root / "current/CAD/PX1_Current_Master.py").read_bytes()
    actual_hash = hashlib.sha256(src).hexdigest()
    manifest_hash = val.get("source_sha256")
    gates.append(gate(
        "cad_source_traceability",
        "PASS_HASH" if manifest_hash == actual_hash else "STALE_VALIDATION",
        f"Validation source sha256 {'matches' if manifest_hash == actual_hash else 'DOES NOT match'} "
        "the CAD script currently checked out.",
        ["current/PX1_Current_Validation.json", "current/CAD/PX1_Current_Master.py"],
    ))
    models = evaluate_model_suite()
    gates.append(gate(
        "analytical_simulation", models["status"],
        "Power-feed, kinematic and link-watchdog mathematical screens ONLY. "
        "Elevated tether voltage is not approved for use.",
        ["engineering/simulation.py"],
    ))
    if models["status"] != "PASS_MODEL_ONLY":
        errors.append("Analytical model invariant failed")
    blockers = [g for g in gates if g["state"] not in ("PASS_STATIC", "PASS_HASH", "PASS_MODEL_ONLY")]
    # No branch of this code can approve a production release without separate
    # independently reviewed A0-A5 hardware records. This avoids self-certification.
    release_permitted = False
    return {
        "verdict": "FAIL_CHECKER" if errors else "INTEGRITY_OK__RELEASE_BLOCKED",
        "integrity_errors": errors,
        "release_permitted": release_permitted,
        "candidate_release_flag_in_old_CAD_validation": val.get("metal_release"),
        "critical_release_blockers": blockers,
        "gates": gates,
        "models": models,
        "scope": "static active-CAD evidence + simplified analytical models; NOT real FEA/CFD/EMC",
    }


def markdown(report: dict) -> str:
    rows = ["# PX1 Independent Engineering Gate", "",
            "**Verdict:** " + report["verdict"], "",
            "**Manufacturing release permitted:** NO", "",
            "| Gate | Status | Evidence summary |",
            "|---|---|---|"]
    for g in report["gates"]:
        summary = g["summary"].replace("|", "/").replace("\n", " ")
        rows.append(f'| {g["gate"]} | {g["state"]} | {summary} |')
    rows += ["", "## Integrity errors", ""]
    rows += ["- " + x for x in report["integrity_errors"]] or ["- None detected"]
    rows += ["", "## Interpretation", "",
             "A PASS_MODEL_ONLY result never releases metal drawings or power wiring. "
             "A0–A5 hardware results and independent reviewer signoff are mandatory.",
             "The 110 V scenario is numerical evaluation only: do not energize an "
             "unverified tether or operator console at this voltage.", ""]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="engineering/out/gates.json")
    parser.add_argument("--md", default="engineering/out/gates.md")
    parser.add_argument("--require-release", action="store_true")
    args = parser.parse_args()
    report = audit()
    for file, body in [(ROOT / args.json, json.dumps(report, indent=2, ensure_ascii=False)),
                       (ROOT / args.md, markdown(report))]:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(body + "\n", encoding="utf-8")
    print(f'PX1: {report["verdict"]}; production_release={report["release_permitted"]}')
    for g in report["gates"]:
        print(f'  {g["gate"]}: {g["state"]} — {g["summary"]}')
    if report["integrity_errors"]:
        return 1
    return 2 if args.require_release and not report["release_permitted"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
