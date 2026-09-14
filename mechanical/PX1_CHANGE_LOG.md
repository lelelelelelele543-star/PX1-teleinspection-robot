# PX1 Change Log

## 2026-09-14 - CURRENT FINAL-ASSEMBLY consolidation

- Replaced the misleading integrated `PASS` wording with scoped validation: geometry checks may pass while any proxy-based component remains HOLD.
- Corrected DRW-002-374 side-drive bearing count: **6 x 61801 per side, 12 total**, plus 2 x 61801 at the two Z16 input shafts.
- Added the source key count: 6 x 4x4x12 wheel/gear keys and 2 x 4x4x7 rear-input keys.
- Preserved Proteus topology: rear X250 drive input, five equal Z50 gears per side, two motors, supported Z16 shafts and transverse Z40 body shafts.
- Replaced the Cincon packaging reserve with the manufacturer quarter-brick envelope 57.9 x 36.8 x 12.7 mm.
- Retained Delta TR-1D*P2 43 x 16 x 15, Nichicon D18 x 25 and NUCLEO footprint 82.5 x 70.
- Refined LAPP 53112000 gland envelope to M12x1.5 / SW16 / L26.5.
- Repacked LM2596/MP1584/MAX485 reserves so all electronic keep-outs fit the dry volume without mutual or motor-input intersections.
- Generated one canonical `PX1_Current_Master.step`; old Rev/WB models remain history and do not control manufacturing.
- Generated HOLD-tagged machining-reference STEP files and fit-check STL files. They are not falsely released as final metal parts.
- Final unresolved dimensions are collected as physical measurement/procurement holds rather than filled with assumed values.
