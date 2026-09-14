# PX-1 Mechanical CAD — current Rev.B

The controlling mechanical artifact is now one integrated crawler master rather than a chain of exploratory sub-studies.

## Current master

- engineering note: `PX1_CURRENT_MASTER.md`
- executable CAD: `cadquery/PX1_Current_Master_RevB.py`
- executed check: `cadquery/PX1_CURRENT_MASTER_VALIDATION.json`
- generated output: `PX1_RevB_Current_Master.step`

Status: **PASS_INTEGRATED_MASTER / WHEEL_GEOMETRY_DN150_HOLD / PRESSURE_TEST_HOLD / PROCUREMENT_HOLD**.

## Hard crawler architecture

- 3 wheel stations per side / 6 wheels total;
- X50 / X150 / X250;
- five m1 Z50 gears per side / ten total;
- two traction motors total;
- rear X250 long axle is the drive input on each side;
- manual camera lift;
- dry pressurized crawler body;
- separately sealed removable camera;
- no mechanical cassette/cartridge architecture.

## Source-derived assembly

The current master combines the recovered Proteus logic in one model:

- `DRW-002-374` side drive;
- `DRW-002-375` crawler housing / Z40 input / seals;
- `DRW-002-386` two-motor Z16 input;
- `DRW-002-744` manual lift / 150 N gas spring principle;
- `DRW-002-745`, `DRW-002-752`, `ASS-002-890` pressure/lift/camera service interface;
- `ASS-002-090`, `ASS-002-364` rear connector and cable strain-relief logic;
- `ASS-002-103` wheel lock assembly.

Where an original proprietary component is unavailable, the replacement is fitted into the same functional location rather than inventing a different crawler architecture.

## Current geometry

- body main screen 307 x 92 mm;
- rear motor housing end X384;
- wheel stations X50/X150/X250;
- Z50 stations X50/X100/X150/X200/X250;
- lift pivot X200;
- lift pivots Z92/Z109;
- links 90 mm;
- arm planes Y±31 mm;
- camera shell Ø52 x 78 mm;
- service cover 86 x 44 x 6 mm;
- opening 48 x 22 mm;
- flush pressure cap envelope Ø12 x 1.5 mm;
- M12 harness gland horizontal;
- camera harness exactly 6 insulated conductors, hard OD max 6.5 mm;
- lift harness guard envelope 10 mm.

## Six-core camera/lift interface

Exactly:

`+12V / GND / UART TX / UART RX / CVBS signal / CVBS return`.

Dry connector candidate: Molex Micro-Fit 3.0 six-way.

Wet camera connector: WEIPU SP13 six-pin.

No 8-core wet lift harness is controlling.

## Wheel rule

The master displays simple Ø90 x 16 cylinders only as visual wheel placeholders. They are not a valid production tire/profile solid and are excluded from final DN150 geometry release.

MiniCam currently specifies `QRW90SR/150` 90 mm wheels for 150 mm pipe. Final wheel release requires the purchased/measured wheel or exact missing outer-profile drawing/solid plus a physical DN150 jig.

Do not redesign the crawler around the simple cylinder proxy.

## Release rule

The integrated master is suitable for continuing design and prototype packaging, not for machining release.

Before manufacturing release it still needs:

- exact wheel profile;
- matched Z16/Z40 bevel hardware;
- exact pressure seal groove from the real elastomer;
- pressure decay/submersion test;
- six-core cable flex/EMC test;
- physical connector pin orientation;
- exact rear tether-tail dimensions;
- physical DN150 validation.

Historical WBxx files remain in the repository only as calculation/revision traceability. New work should update the current integrated master rather than creating a new crawler architecture.
