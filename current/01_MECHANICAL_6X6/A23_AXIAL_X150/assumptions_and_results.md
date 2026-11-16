# PX1 A23 — X150 axial envelope screen (2026-11-16)
All values **ESTIMATED / DESIGN ASSUMED**, not Proteus measurements or supplier data.
This screens only X intervals and does not establish 3D non-interference.
|Parameter|Assumed mm|Rationale|Future verification|
|---|---:|---|---|
|Motor body X start|100|Inherited A17|CAD manufacturer STEP|
|Motor body length|32|Inherited A17|Motor drawing|
|Motor output protrusion|8|Conservative candidate|Gearhead and coupling drawing|
|Rear axle center X|150|Frozen X150 station|Assembly datum|
|Axle radius|6|12 mm candidate axle|Bearing/shaft design|
|Z50 face width|10|Initial gear stock candidate|Gear stress/fit study|
|Motor axial + tolerance|1|Design tolerance budget|Manufacturer drawing|
|Axle position − tolerance|0.5|Design assembly budget|GD&T|
|Axle radius + tolerance|0.2|Deliberately conservative|Shaft tolerance|
|Gear face + tolerance|0.4|Design allowance|Gear supplier drawing|

Nominal motor+output endpoint = 140 mm; nominal axle start = 144 mm; nominal Z50 face start = 145 mm.
Worst-case endpoint = 141 mm; axle start = 143.3 mm; gear face start = 144.3 mm.
**PASS (X-only)** axle 2.3 mm, Z50 face 3.3 mm, using explicitly assumed geometry.
**SKIPPED** actual 3D booleans / FreeCAD. **NEEDS_PHYSICAL_CHECK** all motor and gear dimensions.
**Critical:** The above does NOT prove X150 motor collision is fixed. Axle and gear may intersect other parts or motor extension in Y/Z, and A17 relief was defined at X100–132 only. No manufacture release.
Next: use supplier motor STEP and parametric FreeCAD solids for X/Y/Z intersection and seal/gear checks.
