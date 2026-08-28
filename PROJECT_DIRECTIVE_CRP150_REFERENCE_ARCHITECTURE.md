# PX-1 — CRP-150 reference architecture directive

Status: ACTIVE PROJECT DIRECTION. This directive supersedes any tendency to redesign proven Proteus mechanisms without a clear sourcing/service reason.

## Mission
Build a teleinspection system that preserves the successful working concept, proportions, ergonomics and service behavior of MiniCam Proteus CRP-150, while replacing unavailable, obsolete, expensive or proprietary parts/electronics with readily obtainable and field-serviceable alternatives.

The target is NOT to invent a new crawler architecture. The target is a practical CRP-150-like system that can be maintained from accessible parts.

## What should stay as close as practical to Proteus
### Crawler
- overall CRP-150 style body form and six-wheel layout;
- side geared drivetrain concept;
- wheel positions/stance and low DN150 operating posture;
- manual lift concept and camera placement;
- open forward camera area in LOW position so the camera still sees ahead and wastewater cannot be trapped in a cup/pocket;
- pressurized dry body and serviceable sealing architecture;
- tail/cable strain-relief philosophy.

### Camera
- compact sealed rotating camera head concept;
- useful picture when folded LOW;
- rotation/tilt behavior close to the original operating experience;
- serviceable optical window, lighting and seals;
- proprietary camera electronics may be replaced with simple available video/control hardware.

### Reel
- lightweight mobile manual Proteus/RMP-style reel;
- manual crank, brake, level wind and measuring wheel/counter concept;
- compact frame and easy transport are preferred over powered reel complexity.

### Control unit
- preserve the simple Proteus operator workflow: monitor, joysticks/controls, distance indication, crawler drive, camera motion and lights;
- replace proprietary high-cost control electronics with modular readily available electronics;
- prototype should avoid a custom main PCB where possible.

## What is allowed to change
Change a Proteus detail only if at least one condition is true:
1. original spare part is unavailable or excessively expensive;
2. original part is known to be a recurring repair problem;
3. a standard bearing/seal/motor/connector/module can provide the same function with easier service;
4. the original electronics can be replaced by simpler modular control without changing the operator experience;
5. safety, ingress protection or manufacturability requires the change.

Any such change must preserve the mechanical/functional role of the original part as closely as practical.

## Source hierarchy
Before inventing a PX-1 mechanical solution, check the uploaded MiniCam drawings first.
Useful confirmed source groups already present in the project files include:
- CRP crawler/lift parts drawings such as DRW-002-744 / DRW-002-752 / DRW-002-745;
- CAM026 camera assembly ASS-001-801 / ASM001 and rotate-seal assembly ASS-002-004;
- Proteus cable-end socket ASS-003-215 and related connector drawings;
- RMP300 manual reel assembly ASS-004-097, reel halves ASS-004-094/095, core ASS-004-093, meter counter ASS-004-092 and reel handle ASS-002-712.

Use these documents as the primary architecture reference. Do not create extra pods, special drainage structures, nonstandard mechanisms or complex electronics merely because they are theoretically possible if the Proteus arrangement already solves the same problem more simply.

## Replacement philosophy
Preferred replacements:
- standard metric bearings and seals;
- generic 24 V DC gearmotors with measurable specifications;
- standard industrial waterproof connectors;
- STM32/other common controller modules;
- simple dual H-bridge motor drivers;
- RS-485 for commands/telemetry;
- balanced analog video over the selected 6-core inspection tether;
- common CVBS monitor/OSD/DVR modules;
- standard encoders/measuring wheel for distance.

Keep replacements modular and replaceable with ordinary workshop tools.

## Cable constraint
Main tether remains one Proteus-style reinforced 6-core copper inspection cable. No coaxial main conductor architecture, no optical fibre replacement and no bundle of separate ordinary twisted-pair cables.

## Design rule going forward
For every subsystem use this sequence:
1. reproduce/understand the Proteus source mechanism from uploaded drawings;
2. identify which original parts are actually unavailable/proprietary/expensive;
3. substitute only those parts;
4. keep the rest of the geometry and function as close to the proven Proteus arrangement as practical;
5. validate DN150 fit, sealing, service access and manufacturability.

## Immediate reset of current work
- treat the recent highly modified wet-deck/controller-saddle concepts as exploratory only, not the new design target;
- return the crawler nose/lift/camera packaging to the closest practical CRP-150 geometry supported by the uploaded drawings;
- rebuild the CAD viewer from this CRP-150-reference baseline;
- develop crawler, camera, reel and control unit as one matched system, not as unrelated redesigns.
