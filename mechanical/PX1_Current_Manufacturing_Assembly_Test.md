# PX1 Manufacturing / Assembly / Test - Current

## A. Manufacture / buy now

The following standard/published items can be ordered now for prototype build and physical closure:
- 14 x 61801-2RS;
- 6 x 61903-2RS;
- 2 x 61800-2RS;
- X-ring 18.72x2.62 samples;
- 18x30x7 rotary shaft-seal samples;
- 2 x ISL PGM-32P-24-100-60-02 traction motors (+ spare recommended);
- 2 x NBK MLR-20C-6-6 couplings (+ spare recommended);
- LAPP 53112000 gland;
- STM32 NUCLEO-F446RE;
- Cincon CQB150W-110S24;
- Adafruit MPRLS Product 3965;
- Nichicon UCS2D221MHD1TN;
- selected WEIPU SP13 camera connector pair and SP17 rear connector samples;
- exact BTS7960/IBT-2 ready modules for dimensional closure.

## B. Final machining HOLD

Do **not** final-machine the following until their listed gates close:
- main pressure body / side-cover interfaces;
- wheel shafts and exact 61801 shoulder stack;
- side covers / seal grooves;
- Z16/Z40 matched bevel pair and mounting distances;
- final camera housing and internal pan stack;
- final rear tether strain-relief / aramid termination.

The CAM026 teardown now supplies a real camera architecture reference and an approximately 62.5 mm base OD, but internal wall thickness, bearing fits, ring-gear tooth geometry and seal grooves remain HOLD. No further user teardown measurements are required; close those values with controlled drawings, supplier samples or prototype work.

## C. 3D-print list - Anycubic Chiron

Current printable parts are fit/protection prototypes only:
- `PX1_Lift_Harness_Guard_PROTOTYPE.stl`;
- `PX1_PRESSURE_Cover_FitCheck_ONLY.stl`;
- `PX1_Rear_SP17_FitGauge.stl`.

Use PETG/ASA for dry fit. They are not released as final pressure boundaries or drivetrain structural parts.

## D. Assembly sequence

1. Inspect, deburr and clean all metal parts; record first-article dimensions.
2. Install the two Z40 body bearing/seal paths and rear long input shafts.
3. Build each side drive with three wheel shafts, two 61801 per wheel station, five-Z50 train, 61903, X-rings and flanges; set end float/backlash only from released drawings.
4. Fit supported Z16 shafts, matched Z16/Z40 pairs, NBK couplings and two ISL motors; verify free rotation before power.
5. Fit internal power conversion, controller, MPRLS pressure sensor, communication and video modules.
6. Fit rear service cover / SP17 connector and the independent mechanical tether strength termination. Electrical contacts must carry no towing load.
7. Assemble manual lift / gas spring, short exactly-six-core camera harness and SP13 camera connection.
8. Build the separate sealed camera using the CAM026-derived architecture reference; internal geometry remains prototype-gated.
9. Pressure-test crawler without camera and camera separately; then mate the two units.
10. Install wheels last and verify retention and tool access.

## E. Test sequence

1. Hand rotation: both side trains free, no binding, all three wheels on each side rotate consistently.
2. 24 V current-limited traction bench test, unloaded then restrained-load test.
3. RS-485 watchdog, loss-of-command STOP and hardware E-STOP.
4. Local camera harness: power + TX/RX + live CVBS simultaneously while cycling the lift.
5. +0.25 bar crawler pressure decay, then submerged bubble test; repeat with pressure-valve cap removed.
6. Separate camera pressure/submersion test.
7. Rigid DN150 jig with the **real QRW90SR/150 wheel/profile**, lift LOW, service hardware installed.
8. 40 m tether test with traction, video, control and pressure telemetry simultaneously under load.
9. Dirty/wet service test and timed wheel/camera/motor replacement.
10. Only after 40 m acceptance, validate the 100-150 m electrical/tether equivalent.

## F. Current release holds

1. QRW90SR/150 exact width, tread contour, hub and quick-lock geometry; full DN150 release remains HOLD.
2. Exact axial shoulder-by-shoulder order and Y locations of the two 61801 bearings at each wheel station, including FSS-002-063/FSS-002-064 dimensions.
3. Z16/Z40 pressure angle, face width, tooth system, mounting distance, backlash and heat treatment.
4. Actual purchased BTS7960/IBT-2 board dimensions including terminal/heatsink projections.
5. Exact reinforced six-core tether article, OD and aramid termination; SP17 structural strain relief remains prototype geometry.
6. Pressure-cover groove, valve and all pressure seals require +0.25 bar decay + submerged bubble test.
7. CAM026-derived camera: ~62.5 mm base OD is confirmed, but internal fits, wall thickness and gear/seal geometry remain prototype/supplier-sample HOLD.
8. Exact six-core local camera cable article requires flex + simultaneous CVBS/TX/RX EMC testing.

No global PASS is declared while any HOLD above controls final fabrication or full DN150 release.