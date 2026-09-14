# PX-1 current integrated crawler — Rev.B

Date: 2026-09-14  
Status: **INTEGRATED MASTER PASS / EXACT WHEEL + FINAL BEVEL + PHYSICAL TEST HOLDS**

This is the single controlling crawler assembly. Recovered Proteus CRP150 architecture is used wherever it is known. Old WB files are retained only as engineering history/evidence; they do not override this master.

## Assembly chain

`pressure body -> 3 wheel stations/side -> 5 Z50/side -> rear X250 long-axle input -> 2 x Z40 -> 2 x supported Z16 -> 2 traction motors -> dry electronics -> manual lift -> fixed camera carrier -> sealed removable camera`

Service chain:

`dry pressure body -> removable PRESSURE/CAMERA cover -> compact flush pressure valve -> M12 gland -> exactly 6-core camera harness -> lift-arm guard -> 6-pin SP13 -> camera`.

## Source-controlled drivetrain details now present in the master

From `DRW-002-374`, both side drives together contain:
- 6 wheel stations;
- 10 x Z50 total;
- 6 x 61903-2RS bearings, 17 x 30 x 7;
- 6 x X-ring 18.72 x 2.62;
- 6 axle-flange envelopes;
- 2 x 61801-2RS bearings, 12 x 21 x 5, on the rear long-axle stations.

From `DRW-002-375`, the crawler body input contains:
- 2 x Z40 bevel gears;
- 2 x 61800-2RS bearings, 10 x 19 x 5;
- 2 x shaft seals 18 x 30 x 7.

From `DRW-002-386`, the motor input contains:
- 2 traction motors;
- 2 x Z16 bevel gears;
- 2 separate Z16 shafts;
- 2 x 61801-2RS support bearings, 12 x 21 x 5.

Exact axle shoulders, flange thicknesses and axial Y positions remain drawing/measurement work where the assembly sheets do not state them numerically. The bearing/seal sizes and quantities above are no longer placeholders.

## Current hard geometry

- wheel stations X50 / X150 / X250;
- ten Z50 positions X50 / X100 / X150 / X200 / X250, mirrored left/right;
- main body screen: 307 x 92 mm before rear extension;
- rear dry body now ends at **X410 mm**;
- lift body pivot X200;
- lift pivot heights Z92 / Z109;
- lift links 90 mm;
- camera shell Ø52 x 78 mm;
- service cover 86 x 44 x 6 mm;
- local camera harness: exactly six insulated conductors, hard OD max 6.5 mm.

## Real traction-driver packaging correction

The earlier `34 x 22 x 14 mm` traction-driver placeholders were wrong and are superseded.

The current master uses two conservative **BTS7960 / IBT-2 envelopes of 50 x 50 x 43 mm each**. They are placed in one rear upper dry electronics tunnel, not in a separate cartridge/module.

Current centers:
- driver A: X330 / Y0 / Z91.5;
- driver B: X382 / Y0 / Z91.5.

The tunnel outer envelope is approximately:
- X300...410;
- width 60 mm;
- Z65...117.

Executed CadQuery result:
- both BTS7960 envelopes outside dry volume: **0 mm³**;
- electronics pairwise intersections: **0**;
- electronics vs motor/Z16/coupling package intersections: **0**;
- minimum ideal-DN150 clearance of the new electronics roof: **~3.45 mm**.

This is a packaging PASS, not a manufactured-wall/pressure release. Physical DN150 testing remains mandatory because the margin is small.

## Other electronics retained in the same dry body

The current master also contains:
- STM32 `NUCLEO-F446RE` low-profile envelope;
- Cincon `CQB150W-110S24` converter/carrier envelope;
- Nichicon `UCS2D221MHD1TN` 220 uF / 200 V capacitor envelope;
- Delta-Opti `TR-1D*P2` video balun envelope;
- input-protection reserve.

All of those are inside the dry-volume union with zero pairwise overlap in the executed check.

The old generic Ø24.4 pressure-sensor cylinder has been removed from the fit claim rather than pretending it fits. **Pressure sensor exact article and mounting remain HOLD** and will be added only after selecting a real purchasable part.

## Six-core camera branch

Exactly six insulated conductors:
1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall shield, if used, is EMC only and never a DC-return conductor.

Current connector candidates:
- dry service: Molex Micro-Fit 3.0 `43025-0600` + `43020-0601`, contacts `43030-0007` / `43031-0007`;
- wet camera side: WEIPU `SP1310/S6I-N` powered harness sockets -> `SP1312/P6-C` camera pins.

## Executed integrated result

`mechanical/cadquery/PX1_Current_Master_RevB.py` currently returns:

**PASS_INTEGRATED_MASTER / EXACT_WHEEL_PROFILE_HOLD / Z16_Z40_FINAL_PAIR_HOLD / PRESSURE_TEST_HOLD / PROCUREMENT_HOLD**

Source-count check in the executed result:
- wheels 6;
- Z50 10;
- 61903 6;
- X-rings 6;
- rear side-drive 61801 2;
- Z40 2;
- 61800 2;
- 18x30x7 shaft seals 2;
- Z16 2;
- Z16 support 61801 2;
- traction motors 2;
- lift arms 4;
- local camera conductors 6.

Current ideal-DN150 clearances for non-wheel LOW-state envelopes:
- complete body including electronics roof: ~3.45 mm;
- service cover: ~7.37 mm;
- pressure cap: ~9.27 mm;
- M12 gland: ~13.86 mm;
- lift harness guard: ~27.78 mm;
- rear motor housing: ~18.36 mm.

## Wheel rule

The displayed Ø90 x 16 wheel remains only a visualization cylinder. It is not used as the final DN150 geometry.

MiniCam documentation identifies `QRW90SR/150` as the 90 mm soft-rubber wheel intended for CRP140/150 in 150 mm pipe. The exact production outer profile was not found in the recovered drawing pack, so final wheel clearance remains a measured-solid gate rather than a reason to redesign the crawler.

## Files

- controlling executable: `mechanical/cadquery/PX1_Current_Master_RevB.py`;
- controlling executed result: `mechanical/cadquery/PX1_CURRENT_MASTER_VALIDATION.json`;
- local execution exports `PX1_RevB_Current_Master.step`.

## Remaining hard gates before machining release

1. exact QRW90SR/150 wheel profile or measured equivalent + physical DN150 jig;
2. final hardened matched Z16/Z40 pair and supplier mounting distance;
3. exact axle shoulder/flange dimensions where not dimensioned in the recovered assembly sheets;
4. select a real pressure-sensor article and add its actual model;
5. final pressure-cover O-ring groove from the selected elastomer;
6. +0.25 bar decay/submersion test of body/cover/valve/gland;
7. six-core cable flex + CVBS/UART EMC test;
8. exact rear connector/tether-tail geometry;
9. physical dirty/wet crawler test.

No new crawler architecture is to be introduced unless a source part or physical test proves the Proteus-derived arrangement impossible.
