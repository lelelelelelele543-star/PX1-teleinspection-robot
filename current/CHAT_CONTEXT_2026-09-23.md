# PX1 chat context — 2026-09-23

This note captures the decisions from the current ChatGPT discussion that must carry into Codex/local Work sessions.

## Key correction
The user repeatedly clarified that the actual goal is a CRP-150-class complete teleinspection system. Previous drift toward a generic or 4-wheel cart was wrong.

From now on:
- treat Proteus CRP-150 as the mechanical reference;
- reproduce the mechanical logic and geometry as closely as the available evidence allows;
- keep our own electronics and firmware;
- do not simplify the crawler to four wheels;
- do not redesign the project into a generic pipe robot.

## Missing dimensions
The user explicitly does NOT want design progress stopped by missing dimensions and does not want to be asked to measure parts when the existing source set can support reconstruction.

When a dimension is absent:
- search drawings/open sources;
- scale from photos and known reference dimensions;
- calculate from gear geometry, bearings, fasteners and purchased-part datasheets;
- make a justified engineering estimate if needed;
- continue the design;
- label provenance/confidence rather than blocking the project.

## Fast-track intent
The user wants the project accelerated without reducing it to a toy/demo cart.
Acceleration should come from parallel work and quick physical validation.

## Commercial direction
Short-term plan discussed:
- close the currently unused sole proprietorship to avoid further fixed-cost accrual;
- preserve the business idea of repair/service of professional teleinspection systems;
- later reopen the business when PX1 is physically working and nearing a sellable second unit.

Likely commercial services later:
- repair/diagnostics of Mini-Cam Proteus, IBOS/Revi, IBAK, ROVVER-class equipment;
- cable/connector/camera/crawler/reel/control-unit repair;
- field diagnostics;
- scarce replacement-part fabrication;
- sale/service of PX1 after qualification.

This business note is secondary to the engineering goal and must not distract from finishing PX1.

## Current engineering emphasis
Do not spend more cycles inventing new architectures.
Work from current/ and the governing AGENTS.md.
Resolve unknowns by evidence, calculation, CAD and tests, then move toward the first physical build.
