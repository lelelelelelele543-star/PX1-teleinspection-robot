# PX-1 Rev.BM — TILT worm-set selection

Status: PROTOTYPE CANDIDATE, not release.

## Selected geometry basis
Use a matched module 0.5 worm/wheel set, 20:1, single-start, 20° pressure angle.

Preferred dimensional basis for CAD:
- worm: m0.5, 1 start, right hand
- worm pitch diameter: 9.0 mm
- worm OD: 10.0 mm
- worm bore: 3.0 mm
- worm overall length: 18.0 mm
- wheel: 20 teeth
- wheel pitch diameter: 10.0 mm
- wheel OD: 11.3 mm
- wheel face width: 5.0 mm
- wheel overall length: 11.0 mm
- wheel bore: 3.0 mm
- nominal shaft center distance: 9.5 mm

This geometry follows standard commercial m0.5 20:1 matched worm sets such as Reliance Precision W50SUR1+B + G50B20+R1. Rapid Electronics also lists a compact brass/steel 1:20 m0.5 set with 3 mm bores, confirming that the required size class is commercially available.

## Material target
- worm: stainless steel preferred for wet-environment robustness;
- wheel: brass/bronze preferred;
- no printed plastic gear for final underwater drive.

## Why selected
The complete pair is far smaller than the Ø52 mm head envelope. The 11.3 mm wheel OD and 10 mm worm OD leave ample space for bearings, motor coupling and wall thickness while providing the 20:1 reduction target.

## TILT motor interface
Current motor candidate: DCGM-N20-12V-EN-200RPM.
The 3 mm worm bore will not be mounted directly to an unverified motor shaft. Use a serviceable 3 mm intermediate worm shaft with coupling from the motor output. This avoids making the worm set dependent on one supplier-specific N20 shaft.

## Holding-torque requirement
Design target at TILT axis: >=0.22 N*m including factor of safety from Rev.BK.
The worm set must pass a physical holding/back-drive test before self-locking is credited. Geometry alone is not sufficient to guarantee self-locking under lubrication, vibration and manufacturing tolerance.

## Release holds
1. source exact matched set or equivalent with confirmed dimensions;
2. obtain/measure actual backlash;
3. measure N20 output torque/current on the purchased motor;
4. verify worm-bearing arrangement and 3 mm shaft coupling;
5. perform static 0.22 N*m holding test and cyclic TILT test;
6. corrosion/lubrication test;
7. final collision check in Ø52 head and DN150 robot assembly.
