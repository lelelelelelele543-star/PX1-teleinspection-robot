# PX1 Electrical / Pressure / Pinouts - Current

## 1. Main tether - exactly 6 copper conductors

| Core | Function | Rule |
|---:|---|---|
| 1 | HV+ | long-tether crawler power |
| 2 | HV return | dedicated power return |
| 3 | RS485_A | control/telemetry differential line |
| 4 | RS485_B | control/telemetry differential line |
| 5 | VIDEO+ | balanced video conductor |
| 6 | VIDEO- | balanced video conductor |

Aramid/Kevlar strength member is mechanically terminated in the tail and never used electrically. No coaxial core and no fibre are introduced.

## 2. Local camera/lift harness - exactly 6 insulated conductors

| Pin | Function |
|---:|---|
| 1 | +12V_HEAD |
| 2 | GND_HEAD |
| 3 | UART_TX (crawler/fixed side -> camera node) |
| 4 | UART_RX (camera node -> crawler/fixed side) |
| 5 | CVBS_SIGNAL |
| 6 | CVBS_RETURN |

If an overall shield is used, it is EMC only and is not counted as a seventh signal conductor and is not the DC return.

Dry connector baseline: Molex Micro-Fit 3.0 43025-0600 / 43020-0601 with matching contacts. Wet camera-side baseline: WEIPU SP13 six-way family; exact selected SP13 mechanical variant remains a physical-measurement HOLD.

## 3. Crawler power partition

```text
6-core tether HV+/HV-
   -> rear sealed connector + strain relief
   -> fuse / surge / inrush protection
   -> Cincon CQB150W-110S24
   -> 24 V bus
      -> LEFT BTS7960 -> left PGM-32P motor
      -> RIGHT BTS7960 -> right PGM-32P motor
      -> 24->12 V LM2596 -> camera/lighting branch
      -> 12->5 V MP1584 -> MCU/sensors/interface branch
      -> NUCLEO-F446RE
      -> MAX485 module
```

Prototype bench crawler may be supplied directly from a current-limited 24 V source before the HV tether stage is enabled.

## 4. Video path

```text
Camera CVBS signal/return
 -> short local six-core harness
 -> crawler video interface/balun
 -> tether VIDEO+/VIDEO-
 -> reel/pass-through
 -> surface receiver
 -> OSD
 -> 7 in CVBS monitor
```

The 40 m tether must pass video-noise and UART/RS-485 coexistence tests before 100-150 m release.

## 5. Pressure and sealing scheme

```text
compressor/service gun
 -> protected compact PRESSURE valve
 -> dry crawler volume, target service test +0.25 bar(g)
 -> internal pressure sensor [ARTICLE HOLD]
 -> NUCLEO telemetry
 -> RS-485
 -> console pressure display
```

Primary sealing paths:
- body/service cover: static elastomer seal, groove dimensions HOLD until seal selection;
- six wheel stations: dynamic X-ring 18.72 x 2.62 plus source static flange seal family;
- two Z40 body shafts: 18 x 30 x 7 rotary shaft seals;
- camera: separate sealed pressure body;
- camera cable entry: LAPP 53112000 M12x1.5 gland;
- rear tether entry: independent mechanical pull termination plus sealed electrical bulkhead; electrical contacts carry no towing load.

Acceptance requires pressure-decay and submerged bubble testing; CAD fit alone is not a sealing PASS.

## 6. Safety states

- loss of valid control/heartbeat -> traction STOP;
- MCU reset -> traction STOP;
- overcurrent/jam -> affected traction channel STOP;
- pressure outside configured band -> fault/stop policy;
- surface E-STOP removes dangerous tether power independently of crawler firmware;
- no automatic restart after a safety trip.
