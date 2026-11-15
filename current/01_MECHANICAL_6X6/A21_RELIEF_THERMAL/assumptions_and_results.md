# A21 — combined radial tolerance and thermal budget

All values **ASSUMED/design target**, not measurements of Proteus or certified component specifications.

| Parameter | Assumed value | Reason | Verification |
|---|---:|---|---|
| Relief radius / tolerance | 13.40 ± 0.25 mm | A20 candidate | Inspect machined part |
| Motor radius / tolerance | 12.50 ± 0.25 mm | A20 candidate | Supplier drawing and caliper |
| Radial eccentricity allowance | 0.20 mm | Initial assembly budget | Shaft/plate datum stack |
| Motor thermal rise | +60 °C | Conservative scenario, not test | Instrumented run |
| Plate thermal shift | −30 °C | Independent adverse scenario | Environmental specification |
| Motor expansion coefficient | 12e−6 /K | Steel-like placeholder | Actual material |
| Plate expansion coefficient | 23e−6 /K | Aluminium-like placeholder | Actual alloy |
| Outer, axis and tolerances | 29.5±0.2, 13.5±0.3 mm | A20 baseline | CAD drawing |

Formula: minimum assembled gap = (13.4−0.25)(1+23e−6×(−30)) − (12.5+0.25)(1+12e−6×60) − 0.20 = **0.18175 mm**.

Nominal radial clearance = 0.90 mm; tolerance-only worst case = 0.40 mm; combined worst case = **0.182 mm**. This combines deliberately adverse temperatures and tolerances, not a probability model.

**PASS** analytical arithmetic / positive budget under listed assumptions. **SKIPPED** FreeCAD collision, full 3D positioning and strength. **NEEDS_PHYSICAL_CHECK** dimensions, material, temperature and assembly eccentricity. Remaining web 1.85 mm has not been strength-verified.

Next: establish true X150/motor envelope datums from current CAD, build a solid motor + plate and test 3D intersections; revise the plate if the 0.18 mm reserve proves insufficient.