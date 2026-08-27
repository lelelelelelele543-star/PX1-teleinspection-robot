# PX-1 Rev.BL — camera drive gear decision

Status: engineering candidate, not machining release.

## ROLL
Frozen for packaging/prototype:
- spur gears;
- module 0.5;
- pressure angle 20°;
- pinion z17;
- driven gear z51;
- ratio 3:1;
- theoretical center distance 17.0 mm.

The FreeCAD generator now creates analytical involute flanks. Root fillet/tool geometry is still HOLD, so the generated z17/z51 pair is suitable for packaging, kinematic checks and prototype printing, but not yet for final metal gear manufacture.

## TILT
Current target:
- single-start worm;
- wheel 20 teeth;
- nominal ratio 20:1.

Rev.BL intentionally does **not** invent a production worm tooth form. Worm/wheel geometry is dependent on the selected standard or purchased matched pair, including lead angle, axial/transverse module, pressure angle, center distance and hob/tool geometry.

## Why this split
ROLL benefits from low backlash and easy continuous motion, so a conventional spur pair is appropriate. TILT must resist gravity and impact loads when power is removed, therefore the worm candidate remains preferable, subject to real back-drive testing.

## Next gate
1. source a compact matched worm/wheel set around 20:1 that fits the Ø52 mm head;
2. replace the worm envelope with exact supplier dimensions;
3. run complete head collision check through TILT -105..+105°;
4. verify motor current, holding torque and thermal rise;
5. re-run DN150 passage check;
6. only then freeze head shell and shaft drawings.
