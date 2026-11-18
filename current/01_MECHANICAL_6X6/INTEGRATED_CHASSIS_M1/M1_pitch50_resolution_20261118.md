# M1 integrated pitch resolution — 2026-11-18

**Decision (DESIGN ASSUMPTION, not a verified production gear):** retain AGENTS.md frozen X50/X150/X250 wheel locations and five Z50 gears per side at X50, X100, X150, X200, X250. Use module **m=1.0 mm** for the spur chain, giving pitch diameter d=mz=50 mm and center distance (d+d)/2=50 mm. This supersedes the inconsistent m=1.5/55-mm stations in exploratory audits, **not** any proven manufacturer geometry.

Two sides: 10 Z50 gears total; six wheel stations; input at rear X250 through Z16→Z40 with rigidly keyed Z40/Z50 input. Five consecutive external gears yield four sign inversions, hence X50, X150, X250 wheel stations rotate in the same direction on each side.

**Analytical PASS:** 4×50=200 mm from first to last gear; X50→X250; wheel spacing 100 mm; 10 gears and 6 wheels. At m=1.5 the required center distance would be 75 mm, FAIL for 50-mm station pitch.

**NOT_RUN:** FreeCAD generator, involute geometry, mesh/backlash, tooth root strength, 3D clearance, STEP/reopen, seal pressure validation. **PHYSICAL_CHECK:** available module-1 gears, shafts/bearings, dynamic seals rated for 0.4–0.7 bar, motor/bevel alignment.

**Integration next:** change station source-of-truth in existing M1 FreeCAD generator, preserve 6-wheel and 2-motor architecture, re-evaluate body/gear radial envelope and motor input clearance; produce CAD-based PNG and STEP only after execution.

Do not mark production-ready. Local executable preview and JSON were generated during this run; GitHub text checkpoint intentionally contains no fabricated CAD outputs.
