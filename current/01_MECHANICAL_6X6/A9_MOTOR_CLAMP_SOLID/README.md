# A9 — motor clamp solid generator (15 Nov 2026)

Continuation of A8. FreeCAD script constructs base, upper semi-annular strap, legs, bridging lands and four-hole longitudinal bolt ears. All geometry is **ASSUMED / DESIGN TARGET**, not Proteus measurements. Cross-section SVG is generated from the same numeric design parameters; it is a dimensioned 2D projection, **not** a CAD render or proof of execution.

## Known risks
- Motor Ø24 is a placeholder: verify actual motor body and gearhead separately.
- Bolt edge margin nominal 1.4 mm, probably insufficient for load: redesign tabs after load calculation.
- Clamp inner diameter 25 gives nominal radial 0.5 mm clearance; requires compliant liner or revised clamping split to actually grip motor.
- Motor axis Z17 is provisional; lower motor contour Z5, base top Z3, nominal vertical gap 2 mm.
- Strap/leg bridging may create FreeCAD Boolean problems: actual shape validation SKIPPED.
- No tolerances, screw head clearances, preload, or Z16/Z40 collision analysis yet.

## Checks
Python arithmetic: PASS for 0.5 mm radial clearance, 1.9 mm lateral bolt-to-strap gap, 1.4 mm nominal outer edge margin. FreeCAD run/STEP generation: SKIPPED. Physical motor fit: NEEDS_PHYSICAL_CHECK.

Next: run FreeCAD, repair any invalid solids, add screw-head recesses, evaluate bending and shaft/gear collisions before manufacturing.
