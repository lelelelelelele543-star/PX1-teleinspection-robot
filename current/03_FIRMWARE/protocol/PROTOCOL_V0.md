# PX1 RS-485 protocol V0 — requirements draft

Status: interface draft for early bench firmware; packet bytes/CRC are not released until both endpoint implementations are started.

## Physical/link requirements
- half-duplex RS-485;
- operator console is command master for Rev.A;
- crawler must fail safe to zero traction after communication timeout;
- protocol must tolerate repeated/corrupt frames without unintended motion;
- one documented version field is mandatory.

## Minimum command data
- protocol version;
- rolling sequence number;
- crawler enable;
- left/right requested traction or equivalent speed+steer representation;
- light level;
- optional service flags.

## Minimum crawler telemetry
- protocol version;
- echoed/last accepted sequence;
- link/status flags;
- pressure value;
- supply voltage where measurable;
- left/right motor current where measurable;
- fault flags.

## Safety rule
No stale command may leave motors running indefinitely. Any parse/CRC/version/watchdog failure must produce or retain a safe traction state.

The exact binary frame, baud rate, CRC polynomial and timing will be frozen only after the selected MCU/RS-485 modules are confirmed in the active BOM and a 40 m cable test is performed.
