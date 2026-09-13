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

## Current integration baseline

**Rev.B WB22A — lift/camera integration correction** is the current controlled mechanical integration screen.

Current body/lift screen values include:

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

WB22A corrects a wet-bay extrusion-sign error found in an earlier audit model and replaces the WB20/WB21 direct lift-to-TILT-axis simplification with:

`pressure body -> four-bar lift -> fixed head carrier -> sealed TILT camera`.

WB21 cable electrical selections remain useful, but WB21 moving-clamp coordinates/free-flex length are superseded by WB22A mechanics and must be recalculated in WB23.

## Release rule

`PASS_SCREEN` means the checked CAD geometry passes the stated engineering screen. It is **not** a machining or procurement release. Current WB22A status remains:

**PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**.

The previous README values `250 mm body length`, `94 mm body width` and `160 mm wheelbase` were legacy studies and are explicitly superseded by the active Rev.B controlled baseline above.
