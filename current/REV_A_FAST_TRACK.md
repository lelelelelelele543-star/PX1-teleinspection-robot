# PX1 Rev.A — 6×6 FAST TRACK

Status: ACTIVE WORKING PLAN.

## Non-negotiable architecture
Rev.A is a six-wheel crawler. This is frozen and may not be simplified to 4WD/4-wheel geometry.

Per side:
- wheel stations X50 / X150 / X250;
- five m1 Z50 stations X50 / X100 / X150 / X200 / X250;
- rear X250 long-axle input;
- one traction motor per side;
- Z16 -> Z40 bevel input;
- all three wheels on each side driven through the five-gear train.

System baseline:
- DN150-class crawler target;
- dry pressurized crawler body;
- manual camera lift;
- separately sealed removable camera head;
- professional reinforced six-core copper tether, no coax in main tether;
- first working tether length 40 m;
- 24 V-class power architecture;
- RS-485 control;
- ready-made electronics modules for prototype; no custom main PCB required.

## Fast-track rule
Do not branch into new crawler concepts. Work one physical chain to completion:
`motors -> bevel pair -> 5xZ50 per side -> 6 wheels -> body -> tether -> control -> camera -> lift -> console -> tests`.

A feature may be added only when it is required for the next physical test or removes a verified blocker.

## Build stages
### A0 — drivetrain bench
Goal: prove both motor-to-wheel transmission chains outside final pressure housing.
Exit: both sides run forward/reverse continuously, no tooth interference, shafts/bearings remain seated, current draw recorded.

### A1 — rolling 6×6 chassis
Goal: complete six-wheel crawler mechanically.
Exit: six wheels installed, free rolling verified, powered straight/reverse/turn test passed on bench and DN150 test section.

### A2 — 40 m power/control tether
Goal: drive the crawler from the operator end through the real tether architecture.
Exit: stable power + RS-485 at 40 m under motor load; no resets; voltage drop and motor current recorded.

### A3 — camera/light/manual lift
Goal: useful live inspection image from the moving crawler.
Exit: CVBS image, lighting adjustment, manual lift low/high positions, camera harness survives repeated lift cycles.

### A4 — demonstration system
Goal: director-ready working crawler.
Exit: crawler + 40 m tether + portable console + monitor + controls + pressure indication operate as one system. Reel may remain temporary/manual if it does not block demonstration.

### A5 — sealing and endurance
Goal: qualify body and service interfaces.
Exit: pressure decay/submersion test, repeated driving/lift cycles, thermal/current observations, video/EMC test.

### A6 — manufacturing release
Goal: convert proven prototype geometry into production documentation.
Exit: exact bought-part dimensions, released STEP/STL/drawings/BOM/pinouts/assembly procedure. No HOLD dimensions affecting machining.

## Priority order
1. drivetrain geometry and motor fit;
2. six-wheel rolling chassis;
3. electrical bench assembly;
4. 40 m tether test;
5. camera/light;
6. manual lift integration;
7. console;
8. sealing/endurance;
9. reel 100–150 m and production polish.

## Change control
Any change to wheel count, wheel stations, gear topology, rear-input principle, two-motor architecture, main tether philosophy or manual lift requires an explicit engineering change entry in `PX1_Change_Log.md`. Rev.A default answer is NO CHANGE.
