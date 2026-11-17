# PX1 integrated chassis milestone M1

A single reproducible FreeCAD script combines body, lid/gasket proxy, six wheels, six wheel axles, six bearing proxies, four idler stubs, 10 Z50 pitch envelopes, two motor envelopes and two Z16/Z40 input proxy pairs.

## Assumptions and conflicts
- Body 307×92×70 mm, wheel Ø105×18 mm, gear module 1.0 mm, five Z50 per side at 50 mm pitch, motor envelope Ø24×62: ESTIMATED design targets, not CRP150 measurements.
- The earlier isolated bevel design used module 1.5. This script does **not** silently reuse that incompatible module for the Z50 train.
- No verified gear teeth, proper bevel contact, lid aperture, O-ring gland, shaft pressure seal, bearing seats or full dynamic interference checking.
- Wheel/gear solids may overlap motor/shaft envelopes. STEP export is geometry, not PASS.
- The motor and bevel proxy positions require redesign after CAD collision checks.

## Reproduce
Run `PX1_Integrated_6x6_M1.py` with FreeCAD Python (FreeCADCmd). Outputs FCStd and STEP beside script. SVG is a parameter-based 2D plan, **not** an export of the FreeCAD solid.

## Checks
PASS: analytical gear center distance = module × (50+50)/2 = 50 mm; wheel count 6; Z50 count 10; motor count 2.
NOT_RUN: FreeCAD execution, STEP creation, BREP intersections, kinematics.
PHYSICAL_CHECK: pressure 0.4–0.7 bar, shaft seals, real gear contact and component fit.

Next: run full FreeCAD geometry intersection audit, then replace pitch proxies with verified Z50 teeth and the Z16/Z40 contact stage.
