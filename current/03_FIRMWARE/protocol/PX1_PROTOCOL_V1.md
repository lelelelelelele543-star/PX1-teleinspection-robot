# PX1 protocol V1

Status: BENCH-FROZEN for Rev.A A0/A1/A2. Changes that alter wire bytes require a new protocol version.

## Link
- half-duplex RS-485;
- console is master; crawler replies only to a valid command addressed to it;
- initial baud: 115200 8N1;
- command period: 50 ms nominal;
- crawler traction watchdog: 250 ms from last valid V1 command;
- corrupted, wrong-version or stale frames never refresh the traction watchdog.

115200 is the bench default, not a claim that it is already qualified over the 40 m production tether. A2 tests 115200 first and may lower the baud without changing packet semantics.

## Common frame
All multi-byte integers are little-endian.

| Byte | Field |
|---:|---|
| 0 | SOF0 = `0xA5` |
| 1 | SOF1 = `0x5A` |
| 2 | protocol version = `0x01` |
| 3 | message type |
| 4..5 | sequence `uint16` |
| 6 | payload length N |
| 7..(6+N) | payload |
| 7+N .. 8+N | CRC16-CCITT-FALSE, little-endian |

CRC parameters: poly `0x1021`, init `0xFFFF`, refin=false, refout=false, xorout=`0x0000`. CRC is calculated over bytes 2 through the end of payload; SOF bytes and CRC bytes are excluded.

Maximum V1 payload: 32 bytes. Maximum frame: 41 bytes.

## Message `0x01` — CMD_DRIVE
Payload length = 8.

| Offset | Type | Meaning |
|---:|---|---|
| 0 | uint8 | enable: 0=traction forced zero, 1=traction permitted |
| 1 | uint8 | command flags; reserved bits must be zero |
| 2..3 | int16 | left demand, -1000..+1000 |
| 4..5 | int16 | right demand, -1000..+1000 |
| 6..7 | uint16 | light demand, 0..1000 |

Crawler clamps out-of-range numeric values. `enable=0` always overrides left/right demand.

## Message `0x81` — TELEMETRY
Payload length = 16.

| Offset | Type | Meaning |
|---:|---|---|
| 0..1 | uint16 | status flags |
| 2..3 | uint16 | fault flags |
| 4..7 | int32 | crawler pressure relative to captured atmosphere, Pa |
| 8..9 | uint16 | crawler bus voltage, mV |
| 10..11 | uint16 | left motor current, mA |
| 12..13 | uint16 | right motor current, mA |
| 14..15 | int16 | hottest reported traction motor/driver temperature, 0.1 °C; `INT16_MIN` if unavailable |

Header sequence in telemetry echoes the last accepted command sequence.

## Status flags
- bit0 `LINK_OK`
- bit1 `TRACTION_ENABLED`
- bit2 `PRESSURE_VALID`
- bit3 `MOTOR_LEFT_READY`
- bit4 `MOTOR_RIGHT_READY`
- bit5 `VIDEO_POWER_ON`
- bit6 `LIGHT_ON`
- remaining bits reserved.

## Fault flags
- bit0 `COMM_TIMEOUT`
- bit1 `PRESSURE_LOW`
- bit2 `PRESSURE_HIGH`
- bit3 `BUS_UNDERVOLTAGE`
- bit4 `BUS_OVERVOLTAGE`
- bit5 `MOTOR_LEFT_FAULT`
- bit6 `MOTOR_RIGHT_FAULT`
- bit7 `OVERTEMPERATURE`
- bit8 `PROTOCOL_ERROR_LATCH`
- remaining bits reserved.

## Sequence handling
The sequence rolls modulo 65536. The crawler accepts a valid frame even across rollover. Duplicate sequence may be acknowledged but must not be interpreted as a new edge-triggered service action. Rev.A traction commands are level commands, so duplicates are safe.

## Safety behavior
- no valid command for >250 ms: left/right output immediately requested to zero and `COMM_TIMEOUT` set;
- invalid CRC/version/length: discard frame and do not refresh watchdog;
- enable=0: traction zero regardless of demands;
- crawler boot: traction disabled until the first valid frame with enable=1 and local motor-driver readiness;
- motor-driver fault: affected side is commanded zero; policy may force both sides zero for the first Rev.A prototype;
- E-stop is electrical power removal and does not depend on RS-485 software.
