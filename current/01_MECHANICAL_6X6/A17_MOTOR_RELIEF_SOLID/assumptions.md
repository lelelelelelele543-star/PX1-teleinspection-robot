# A17 — two internal motor relief plates (DESIGN ASSUMPTION)
Continuation of A16; not a new drivetrain architecture. The cutter is a cylinder aligned with X, rather than a rectangular pocket. This is a parametric FreeCAD solid-generation script; **not executed in this run**. SVG is a dimensioned 2D projection based on the same design constants, not a CAD render.

| parameter | assumed mm | reason | verification |
|---|---:|---|---|
| plate X interval | 90..140 | local mounting envelope only | compare current 6x6 assembly |
| plate Y inner faces | ±22.5 | A16 baseline | assembly Boolean |
| plate thickness | 6 | A16 baseline | strength/fasteners |
| plate Z interval | -20..20 | preliminary local section | shaft/bearing envelope |
| motor axis Y | ±13.5 | A16 baseline | purchased motor STEP |
| motor diameter | 25 | A16 envelope | supplier drawing |
| cutter radius | 13 | motor radius 12.5 + 0.5 clearance | tolerance stack |
| motor X interval | 100..132 | assumed 32 mm occupied length | actual motor/gearbox envelope |

At motor equator: plate inner face Y=22.5, cutter extreme Y=26.5, hence **4.0 mm** maximum intrusion and **2.0 mm** residual web. This is **not a strength validation**. Note: the cut removes material along a cylindrical profile; it must not be confused with a through-hole. This plate is an internal structural plate, **not** the pressure housing.

## Validation
- PASS (analytic): 6 - (13.5 + 13 - 22.5) = 2 mm minimum nominal web.
- SKIPPED: FreeCAD runtime, STEP/FCStd export, 3D Boolean, actual fit, whole assembly interference.
- NEEDS_PHYSICAL_CHECK: web fatigue, material, fastening, tolerance, actual motor, pressure envelope.

## Next
Run macro in FreeCAD and inspect solids. Then import A3/A16 current assembly and check **X150 shaft, Z50, bearings, screws**. Reject or reinforce 2 mm web if load analysis requires. No manufacturing release.
