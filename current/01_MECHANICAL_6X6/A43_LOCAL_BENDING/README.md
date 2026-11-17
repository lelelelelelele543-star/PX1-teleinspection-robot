# A43: local bending at X150 grooves
**Assumptions:** bearings x=±12 mm; gear force at x=0; grooves x=±15 mm; T=10 Nm; module 1.5; Z50; pressure angle 20°; groove root Ø11; stress factors Kb=Kt=2. All are ESTIMATED/DESIGN TARGET, not measured Proteus dimensions. Verify against CAD, DIN 471 manufacturer drawings, motor torque budget, and actual loads.

**Correction to A42:** The maximum midspan bending moment 1.70268 Nm cannot be assigned to grooves outside the supports in this ideal single-force model. The groove bending moment is 0 here; the torque-induced von Mises stress is 132.55 MPa (conditional). Real gear forces at other stations, wheel reactions, overhang loads, bearing widths, misalignment and fatigue can change this dramatically.

**PASS:** formula symmetry, support equilibrium and local Python test. **SKIPPED:** FreeCAD/STEP. **NEEDS_PHYSICAL_CHECK:** actual forces, fatigue, notch radii, shaft sealing.

Next: integrate all Z50 mesh forces and wheel forces using CAD coordinates and calculate a true combined moment envelope.