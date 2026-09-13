# PX-1 Mechanical CAD

Controlled mechanical development uses source-controlled engineering notes plus executable CadQuery interference/clearance models. FreeCAD/STEP/STL are manufacturing and prototype handoff formats; no machining file is released until it is copied into `/release` with a controlled drawing revision.

## Hard Rev.B crawler architecture

- 3 wheel stations per side / 6 wheels total;
- wheel stations: `X50 / X150 / X250`;
- wheel-center pitch: `100 mm`;
- front-to-rear wheelbase: `200 mm`;
- five equal module-1 Z50 gears per side / ten total;
- two traction motors total;
- rear `X250` long axle is the drive input on each side;
- nominal wheel OD used by the current screen: `90 mm`.

Any four-wheel/two-axle interpretation is non-controlling unless an explicit architecture-change revision is approved.

## Controlled assembly hierarchy

1. `00_MASTER_PARAMETERS` — global dimensions and interfaces.
2. `10_BODY` — pressure body, covers and seal seats.
3. `20_DRIVETRAIN` — shafts, gears, bearings and wheel interfaces.
4. `30_CAMERA_LIFT` — manual parallelogram lift and fixed head carrier.
5. `40_CAMERA_HEAD` — sealed TILT/ROLL head and quick release.
6. `50_TAIL` — tether tail, strain relief and lowering eye.
7. `90_ASSEMBLY` — full crawler assembly and interference checks.

## Current hard lift/camera baseline — WB22A

**Rev.B WB22A** remains the controlled lift/camera geometry:

- body main screen length: `307 mm` plus rear extension features;
- body width: `92 mm`;
- wet-bay half width: `38 mm`;
- lift body pivot X: `200 mm`;
- lift pivots Z: `92 / 109 mm`;
- lift-link length: `90 mm`;
- arm planes: `Y=±31 mm`;
- arm screen section: `4 x 14 mm`;
- sealed camera shell: `Ø52 x 78 mm`;
- LOW camera axis: `X83.5569 / Z75.0 mm`.

WB22A corrected the wet-bay extrusion sign and separated the four-bar from the TILT axis using:

`pressure body -> four-bar lift -> fixed head carrier -> sealed TILT camera`.

Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**.

## Current pressure/service and local harness baseline — WB23C

**Rev.B WB23C** is the controlling camera-lift service topology.

It replaces the abandoned WB23B dual-flex-chamber / R16 flex-fan direction and supersedes WB23A absolute routing coordinates. WB23A remains historical evidence that a thin protected harness fits the lower arm, but it had a one-sided XZ-workplane Y-sign ambiguity and is not manufacturing control.

Controlling WB23C topology:

`dry pressure body -> removable PRESSURE/CAMERA SERVICE cover -> fill valve + horizontal M12 gland -> <=5 mm local harness -> removable arm guard -> fixed SP13 connector -> sealed removable camera`.

WB23C retains WB22A body pivot `X200`; there is no X207.5 shift.

Current screen values:

- service cover: `78 x 42 x 6 mm`;
- service opening: `58 x 24 mm`;
- prototype retention: `2 x M4` as a PX-1 choice, not asserted as exact Proteus screw count;
- provisional seal target: `2.0 mm` cord, groove study `2.5 x 1.5 mm` — not machining release;
- fill-valve hard envelope: `<=Ø14 x 6 mm`;
- gland candidate: LAPP `SKINTOP MS-M 53112000`, M12x1.5, 3.5–7 mm cable;
- gland orientation: horizontal / forward-facing;
- local harness target: `<=Ø5 mm`, 8 insulated cores + shield preferred;
- protected lower-arm run: approximately `s=20...72 mm`;
- service slack target: about `35 mm` at body side and `35 mm` at head side;
- dry connector candidate: JST `B8P-VH-B` + `VHR-8N`;
- camera quick disconnect remains WB15 WEIPU `SP1312/P6-C` + `SP1310/S6I-N` if final cable OD fits.

Executed WB23C ideal-DN150 fixed-part screen:

- cover ≈ `7.69 mm` clearance;
- pressure-port hard envelope ≈ `4.70 mm` — current limiting fixed item;
- horizontal M12 gland ≈ `13.86 mm`;
- M4 screw heads ≈ `7.93 mm`;
- LOW protected local harness/guard ≈ `30.20 / 29.23 mm`.

Only LOW must fit DN150. MID/HIGH are larger-pipe lift positions and may leave the DN150 envelope.

Status: **PASS_PACKAGING_SCREEN / SEAL TEST HOLD / FLEX TEST HOLD / PROCUREMENT HOLD**.

Controlled WB23C files:

- `REVB_WB23C_PRESSURE_LIFT_INTERFACE.md`;
- `PX1_PRESSURE_SERVICE_COVER_BOM_RevB.md`;
- `PX1_PRESSURE_SERVICE_COVER_DRAWING_SPEC_RevB.md`;
- `cadquery/PX1_WB23C_PressureLiftInterface_RevB.py`;
- `cadquery/REV_B_WB23C_VALIDATION.json`;
- `../electrical/PX1_CAMERA_LIFT_INTERFACE_RevB.md`;
- `../docs/PX1_SERVICE_CAMERA_HARNESS_RevB.md`;
- `../docs/PX1_WB23C_QUALIFICATION_PLAN_RevB.md`.

Source evidence supplement:

- `../reference/Proteus-CRP-150/PRESSURE_LIFT_INTERFACE_EVIDENCE.md`.

## Release rule

`PASS_SCREEN` or `PASS_PACKAGING_SCREEN` means only that the stated engineering packaging check passed. It is not a machining, pressure-boundary, cable-life or procurement release.

Current mandatory physical gates include purchased-part measurement, pressure decay, submerged leak test, lift flex cycling, wet/grit cycling, video/UART/power checks and physical DN150 validation.

Legacy README values `250 mm body length`, `94 mm body width` and `160 mm wheelbase` are superseded by the active Rev.B controlled baseline above.
