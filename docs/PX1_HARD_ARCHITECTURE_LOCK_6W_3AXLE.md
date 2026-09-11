# PX-1 HARD ARCHITECTURE LOCK — 3 AXLES / 6 WHEELS

Date: 2026-09-11
Status: MANDATORY / SUPERSEDES ANY CONFLICTING VISUAL OR HISTORICAL STUDY

## Non-negotiable crawler layout

PX-1 active crawler architecture is:
- **three wheel axles / wheel stations per crawler length**;
- **six wheels total**;
- three wheels on LEFT side and three wheels on RIGHT side;
- wheel station X coordinates: **X50 / X150 / X250**;
- wheel-center pitch: **100 mm**;
- front-to-rear wheelbase: **200 mm**;
- two idler gears between the three driven wheel-station gears per side;
- five equal Z50, module-1 side gears per side;
- one traction motor per side;
- rear long axle X250 is the drive input for each side.

Terminology:
- `3-axle`, `three-axle`, `three wheel stations per side`, `6-wheel` all refer to the same active geometry.
- `4WD`, `four-wheel`, `two-axle`, `2 wheel stations per side` are **NOT PX-1 Rev.B architecture**.

## CAD / render rule

Every active crawler CAD, drawing, render, generated image, assembly view and marketing/engineering illustration MUST visibly preserve:
- 3 wheel centers along each side;
- 6 wheels total;
- X50/X150/X250 station logic;
- no hiding/deleting the middle wheel to simplify a render.

If perspective hides one or more wheels, the underlying model must still contain all six. For engineering review, at least one side/orthographic/isometric view must make all three stations on one side unambiguous.

Any generated image showing only four wheels is illustrative error and must be rejected, not used as design evidence.

## Mechanical consequence

All following checks must use the six-wheel master:
- DN150 hard-part sweep;
- wheel profile/tread clearance;
- side-cover geometry;
- axle-flange/seal count;
- five-Z50 side gear train;
- motor torque and pull calculations;
- cable drag / obstacle climbing;
- lift and camera LOW-position clearance;
- weight/CG calculations;
- manufacturing drawings;
- BOM quantities.

Required per crawler:
- wheel shafts: 6;
- outer wheel dynamic seals: 6;
- wheel-station axle flanges: 6;
- wheels: 6;
- Z50 wheel gears: 6 total (3 per side), plus four Z50 idlers total (2 per side) = 10 Z50 side gears total;
- traction motors: 2.

## Change control

Changing PX-1 to four wheels or two axles requires an explicit written architecture-change request from the user and a new revision. It must never occur implicitly because of a render, packaging shortcut, legacy study, or component change.

## Correction record

2026-09-11:
- a generated development image incorrectly depicted a four-wheel/two-axle-looking crawler;
- that image is declared NON-CONTROLLING / REJECTED;
- active GitHub system baseline `PROJECT_STATUS_RevPO.md` already correctly specifies 3 wheel stations per side and a six-wheel layout;
- this hard-lock document is added so the error cannot propagate into future CAD/render/BOM work.
