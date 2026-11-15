# A20 — motor relief revision (candidate, not manufacturing release)

A19 worst-case web 1.25 mm and clearance 0 mm. Candidate A20 increases **outer reference** 28.5→29.5 mm and relief radius 13.0→13.4 mm; other dimensions unchanged. These are **ASSUMED design targets**, not CRP150 measurements or supplier dimensions.

| Dimension | Nominal mm | Tolerance mm | Basis | Verification |
|---|---:|---:|---|---|
| outer radial reference | 29.5 | ±0.20 | assumed, +1.0 over A19 | CAD body envelope and X150/Z50 collision |
| motor axis reference | 13.5 | ±0.30 | inherited A19 assumed | CAD coordinate audit |
| relief radius | 13.4 | ±0.25 | assumed, +0.4 over A19 | machining feasibility and CAD solid |
| motor radius | 12.5 | ±0.25 | inherited A19 assumed | motor manufacturer drawing |

Worst-case web = (29.5−0.2)−(13.5+0.3)−(13.4+0.25) = **1.85 mm**. Worst-case radial gap = (13.4−0.25)−(12.5+0.25) = **0.40 mm**. Neither is a strength or assembly PASS. Enlarging outer reference may create a new collision with shell/gear train; **3D interference not checked**. This is a **radial schematic**, not a section of the full plate or true solid model.

Test: `python px1_a20.py`. PASS Python numerical assertions; SKIPPED FreeCAD and manufacturer dimensional verification; NEEDS_PHYSICAL_CHECK strength, alignment, seals. Next: build true solid with new radial envelope and run Boolean collision against X150, motor and Z50; revise if incompatible. Main remains untouched.
