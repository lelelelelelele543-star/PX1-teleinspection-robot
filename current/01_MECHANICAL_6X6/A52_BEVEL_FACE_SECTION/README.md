# A52 — 8 mm bevel face section (design assumption)

A51 provided only pitch-cone angles. This stage adds an **assumed** 8 mm face-width interval along the common pitch generator and calculates inner pitch radii. It does **not** create bevel teeth or validate gear strength. Run `python a52.py` to regenerate the SVG and JSON; source of truth is this script.

At module 1.5, Z16/Z40, 90°: R=32.31099 mm, outer pitch radii 12/30 mm; inner pitch radii 9.02887/22.57219 mm. Face width is assumed, not from Mini-Cam or a vendor catalogue.

PASS: geometric identities, positive inner radii. SKIPPED: FreeCAD, tooth generation, contact and interference checks. NEEDS_PHYSICAL_CHECK: tooth geometry, mounting distance, bearings, torque, clearances. Next: true parametric straight-bevel tooth flanks and 3D solids, then mesh/interference validation.
