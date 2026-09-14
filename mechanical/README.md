# PX-1 Mechanical CAD

Controlled mechanical development uses source-controlled engineering notes plus executable CadQuery interference/clearance models. FreeCAD/STEP/STL are manufacturing/prototype handoff formats; no machining file is released until it is copied into `/release` with a controlled drawing revision.

## Hard Rev.B crawler architecture

- 3 wheel stations per side / 6 wheels total;
- wheel stations X50 / X150 / X250;
- wheel-center pitch 100 mm;
- front-to-rear wheelbase 200 mm;
- five m1 Z50 gears per side / ten total;
- two traction motors total;
- rear X250 long axle is the drive input on each side;
- nominal wheel OD used by the current screen: 90 mm.

Any four-wheel/two-axle interpretation is non-controlling unless an explicit architecture-change revision is approved.

## Controlled assembly hierarchy

1. `00_MASTER_PARAMETERS` — global dimensions and interfaces.
2. `10_BODY` — pressure body, covers and seal seats.
3. `20_DRIVETRAIN` — shafts, gears, bearings and wheel interfaces.
4. `30_CAMERA_LIFT` — manual parallelogram lift and fixed head carrier.
5. `40_CAMERA_HEAD` — sealed TILT/ROLL head and quick release.
6. `50_TAIL` — tether tail, strain relief and lowering eye.
7. `90_ASSEMBLY` — full crawler assembly and interference checks.

## WB22A — hard lift/camera baseline

Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**.

- body main screen length 307 mm plus rear extension features;
- body width 92 mm;
- wet-bay half width 38 mm;
- lift body pivot X200;
- lift pivots Z92 / 109;
- lift-link length 90 mm;
- arm planes Y=±31 mm;
- arm screen section 4 x 14 mm;
- sealed camera shell Ø52 x 78 mm;
- LOW camera axis X83.5569 / Z75.0 mm.

WB22A corrected the wet-bay extrusion sign and separated the four-bar from the TILT axis using:

`pressure body -> four-bar lift -> fixed head carrier -> sealed TILT camera`.

## WB23E — current pressure/service-cover geometry

WB23C established the source-like service topology and WB23D proved first full integration. WB23E is the current dimensional cover baseline and supersedes the earlier 78 x 42 study.

Status: **PASS_SEAL_LAND_AND_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / PROCUREMENT HOLD**.

Current prototype screen:

- cover 86 x 44 x 6 mm;
- cover centre X261 / Y0;
- service opening 48 x 22 mm;
- two M4 centres X226 / X296;
- provisional face-seal groove centre path 4.0 mm outside opening;
- provisional groove width 2.5 mm;
- minimum M4 clearance-hole edge to groove outer edge 3.5 mm;
- minimum Ø8 screw-head edge to cover end 4.0 mm;
- minimum groove outer edge to cover Y edge 5.75 mm;
- horizontal M12 gland architecture retained.

Exact groove depth, screw torque and fill-valve thread remain HOLD until real parts/seal are measured.

## WB23F — pressure-port DN150 procurement envelope

Status: **PACKAGING RULE FROZEN / VALVE ARTICLE PROCUREMENT HOLD**.

The pressure valve is the limiting fixed roof item in LOW.

- preferred exposed valve+cap envelope: <=Ø12 x 5 mm;
- current prototype hard screen: <=Ø14 x 6 mm, ~4.70 mm ideal-DN150 clearance;
- Ø14 x 8 mm falls to ~2.71 mm and fails the current 3 mm screen.

Do not enlarge the crawler body for a convenient valve; use a lower-profile/recessed service port.

## WB23G — controlling local camera/lift harness

Status: **PASS_SIX_CORE_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / CABLE_SAMPLE_HOLD / PROCUREMENT_HOLD**.

The local harness is exactly **six insulated cores**, mapped 1:1 to the six camera functions:

`+12V / GND / UART TX / UART RX / CVBS signal / CVBS return`.

Overall braid/shield is EMC only and is not a DC return.

Current packaging:

- conductor target 0.25 mm² class;
- preferred cable OD 5.5...6.0 mm;
- hard maximum cable OD 6.5 mm;
- conservative removable lower-arm guard envelope 10 mm;
- WB22A body pivot remains X200;
- WB23E cover/opening remains unchanged;
- dry service connector candidate: Molex Micro-Fit 3.0 six-way `43025-0600` + `43020-0601`;
- camera quick disconnect remains WEIPU `SP1312/P6-C` + `SP1310/S6I-N`.

Executed WB23G check:

- all 6 wheel envelopes retained;
- all 10 Z50 retained;
- fixed service package vs wheels/Z50/lift/camera: 0 mm³ unintended collision;
- 10 mm guard vs Z50: 0 mm³;
- 10 mm guard vs camera: 0 mm³;
- LOW guard ideal-DN150 clearance ~27.78 mm;
- six-way dry connector envelope fits the 48 x 22 service opening.

Only LOW must fit DN150. MID/HIGH are larger-pipe lift positions and are not DN150 pass-through requirements.

Historical WB21/WB23A cable geometry and any 8-core local-harness text are superseded and retained only for engineering traceability.

## Controlled current files

- `REVB_WB23E_SERVICE_COVER_SEAL_LAND.md`;
- `REVB_WB23F_PRESSURE_PORT_DN150_SENSITIVITY.md`;
- `REVB_WB23G_SIX_CORE_LOCAL_HARNESS.md`;
- `PX1_PRESSURE_SERVICE_COVER_BOM_RevB.md`;
- `PX1_PRESSURE_SERVICE_COVER_DRAWING_SPEC_RevB.md`;
- `cadquery/PX1_WB23E_ServiceCoverSealLand_RevB.py`;
- `cadquery/REV_B_WB23E_VALIDATION.json`;
- `cadquery/PX1_WB23G_SixCoreHarness_RevB.py`;
- `cadquery/REV_B_WB23G_VALIDATION.json`;
- `../electrical/PX1_CAMERA_LIFT_INTERFACE_RevB.md`;
- `../docs/PX1_SERVICE_CAMERA_HARNESS_RevB.md`;
- `../docs/PX1_WB23C_QUALIFICATION_PLAN_RevB.md`;
- `../docs/PX1_DECISION_LOG_RevB.md`;
- `../reference/Proteus-CRP-150/PRESSURE_LIFT_INTERFACE_EVIDENCE.md`.

## Release rule

PASS_SCREEN / PASS_*_PACKAGING means only that the stated engineering geometry check passed. It is not machining, pressure-boundary, cable-life or procurement release.

Mandatory physical gates remain purchased-part measurement, pressure decay, submerged leak test, lift flex cycling, wet/grit cycling, measured cable resistance/head voltage, CVBS/UART/power interference testing and physical DN150 validation.

Legacy README values 250 mm body length, 94 mm body width and 160 mm wheelbase are superseded by the active Rev.B controlled baseline above.
