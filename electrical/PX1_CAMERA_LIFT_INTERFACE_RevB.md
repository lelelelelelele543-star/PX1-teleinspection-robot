# PX-1 camera/lift electrical interface — Rev.B WB23C

Date: 2026-09-14
Status: **ELECTRICAL TOPOLOGY FROZEN / EXACT CONTACT NUMBERS + CABLE SAMPLE HOLD**

## 1. Controlled architecture

The pressure/service cover is a mechanical pressure boundary. The external local cable passes through an M12 gland; the gland is not an electrical connector.

Electrical chain:

`crawler camera power/control board -> J_CAM_LIFT dry connector -> <=5 mm local harness -> SP13 lift plug -> SP13 camera panel connector -> sealed camera electronics`.

## 2. Eight-conductor local harness allocation

| Local core | Function | Camera SP13 destination |
|---|---|---|
| 1 | +12V_HEAD_A | +12V_HEAD |
| 2 | +12V_HEAD_B | +12V_HEAD |
| 3 | GND_HEAD_A | GND_HEAD |
| 4 | GND_HEAD_B | GND_HEAD |
| 5 | HEAD_UART_TX | HEAD_UART_TX |
| 6 | HEAD_UART_RX | HEAD_UART_RX |
| 7 | CVBS_SIGNAL | CVBS_SIGNAL |
| 8 | CVBS_RETURN | CVBS_RETURN |
| braid/shield | EMC screen only | chassis/EMC strategy; never power return |

The two +12 V cores and two GND cores are joined only at controlled termination points so one small conductor or solder joint does not carry the complete head load.

## 3. Internal dry connector candidate

Prototype family:

- header: JST `B8P-VH-B`;
- housing: JST `VHR-8N`;
- crimp contacts selected only after the real conductor cross-section is measured.

Draft logical order before physical sample numbering is frozen:

1. +12V_HEAD_A
2. +12V_HEAD_B
3. GND_HEAD_A
4. GND_HEAD_B
5. UART_TX
6. UART_RX
7. CVBS_SIGNAL
8. CVBS_RETURN

Before fabrication, inspect the real connector front/rear numbering and freeze the drawing with keyed orientation.

## 4. Camera-side six-pin interface

WB15 remains controlling:

- head panel: WEIPU `SP1312/P6-C`, male pins;
- powered crawler/lift harness: WEIPU `SP1310/S6I-N`, female sockets, 4.0–6.5 mm cable class.

Six camera functions:

- PWR_HEAD_12V
- PWR_HEAD_GND
- UART_HEAD_TX
- UART_HEAD_RX
- CVBS_SIGNAL
- CVBS_RETURN

The powered harness intentionally uses female sockets so live protruding pins are not exposed when the camera is removed.

Numeric SP13 contact numbers remain HOLD until a physical pair is checked against moulded numbering and front/rear-view convention.

## 5. Shield treatment

- shield is never a DC current return;
- CVBS return has its own insulated conductor;
- prototype starts with controlled body-side shield termination to chassis/EMC reference;
- camera-side shield bond remains configurable during EMC/video tests to detect ground-loop or PWM-noise sensitivity;
- final one-end versus both-end shield bonding is released only after complete crawler/reel/tether video testing.

Do not solder the braid to a random signal ground for convenience.

## 6. Harness construction rules

- target finished OD <= 5.0 mm;
- eight insulated cores plus shield preferred;
- no loose individual wires across the wet lift;
- jacket captured by gland and connector strain relief;
- SP13 solder joints individually heat-shrunk plus overall strain relief;
- dry connector gets a separate mechanical cable clamp within the service cavity;
- about 35 mm service slack at both moving ends as an assembly target;
- straight lower-arm run gets a removable anti-snag guard.

## 7. Cable qualification

A cable is not released from OD/conductor count alone.

Prototype acceptance:

1. measure OD at several points;
2. measure resistance of every core per metre;
3. verify insulation and braid construction;
4. carry maximum camera/LED/motor load on paired power cores;
5. record voltage at camera during pan/tilt/roll + maximum LED state;
6. run raw CVBS and UART simultaneously;
7. LOW-HIGH-LOW cycle >=500 times, target 1000;
8. repeat after wet/grit exposure;
9. inspect jacket, conductor continuity and shield;
10. repeat video-interference test.

Autonics `CID9S-2` remains only a possible prototype donor. No continuous-flex lifetime is assumed from its catalog description.

## 8. Service isolation

The camera branch must be de-energized before SP13 disconnection. The final electronics should provide a controllable `HEAD_12V_ENABLE` so the camera can be serviced without cycling traction power.

A replaceable fuse/PTC on the 12 V head branch is recommended in the dry body so a crushed wet harness cannot take down traction/control power.

## 9. Open release items

- exact local cable article;
- exact JST VH crimp contact for measured conductor size;
- numeric JST pin orientation;
- numeric SP13 pin table from real pair;
- final shield-bond strategy;
- head-branch fuse/PTC value after measured peak current;
- measured voltage drop under worst head load;
- CVBS immunity to lift, traction and LED PWM noise.
