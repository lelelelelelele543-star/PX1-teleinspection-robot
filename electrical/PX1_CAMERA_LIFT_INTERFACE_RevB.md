# PX-1 camera/lift electrical interface — Rev.B WB23G/H

Date: 2026-09-14
Status: **SIX-CORE TOPOLOGY FROZEN / PRIMARY FLEX SAMPLE SELECTED / EMC + PHYSICAL QUALIFICATION HOLD**

## 1. Controlled architecture

The pressure/service cover is a mechanical pressure boundary. The external local cable passes through an M12 gland; the gland is not an electrical connector.

Electrical chain:

`crawler camera power/control board -> J_CAM_LIFT dry 6-way connector -> 6-core local harness -> SP13 lift plug -> SP13 camera panel connector -> sealed camera electronics`.

The local harness may be screened or unscreened depending on the completed EMC/video qualification. Six insulated circuits remain frozen either way.

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
| optional overall braid/shield | EMC screen only | controlled shield strategy; never DC return |

The previous 8-core study with parallel power conductors is superseded. The local lift harness is short enough that a correctly sized single +12 V conductor and single GND conductor are preferable to extra splices and a larger cable.

## 3. Conductor and cable target

Hard electrical/mechanical target:

- exactly 6 insulated cores;
- conductor target `0.25 mm²` class;
- preferred finished cable OD `5.4...6.0 mm`;
- hard packaging maximum `6.5 mm`;
- no loose individual wires across the wet lift.

### Primary flex/mechanical sample — LAPP 0028679

LAPP `UNITRONIC FD P plus A`, article `0028679`:

- exactly 6 x 0.25 mm²;
- current LAPP nominal OD 5.4 mm;
- PUR outer sheath;
- extra-fine stranded copper;
- intended for continuously flexing drag-chain service;
- current minimum flexing radius 5 x OD, about 27 mm nominal;
- current max conductor resistance 79 ohm/km at 20 C;
- **unshielded**.

This is now the primary physical lift-cycle sample because it best matches the mechanical duty and current connector/gland package. It is not production-released until raw CVBS/UART passes motor/LED interference testing.

### Shielded A/B comparison sample

LAPP `UNITRONIC LiYCY 0034406`, 6 x 0.25 mm², shielded, nominal OD about 6.0 mm, remains useful as an EMC/video comparison. It does not carry the same strong continuous-flex claim and therefore cannot replace 0028679 solely because it has a screen.

### Other screened high-flex references

A Pepperl+Fuchs current PUR cordset construction exists with six 0.25 mm² cores, OD 6.0 mm, foil + braid shielding and manufacturer drag-chain life of at least 2 million cycles. Its moving bend-radius requirement is >10 x OD (~60 mm) and it is surfaced mainly as long pre-terminated cordsets, so it remains a reference/secondary sample rather than baseline.

Current standard screened drag-chain families examined from SAB/HELUKABEL do not give a better direct fit: SAB SD90C has no standard 6 x 0.25 article, while surfaced HELUKABEL six-core shielded chain variants are about 7.2 or 8.8 mm OD and exceed the current SP13 S6I cable limit.

See `REVB_WB23H_SIX_CORE_CABLE_CANDIDATES.md`.

## 4. Internal dry connector candidate

The previous JST VH 8-way candidate is superseded.

Prototype dry wire-to-wire pair:

- receptacle housing: Molex Micro-Fit 3.0 `43025-0600`, 6 circuits;
- plug housing: Molex Micro-Fit 3.0 `43020-0601`, 6 circuits, no panel ears;
- female crimp terminal: Molex `43030-0007`, tin, 20/22/24 AWG, max insulation OD 1.85 mm;
- male crimp terminal: Molex `43031-0007`, tin, 20/22/24 AWG, max insulation OD 1.85 mm.

Both contacts are now exact prototype articles. Final crimp release still requires measuring the purchased cable insulation OD and making/pull-testing sample crimps.

The service opening 48 x 22 mm easily accepts the conservative Micro-Fit connector envelope used in WB23G.

Draft logical order before physical housing orientation is frozen:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Numeric cavity numbering is not released until physical samples are inspected from the correct mating and wire-side views.

## 5. Camera-side six-pin interface

WB15 remains controlling:

- head panel: WEIPU `SP1312/P6-C`, male pins;
- powered crawler/lift harness: WEIPU `SP1310/S6I-N`, female sockets, cable class 4.0...6.5 mm.

The six functions map 1:1 from the dry connector through the six-core cable to SP13. No power-core combining/splitting occurs in the wet harness.

The powered harness intentionally uses female sockets so live protruding pins are not exposed when the camera is removed.

## 6. Shield treatment

A shield is **preferred only if it does not compromise flex life/packaging and the EMC test shows a benefit**.

Rules if a screened candidate is used:

- shield is never DC current return;
- CVBS return always has its own insulated conductor;
- prototype starts with controlled body-side shield termination to chassis/EMC reference;
- camera-side bond remains configurable during EMC tests;
- final one-end versus both-end bonding is released only after complete crawler/reel/tether video testing.

If unshielded LAPP 0028679 passes the complete interference test, an overall screen is not added merely by preference.

## 7. Electrical screen

Using 0.25 mm² copper and the current 2.92 A peak head-load screen:

- 0.4 m local harness: about 0.164 V copper-only round-trip drop at room-temperature resistivity; about 0.196 V with +20% resistance screen;
- 0.6 m local harness: about 0.245 V room-temperature screen; about 0.294 V with +20% resistance screen.

Current LAPP data for 0028679 gives max conductor resistance 79 ohm/km at 20 C; the actual purchased sample must be measured because real voltage drop includes both conductors and every connector/contact.

Parallel power conductors are not required by the current local-run screen.

## 8. Harness construction rules

- jacket captured by M12 gland and SP13 strain relief, not solder joints;
- dry Micro-Fit connector receives separate mechanical strain relief inside the service cavity;
- about 35 mm service slack at body and head ends is an assembly starting target, adjusted from the real lift;
- straight lower-arm section is protected by a removable drain-open anti-snag guard;
- WB23G conservative guard envelope is 10 mm for cable up to Ø6.5 mm.

## 9. Cable qualification

For primary candidate 0028679 and the shielded A/B comparator:

1. measure actual finished OD;
2. measure every core resistance per metre;
3. measure conductor and insulation diameter;
4. verify seal in LAPP M12 gland and SP13 S6I backshell;
5. crimp Micro-Fit 43030-0007 / 43031-0007 samples and pull-test them;
6. verify +12 V/GND temperature rise and camera voltage at maximum head load;
7. run raw CVBS and UART simultaneously;
8. operate traction forward/reverse/PWM, camera TILT/ROLL and LED PWM while observing video;
9. LOW-HIGH-LOW cycle >=500 times, target 1000;
10. repeat after wet/grit exposure;
11. inspect jacket, conductor continuity and optional shield;
12. repeat pressure test around gland after cycling.

## 10. Service isolation

The camera branch must be de-energized before SP13 disconnection. Final electronics should provide `HEAD_12V_ENABLE` plus a replaceable fuse/PTC on the 12 V head branch so a damaged wet harness cannot disable traction/control power.

## 11. Open release items

- result of LAPP 0028679 EMC/video test;
- whether production local cable requires an overall screen;
- real cable insulation OD and crimp pull-test result;
- numeric Micro-Fit cavity orientation;
- numeric SP13 pin table from real pair;
- final shield-bond strategy if a screened cable wins;
- head-branch fuse/PTC value after measured peak current;
- measured complete-harness voltage drop and temperature rise.
