# PX1 — read-only HOLD gate (2026-11-14)

This is a guard against accidental release-state drift, **not** a CAD or manufacturing certification.

Run from the repository root:

```sh
python autonomy/qa/check_release_gate.py --root .
```

- Exit 0 / `PASS_HOLD_ENFORCED`: H01–H10 are present once, the validation file still says `HOLD_NOT_MANUFACTURING_RELEASE`, the expected six wheels, two motors and six camera-harness conductors are recorded, and a source hash exists.
- Exit 1 / `FAIL`: required file missing, JSON malformed, a HOLD item missing/duplicated, counts differ or release status changes.
- It **does not** prove the source hash matches current CAD, collision-free geometry, seal dimensions, real cable viability or successful physical tests.
- Current data read: `current/HOLD_REGISTER.json`, `current/PX1_Current_Validation.json`. The historical reference and dimensional uncertainty are documented in `current/SOURCE_REGISTER.md`.
- This tool never changes CAD, BOM, validation or release status.

Validation during development: Python syntax check passed; synthetic positive fixture returned exit 0, and synthetic fixture with `status=PASS` returned exit 1. **Running the exact GitHub file against the complete repository in CI is still pending.**

Next: add automated test fixtures and a read-only GitHub Actions check, then expand to geometric interference regression. The existing `current/` master remains authoritative and on HOLD.
