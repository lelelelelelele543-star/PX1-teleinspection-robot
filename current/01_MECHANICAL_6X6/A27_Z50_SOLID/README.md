# PX1 A27 — Z50 solid generator

Source: A26 involute profile (project assumptions, not Mini-Cam measurements). Added FreeCAD macro generating a 50-tooth solid with Ø12 through-bore, Ø24 hub, 8 mm gear thickness and 4 mm hub extension. SVG is an independent 2D projection computed from the same equations, **not** a render of an executed FreeCAD model.

## Verification status
- PASS: mathematical design dimensions: pitch Ø75, outside Ø78, root Ø71.25 mm.
- SKIPPED: FreeCAD macro execution, solid validity, STEP export and Boolean collisions (FreeCAD not executed in this run).
- NEEDS_PHYSICAL_CHECK: bearing fits, shaft interface, keyway, root fillet, backlash, tooth strength, tolerances and 0.4–0.7 bar sealing.

## Next
Execute macro in FreeCAD; inspect wire closure/solid validity, then compare exported STEP with A25 motor/shaft envelopes and replace simplified A25 cylinder. Correct tooth root transitions and add shaft keyway before manufacturing.
