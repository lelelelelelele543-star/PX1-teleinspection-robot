# A5 — motor relocation away from X150 (preliminary)
This is an **assumed XY envelope** for the existing 6-wheel PX1 architecture, not a CRP150 measurement or a motor mounting drawing. The earlier motor/central axle conflict is addressed at **2D envelope level only** by locating both motor housings between X170 and X224, behind X150 and before X250. The Z16/Z40 drive geometry is NOT proven.

## Assumptions (mm)
| Parameter | Value | Confidence | Rationale | Future verification |
|---|---:|---|---|---|
| Body outside XY | 278 × 68 | ESTIMATED | current/HOLD_REGISTER H02 | FreeCAD cavity reconstruction |
| Wall allowance | 4 | ASSUMED | early machined enclosure budget | stress, sealing and machining |
| Motor envelope | Ø25 × 54 | DESIGN TARGET | rounded current BOM Pololu5707 Ø25×53.8 | exact STEP and shaft orientation |
| Motor X start | 170 | ASSUMED | move behind X150 keep-out | full 3D shaft/bearing fit |
| Motor center Y | ±15.5 | ASSUMED | fit two motors in 60 mm cavity | full mounting bracket |
| Axle stations | 50, 150, 250 | BASELINE | AGENTS.md | 3D assembly |
| Axle keep-out diameter | 17 | ASSUMED | conservative transverse 2D projection | actual bearing/flange volumes |
| Minimum gap | 2 | DESIGN TARGET | initial envelope check | manufacturing tolerances |

## Computed envelope checks
- X150 axle outer edge X158.5 to motor start X170: **11.5 mm**.
- Motor end X224 to X250 axle near edge X241.5: **17.5 mm**.
- Motor-to-inner-wall minimum: **2.0 mm**.
- Gap between motor cylinders: **6.0 mm**.
- All four nominal 2D envelope checks >= 2 mm: **PASS**.
- Gear train, bevel stages, brackets, shaft seals, motor heat, wiring and dynamic tolerances: **SKIPPED / NEEDS_3D_CHECK**.
- Pressurization, strength, heat and physical clearance: **NEEDS_PHYSICAL_CHECK**.

Run `python3 px1_a5_motor_clearance.py` to recalculate and regenerate the SVG. Do not interpret nominal clearance as a manufacturing release. Next: model a 3D motor bracket and actual bevel gear axis intersections in FreeCAD, then test collisions against X150 axle and X250 drive.
