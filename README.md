> Current design study: **R16**. R15's external packaging was rejected in
> review because the rear tail, wheel contact and camera/lift arrangement were
> not serviceable. R16 rebuilds the CRP-150-class envelope, ties the six wheels
> into the side covers, adds recessed hand quick-release pins and replaces the
> camera pod. Start with `PROJECT_STATUS_R16.md`. This is **not a manufacturing
> release**.

# PX-1 Teleinspection Robot

Open engineering project for a pipe-inspection crawler based on the proven Mini-Cam Proteus CRP-150 / CAM026 / RMP architecture, rebuilt around available, replaceable and serviceable components.

## R12 component-fit study

R12 selects purchasable electronics and adds reproducible body/camera CAD checks. **Local packing passes; the retained lift conflicts with the packed body. R12 is not a complete assembly or manufacturing release.** Start with [PROJECT_STATUS_R12.md](PROJECT_STATUS_R12.md) and [the assembly review](mechanical/R12_ASSEMBLY_REVIEW.md). The source-derived Proteus architecture below remains the reference; do not mix the R12 DRV8871 pin profile with legacy BTS7960 code.

## Active controlled baseline

Start here:

- [`PROJECT_STATUS_RevPO.md`](PROJECT_STATUS_RevPO.md) — active complete system architecture;
- [`PROJECT_STATUS_R15.md`](PROJECT_STATUS_R15.md) — corrected selected-part assembly and validation scope;
- [`PROJECT_STATUS_R16.md`](PROJECT_STATUS_R16.md) — active CRP-150-style rebuild after user review;
- [`PROJECT_STATUS_R14.md`](PROJECT_STATUS_R14.md) — historical study, assembly PASS revoked;
- [`PROJECT_STATUS_RevPR.md`](PROJECT_STATUS_RevPR.md) — retained source-derived rear-wheel X250 topology;
- [`PROJECT_SUPERSESSION_RevPP.md`](PROJECT_SUPERSESSION_RevPP.md) — which historical experiments are no longer active;
- [`electrical/PX1_SystemWiring_RevPP.md`](electrical/PX1_SystemWiring_RevPP.md) — active end-to-end wiring and safety architecture;
- [`tether/PX1_Tether_RevPP.md`](tether/PX1_Tether_RevPP.md) — active six-core tether allocation;
- [`MASTER_DESIGN_BASIS_PROTEUS.md`](MASTER_DESIGN_BASIS_PROTEUS.md) — Proteus-derived mechanical design basis;
- [`reference/Proteus-CRP-150/`](reference/Proteus-CRP-150/README.md) — controlled source/evidence reconstruction.

If an older experimental revision conflicts with R16 or Rev.PO/Rev.PP/Rev.PR,
R16 takes precedence for the scoped nominal geometry; Rev.PR remains the
topology reference. R14's historical PASS must not be used as acceptance evidence.

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

Latest selected-part packaging study:
`mechanical/cadquery/PX1_R16_ProteusRebuild.py`

Review: `mechanical/R16_PROTEUS_REBUILD_REVIEW.md`.
R16 corrects the external package after user inspection: compact body end,
wheel-ground contact, integrated wheel stations, captive wheel pins, a central
folded lift and an armoured camera pod. Gear teeth/retention, tolerances and
physical qualification remain unfinished.

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
- R16 onboard conversion candidate: Mean Well RSD-60H-24, 128×60×25 mm, 60 W;
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

