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

### WB23C — pressure/service cover and local camera harness

Status: **PASS_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**.

WB23C supersedes WB23B-style dual flex chambers and supersedes WB23A as the controlling routing concept while retaining WB23A's useful conclusion that a thin local harness fits the lift.

Current topology:

`dry body -> sealed PRESSURE/CAMERA SERVICE cover -> fill valve + M12 gland -> <=5 mm local harness -> simple arm guard -> fixed SP13 -> sealed removable camera`.

Important: exact original Proteus two-bolt cover count is not claimed. PX-1 chooses 2 x M4 for its compact prototype cover and must prove sealing/flatness physically.

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

WB23C prototype screen:

- cover 78 x 42 x 6 mm;
- opening 58 x 24 mm;
- 2 x M4 prototype retention;
- horizontal LAPP 53112000 M12 gland;
- low-profile fill valve <=Ø14 x 6 mm hard envelope;
- limiting fixed ideal-DN150 clearance ~4.70 mm at pressure-valve envelope.

Pressure release still requires real parts, final groove, decay/submersion tests and full-master tolerance check.

## Source/evidence correction

Repair photographs and MiniCam drawings now control the camera-lift service topology. The project no longer invents large local flex loops when source hardware demonstrates a compact gland/cover/lift-guard approach.

WB23A also contained a CAD Y-direction/sign ambiguity in a helper used for one-sided cover geometry. Because WB23C supersedes that routing model, no downstream manufacturing decision may use WB23A's absolute one-sided Y geometry as released data.

## Immediate procurement samples — not bulk release

After availability check, sample only:

1. 1–2 x LAPP 53112000 M12 glands;
2. small sample / one assembly of <=5 mm, 8-core + shield cable;
3. 2 x WEIPU SP13 working pairs;
4. JST VH 8-position connector samples + correct contacts;
5. 2–3 candidate low-profile fill valves;
6. FKM 2 mm cord / candidate molded seal material.

## Immediate physical prototypes

1. 3D-print dummy pressure cover and arm guard on Anycubic Chiron for access/fit only.
2. Machine first aluminium cover coupon after real gland/valve arrive.
3. Build a pressure-box coupon reproducing cover/gland/valve geometry before risking the complete crawler body.
4. Build a lift-cycle fixture with actual local cable and arm guard.

## Qualification gates before machining release

- exact part measurement;
- +0.25 bar pressure decay;
- submerged leak test;
- 500 cycle minimum / 1000 target lift endurance;
- wet/grit repeat;
- post-cycle pressure test;
- raw CVBS + UART + power under simultaneous motor/LED interference;
- physical DN150 jig with final pressure cap/gland/screw heads;
- final full-master collision check;
- only then freeze manufacturing drawing/BOM and STL/STEP handoff.

## Next controlled work blocks

- WB24A: exact pressure-service boss/seal drawing after real valve/gland selection.
- WB24B: local cable sample electrical/flex qualification and final pin-number table.
- WB25: integrate WB22A + WB23C into complete crawler master with real connector/fastener envelopes.
- Release candidate: prototype body/lift drawings, arm guard, service cover and assembly/service documentation.
