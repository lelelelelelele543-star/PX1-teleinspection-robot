# PX-1 Teleinspection Robot

Open engineering project for a pipe-inspection crawler based on the proven Mini-Cam Proteus CRP-150 / CAM026 / RMP300 architecture, rebuilt around available, replaceable and serviceable components.

## Active project direction

The project preserves the useful Proteus mechanical and operator logic instead of inventing an unrelated crawler:

- six-wheel CRP-150-style crawler;
- five equal side gears per side;
- two traction motors with Z16 to Z40 bevel inputs;
- manual camera lift;
- sealed CAM026-like PAN/ROTATE camera;
- lightweight manual RMP300-style reel;
- simple modular control unit.

The controlled Proteus reconstruction and replacement register is maintained in [`reference/Proteus-CRP-150/`](reference/Proteus-CRP-150/README.md).

## Current electrical baseline

- internal robot power: 24 V class;
- crawler and console controllers: STM32 NUCLEO-F446RE;
- RS-485 command and telemetry link;
- balanced analog video over dedicated conductors in one reinforced six-core inspection tether;
- no coaxial main tether, no optical fiber and no bundle of loose ordinary twisted pairs;
- ready-made replaceable electronic modules for the prototype;
- no custom main PCB required for the prototype.

## Project structure

- `reference/Proteus-CRP-150/` verified original architecture and replacement decisions;
- `mechanical/` FreeCAD, STEP, STL, DXF and mechanical drawings;
- `electronics/` schematics, harnesses, pinouts and protection;
- `electrical/` electrical architecture and interfaces;
- `firmware/crawler/` crawler firmware;
- `firmware/console/` operator-console firmware;
- `firmware/common/` shared protocol and utilities;
- `manufacturing/` machining, assembly and inspection instructions;
- `bom/` purchasable parts and alternates;
- `tests/` prototype verification and acceptance tests;
- `docs/` controlled documentation;
- `release/` manufacturing release only.

## Release rule

Files in `release/` are the only files intended for manufacturing. Reference, historical, reconstructed and experimental material must not be treated as released production data.

