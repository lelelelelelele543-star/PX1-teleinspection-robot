# PX1 GitHub baseline audit — 18 October 2026

Scope: read-only inventory of repository `main` baseline as visible through GitHub. This is **not** a local FreeCAD re-run or physical acceptance.

## Verified repository state

- Repository: `lelelelelelele543-star/PX1-teleinspection-robot`.
- Main current master: `current/`; old Rev folders and reports are not authoritative.
- Current mechanical configuration: six wheels (3 per side), 10× Z50, 2× Z40, 2× Z16, 2 traction motors, manual camera lift, separate sealed camera, 6-core tether.
- Active fast-track stages: A0 (drivetrain bench), A1 (rolling chassis), A2 (40m tether), A3 (camera/lift), A4 (integrated demo), A5 (sealing/endurance), A6 (manufacturing release).
- Existing limited local agent: `tools/px1_autorun.py` + `autonomy/CRP150_REFERENCE_TASK.md`. It is a bounded single-agent reference CAD workflow. The new team runner is separate.

## Existing validation facts (DO NOT mark manufacturing released)

File: `current/PX1_Current_Validation.json`, internal revision `Rev.C 2026-09-14` (may be older than branch-specific work).

- `status = HOLD_NOT_MANUFACTURING_RELEASE`, `metal_release = false`.
- `counts_match = true`: this verifies part counts only.
- `component_count = 146`; `invalid_shapes = []` in this saved artifact.
- `interferences = 55` recorded, including rigid interference of unconfirmed enclosure/connector geometry.
- DN150 check includes wheel-pipe negative clearance around `-4.4427 mm` at the LOW position with wheel/profile assumption H01; these are saved-screen results, **not a renewed validated clearance measurement**.
- Holds H01–H10 remain: wheel/quick-release, body/axle package, pressure sealing, gear profile, motor fit, camera lift, tether/connectors, camera internals, modules/packaging, power & physical tests.

The existence of the STEP export and PDF drawings does **not** mean the geometry is machinable or that watertightness/electrical safety has been tested.

## Parallel team first wave

| Task | Engineer | Concrete goal | Independent artifacts |
|---|---|---|---|
| T001 | Reference CAD | Audit CRP150/CAM026 reference evidence and create/source geometry comparison | `reference/Proteus-CRP-150/cad/reconstruction/`, `autonomy/team_work/R2_REFERENCE_CAD/` |
| T002 | Tether/video/power | Confirm 40 m six-conductor power/video/control feasibility and safe bench tests, later 100–150 m | `autonomy/team_work/R6_TETHER_VIDEO_POWER/` |
| T003 | QA reviewer | Reproduce available CAD/tests, classify all interferences and H01–H10; distinguish skipped tools from tested passes | `autonomy/team_work/R11_QA/` |

Coordinator should launch actual subagents, wait for evidence, reconcile interfaces and change only reviewed artifacts. If native subagents are not supported, record that fact rather than falsely claiming parallelism.

## Related prior branch

An existing separate PR #12, `feature/px1-engineering-agents-20261013`, proposes seven engineering roles, simulation scripts and an independent HOLD gate. It is **not merged** into this new team feature branch or main. Before publishing further integration work, coordinate these efforts instead of inventing incompatible parallel source-of-truth structures.

## Provenance & limitations

Repository sources: `AGENTS.md`, `README.md`, `current/README.md`, `current/REV_A_FAST_TRACK.md`, `current/PX1_Current_Validation.json`, `current/HOLD_REGISTER.json`, `autonomy/README.md`, `autonomy/CRP150_REFERENCE_PROGRESS.md`. Data were read from GitHub on 2026-10-18. No physical measurements, simulated executions or current supplier availability are represented by this audit.
