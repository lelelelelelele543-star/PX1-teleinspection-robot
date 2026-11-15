# A12 — screening Z16 undercut (2026-11-15)

Design assumptions, NOT Proteus measurements: module m=1.5 mm; standard 20° full-depth rack with addendum coefficient ha*=1; Z16/Z40 external gears; nominal center distance 42 mm. Historical A10/A11 remain independent preliminary geometry.

## Reproducible analytic result
For ideal rack generation, approximate minimum profile shift to avoid root undercut: x_min=max(0,ha* - z sin²(alpha)/2). Critical unshifted count zcrit=2/sin²20°=17.097264. For Z16 x_min=0.064178; Z40 x_min=0. Thus **unshifted Z16 is at theoretical undercut risk**. A candidate x1=+0.20, x2=-0.20 preserves sum shift zero for a future gear-pair design, but x2 negative requires checking tooth root, tooth thickness, actual working pressure angle, contact ratio and backlash. This candidate is NOT validated.

## Status
PASS (analytic): formula evaluated; nominal center 42 mm. SKIPPED: executable Python on GitHub, FreeCAD solid, tooth-generation and interference/contact sweep. NEEDS_PHYSICAL_CHECK: machining quality, strength, backlash, wear. No release for manufacturing.

## Next
Integrate actual shifted involute profiles into A11 generator, verify mating teeth at 42 mm over a full mesh cycle, and check Z16 root thickness and Z40 negative shift. Keep prior A11 profile as reference, not production geometry.

## Provenance / verification
All parameters assumed/design target. Formula based on standard involute rack-generation geometry, not a manufacturer datasheet. Verify against ISO 21771 / ISO 6336 definitions and actual cutter/gear supplier before manufacturing.
