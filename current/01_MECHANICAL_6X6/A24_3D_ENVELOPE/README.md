# A24 — preliminary 3D bounding-envelope separation (not FreeCAD)
All dimensions in millimetres and marked **ESTIMATED/design target**. This is an independent candidate layout, NOT a verification of the A23 geometry or of Proteus. The A23 file could not be fetched via connector; therefore no inheritance of its dimensions is claimed.

Motor longitudinal cylinder X=101..135, Y=0, Z=0, radius=12.5. Shaft transverse cylinder axis X=150,Z=0,Y=-32..32, radius=6. Gear Z50 bounding disk XZ radius 37.5 at X=150,Z=0, Y=24..30. The disk radius is a conservative placeholder, not an involute tooth model.

The separating X-plane gap between motor and shaft is 150-6-135 = **9 mm**. Assumed total adverse axial error 1 mm => **8 mm**. Motor and gear projected XZ regions overlap, but their assumed Y envelopes are separated by 24-12.5 = **11.5 mm**. This is a bounding-box **candidate** screen only; it is not a complete 3D interference analysis. A change in axial/Y gear placement invalidates the conclusion.

| Parameter | Status | Rationale | Future verification |
|---|---|---|---|
| Motor Ø25, X101..135 | ESTIMATED | compact motor candidate | manufacturer mechanical drawing and assembly |
| Shaft Ø12, X150 | ESTIMATED | prior axle candidate | frozen CAD and bearing stack |
| Gear R37.5, Y24..30 | ESTIMATED | intentionally broad placeholder | Z50 model and actual hub thickness |
| Combined X error 1mm | ESTIMATED | screening allowance | tolerance stack of all mounts |

**PASS (script self-tests):** arithmetic separating gaps and deliberate overlap regression. **SKIPPED:** FreeCAD, true solid Boolean checks, complete housing, actual tooth geometry. **NEEDS_PHYSICAL_CHECK:** all bought part sizes, pressure seals and mechanical loading.

Next: replace these placeholder placements with actual transforms from current master, generate FreeCAD solids, run `common()` intersection volumes and export STEP plus CAD-derived preview. No manufacturing release.
