# PX1 Rev.PM — simplified CAM026 electrical architecture through original 6-way function

Status: ACTIVE CAMERA ELECTRICAL BASELINE.

## Source-derived reason for a local rotating controller
Uploaded CAM026 documentation shows:
- COM-001-800 SLIP RING 6 WAY in ASS-001-920;
- a camera-side connection PCB after the slip ring;
- PAN motor control PCB and angle encoder PCB in the rotating side-frame assembly;
- separate ROTATE motor/control/angle mechanism in the rear bearing housing.

PX1 keeps this functional topology but replaces proprietary MiniCam PCBs with ready modules.

## Six slip-ring circuits
Proposed PX1 camera slip-ring assignment:
1. +12 V camera power
2. GND power/control
3. UART fixed-side TX -> rotating camera MCU RX
4. UART rotating camera MCU TX -> fixed-side RX
5. balanced VIDEO+
6. balanced VIDEO-

This preserves the original 6-way concept without sending individual motor/sensor wires through the continuous-rotation joint.

## Rotating-side electronics
Ready-module candidates:
- Waveshare RP2040-Zero, approximately 18 x 23.5 mm;
- DRV8871 ready H-bridge module for PAN motor;
- AS5600-class magnetic angle sensor at PAN axis;
- small 12->5 V buck for MCU/sensor;
- ready constant-current/PWM LED driver for the six white LEDs;
- compact balanced CVBS transmitter after the fixed-focus camera module.

No custom PCB required.

Rotating MCU functions:
- receive PAN/light/HOME commands via UART;
- control PAN motor through DRV8871;
- read PAN absolute angle;
- enforce +/-135 degree software travel with independent mechanical stop/service margin;
- PWM the six LEDs;
- report PAN angle/faults back through UART.

## Fixed-side camera/crawler functions
The crawler MCU remains outside the continuous-rotation joint.
It:
- controls the ROTATE motor through a second DRV8871 module;
- reads the ROTATE angle/reference sensor on the fixed side;
- passes PAN/light commands to the rotating RP2040-Zero;
- forwards camera status to the console over main RS-485.

Using the same DRV8871 family for PAN and ROTATE makes the motor-driver spare common.

## Video path
Fixed-focus camera CVBS -> balanced video transmitter on rotating side -> slip-ring VIDEO+/VIDEO- -> main crawler camera connector -> main tether VIDEO+/VIDEO- -> console balanced receiver -> OSD -> monitor.

This avoids unbalanced CVBS over the 100–150 m tether and avoids coax in the main tether.
The balanced transmitter must be tested through the selected slip ring for noise while PAN/ROTATE motors and LEDs operate.

## Packaging screen
The current Rev.PC rear internal reference cavity is approximately Ø60 x 40 mm.
A first packing screen places, without overlap and fully inside that cylinder:
- RP2040-Zero reference: 18 x 23.5 x 5 mm;
- PAN DRV8871 reference: 26 x 20 x 8 mm;
- balanced-video transmitter reserve: 30 x 20 x 8 mm;
- 12->5 V buck reserve: 20 x 15 x 8 mm.

This is a packaging proof only; exact bought-module connectors/wire bend radii remain a physical gate.

## Why focus electronics are deleted
The original CAM026 contains a dedicated focus gearmotor and focus control PCB. PX1 uses a fixed-focus ~75-degree class lens, so these parts and their failure modes disappear entirely.

## Failure behaviour
- UART timeout on rotating MCU -> PAN motor STOP, LEDs remain at safe configured state;
- invalid PAN angle -> PAN STOP;
- crawler RS-485 timeout -> both traction motors, ROTATE and PAN commands STOP;
- hardware console ALL STOP removes crawler/tether power independently of both MCUs.

## Remaining gates
1. exact RP2040-Zero purchase/source availability;
2. exact compact DRV8871 board dimensions/current setting;
3. select balanced CVBS transmitter/receiver modules and test 150 m cable + slip ring;
4. physical noise test with PAN/ROTATE and LEDs switching;
5. exact PAN/ROTATE motor selection after mechanical gearing is frozen;
6. mechanical hard-stop and sensor magnet geometry.
