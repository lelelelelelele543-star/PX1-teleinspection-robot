# A39 — assumptions and verification
| Item | Value | Status | Reason | Future verification |
|---|---|---|---|---|
| Shaft diameter | 12 mm | ASSUMED inherited A37 | existing baseline | physical prototype/CAD |
| Groove root diameter | 11 mm | ASSUMED inherited A37 | unverified groove | manufacturer DIN 471 catalogue |
| Torque | 5,10,20 N·m | ASSUMED scenarios | sensitivity study | motor/gear load and stall torque |
| Kt | 1.0–3.0 | ASSUMED sweep, not a sourced value | show notch sensitivity | groove radius, Peterson charts/FEA |
| Material allowable | not selected | UNVERIFIED | no validated material | select grade, fatigue data |
| Shaft load | pure torsion | SIMPLIFICATION | no bending model | combined loading |
## Interpretation
At 20 N·m, nominal shear at Ø11 is 76.53 MPa; with assumed Kt=3 the peak proxy is 229.59 MPa. These are NOT allowable stresses and cannot establish PASS for manufacture. Physical sealing and 0.7 bar qualification remain open.
## Next
Source DIN 471 dimensions for Ø12, add fillet geometry and combined bending/torsion model; perform FreeCAD solid validation.
