# PX-1 Rev.CD — digital ROLL repack

Status: engineering packaging candidate.

## Architecture
Final video path remains fully digital:

32x32 H.265 IP camera -> 100BASE-TX Ethernet-rated rotary joint -> fixed head electronics -> 10BASE-T1L -> long tether pair -> operator console.

No NTSC/PAL/CVBS and no coaxial video conductor are used.

## Mechanical result
The 32x32 camera board is rotated 45 degrees inside the head. Its diagonal is approximately 45.25 mm. With a 52 mm OD head and 2.5 mm wall, the nominal internal diameter is 47 mm, leaving only about 0.87 mm radial corner margin.

Therefore Ø52 mm is still possible on pure PCB outline, but this is now a **critical fit**, not a comfortable one. The exact lens mount, Ethernet/power connector, tall components and solder joints must be included before the shell can be frozen.

## Ethernet rotary joint
Current packaging assumes Ø22 mm class 100BASE-TX rotary joint with separate power circuits. Exact body length, cable exit geometry and mounting method remain HOLD until the selected purchased SKU drawing is verified.

## Bearing change
The previous 6803 (17x26x5) concept conflicts with a Ø22 rotary joint through the center. Rev.CD therefore removes 6803 from the digital ROLL baseline.

New bearing envelope candidate is 25x37x7 class (6805-size envelope) around the rotary-joint body. This is only a packaging candidate; fit, load, available sealing variant and actual OD stack must be verified before selection.

## Consequences
- central passage grows from 17 mm to >=25 mm;
- ROLL gear geometry must be recalculated around the larger bearing stack;
- camera board corner clearance becomes the current limiting dimension of the Ø52 head;
- 10BASE-T1L converter remains on the fixed side, so it does not rotate.

## Next gate
1. obtain exact 32x32 camera mechanical drawing including connector/lens heights;
2. obtain exact Ethernet rotary-joint drawing;
3. freeze bearing type around the rotary joint;
4. rebuild ROLL gear pair;
5. check resulting head OD/length;
6. re-run DN150 sweep with final external solid.
