# A3.0 — camera + lighting bench before sealed head

Status: ACTIVE FAST-TRACK BENCH / NOT PRESSURE-RATED / NOT FINAL CAMERA HOUSING.

## Source architecture preserved
The recovered CAM026 source pack is used for architecture, not copied blindly into PX1:
- `ASM000`: complete pan/rotate camera consists of camera housing, side-frame housing and a separate bearing/rotate housing; overall source drawing shows a 132 mm axial dimension and a Ø73-class overall callout.
- `ASM001`: camera housing includes the camera module, camera pan gear, focus motor/gear, rear cover, O-rings and the light-ring assembly.
- `ASM004`: the rotate bearing housing contains a separate pan/rotate motor, rotate motor PCB, rotate axle/connector/spur gear assemblies and multiple static/dynamic seals.
- `ASM006`: the front light-ring assembly includes LED PCB assembly, sapphire lens glass, lock ring and O-rings.

PX1 therefore keeps these functional boundaries:
`removable head -> optical camera core + front light ring -> pan axis -> rotate support -> crawler/lift interface`.

The first A3 bench does **not** attempt to reproduce unmeasured CAM026 seals/gears. It proves picture, lighting, thermal behavior and the six-core head harness first.

## Camera selected for the functional bench
Current bench camera: `RunCam Phoenix 2` family.

Manufacturer-published characteristics used here:
- analog CVBS output;
- PAL/NTSC switchable;
- 5…36 V DC input;
- 19×19 mm camera board/body class, about 19–20 mm deep depending revision/manual;
- M12 lens;
- current roughly 85…120 mA at 12 V depending published revision.

The small power demand means the camera can run directly from the local 12 V head rail. No video encoder is required for Rev.A.

## A3.0 lighting architecture
Six white LEDs remain the design target, matching the existing PX1 BOM direction.

For first thermal/video tests:
- six Cree XP-G-class 3535 LEDs on individual metal-core carriers;
- split into **two independent strings of three LEDs**;
- one current driver per string;
- initial current limit: **350 mA per string**;
- dimming via driver DIM/PWM input;
- 12 V head rail;
- aluminium front heat spreader under the MCPCBs.

Do not parallel two LED strings behind one uncontrolled current source. Two drivers make a single open LED/string failure easier to diagnose and reduce current-sharing uncertainty.

350 mA is intentionally conservative. Higher light power is allowed only after the metal heat spreader/head temperature has been measured.

## A3.0 six-core local head harness
Exactly six insulated conductors:
1. `+12V_HEAD`
2. `GND_HEAD`
3. `UART_TX_CRAWLER_TO_HEAD`
4. `UART_RX_HEAD_TO_CRAWLER`
5. `CVBS_SIGNAL`
6. `CVBS_RETURN`

Any braid/shield is EMC only, never normal DC return.

For the first static bench, UART may be idle; it is reserved for local head MCU control when pan/rotate is added. Video and power still use the final six-wire allocation, so the bench tests the real harness philosophy from day one.

## Grounding rule
The two harness return conductors are routed separately through the dynamic harness. `CVBS_RETURN` carries video return current only. If the camera module internally joins its video ground and power ground, that unavoidable local bond is kept at the camera end; do not deliberately use the CVBS return as head power return.

## Bench carrier
`PX1_A3_Camera_Bench.py` generates an open serviceable fixture instead of a fake sealed camera:
- 60 mm front LED/optical carrier;
- 2 mm aluminium heat-spreader screen with central lens opening and six shallow MCPCB locating pads;
- 19.4 mm camera pocket/cradle;
- protected cable exit;
- overall package kept inside the approximate CAM026 axial envelope for packaging studies.

The fixture is printable on the Anycubic Chiron. The aluminium heat-spreader is a simple disk/plate manufacturing part, not a pressure window.

## Test sequence
1. Camera only, 12 V, monitor directly connected: verify PAL/NTSC and stable picture.
2. Add 40 cm local six-core harness: verify picture and measure camera supply.
3. Switch first 3-LED string at 350 mA; inspect video noise.
4. Switch second string; inspect video noise.
5. PWM dim both strings through 0/25/50/75/100% while recording picture artifacts.
6. Run camera + both LED strings continuously and record heat-spreader temperature.
7. Place the harness next to an operating traction motor/driver and repeat the video test.
8. Flex the local harness through the full manual-lift route repeatedly; inspect jacket and video.

## PASS A3.0
- stable live CVBS image with both LED strings operating;
- no unacceptable bands/sync loss during PWM dimming;
- camera supply remains stable;
- thermal result recorded and acceptable for the chosen current;
- harness survives lift motion without pinch/rub damage;
- the head can be disconnected as one service unit.

Only after A3.0 passes do we lock the pan/rotate motors, local controller and sealed head machining details.
