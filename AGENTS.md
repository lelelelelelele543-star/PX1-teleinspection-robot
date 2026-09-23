# AGENTS.md — PX1 governing instructions for Codex

This repository contains the PX1 teleinspection system project. Treat this file as the highest-priority project brief unless the user explicitly overrides it in the current session.

## True project objective
Build a complete professional teleinspection complex mechanically based as closely as possible on Mini-Cam Proteus CRP-150, while using our own electronics, controls, power architecture and firmware.

This is NOT a generic pipe robot and NOT a simplified cart.

## Mechanical baseline
- Proteus CRP-150 is the primary mechanical reference.
- Rev.A must remain 6-wheel / 6x6 in the established layout.
- Preserve the approved drivetrain concept: wheel stations X50/X150/X250, five Z50 gear stations per side, 10x Z50 total, two traction motors, Z16 -> Z40 input, rear X250 axle input and the gear train driving all three wheels on each side.
- No 4-wheel simplification.
- No belt drive.
- No new crawler concept unless a real technical impossibility forces a change.
- Preserve the Proteus-like pressurized dry body, shaft sealing, tail/tether entry logic, serviceability and camera-lift architecture.
- Manual camera lift remains part of the baseline.
- Camera head is a separately sealed, removable module.
- Main tether philosophy: professional reinforced six-core copper inspection cable, no coax in the main tether, no fiber, no bundle of separate twisted-pair lines.
- First working tether length: 40 m. Later: 100-150 m.
- No custom main PCB is required for the first working prototype; use available ready-made modules unless there is a strong reason not to.

## Electronics baseline
Electronics are OUR design, not a copy of Proteus electronics.
Use the approved project architecture and components from current documentation unless explicitly superseded by newer verified choices.
Core functions include:
- 24 V-class system architecture;
- STM32-class controller;
- motor drivers appropriate to the actual selected motors;
- RS-485 control;
- pressure telemetry;
- lighting control;
- live video / OSD as specified;
- operator console with monitor, joystick/buttons/potentiometer;
- distance, pressure, time/address/OSD functions as defined in project docs.

Do not assume an old BOM item is still valid if it conflicts with the current motor or mechanical package. Check current/ first.

## Rule for missing dimensions
Do NOT stop the project just because a factory dimension cannot be found.

Use this order:
1. Search existing CRP-150 drawings, project files, photos, source register and manufacturer/open sources.
2. Derive dimensions from known geometry, scale references, multiple views, gear geometry, bearings, fasteners and bought-part datasheets.
3. If an exact value still cannot be recovered, choose an engineering-reasoned dimension that preserves the Proteus geometry/function and verify it in CAD.

Every dimension should be tagged conceptually as:
- CONFIRMED — directly sourced;
- DERIVED — calculated/reconstructed from evidence;
- ESTIMATED — engineering estimate.

These confidence tags are informational and MUST NOT automatically block design progress.

The user does not want to be sent away to measure parts when the dimension can reasonably be reconstructed from existing material.

## HOLD policy
Historical HOLD entries remain useful as a record of uncertainty, but HOLD is NOT permission to stop work.
Resolve blockers by research, reconstruction, engineering calculation, CAD validation and physical testing.
Do not answer with "need measurement" as the default.

## Speed policy
"Faster" means parallel engineering, procurement and validation — NOT simplification of the CRP-150-like design.

Work streams should run in parallel where possible:
- mechanics/CAD;
- drivetrain;
- sealing;
- camera/lift;
- electronics;
- firmware;
- tether/reel;
- console;
- procurement;
- test planning.

## Physical development chain
Follow the established physical chain without branching into unrelated concepts:
motors -> bevel/input stage -> 5xZ50 per side -> 6 wheels -> body -> tether -> control -> camera -> lift -> console -> sealing/endurance -> production release.

## Commercial target
The end product must be a complete sellable professional teleinspection system, not just a moving crawler.

The first physical unit is primarily an engineering/demo unit. Correct its discovered weaknesses, then build a repeatable second unit as the first serious sales candidate.

## Intellectual-property workflow
Do not make patent/IP review a blocker for engineering work unless the user explicitly asks for it. Do not claim legal clearance.

## Change-control rule
Before changing any frozen architectural choice, explain:
- what CRP-150 feature/current PX1 baseline is being changed;
- why the current solution is technically impossible or materially inferior;
- effects on sealing, serviceability, manufacturability and tether operation.

Absent a concrete reason, keep the baseline.

## Repository precedence
Use current/ as the active master. Historical Rev/WB files are reference/history only and cannot override current/.
If a historical file conflicts with this brief or current/, ignore the historical branch.

## Interaction style for this project
The user wants execution, not repeated conceptual resets.
Prefer doing the engineering work, updating project artifacts and presenting concrete results.
Do not repeatedly ask for approval on small internal steps.
