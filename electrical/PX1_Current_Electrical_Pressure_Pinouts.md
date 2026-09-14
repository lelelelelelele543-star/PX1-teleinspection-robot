# PX1 Electrical / Pressure / Pinouts - Current

## Main tether - exactly 6 copper conductors

| Core | Function |
|---:|---|
| 1 | HV+ |
| 2 | HV return |
| 3 | RS485_A |
| 4 | RS485_B |
| 5 | VIDEO+ |
| 6 | VIDEO- |

Aramid/Kevlar is mechanical only and is never an electrical conductor. The main tether contains no coaxial core and no fibre.

## Local camera harness - exactly 6 insulated conductors

| Pin | Function |
|---:|---|
| 1 | +12V_HEAD |
| 2 | GND_HEAD |
| 3 | TX |
| 4 | RX |
| 5 | CVBS signal |
| 6 | CVBS return |

The CAM026 teardown showed six visible contact pads on one interface board, but pad count is evidence only; PX1 electrical functions are not inferred from that board.

## Power chain

```text
surface HV source / hardware E-STOP
 -> 6-core tether HV+ / HV return
 -> rear sealed connector + separate mechanical strain relief
 -> fuse / transient / inrush protection
 -> Cincon CQB150W-110S24
 -> 24 V bus
    -> LEFT BTS7960 -> left traction motor
    -> RIGHT BTS7960 -> right traction motor
    -> 24->12 V camera / lighting branch
    -> 12->5 V logic / sensor branch
    -> STM32 NUCLEO-F446RE
    -> MAX485 interface
```

Current rear connector architecture: WEIPU SP17 family with 7 contacts, exactly 6 tether cores used and one contact left unused/spare. The connector contacts carry no towing load.

## Video path

```text
camera CVBS signal/return
 -> short local six-core harness
 -> crawler video interface/balun
 -> tether VIDEO+/VIDEO-
 -> reel/pass-through
 -> surface receiver / OSD
 -> 7 in CVBS monitor
```

## Pressure chain

```text
external compressor/service fill adapter
 -> compact spring/ball pressure valve
 -> common dry crawler pressure volume
 -> Adafruit MPRLS Product 3965 absolute-pressure sensor
 -> STM32
 -> RS-485 telemetry
 -> control-unit pressure display
```

MPRLS current reference: 17.8 x 16.7 x 7.5 mm, absolute 0-25 PSI. Firmware records ambient absolute pressure immediately before pressurisation and displays the gauge delta.

Primary sealing paths:
- body/service cover: static elastomer face seal; final groove HOLD;
- six wheel stations: X-ring 18.72 x 2.62 plus static flange seal family;
- two Z40 body paths: 18 x 30 x 7 rotary shaft seals;
- camera: separate sealed pressure body;
- camera cable entry: LAPP 53112000 M12x1.5 gland;
- rear tether: sealed bulkhead plus independent mechanical strength termination.

## Safety states

- loss of valid control/heartbeat -> traction STOP;
- MCU reset -> traction STOP;
- overcurrent/jam -> affected traction channel STOP;
- pressure outside configured band -> fault/stop policy;
- hardware E-STOP removes tether HV independently of crawler firmware;
- no automatic restart after a safety trip.

Acceptance still requires +0.25 bar decay and submerged bubble testing, plus simultaneous motor + RS-485 + CVBS testing on the real 40 m tether before any 100-150 m release.