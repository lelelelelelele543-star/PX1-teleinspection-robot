# PX1 A10 — Z16/Z40 analytical input mesh

All numerical geometry is **ASSUMED/DESIGN TARGET**, not measured from Mini-Cam Proteus or verified purchased parts.

- External spur gear module m=1.5 mm; tooth counts 16/40; nominal pressure angle 20 degrees; zero profile shift; full-depth addendum 1m and dedendum 1.25m. These are provisional design inputs, not a supplier catalog claim.
- Assumed face width 8 mm (not used in contact ratio). Shaft axes nominally parallel and center distance 42 mm.
- Derived pitch diameters 24/60 mm, tip diameters 27/63 mm, root diameters 20.25/56.25 mm, ratio 2.5:1, theoretical radial clearance 0.375 mm.
- Nominal transverse contact ratio 1.6061 from ideal involute equation, no backlash/profile modification or tolerance included.
- The SVG draws exact analytic circles, **NOT actual involute teeth**, motor envelope, or collision-tested solids.

Verification: run `python px1_a10_mesh.py OUTPUT_DIRECTORY`; check JSON and SVG against tracked output. PASS: independent JavaScript arithmetic for center distance, ratio and contact ratio >1. SKIPPED: actual Python execution in connector runtime, FreeCAD and tooth solid generation. NEEDS_PHYSICAL_CHECK: backlash, gear strength, tolerances, shafts, lubrication, runout and gear quality.

Next: generate actual involute solids and place axes relative to rear X250 shaft and motor; verify motor/shaft/gear intersections before release.
