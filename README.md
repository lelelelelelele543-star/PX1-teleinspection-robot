# PX-1 Teleinspection Robot

Open engineering project for a pipe-inspection crawler based on the proven Mini-Cam Proteus CRP-150 / CAM026 / RMP architecture, rebuilt around available, replaceable and serviceable components.

## Active controlled baseline

Start here:

- [`PROJECT_STATUS_RevPO.md`](PROJECT_STATUS_RevPO.md) — active complete system architecture;
- [`PROJECT_STATUS_RevPR.md`](PROJECT_STATUS_RevPR.md) — active corrected crawler mechanical master, rear-wheel X250 drive input;
- [`PROJECT_SUPERSESSION_RevPP.md`](PROJECT_SUPERSESSION_RevPP.md) — which historical experiments are no longer active;
- [`electrical/PX1_SystemWiring_RevPP.md`](electrical/PX1_SystemWiring_RevPP.md) — active end-to-end wiring and safety architecture;
- [`tether/PX1_Tether_RevPP.md`](tether/PX1_Tether_RevPP.md) — active six-core tether allocation;
- [`MASTER_DESIGN_BASIS_PROTEUS.md`](MASTER_DESIGN_BASIS_PROTEUS.md) — Proteus-derived mechanical design basis;
- [`reference/Proteus-CRP-150/`](reference/Proteus-CRP-150/README.md) — controlled source/evidence reconstruction.

If an older experimental revision conflicts with Rev.PO/Rev.PP/Rev.PR, the active documents above take precedence.

## Current project direction

The project preserves the useful Proteus mechanical and operator logic instead of inventing an unrelated crawler:

- six-wheel CRP-150-style crawler;
- five module-1 Z50 side gears per side;
- rear long-axle side-drive input at the rear wheel station;
- two traction motors with Z16 to Z40 bevel inputs;
- manual 150 N camera lift integrated into the crawler body;
- separately sealed CAM026-like PAN/ROTATE camera;
- lightweight manual reel with brake, mechanical level-wind, meter wheel and slip ring;
- portable CCU with hardware E-STOP and high-voltage tether supply.

## Current mechanical master

Active CAD source:
`mechanical/cadquery/PX1_CRP150_Master_RevPR.py`

Rev.PR corrects the old X200 side-input placeholder to the verified Proteus topology:
- X50 front wheel;
- X100 idler;
- X150 centre wheel;
- X200 idler;
- X250 rear wheel + driven long axle.

Executed Rev.PR validation passes the current ideal-DN150 body screen, five-Z50 pitch-spacing check, Ø35 x 100 motor-envelope screen and current dry-volume packaging reserves. It remains prototype engineering, not machining release.

## Current electrical baseline

- CCU-side high-voltage generation, Proteus principle;
- main tether power: 100-120 VDC design class, exact commercial modules still open;
- crawler local traction/electronics bus: 24 V class;
- crawler/controller baseline: STM32 NUCLEO-F446RE or serviceable equivalent;
- command/telemetry: RS-485;
- video: balanced analog CVBS;
- one reinforced six-core copper inspection tether:
  1. HV+;
  2. HV return;
  3. RS485_A;
  4. RS485_B;
  5. VIDEO+;
  6. VIDEO-;
- no coaxial main tether, optical fibre or Ethernet patch-cable substitution;
- ready-made replaceable electronic modules for the prototype;
- no custom multilayer main PCB required for the prototype;
- no cartridge/cassette mechanical service modules.

## Project structure

- `reference/Proteus-CRP-150/` verified original architecture and replacement decisions;
- `mechanical/` FreeCAD, STEP, STL, DXF and mechanical drawings;
- `electronics/` component studies, protection and historical electronics work;
- `electrical/` active electrical architecture and interfaces;
- `tether/` cable architecture and qualification;
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
