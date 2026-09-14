# PX-1 camera/lift electrical interface — Rev.B WB23G

Date: 2026-09-14
Status: **SIX-CORE TOPOLOGY FROZEN / EXACT CONTACT NUMBERS + CABLE SAMPLE HOLD**

## 1. Controlled architecture

The pressure/service cover is a mechanical pressure boundary. The external local cable passes through an M12 gland; the gland is not an electrical connector.

Electrical chain:

`crawler camera power/control board -> J_CAM_LIFT dry 6-way connector -> 6-core shielded local harness -> SP13 lift plug -> SP13 camera panel connector -> sealed camera electronics`.

## 2. Six-core local harness allocation

There are exactly six insulated conductors:

| Local core | Function | Camera SP13 destination |
|---:|---|---|
| 1 | +12V_HEAD | +12V_HEAD |
| 2 | GND_HEAD | GND_HEAD |
| 3 | HEAD_UART_TX | HEAD_UART_TX |
| 4 | HEAD_UART_RX | HEAD_UART_RX |
| 5 | CVBS_SIGNAL | CVBS_SIGNAL |
| 6 | CVBS_RETURN | CVBS_RETURN |
| overall braid/shield | EMC screen only | controlled shield strategy; never DC return |

The previous 8-core study with parallel power conductors is superseded. The local lift harness is short enough that a correctly sized single +12 V conductor and single GND conductor are preferable to extra splices and a larger cable.

## 3. Conductor and cable target

- conductor target: `0.25 mm²` class for all six insulated cores;
- preferred finished cable OD: `5.5...6.0 mm`;
- hard packaging maximum: `6.5 mm`;
- overall copper braid/shield preferred;
- no loose individual wires across the wet lift.

Size/electrical benchmark: LAPP `UNITRONIC LiYCY 0034406`, 6 x 0.25 mm², shielded, nominal OD 6.0 mm. This is a prototype/sample benchmark only, not final flex-life release, because the selected cable must pass the PX-1 lift-cycle and wet/grit qualification.

## 4. Internal dry connector candidate

The previous JST VH 8-way candidate is superseded for this interface because the current conductor target is 0.25 mm² while the normal VH published range starts at 0.33 mm².

Prototype dry wire-to-wire candidate:

- receptacle housing: Molex Micro-Fit 3.0 `43025-0600`, 6 circuits;
- plug housing: Molex Micro-Fit 3.0 `43020-0601`, 6 circuits, no panel ears;
- female contact candidate: Molex `43030-0007`, 20/22/24 AWG class;
- mating male contact: `43031` family; exact bag/reel article remains HOLD until purchased cable strand and insulation diameters are measured.

The service opening 48 x 22 mm easily accepts the conservative Micro-Fit connector envelope used in WB23G.

Draft logical order before physical connector orientation is frozen:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Numeric cavity/contact numbering is not released until physical samples are inspected from the correct mating and wire-side views.

## 5. Camera-side six-pin interface

WB15 remains controlling:

- head panel: WEIPU `SP1312/P6-C`, male pins;
- powered crawler/lift harness: WEIPU `SP1310/S6I-N`, female sockets, 4.0...6.5 mm cable class.

The six functions map 1:1 from the dry connector through the six-core cable to SP13. No power-core combining/splitting occurs in the wet harness.

The powered harness intentionally uses female sockets so live protruding pins are not exposed when the camera is removed.

## 6. Shield treatment

- shield is never a DC current return;
- CVBS return has its own insulated conductor;
- prototype starts with controlled body-side shield termination to chassis/EMC reference;
- camera-side shield bond remains configurable during EMC/video tests;
- final one-end versus both-end shield bonding is released only after complete crawler/reel/tether video testing.

## 7. Electrical screen

Using 0.25 mm² copper and the current 2.92 A peak head-load screen:

- 0.4 m local harness: about 0.164 V copper-only round-trip drop at room-temperature resistivity; about 0.196 V with +20% resistance screen;
- 0.6 m local harness: about 0.245 V room-temperature screen; about 0.294 V with +20% resistance screen.

Therefore parallel power conductors are not required by the present local-run screen. Final release depends on measured resistance of the purchased cable and measured head voltage under worst simultaneous camera/LED/motion load.

## 8. Harness construction rules

- jacket captured by the M12 gland and SP13 strain relief, not solder joints;
- dry Micro-Fit connector receives separate mechanical strain relief inside the service cavity;
- about 35 mm service slack at body side and head side is an assembly target, adjusted after the real lift is built;
- straight lower-arm section is protected by a removable drain-open anti-snag guard;
- WB23G conservative guard envelope is 10 mm to accommodate cable up to Ø6.5 mm.

## 9. Cable qualification

1. measure actual finished OD;
2. measure every core resistance per metre;
3. measure conductor and insulation diameter before selecting final crimp contacts;
4. verify cable seals correctly in LAPP M12 gland and SP13 S6I backshell;
5. verify +12 V/GND temperature rise and camera voltage at maximum head load;
6. run raw CVBS and UART simultaneously;
7. LOW-HIGH-LOW cycle >=500 times, target 1000;
8. repeat after wet/grit exposure;
9. inspect jacket, conductor continuity and shield;
10. repeat video/PWM interference test.

## 10. Service isolation

The camera branch must be de-energized before SP13 disconnection. The final electronics should provide `HEAD_12V_ENABLE` plus a replaceable fuse/PTC on the 12 V head branch so a damaged wet harness cannot disable traction/control power.

## 11. Open release items

- exact six-core cable article;
- exact Micro-Fit male contact article after conductor measurement;
- numeric Micro-Fit cavity orientation;
- numeric SP13 pin table from real pair;
- final shield-bond strategy;
- head-branch fuse/PTC value after measured peak current;
- measured voltage drop and temperature rise;
- CVBS immunity to lift, traction and LED PWM noise.
