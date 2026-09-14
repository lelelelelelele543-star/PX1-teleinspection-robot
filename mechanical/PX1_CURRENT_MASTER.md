# PX1_Current_Master

**Date:** 2026-09-14  
**Controlling 3D assembly:** `CAD/PX1_Current_Master.step`  
**Status:** `INTEGRATED_GEOMETRY_COMPLETE_WITH_HOLDS / NOT_FINAL_MACHINING_RELEASE`

This is the single active PX1 mechanical integration master. Proteus CRP-150 remains the mechanical reference; old WB/Rev files are historical evidence only. No HOLD proxy is treated as a manufacturing PASS.

## Frozen architecture

- 6 wheels at X50 / X150 / X250, mirrored left/right.
- 5 x Z50 per side at X50 / X100 / X150 / X200 / X250; m1, Z50, B4 source topology.
- Rear X250 wheel station is driven.
- Two motors total; each path is motor -> supported Z16 -> Z40 -> rear long axle -> five-Z50 train.
- Dry positively pressurized body; dynamic wheel sealing by X-rings, Z40 body shafts by 18x30x7 seals.
- Manual four-arm camera lift; camera is separately sealed and removable.
- Removable PRESSURE/LIFT service cover with compact pressure valve and M12 camera-cable gland.
- Local camera harness exactly six insulated conductors: +12V, GND, TX, RX, CVBS signal, CVBS return.
- Main tether exactly six copper cores: HV+, HV return, RS485_A, RS485_B, VIDEO+, VIDEO-. Tensile aramid member is mechanical only.
- No coax in main tether, no mechanical cassettes, no external pressure-body hinges, no custom PCB in prototype.

## Corrected source drivetrain count

Current master now contains 12 x 61801 bearings in the two side drives (6 per side), plus 2 x 61801 supporting the two Z16 shafts. This corrects the previous current-master simplification that represented only two side-drive 61801 bearings. Also present: 6 x 61903, 6 x X-ring 18.72x2.62, 2 x 61800, 2 x 18x30x7 shaft seals, 10 x Z50, 2 x Z16, 2 x Z40, 6 x 4x4x12 wheel keys and 2 x 4x4x7 rear-input keys.

## CAD truth

The master includes the full integration chain, but parts whose exact source/vendor geometry is unresolved are explicitly named `HOLD_*` in STEP. This applies to the QRW90 wheel profile, side-cover contour, axle shoulders/flanges, bevel tooth/mounting details, exact motor length/flange, BTS7960 purchased-board variant, gas-spring end fittings, SP13 exact variant, pressure sensor and rear tether termination.

Non-wheel ideal-DN150 LOW-state geometry currently clears the pipe model by at least 3.45 mm. This is a screen only; the 90 mm wheel proxy is not used for DN150 release.

## Purchased components already represented by verified dimensions

- NBK MLR-20C-6-6 coupling: OD20 x L24, bores 6/6 mm.
- LAPP 53112000 SKINTOP MS-M: M12x1.5, clamp 3.5-7 mm, SW16, total length 26.5 mm, thread length 6.5 mm.
- Cincon CQB150W-110S24: quarter-brick 57.9 x 36.8 x 12.7 mm.
- Nichicon UCS2D221MHD1TN: 220 uF / 200 V, D18 x 25 mm.
- Delta-Opti TR-1D*P2: 43 x 16 x 15 mm.
- NUCLEO-F446RE footprint: 82.5 x 70 mm; installed height remains configuration dependent.

## Controlling files

- `mechanical/cadquery/PX1_Current_Master_RevB.py` - historical executable path; current final-assembly source is also included in the release package as `PX1_Current_Master.py`.
- `CAD/PX1_Current_Master.step` - single current assembly STEP in the release package.
- `mechanical/PX1_CURRENT_CRAWLER_BOM_RevB.md` - current BOM mirror in GitHub.
- `mechanical/cadquery/PX1_CURRENT_MASTER_VALIDATION.json` - current validation.
- `mechanical/PX1_CHANGE_LOG.md` - current change journal.
- `electrical/PX1_Current_Electrical_Pressure_Pinouts.md` - electrical, pinout, sealing/pressure specification.
- `mechanical/PX1_Current_Manufacturing_Assembly_Test.md` - fabrication lists, assembly and test sequences.
