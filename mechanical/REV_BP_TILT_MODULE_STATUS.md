# PX-1 Rev.BP — TILT module status

Status: ASSEMBLY-CANDIDATE, not machining release.

## Frozen prototype architecture
- motor: DCGM-N20-12V-EN-200RPM class;
- motor shaft connected through separate turned coupler;
- independent Ø3 mm worm shaft;
- 2x 693-ZZ 3x8x4 mm support bearings;
- matched worm set: m=0.5, 1-start worm, 20-tooth wheel, ratio 20:1;
- non-contact HOME sensor near 0°;
- software working range: -105°..+105°;
- physical stops target: approximately -108° and +108°.

## Why physical stops are outside software limits
The hard stops are deliberately placed slightly beyond the commanded operating range so normal control does not hammer the mechanical stops. Final offsets must be adjusted after real assembly backlash and collision measurements.

## Holding requirement
Output holding target remains >=0.22 N·m with engineering margin. Worm reduction is expected to provide ample torque, but self-locking is NOT assumed.

## Acceptance before release
1. full range achieved without wire, shell or gear collision;
2. repeatable HOME position after 50 homing cycles;
3. no uncontrolled backdrive at 0°, +90°, -90° for 10 min each with power removed;
4. 500 cycles -105°..+105° without binding, overheating or visible gear damage;
5. measured backlash recorded at camera optical axis;
6. current at no-load and loaded motion recorded;
7. bearing pockets finalized from measured purchased 693-ZZ parts;
8. hard-stop geometry moved from envelope to manufacturable features.

## Next step
Integrate TILT module with the ROLL assembly and camera envelope, then run the complete Ø52 mm packaging and DN150 clearance check.
