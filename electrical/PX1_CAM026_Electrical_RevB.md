# PX-1 Rev.B — CAM026-inspired camera electrical baseline

Date: 2026-09-11
Status: ACTIVE CAMERA ELECTRICAL BASELINE / SLIP-RING QUALIFICATION HOLD
Supersedes `PX1_CAM026_Electrical_RevPM.md` where the video-balun location or camera rotary pinout differs.

## 1. Source-derived architecture retained

MiniCam CAM026 source evidence shows:
- `COM-000-003 PAL DSP CAMERA MODULE` in the rotating camera housing;
- `COM-001-800 SLIP RING 6 WAY` in the rotate connector assembly;
- camera-side connection PCB after/around the rotary interface;
- separate PAN and ROTATE motor/control mechanisms;
- six-way rotary electrical architecture.

PX-1 retains a six-function camera rotary interface but uses replaceable modern modules.

## 2. Rev.B six rotary functions

1. +12V_ROT
2. GND_ROT — motor/control power return
3. CAM_UART_TX
4. CAM_UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN — dedicated video return

Important:
- `CVBS_RETURN` does not carry PAN-motor or LED current;
- main tether is still balanced `VIDEO+ / VIDEO-`;
- the 75/100-ohm conversion happens on the **fixed crawler side immediately after the camera slip ring**;
- no coax is introduced into the main tether.

## 3. Why the balun moved to the fixed side

Rev.PM assumed a balanced-video transmitter inside the rotating camera volume but did not freeze a real compact purchasable part.

WB12 selected the real commercial Delta-Opti `TR-1D*P2`, approximately 43 x 16 x 15 mm plus a 90 mm BNC lead. Although the transformer body can geometrically fit a Ø60-class cavity when tilted, the complete BNC/service package competes with the MCU, PAN driver, LED electronics and wiring.

Moving the balun to the fixed side:
- reduces rotating mass and clutter;
- gives normal access to BNC and balanced terminals;
- leaves the camera head easier to seal and service;
- preserves the six rotary functions;
- does not alter the six-core main tether.

This is therefore an approved Rev.B serviceability correction, not a main-system architecture change.

## 4. Rotating camera electronics

Retained ready-module concept:
- fixed-focus CVBS camera module — exact purchase article remains HOLD;
- RP2040-Zero-class local controller — prototype candidate;
- DRV8871-class PAN motor driver — exact ready board HOLD;
- absolute/position sensor as selected by mechanical camera work block;
- compact 12->5 V buck for rotating logic;
- current-controlled/PWM LED driver;
- no focus motor for first prototype.

PAN/light/HOME commands travel over local UART through the rotary interface.

## 5. Fixed crawler camera electronics

Immediately after camera slip ring:
- dedicated 75-ohm CVBS pigtail from `CVBS_SIGNAL/CVBS_RETURN`;
- Delta-Opti `TR-1D*P2` passive balun;
- balanced output becomes the crawler/tether `VIDEO+ / VIDEO-` pair.

Crawler MCU:
- main tether RS-485 remains on USART3;
- local camera UART remains on UART5 PC12/PD2;
- ROTATE/other fixed-side functions remain outside the continuously rotating camera node as mechanically applicable.

## 6. Video qualification

The selected camera slip ring is not allowed to be released from a resistance/noise catalog number alone.

Required with physical video:
- camera direct baseline;
- camera slip ring rotating continuously;
- Delta balun pair;
- 40 m tether;
- reel slip ring;
- 100/150 m extension/equivalent;
- traction PWM, PAN/ROLL motors and LED PWM active.

See `REVB_WB12_BALANCED_CVBS_VIDEO.md`.

## 7. Rotary-current gate

The current candidate PAN motor can approach ~1.1 A stall at 12 V. The same rotating +12/GND conductors also supply camera, local MCU and LEDs.

Therefore a miniature 1.5 A/circuit slip ring must **not** be frozen merely because it has six circuits.

Camera rotary device must meet one of:
- each +12/GND circuit has verified transient current margin above the measured combined rotating load; or
- a manufacturer-supported higher-current six-function configuration is used; or
- multiple physical contacts are paralleled only if the slip-ring manufacturer explicitly permits it and the pin count/package is requalified.

WB13 closes this gate.

## 8. Failure behavior

- camera UART timeout -> PAN command zero;
- invalid position sensor -> PAN stop;
- crawler command timeout -> traction and camera-axis commands stop;
- video failure does not disable the hardware E-STOP path;
- hardware CCU E-STOP removes crawler/tether power independently of camera MCU.

## 9. Service rule

The sealed camera can be removed/replaced without opening side-drive pressure zones.

The fixed-side video balun is accessible without opening the sealed rotating camera head.

No balun, slip ring or camera-service bracket is a pressure-boundary shortcut; camera O-rings and crawler body seals remain ordinary separately serviced sealing features.

## Change log

### 2026-09-11 — Rev.B / WB12
- retained six-way CAM026-inspired rotary architecture;
- changed rotary video circuits from `balanced VIDEO+/VIDEO-` to dedicated `CVBS_SIGNAL/CVBS_RETURN`;
- moved 75/100-ohm balun to fixed crawler side for serviceability and packaging;
- preserved balanced main tether video;
- added explicit combined rotating-current gate before selecting the camera slip ring.
