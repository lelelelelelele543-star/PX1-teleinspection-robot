# A18 — independent geometry cross-check of A17

All dimensions are **ASSUMED** (A17), not measured Proteus dimensions. The source script reproduces the SVG's section geometry.

| Parameter | Value | Status | Verification |
|---|---:|---|---|
| Plate Y inner/outer | 22.5 / 28.5 mm | ASSUMED | Full CAD assembly |
| Motor Y axis | 13.5 mm | ASSUMED | Supplier motor drawing |
| Motor envelope Ø | 25 mm | ASSUMED | Supplier motor drawing |
| Cutter Ø | 26 mm | DESIGN TARGET | Tolerance analysis |
| Minimum nominal web | 2.0 mm | DERIVED | FreeCAD section + strength |
| Relief half-height | 9.380832 mm | DERIVED | FreeCAD section |
| Removed volume per plate | 1657.786 mm³ | DERIVED | FreeCAD Boolean volume |

**PASS:** analytic computation, positive residual web, cylinder segment integration. **SKIPPED:** FreeCAD, STEP, full robot collision. **NEEDS_PHYSICAL_CHECK:** actual motor, structural strength, manufacturing tolerances.

Next: execute A17 FreeCAD macro and compare its cut volume against 1657.786 mm³ per plate; then check X150 shaft, bearings, Z50 gears. No manufacturing release.
