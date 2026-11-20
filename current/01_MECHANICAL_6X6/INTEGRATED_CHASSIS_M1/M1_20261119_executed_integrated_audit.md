# PX1 M1 — executable integrated collision audit (2026-11-19)

This file records a **run**, not a claim of completed CAD. The existing PR83 FreeCAD generator was inspected and its numerical design assumptions were used to check the full drivetrain layout.

**PASS**: 50 mm center distances for five Z50 stations per side (module 1 design assumption); conservative DN150 wheel corner clearance 3.44 mm.

**FAIL**: both motor cylinders at x=35..77 mm, y=±14 mm, z=10 mm conflict with internal idler bearing envelopes at x=50 mm, y=±19..26 mm, z=0 mm. Conservative clearance -10.82 mm. The earlier relocation proposal is not integrated into the existing FreeCAD generator. No motor-to-rear-bevel verified torque path.

**PHYSICAL_CHECK**: 714 N nominal lid opening pressure load at 0.7 bar, 170×60 mm opening. Dynamic shaft seals, lid fastener preload and thread engagement remain unverified.

**NOT_RUN**: FreeCAD Boolean, STEP export and re-import, involute/bevel tooth contact, motion collision sweep.

The local Python audit generated an SVG and JSON, but this branch update stores the numerical findings and next integration gate only. Do not treat the sketch or envelope tests as manufacturing proof.

**Next integrated milestone**: change both motor placements and add the complete two-sided torque transfer in the same FreeCAD source, then execute FreeCADCmd, validate all solid intersections, and export/reimport STEP. No more isolated shaft-only revisions.
