# A55 — straight bevel formative-tooth correction

A54 uses `z/cos(delta)^3`, a helical-gear virtual-tooth approximation, not the usual straight-bevel Tredgold formative-tooth approximation. For a straight bevel gear use `z_v=z/cos(delta)` (approximate, not a conjugate tooth generator).

ASSUMED: module 1.5 mm, pressure angle 20 degrees, face width 8 mm, intersecting axes 90 degrees, z=16/40. These are PX1 design targets, not Mini-Cam measurements.

Analytic test: pitch cone angles sum to 90 degrees, formative tooth radii obey base < pitch < tip, face width <= cone distance/3. Run `python a55.py` to regenerate JSON. SVG is computed from exactly the same parameters and involute equations.

PASS: analytical identities. SKIPPED: FreeCAD and actual mesh/contact analysis. NEEDS_PHYSICAL_CHECK: tooth geometry, backlash, strength, shaft mounts, pressure sealing. The virtual 2D profile is NOT manufacturable straight-bevel gearing.

Next: implement 3D spherical involute/conjugate bevel gear surfaces or validated gear generator, then test contact and interference against A50 shafts.
