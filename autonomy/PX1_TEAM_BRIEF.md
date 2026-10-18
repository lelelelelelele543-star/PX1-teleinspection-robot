# PX1 multi-agent engineering: contract

## Goal
Develop one full working CRP150+CAM026-like PX1 system (robot, camera, reel, console) using purchasable standardized COTS components/modules without custom PCBs. After actual first-unit verification, produce reproducible BOM/CAD/firmware/assembly instructions for two additional identical systems. Spare-parts manufacturing is a future phase, NOT today's priority.

## Read first
AGENTS.md; current/README.md; current/HOLD_REGISTER.json; current/PX1_Current_Validation.json; autonomy/CRP150_REFERENCE_PROGRESS.md. current/ is authoritative PX1 adapted project; keep Proteus original CRP150_REFERENCE/CAM026_REFERENCE separate. Current manufacturing release remains HOLD until verified. Do not silently change architecture or claim completion based on successful CAD export.

## Team assignments (roles, not permanent running threads)
CHIEF ENGINEER: one coordinator, owner of task board, message routing, change decisions and integration.
R1 PROTEUS RESEARCH: dated images, drawings, video frames, reference dimensions, evidence register.
R2 REFERENCE CAD: CRP150_REFERENCE, CAM026_REFERENCE, photo overlays, uncertain dimensions.
R3 DRIVETRAIN: 6 wheels, gears, motor ratios, clearances, load calculations.
R4 HOUSING/SEALS: dry chamber, bearings, seal selection, shaft glands, pressure verification plan.
R5 CAMERA: removable sealed pan/rotate head, kinematics, illumination, available imager.
R6 TETHER/VIDEO/POWER: 6-core bus, video feasibility at 40m, later 100-150m; conductor resistance, electrical safety/interlocks.
R7 COTS ELECTRONICS: manufacturer/part number/dimensions for purchasable modules, drivers, connectors, sensors.
R8 FIRMWARE: MCU logic, safe motor and lighting control, protocols, repeatable build and flashing.
R9 REEL+CONSOLE: reel mechanics, distance meter, operator control interface, OSD/display.
R10 PROCUREMENT: datasheets, verifiable suppliers in RF, substitute components, BOM costs.
R11 QA: independent CAD, build, fit, simulation, firmware, safety, requirements tests. May veto a release.

## Concurrent work rules
Use the native Codex subagent tools to spawn actual independent agents, if available. Start at 3 concurrent specialists plus coordinator; do NOT start all 11 simultaneously. Assign clear input/output paths and tests for each delegation. Agents working on distinct files can work concurrently. Never simultaneously edit current/ master CAD, authoritative BOM, shared interface contracts, or checkpoint. Only coordinator integrates verified outputs.

Use native subagent messages: each engineer immediately reports dimensional/interface changes, blockers and relevant research to coordinator; coordinator forwards each change to affected engineers. End-of-task message must include (1) real file paths, (2) source URLs/datasheets, (3) commands and PASS/FAIL/SKIP checks, (4) confidence level, (5) risks, (6) next dependency. Log cross-team decisions in autonomy/PX1_TEAM_PROGRESS.md. If subagents cannot be spawned, explicitly record SUBAGENTS_UNAVAILABLE and proceed with a single bounded task; NEVER fake agent activity.

## Subsystem contracts
- R1 -> R2: original dimensions and provenance
- R2 -> R3/R4/R5: mechanical reference envelopes and camera mount
- R3/R4/R5/R6/R7: interlocking mechanical/electrical interfaces, exact pinouts and mounting envelopes
- R6 -> R7/R8/R9: tether allocation, power and video interface constraints
- R7 -> R8: board, driver and pinout data
- R8 -> R9: telemetry and control protocol
- ALL -> R11: evidence and test artifacts
- QA -> CHIEF: explicit blockers to physical release

## Engineering/release gates
G0: verify existing files/status and HOLD blockers.
G1: source-faithful reference geometry and error map.
G2: actual bought-part mechanical/electrical envelopes and tether feasibility.
G3: adapted PX1 CAD assembly and checked mechanisms.
G4: functional circuit/wiring drawings, compilable firmware, reel and console package.
G5: independent reproducible validation and manufacturing documentation, pending bench tests.
G6: physical prototype, pressure/electrical/cable/endurance tests — human workshop only.
G7: only after G6, same-version documentation for units 2 and 3.

Keep STATUS IN_PROGRESS until engineering AND physical verification are complete. No order placement, external publication, force push or unrestricted PC permissions. Tests alone do not certify high-voltage electrical safety or pressure integrity. Any potentially hazardous high-voltage tether architecture requires qualified design review and real protective testing before fabrication.

## Each loop must
1. Inspect git status/current checkpoint.
2. Pick at least one engineering output task, NOT merely edit management text.
3. Delegate 2-3 independent subtasks when spawn tools exist; request status messages and wait for results.
4. Run actual CAD/test/build tools if installed; record exact failures when unavailable.
5. Reconcile interface conflicts and integrate only verified changes.
6. Update checkpoint with actual outcomes, filenames and next executable tasks.
