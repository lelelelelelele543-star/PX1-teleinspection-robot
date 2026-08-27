# PX-1 Rev.EY — X200 central bevel stage detail

Status: prototype machining candidate, not production release.

## Function
The traction input is centered at X=200 mm so the folded camera/lift remains clear of the motor package.

Per side power path:
JGB37-555 -> flexible/rigid short coupling -> supported bevel-pinion shaft -> KHK SB1.5-1845H (Z18) -> KHK SB1.5-4518H (Z45) -> transverse output shaft -> sealed P0/P1 or P0/P2 boundary -> coupling -> center Z50 wheel shaft.

## Bevel geometry
Current catalog pair:
- module 1.5;
- ratio 45/18 = 2.5:1;
- small gear bore 8 mm class;
- large gear bore 10 mm class;
- pressure/load capacity must be verified against the exact purchased KHK revision before release.

## Pinion shaft
Own PX-1 shaft, not motor shaft load-bearing.

Candidate stack:
- motor coupling seat Ø6 or actual motor D-shaft adapter;
- shaft Ø8 h6 under small bevel gear;
- shoulder;
- Ø12 h6 under 61801 support bearing;
- axial retention by M5 thread + washer or DIN 471 circlip depending final axial space.

Material candidate: 40Х / 42CrMo4 or corrosion-protected stainless where practical.

The JGB37 output bearing is not used as the only bevel-mesh support.

## Output shaft
Candidate from body center outward:
- large bevel gear seat Ø10 h6 with key/retainer;
- 61800 bearing journal Ø10 h6;
- seal running land Ø18 h9, Ra <=0.4 um, no keyway/thread under seal lip;
- outboard service coupling journal Ø12 h6.

Dynamic boundary candidate: FKM 18x30x7 lip seal class, exact article after shaft-speed/pressure validation.

## Alignment
Critical geometry:
- bevel shaft axes nominally 90 degrees;
- center distance / mounting distance follows KHK pair drawing, not generic cone approximations;
- bearing shoulders on one machining setup where possible;
- output shaft bearing bore and seal bore coaxiality <=0.03 mm target;
- pinion shaft axis position to output-shaft axis <=0.03 mm target before backlash setting.

## Backlash / mesh setting
Do not hard-machine final axial shim position from nominal CAD only.
Use a shim pack or selectable spacer to set the pair after real gears arrive.

Prototype target:
- smooth full-turn contact with no tight spots;
- measured backlash recorded at 4 angular positions;
- blue/contact pattern centered on tooth flank;
- motor current at no-load compared left/right.

## Torque protection
Until exact motor bench calibration is complete, retain the project mechanical input limit of approximately 1.5 N*m at the bevel pinion.
Firmware/electronic current limiting should trip before gear or shaft overload.

## Service
The paired motor holder is removable from the top service opening.
Bevel pinion shafts remain captured in the holder so motor replacement does not disturb the P0/P1/P2 dynamic shaft seals.

## Release gates
- exact KHK gear pair physically measured;
- actual JGB37 shaft measured;
- contact pattern accepted;
- backlash hot/cold accepted;
- 30 min loaded run;
- 100 forward/reverse cycles;
- jam-current test;
- no oil/grease migration onto the shaft-seal lip.