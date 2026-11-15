# A4 — Shaft pressure boundary: preliminary axial stack (2026-11-15)

**Engineering status:** DESIGN CONCEPT, not a production seal assembly. This does not release H03 or change main/current.

## Parameters and assumptions
| Parameter | Value | Confidence | Reason | Future verification |
|---|---:|---|---|---|
| Shaft diameter | 12 mm | ASSUMED | initial design envelope; not a Proteus measurement | confirm fit to drivetrain shaft/bearing and shaft seal catalogue |
| Seal A width | 7 mm | ASSUMED | axial allowance only; no specific seal selected | select pressure-rated lip seal with full drawing |
| Vent / inspection gap | 4 mm | ASSUMED | conceptual interseal drain space | prove drain and pressure relief path; avoid water ingress |
| Seal B width | 7 mm | ASSUMED | second axial allowance only | select validated seal and lip orientation |
| Bearing width | 7 mm | DESIGN TARGET | dimensional envelope; no model selected | verify exact bearing ID/OD and loads |
| End shoulders | 3 mm each | ASSUMED | conceptual retention allowances | mechanical tolerance stack, clips, assembly sequence |
| Internal gauge pressure | 0.4–0.7 bar | USER DESIGN TARGET | project requirement | pressure vessel and seal validation |

Axial length = 3 + 7 + 4 + 7 + 7 + 3 = **31 mm**. The diagram shows only an axial envelope. Radial gland geometry, OD/ID of selected pressure seals, lip contact, bearings, and vent plumbing are NOT designed yet.

## Pressure load (not a seal rating)
Using nominal shaft diameter D=12 mm, projected area A=pi*D²/4=113.097 mm². Force F = p*A, p in N/mm² = bar*0.1.

- 0.4 bar gauge: 4.5239 N
- 0.7 bar gauge: 7.9168 N

**These forces do not establish allowable pressure of any bearing or seal.** The historical 0.3 bar SKF warning is treated as an unresolved candidate-specific restriction, not as a proven limit of this conceptual two-seal design. Pressure acting on different effective diameters, differential pressure across each lip, dynamic shaft runout, friction, heat, contamination and assembly tolerances remain unknown.

## Validation and next step
Run: `python3 px1_pressure_axle.py --out .` to regenerate SVG/CSV and run analytical assertions. Script-level analytical check: PASS (algebra and dimensions); FreeCAD 3D: SKIPPED; seal manufacturer datasheet rating: SKIPPED; physical pressure test: NEEDS_PHYSICAL_CHECK.

**Next:** select a documented pressure-rated seal family for actual shaft diameter and pressure direction; design its true gland, shaft finish, vent/drain route, bearing support and tolerance stack; generate FreeCAD solid assembly and collision check. Do not use this diagram as a manufacturing drawing.
