# A47 — staggered motor envelope (conceptual engineering check)
Source: A15 motor/plate conflict, A46 follow-up. **DESIGN TARGET**, not Proteus dimensions.
Preserve two motors, 6 wheels, Z16→Z40 and five Z50 per side. Avoid moving the existing plates outward.
Assumed Ø25×65 mm motors, Y=±8.5 mm, X ranges 55–120 and 150–215 mm; inner plate faces Y=±22.5 mm.
Calculated nominal plate clearance = 22.5−8.5−12.5 = **1.5 mm**, motor end gap = **30 mm**.
This is a **top-view 2D envelope**, not an assembled mechanism. Motor shafts, rear X250 input, bearing seats, pressure shell and routing are unresolved. This is NOT a release of a motor arrangement; a two-motor input path must be physically realizable without belts.
PASS: 2D arithmetic and bounds. SKIPPED: FreeCAD Boolean/STEP, 3D collision, gear mesh. NEEDS_PHYSICAL_CHECK: purchased motor lengths, mounts, thermal, sealing and DN150.
Run: `python a47.py` to regenerate SVG and CSV.
Next: create explicit longitudinal shaft-to-X250 gear path and 3D collision model before choosing this alternative.
