# A13 — Shifted involute Z16/Z40 (design only)

## Inputs and provenance
All values are **ASSUMED / DESIGN TARGET**, not measured Proteus values: module 1.5 mm, 20° rack pressure angle, z1=16, z2=40, shift x1=+0.20, x2=-0.20, standard addendum coefficient 1 and dedendum coefficient 1.25. Design centre distance 42 mm. The zero sum of shifts retains nominal centre distance. No vendor catalogue geometry is claimed.

## Calculations
Pitch radii: 12 / 30 mm. Base radii: 11.2763 / 28.1908 mm. Tip radii: 13.800 / 31.200 mm. Root radii: 10.425 / 27.825 mm. Nominal root-tip clearances: 0.375 / 0.375 mm. Analytical transverse contact ratio: 1.571508. These are **nominal geometrical calculations**, not evidence of non-interference under rotation.

## Important limitations
SVG is generated from analytic involute flanks with **placeholder radial extensions below base circles**. Trochoidal root fillets, protuberance, backlash, cutter tip radius, minimum tooth thickness, profile-shift effect on working pressure angle, tolerance stack, 3D solids, shaft bores, strength, alignment and real contact simulation are NOT validated. Phase is illustrative. Therefore not manufacturing-ready.

## Checks
- PASS (analytical / formula evaluation): sum shifts zero, 42 mm centre distance, root-tip radial clearances 0.375 mm, analytical contact ratio > 1.2.
- PASS (analytical): Z16 positive shift 0.20 exceeds theoretical standard-rack undercut threshold 0.06418.
- SKIPPED: actual Python interpreter execution in GitHub, FreeCAD, CAD collisions, contact sweep.
- NEEDS_PHYSICAL_CHECK: tooth contact, backlash, strength, motor fit, cutting, lubrication.

## Reproduce
Run `python3 px1_a13_shifted_mesh.py`. The SVG is a formula-derived design preview (not a FreeCAD render). Its tooth flank equations use involute function inv(t)=tan(t)-t and angular half-thickness at pitch pi/(2z)+2*x*tan(alpha)/z. Root contours are approximate.

## Next
Generate true rack-generated root trochoids and verify mesh across one least-common-tooth cycle with swept intersection; then create FreeCAD solid gear pair and test motor/axle fit.

## Assumptions / future verification
| Value | Class | Rationale | Verification |
|---|---|---|---|
| m=1.5 mm | ASSUMED | Continuity with A10-A12 | supplier gear stock / torque calculation |
| alpha=20 deg | ASSUMED | common rack design | cutting tool data |
| x1=+0.20, x2=-0.20 | DESIGN TARGET | mitigate Z16 undercut, preserve centre | generated tooth geometry / contact test |
| 42 mm centre | DERIVED FROM ASSUMED INPUTS | m*(16+40)/2 | CAD housing and motor envelope |
