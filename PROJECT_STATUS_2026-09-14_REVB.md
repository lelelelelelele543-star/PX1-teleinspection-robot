# PX-1 project status — Rev.B — 2026-09-14

## Current state

PX-1 now has one integrated current crawler master built directly around the recovered Proteus architecture instead of separate exploratory concepts.

Current master status:

**PASS_INTEGRATED_MASTER / WHEEL_GEOMETRY_DN150_HOLD / PRESSURE_TEST_HOLD / PROCUREMENT_HOLD**

Files:

- `mechanical/PX1_CURRENT_MASTER.md`
- `mechanical/cadquery/PX1_Current_Master_RevB.py`
- `mechanical/cadquery/PX1_CURRENT_MASTER_VALIDATION.json`

Running the master exports one complete `PX1_RevB_Current_Master.step`.

## Frozen crawler architecture

- 3 wheel stations per side / 6 wheels total;
- X50 / X150 / X250;
- 5 x m1 Z50 gears per side / 10 total;
- rear X250 long-axle drive input;
- 2 traction motors total;
- dry pressurized body;
- manual camera lift;
- separately sealed removable camera;
- no mechanical cassette/cartridge architecture;
- no custom main PCB required for first working prototype.

## Current integrated mechanical chain

`pressure body -> side-drive / wheel stations -> rear X250 drive input -> two supported motor inputs -> manual lift -> fixed head carrier -> sealed camera`.

Current main values:

- main body screen length 307 mm, width 92 mm;
- current rear motor-housing end X384;
- wheel stations X50/X150/X250;
- Z50 stations X50/X100/X150/X200/X250;
- lift body pivot X200;
- lift pivots Z92/109;
- lift links 90 mm;
- arms Y±31, 4 x 14 mm screen;
- camera shell Ø52 x 78 mm;
- LOW camera axis X83.5569 / Z75.

## Pressure / camera service interface

Source-like service chain:

`dry body -> removable PRESSURE/CAMERA cover -> flush pressure valve -> horizontal M12 gland -> six-core local harness -> arm guard -> SP13 -> camera`.

Current geometry:

- cover 86 x 44 x 6 mm;
- service opening 48 x 22 mm;
- 2 x M4 centres X226/X296 as PX-1 prototype choice;
- horizontal LAPP `53112000` M12 gland candidate;
- compact pressure-cap envelope Ø12 x 1.5 mm;
- local harness hard OD maximum 6.5 mm;
- arm-guard envelope 10 mm.

Integrated LOW ideal-DN150 screen for released non-wheel envelopes:

- body ~7.81 mm;
- service cover ~7.37 mm;
- pressure cap ~9.27 mm;
- M12 gland ~13.86 mm;
- lift guard ~27.78 mm;
- rear motor housing ~18.36 mm.

Pressure release still requires real seal dimensions and +0.25 bar decay/submersion testing.

## Camera/lift local wiring — six cores only

Exactly six insulated conductors:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall braid/shield, when present, is EMC only and never DC return.

Dry service connector candidate:

- Molex Micro-Fit 3.0 `43025-0600`;
- `43020-0601`;
- female contacts `43030-0007`;
- male contacts `43031-0007`.

Camera quick disconnect remains WEIPU `SP1310/S6I-N` powered-side sockets -> `SP1312/P6-C` camera-side pins.

Local cable target: 6 x 0.25 mm² class, preferred OD 5.5...6.0 mm, hard maximum 6.5 mm. LAPP `0028679` is a promising 6 x 0.25 mm² Ø5.4 mm continuous-flex sample but is unshielded and must pass the complete CVBS/UART/PWM interference test before release.

## Wheels / DN150

The assembly uses six 90 mm wheel placeholders so the STEP is complete, but the simple Ø90 x 16 cylinder is not treated as the real production tire profile.

MiniCam's current Proteus compatibility table specifies `QRW90SR/150` 90 mm wheels for 150 mm pipe. The recovered source pack contains the wheel-lock assembly `ASS-002-103`, but not the exact production outer tire solid/profile.

Therefore:

- crawler architecture remains unchanged;
- 90 mm / DN150 compatibility is source-supported;
- final geometric DN150 release waits for a purchased/measured `QRW90SR/150` or exact recovered wheel model;
- physical DN150 jig remains mandatory.

## Rear tether interface

Current master follows the recovered `ASS-002-090` / `ASS-002-364` functional layout:

`crawler connector -> contacts/spring -> cable housing/nut -> seals/gland -> PU sleeve/crimp -> adhesive heatshrink -> cable cup -> reinforced six-core tether`.

Exact dimensions of the PX-1 replacement tail remain a manufacturing/detail gate; no new tail architecture is being invented.

## Immediate next work

Do not branch into new concepts. Continue the current master only:

1. recover or measure the real 90 mm wheel profile;
2. lock the matched Z16/Z40 bevel pair and mounting distance;
3. convert the current service-cover/valve/gland screens into exact machining dimensions after samples;
4. freeze six-pin connector numbering from physical parts;
5. finish the rear tether connector/strain-relief dimensions;
6. add purchased electronics envelopes and final internal mounts to this same master;
7. perform pressure, lift-cycle, EMC/video and physical DN150 tests;
8. only then issue production drawings/STL/STEP/BOM release.
