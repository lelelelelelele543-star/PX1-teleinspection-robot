# A19 — Tolerance sensitivity (design assumptions only)
Source: A18 analytic dimensions; not verified component measurements.
| Parameter | Nominal mm | Assumed ± mm | Verification |
|---|---:|---:|---|
| Outer face Y | 28.50 | 0.20 | CAD datum and machined inspection |
| Motor axis Y | 13.50 | 0.30 | Mounting stack / real motor |
| Relief radius | 13.00 | 0.25 | Tooling and bore inspection |
| Motor radius | 12.50 | 0.25 | Manufacturer drawing + measured sample |

Web = outer - axis - relief radius. Nominal 2.00 mm; worst-case 1.25 to 2.75 mm.
Radial clearance = relief radius - motor radius. Nominal 0.50 mm; worst-case 0.00 mm.
**FAIL** positive guaranteed clearance: even before shaft alignment, motor tilt or thermal effects, worst-case contact is possible. A17 is not cleared for manufacture. A future A20 variant should increase relief radius or tighten mounting/motor tolerances, while maintaining a structurally justified web; avoid assuming wall strength.
**PASS** arithmetic consistency. **SKIPPED** FreeCAD boolean and strength. **NEEDS_PHYSICAL_CHECK** motor size, tolerances, web strength, sealing effects.
