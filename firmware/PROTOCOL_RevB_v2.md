# PX-1 Rev.B — WB11 protocol v2 / telemetry / fault semantics

Date: 2026-09-11
Status: LOGICAL PROTOCOL FROZEN / PHYSICAL-LINK QUALIFICATION HOLD

## 1. Why protocol v1 is superseded

The first firmware header carried a useful minimal prototype telemetry struct, but Rev.B hardware has moved beyond it.

The old telemetry contained:
- one `pressure_mbar` value;
- crawler `distance_mm`;
- no per-side calibrated traction current;
- no three-zone pressure temperatures;
- no direct P0 leak state;
- only a small single `fault_code`.

Those fields conflict with the active architecture:
- crawler pressure is now P0/P1/P2 independently;
- reel payout distance is measured at the surface and does not originate in the crawler;
- LEFT/RIGHT current sensors are distinct;
- safety now needs simultaneous fault bits, not one mutually exclusive code.

Therefore Rev.B increments the wire protocol to **version 2** rather than silently changing the meaning of a version-1 packet.

## 2. Physical transport remains unchanged

Main link:
- half-duplex RS-485;
- CCU is the only normal bus master;
- crawler responds only to addressed requests/commands;
- CRC16-CCITT remains required;
- physical two-wire/no-reference common-mode qualification remains WB09 HOLD and is not waived by this protocol document.

The protocol does not consume any additional tether core.

## 3. Node addresses

Freeze:
- `0x01` — CCU / master;
- `0x10` — crawler;
- `0x20` — reel controller, reserved/local future use;
- `0x30` — camera auxiliary node, reserved;
- `0xFF` — broadcast, restricted to safe commands such as STOP/DISARM where implemented.

Normal crawler telemetry is unicast to the CCU.

## 4. Frame format

Wire order:

```text
SOF1  SOF2  VER  DST  SRC  TYPE  SEQ  LEN  PAYLOAD[LEN]  CRC16_H  CRC16_L
AA    55    02   ..   ..   ..    ..   ..   ...           ...      ...
```

Fields:
- `SOF1/SOF2`: constant 0xAA / 0x55;
- `VER`: protocol version, Rev.B = 2;
- `DST`: destination address;
- `SRC`: source address;
- `TYPE`: message type;
- `SEQ`: 8-bit sequence number incremented by sender;
- `LEN`: payload length 0...64;
- CRC16-CCITT polynomial 0x1021, initial value 0xFFFF.

CRC covers:
- `VER` through the final payload byte;
- SOF bytes are excluded.

Maximum wire frame at current payload limit:
- 2 SOF + 6 header + 64 payload + 2 CRC = 74 bytes.

## 5. Message types

Rev.B type map:
- `0x01 PX1_CMD_CONTROL`;
- `0x02 PX1_CMD_HOME`;
- `0x03 PX1_CMD_ZERO_DISTANCE` — CCU/reel-local semantic; crawler does not invent distance;
- `0x04 PX1_CMD_ARM`;
- `0x05 PX1_CMD_DISARM`;
- `0x06 PX1_CMD_CLEAR_FAULTS`;
- `0x10 PX1_TELEMETRY`;
- `0x11 PX1_FAULT_EVENT`;
- `0x12 PX1_ACK`;
- `0x13 PX1_PING`;
- `0x14 PX1_PONG`.

`DISARM` is always safe to accept when frame integrity/addressing are valid.

`CLEAR_FAULTS` never overrides a still-present hardware condition and never re-arms traction by itself.

## 6. Control payload

`px1_control_t` remains intentionally compact:
- `drive`: -1000...+1000;
- `steer`: -1000...+1000;
- `tilt`: -1000...+1000;
- `roll`: -1000...+1000;
- `light`: 0...1000;
- `flags`: command bits.

Manual camera lift remains mechanical and has no lift-motion field.

Control updates target 20...50 Hz.

Crawler command watchdog:
- current hard timeout baseline: 300 ms;
- on timeout: traction disabled/coast, camera-axis motion stopped, fault bit set;
- hardware E-STOP remains independent.

## 7. Rev.B crawler telemetry payload

The crawler sends only values that physically originate in the crawler.

Fields:
- state;
- 32-bit simultaneous `fault_bits`;
- P0 absolute pressure, 0.1 hPa/count;
- P1 absolute pressure, 0.1 hPa/count;
- P2 absolute pressure, 0.1 hPa/count;
- P0/P1/P2 pressure-sensor temperature, 0.1 C/count;
- 24 V bus, mV;
- LEFT traction branch current, mA signed;
- RIGHT traction branch current, mA signed;
- dedicated power-stage temperature, 0.1 C/count;
- P0 leak-probe raw ADC;
- TILT angle, 0.1 degree/count;
- ROLL angle, 0.1 degree/count;
- light command/output permille;
- status flags.

### Pressure units

LPS28 4060 hPa mode maximum is represented as 40600 counts at 0.1 hPa/count, fitting `uint16_t`.

The crawler does **not** transmit a fake gauge pressure based on assumed atmospheric pressure.

CCU computes:
- `P0_gauge = P0_abs - PAMB_abs`;
- `P1_gauge = P1_abs - PAMB_abs`;
- `P2_gauge = P2_abs - PAMB_abs`;
using its own surface ambient sensor.

## 8. Distance ownership correction

`distance_mm` is removed from crawler telemetry.

Reason:
- payout distance sensor/encoder is on the reel/CCU side;
- this value does not traverse the main six-core tether from the crawler;
- putting distance in crawler telemetry would either duplicate a surface value or imply a nonexistent crawler measurement.

The CCU display combines:
- local reel distance;
- crawler telemetry;
- local ambient pressure;
- operator job/address/time data.

This is the clean system boundary.

## 9. Fault bit allocation

Rev.B `uint32_t fault_bits`:
- bit 0 `COMM_TIMEOUT`;
- bit 1 `BUS_OVERVOLT`;
- bit 2 `LEFT_OVERCURRENT_JAM`;
- bit 3 `RIGHT_OVERCURRENT_JAM`;
- bit 4 `P0_PRESS_LOW_OR_DECAY`;
- bit 5 `P1_PRESS_LOW_OR_DECAY`;
- bit 6 `P2_PRESS_LOW_OR_DECAY`;
- bit 7 `PRESS_SENSOR_FAULT`;
- bit 8 `P0_LEAK_WET`;
- bit 9 `POWER_STAGE_OVERTEMP`;
- bit 10 `CAMERA_COMM_FAULT`;
- bit 11 `CAMERA_TILT_FAULT`;
- bit 12 `CAMERA_ROLL_FAULT`;
- bit 13 `ESTOP_ACTIVE`;
- bit 14 `CURRENT_SENSOR_FAULT`;
- bit 15 `BUS_UNDERVOLT`;
- bits 16...31 reserved.

Multiple bits may be present at the same time.

## 10. Latching policy

Latched until deliberate clear + condition removed:
- bus over-voltage;
- left/right jam over-current;
- direct P0 leak wet;
- power-stage over-temperature trip;
- E-STOP event;
- critical pressure rapid-loss event.

Auto-clearing status after healthy interval may be used for:
- transient sensor communication retry flags;
- non-critical warning-only pressure threshold;
- temporary camera communication retry status.

A latched fault does not clear simply because the CCU starts sending control packets again.

## 11. State field

Starting state enumeration:
- `0 SAFE_OFF`;
- `1 BOOT`;
- `2 DISARMED`;
- `3 ARMED_IDLE`;
- `4 ACTIVE`;
- `5 FAULT_LATCHED`;
- `6 SERVICE`.

After reset the crawler must not jump directly into ACTIVE.

## 12. Sequence handling

CCU increments `SEQ` for command frames.

Crawler records last accepted control sequence.

Reject as stale/duplicate where appropriate:
- repeated motion-control packet with an already consumed sequence may be ACKed but need not re-trigger edge commands;
- HOME/CLEAR_FAULTS edge commands require sequence-aware handling;
- sequence wrap 255 -> 0 is normal.

The communication watchdog is based on receipt of **valid, addressed, CRC-correct, semantically accepted control traffic**, not on raw UART bytes.

## 13. CRC/error behavior

On bad CRC:
- discard frame;
- do not change actuator command;
- do not refresh the command watchdog;
- increment diagnostic error counter.

On unsupported version:
- no actuator command;
- optional version-mismatch fault/diagnostic response if link behavior permits.

On wrong destination:
- ignore except approved broadcast-safe commands.

On impossible payload length:
- discard and resynchronize by SOF scanner.

## 14. Fault-event message

`PX1_FAULT_EVENT` is supplemental to periodic telemetry.

Send immediately after a newly latched critical fault when bus timing permits.

Minimum payload:
- current `fault_bits`;
- bus mV;
- left/right mA;
- P0/P1/P2 pressure values;
- event uptime/timestamp counter if available.

Periodic telemetry remains the authoritative current state; loss of a fault-event packet must not hide the fault.

## 15. CCU presentation

The CCU composes operator information from multiple local/remote domains:

Crawler packet:
- pressure absolute values;
- currents;
- voltage;
- temperatures;
- camera state;
- fault bits.

CCU-local:
- ambient pressure;
- reel distance;
- time;
- job/address;
- HV source state/current where measured.

Derived:
- three gauge pressures;
- pressure decay/trend;
- fault text;
- total operator OSD.

## 16. Compatibility policy

Version 2 is intentionally not binary-compatible with the old packed telemetry structure.

During bench development the CCU parser may support both `VER=1` and `VER=2`, but:
- Rev.B crawler firmware transmits version 2;
- production Rev.B CCU must support version 2;
- no field is reinterpreted under the same protocol version.

This is safer than preserving a stale struct layout and changing field meaning invisibly.

## 17. Release gates

1. unit-test CRC with known vectors;
2. test parser resynchronization after inserted/deleted bytes;
3. test duplicate and wrapped sequence numbers;
4. prove watchdog does not refresh on bad CRC/wrong destination;
5. inject each fault bit and verify exact CCU text/action;
6. confirm distance remains correct with crawler disconnected because it is surface-local;
7. verify P0/P1/P2 absolute values and CCU ambient subtraction;
8. test 20/50 Hz command rates through the actual isolated RS-485 modules;
9. repeat packet-error/logging tests at 40/100/150 m physical-link qualification;
10. capture protocol examples in the final service manual.

## Change log

### 2026-09-11 — WB11 protocol v2
- incremented protocol version rather than silently changing telemetry layout;
- added addressing and explicit frame header semantics;
- removed surface-local reel distance from crawler telemetry;
- expanded one pressure field into P0/P1/P2 absolute pressure plus sensor temperatures;
- added LEFT/RIGHT calibrated current telemetry, leak raw, power-stage temperature and wider fault bits;
- defined latching and watchdog semantics;
- preserved 64-byte payload limit and CRC16-CCITT.
