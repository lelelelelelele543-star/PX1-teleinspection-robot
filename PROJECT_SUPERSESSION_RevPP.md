# PX-1 PROJECT SUPERSESSION MAP — Rev.PP

Date: 2026-09-01
Status: ACTIVE CONTROL DOCUMENT

## Purpose
This document prevents old experimental branches from being mistaken for the active PX-1 design after completion of the Proteus CRP-150 / RMP / CCU reverse-engineering pass.

## Active master documents
The following documents define the active architecture, in priority order:

1. `PROJECT_STATUS_RevPO.md` — active system architecture baseline.
2. `MASTER_DESIGN_BASIS_PROTEUS.md` — mechanical and project design basis.
3. `PROJECT_MASTER_PROTEUS_REPLACEMENT_BASELINE.md` — Proteus replacement mission and preservation rules.
4. `electrical/PX1_SystemWiring_RevPP.md` — active end-to-end electrical architecture.
5. `tether/PX1_Tether_RevPP.md` — active six-core tether allocation and safety architecture.
6. `reference/Proteus-CRP-150/` — controlled reference/evidence register.

If an older file conflicts with the documents above, the Rev.PO/Rev.PP architecture wins.

## Superseded power architecture
The following earlier 48/60 V tether studies remain useful only as historical calculations and component studies:

- `electronics/REV_CJ_POWER_BUDGET_48V_DISTRIBUTION.md`
- `electronics/REV_CL_48V_INPUT_PROTECTION.md`
- `electronics/REV_DJ_COMPACT_48_TO_24_POWER_CORRECTION.md`
- 48/60 V line-voltage decisions inside `electronics/REV_GS_TWO_MOTOR_POWER_BUDGET.md`
- 48/60 V line-voltage decisions inside `tether/REV_GS_PROTEUS_6CORE_CABLE_BASELINE.md`

They are superseded by the Proteus-derived long-tether principle:

`CCU high-voltage source -> 100-120 VDC-class tether -> crawler local 24 V bus`.

The old 48 V material may still be used for low-voltage bench testing and as reference for power budgeting, but not as the released long-tether architecture.

## Superseded digital-video / Ethernet experiments
The following remain engineering experiments only and are not the active tether/video architecture:

- `electronics/REV_BY_DIGITAL_VIDEO_ARCHITECTURE.md`
- `electronics/REV_BZ_DIGITAL_VIDEO_COMPONENT_SELECTION.md`
- `electronics/REV_CA_ROLL_DIGITAL_LINK_SELECTION.md`
- `electronics/REV_CB_ETHERNET_ROLL_AND_CAMERA_CORRECTION.md`
- `electronics/REV_CC_32MM_DIGITAL_CAMERA_SELECTION.md` where it depends on Ethernet/digital tether video
- `electronics/REV_CD_DIGITAL_ROLL_REPACK.md`
- `electronics/REV_CE_MINI_ETHERNET_SLIP_RING.md`
- `electronics/REV_CG_DIGITAL_HEAD_DIMENSION_THERMAL_FREEZE.md` where it depends on the superseded digital link
- 10BASE-T1L allocation inside `tether/REV_GS_PROTEUS_6CORE_CABLE_BASELINE.md`

Active prototype architecture:
- RS-485 command/telemetry over one differential pair;
- balanced analog CVBS over one differential pair;
- no Ethernet requirement;
- no coax in the main tether;
- no optical fibre.

## Superseded cartridge/cassette mechanical concepts
Any file using a cartridge/cassette concept as a required mechanical service unit is historical only, including:

- `mechanical/REV_BV_ROLL_CARTRIDGE.md`
- `mechanical/REV_BW_ROLL_CARTRIDGE_SERVICE_INTERFACE.md`
- `mechanical/freecad/PX1_Roll_Cartridge_RevBV.py`
- `mechanical/freecad/PX1_Roll_Cartridge_Service_RevBW.py`
- `mechanical/freecad/PX1_Digital_Roll_Cartridge_RevCD.py`
- `mechanical/freecad/PX1_Digital_Roll_Cartridge_RevCF.py`

Active rule: use ordinary integrated mechanical parts and serviceable covers, flanges, shafts, bearings and seals. Do not create mandatory cartridge/cassette assemblies.

## Superseded crawler geometry
Historical CAD that conflicts with the audited CRP-150 source architecture must not be machined.

Specifically reject any variant with:
- centre-wheel input instead of rear long-axle input;
- module-1.25 side gears instead of module 1.0;
- side-cover O-ring geometry inconsistent with the confirmed 190x1.5 source architecture;
- four traction motors or independent wheel motors.

Active side drive per side:
`front Z50 -> idler Z50 -> middle Z50 -> idler Z50 -> rear/input Z50`.

## Still-useful older work
Older documents are not deleted. Component dimensions, test methods, CAD methods, seal studies, motor packaging, thermal calculations and service ideas may be reused if they do not conflict with the active master documents.

## Release rule
No file is manufacturing-released merely by being present in the repository. Only files explicitly promoted into a controlled `release/` set after dimensional, safety and prototype validation may be used for machining or final electrical construction.
