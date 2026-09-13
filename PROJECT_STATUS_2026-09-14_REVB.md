# PX-1 project status — Rev.B snapshot — 2026-09-14

## Controlling architecture

PX-1 remains a Proteus-inspired, serviceable six-wheel inspection crawler:

- 3 wheel stations per side / 6 wheels;
- X50 / X150 / X250;
- 10 x m1 Z50 side gears;
- 2 traction motors;
- rear X250 long-axle input;
- dry pressurized body;
- manual camera lift;
- separately sealed removable camera;
- no mechanical cassette/cartridge architecture;
- no custom PCB required for first working prototype.

## Mechanical state

### WB22A — lift/camera integration

Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**.

Controls:

- corrected symmetric wet-bay cut;
- four-bar separated from TILT axis by rigid fixed carrier;
- body pivot X200;
- pivots Z92/109;
- link 90 mm;
- arms Y±31, 4 x 14 mm;
- camera Ø52 x 78;
- LOW optical axis X83.5569 / Z75;
- complete TILT screen retained.

### WB23C — controlling pressure/service topology

Status: **PASS_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**.

WB23C supersedes the abandoned WB23B dual-flex-chamber direction and WB23A routing coordinates.

Functional topology:

`dry body -> sealed PRESSURE/CAMERA SERVICE cover -> fill valve + horizontal M12 gland -> <=5 mm local harness -> simple arm guard -> fixed SP13 -> sealed removable camera`.

### WB23D — first full WB22A integration

Status: **PASS_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**.

WB23D inserted the WB23C service package into the exact corrected WB22A body and confirmed zero unintended collision with six wheel envelopes, all ten Z50, lift arms and camera outer envelope.

### WB23E — current service-cover dimensional baseline

Status: **PASS_SEAL_LAND_AND_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**.

WB23E corrected a real weakness in the first cover layout: the old 78 x 42 cover / 58 x 24 opening left too little material between M4 clearance holes and a realistic face-seal groove.

Controlling prototype screen:

- cover centre X261 / Y0;
- cover **86 x 44 x 6 mm**;
- cover X span 218...304;
- service opening **48 x 22 mm**;
- opening X237...285 / Y-11...+11;
- 2 x M4 centres **X226 / X296**;
- provisional groove centre path 4.0 mm outside opening;
- provisional groove width 2.5 mm;
- minimum M4 clearance-hole edge to provisional groove outer edge **3.5 mm**;
- minimum Ø8 screw-head edge to cover end **4.0 mm**;
- minimum groove outer edge to cover Y edge **5.75 mm**;
- dry JST VH 8-way connector envelope fits through opening.

The exact original Proteus small pressure-cover screw count is still not claimed. Two M4 screws are a PX-1 prototype design choice and remain subject to pressure/seal/alignment tests.

## Electrical camera/lift state

- eight insulated local conductors preferred;
- 2 x +12 V in parallel;
- 2 x GND in parallel;
- UART TX/RX;
- CVBS signal/return;
- shield for EMC only;
- dry internal disconnect candidate JST B8P-VH-B / VHR-8N;
- removable camera interface remains WEIPU SP1312/P6-C + SP1310/S6I-N if purchased cable OD fits.

## Pressure-service state

Current WB23E screen:

- corrected cover 86 x 44 x 6 mm;
- opening 48 x 22 mm;
- 2 x M4 prototype retention at X226/X296;
- horizontal LAPP 53112000 M12 gland;
- fill-port current hard screen <=Ø14 x 6 mm;
- limiting fixed ideal-DN150 clearance remains about **4.70 mm** at the pressure-port envelope;
- corrected cover ideal-DN150 clearance ~7.37 mm;
- gland ~13.86 mm;
- M4 heads ~7.93 mm;
- LOW lift guard ~29.23 mm.

Pressure release still requires real parts, final groove, decay/submersion tests and physical DN150 tolerance validation.

## Source/evidence correction

Repair photographs and MiniCam drawings now control the camera-lift service topology. Source drawings directly support M12 3.5–5 mm cable fittings, camera connector/lift cover architecture, compact pressure-valve family and a dedicated camera-lift arm cover.

The project no longer invents large local flex loops where source hardware demonstrates a compact gland/cover/lift-guard solution.

WB23A also contained a CAD Y-direction/sign ambiguity in a helper used for one-sided geometry; no downstream manufacturing decision may use WB23A absolute one-sided Y coordinates.

## Immediate procurement samples — not bulk release

After availability check, sample only:

1. 1–2 x LAPP 53112000 M12 glands;
2. small sample / one assembly of <=5 mm, 8-core + shield cable;
3. 2 x WEIPU SP13 working pairs;
4. JST VH 8-position connector samples + correct contacts;
5. 2–3 candidate **very low-profile** fill valves;
6. FKM 2 mm cord / candidate molded seal material.

## Immediate physical prototypes

1. 3D-print dummy WB23E pressure cover and arm guard on Anycubic Chiron for access/fit only.
2. Machine first aluminium cover coupon after real gland/valve arrive.
3. Build a pressure-box coupon reproducing cover/gland/valve geometry before risking the complete crawler body.
4. Build a lift-cycle fixture with actual local cable and arm guard.

## Qualification gates before machining release

- exact purchased-part measurement;
- +0.25 bar pressure decay;
- submerged leak test;
- 500-cycle minimum / 1000 target lift endurance;
- wet/grit repeat;
- post-cycle pressure test;
- raw CVBS + UART + power under simultaneous motor/LED interference;
- physical DN150 jig with final pressure cap/gland/screw heads;
- final full-master tolerance/collision check;
- only then freeze manufacturing drawing/BOM and STL/STEP handoff.

## Next controlled work blocks

- WB23F: pressure-port DN150 sensitivity and preferred procurement envelope.
- WB24A: exact pressure-service boss/seal drawing after real valve/gland selection.
- WB24B: local cable sample electrical/flex qualification and final pin-number table.
- WB25: complete crawler master with purchased connector/fastener/valve envelopes.
- Release candidate: prototype body/lift drawings, arm guard, service cover and assembly/service documentation.
