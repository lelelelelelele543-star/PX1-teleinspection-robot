#!/usr/bin/env python3
"""Read-only PX1 release HOLD guard. Standard-library Python; no CAD needed."""
import argparse
import json
from pathlib import Path
import sys

EXPECTED = {f"H{i:02}" for i in range(1, 11)}
HOLD = "HOLD_NOT_MANUFACTURING_RELEASE"


def inspect(root):
    issues = []
    try:
        holds = json.loads((root / "current/HOLD_REGISTER.json").read_text(encoding="utf-8-sig"))
        validation = json.loads((root / "current/PX1_Current_Validation.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return {"result": "FAIL", "issues": [f"Cannot read/parse required JSON: {exc}"]}
    if not isinstance(holds, list):
        issues.append("HOLD_REGISTER must be a list")
        holds = []
    ids = [item.get("id") for item in holds if isinstance(item, dict)]
    if len(ids) != len(holds) or set(ids) != EXPECTED or len(ids) != len(set(ids)):
        issues.append(f"HOLD IDs must be exactly H01..H10 once; got {ids}")
    for item in holds:
        if not isinstance(item, dict) or not all(item.get(key) for key in ("id", "title", "required", "blocks")):
            issues.append("HOLD entry lacks id/title/required/blocks")
    if not isinstance(validation, dict):
        issues.append("Validation must be a JSON object")
        validation = {}
    if validation.get("status") != HOLD:
        issues.append(f"Unexpected release status: {validation.get('status')!r}; expected {HOLD}")
    counts = validation.get("counts")
    if not isinstance(counts, dict):
        counts = {}
    for key, value in (("wheel", 6), ("traction_motor", 2), ("camera_harness_cores", 6)):
        if counts.get(key) != value:
            issues.append(f"Expected {key}={value}, got {counts.get(key)!r}")
    if not validation.get("source_sha256"):
        issues.append("Missing CAD source hash")
    # PASS_HOLD_ENFORCED is NOT manufacturing approval.
    return {"result": "FAIL" if issues else "PASS_HOLD_ENFORCED",
            "release": HOLD, "issues": issues, "hold_count": len(holds)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    result = inspect(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS_HOLD_ENFORCED" else 1


if __name__ == "__main__":
    sys.exit(main())
