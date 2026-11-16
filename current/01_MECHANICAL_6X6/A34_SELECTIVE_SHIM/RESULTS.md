# PX1 A34 — selective axial shim (not production release)

A33 worst-case 0.05–1.15 mm is improved by increasing the *assumed* retainer-face span from 28.60 ±0.15 to 28.80 ±0.15 mm, then selecting a 0.0–1.3 mm shim in 0.1-mm steps after measuring actual parts.

**PASS:** Python discrete grid: 2511 combinations of stack 27.60–28.40 mm and span 28.65–28.95 mm (0.01-mm steps), all produce endplay 0.15–0.25 mm with selectable shim. Nominal stack 28.00 / span 28.80 -> shim 0.60, play 0.20 mm. SVG is exact nominal axial schematic, not a 3D render.

**SKIPPED:** FreeCAD and boolean 3D checks. **NEEDS_PHYSICAL_CHECK:** DIN471 groove, clip deflection, inner-ring-only shim contact, actual tolerance, bearing fit, thermal expansion, sealing 0.7 bar.

Next: verify manufacturer DIN471 Ø12 groove dimensions and redesign shaft shoulders / retainer placement; check shims do not load outer races.
