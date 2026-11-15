# A8 — motor clamp cross-section / A7 interface correction

## Finding
The A7 macro uses MOTOR_D=24 mm, base width=26 mm, and mounting hole centres y=±9.5 mm with Ø3.2 holes. In a transverse motor envelope, the bolt-hole envelope overlaps the motor envelope by 12+1.6-9.5=**4.1 mm**. This is a **2D interference warning**, not proof of a 3D collision, since the longitudinal position and fastener protrusion matter.

## Proposed A8 geometry (all DESIGN TARGETS, not vendor-confirmed)
- Motor Ø24 mm (inherited A7 assumed).
- Clamp inner Ø25 mm, outer Ø31 mm (radial clearance 0.5 mm; wall 3 mm).
- Base width 44 mm, screw centres y=±19 mm, Ø3.2 holes.
- Nominal transverse clearance bolt-hole envelope to strap outer envelope: 19-1.6-15.5=**1.9 mm**.
- New base replaces A7's 26 mm width; it is NOT a drop-in upper strap. Length, hole x positions and motor footprint need integrated redesign.

## Tests
- PASS: arithmetic and positive nominal 2D radial clearance in script.
- FAIL (A7 legacy interface): bolt envelope intersects nominal motor section by 4.1 mm.
- SKIPPED: FreeCAD solid, tolerance stack, motor body and gear interference.
- NEEDS_PHYSICAL_CHECK: motor actual dimensions, clamp force, fastener access, vibration, sealing.

## Reproduce
Run `python3 px1_a8_motor_clamp.py` in this folder; it regenerates the SVG using dimensions and asserts. Preview is a dimension-driven schematic, not a CAD rendering.

## Assumptions / validation
| Parameter | Value | Confidence | Rationale | Verify |
|---|---:|---|---|---|
| Motor OD | 24 mm | ESTIMATED A7 | A7 script baseline | Vendor drawing / physical motor |
| Clamp radial clearance | 0.5 mm | DESIGN TARGET | Assembly allowance | Tolerance and thermal stack |
| Clamp wall | 3 mm | DESIGN TARGET | Preliminary section | FEA/physical clamp load |
| Base width | 44 mm | DESIGN TARGET | Separate fasteners from strap | Full 3D fit to chassis |
| Bolt y | ±19 mm | DESIGN TARGET | 1.9 mm nominal 2D gap | Edge-distance / fastener access |

## Next
Build the full A8 base + split upper clamp as FreeCAD solids; include x-direction holes, fasteners, gear Z16/Z40 and both motors, check 3D interference before approving the footprint.
